from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import threading
import unittest
import winreg
from pathlib import Path
from unittest.mock import patch

import hub_core as core

TEST_KEY = r"Software\SelimToolsTest\Uninstall"  # 실제 Uninstall 키 대신 쓰는 시험용 키


def make_app(**changes) -> core.App:
    fields = dict(id="demo", name="데모", version="1.2.0", kind="portable", url="", sha256="", size=0, exe="데모.exe")
    fields.update(changes)
    return core.App(**fields)


class CoreTestCase(unittest.TestCase):
    """DATA_DIR를 임시 폴더로 바꾸고, 올린 파일은 file:// 주소로 받는다."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        patcher = patch.object(core, "DATA_DIR", self.tmp / "data")
        patcher.start()
        self.addCleanup(patcher.stop)

    def publish(self, content: bytes, name: str = "demo.exe", **changes) -> core.App:
        source = self.tmp / "release" / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(content)
        return make_app(url=source.as_uri(), sha256=hashlib.sha256(content).hexdigest(), size=len(content), **changes)

    def missing(self, **changes) -> core.App:
        return make_app(url=(self.tmp / "missing.exe").as_uri(), sha256="0" * 64, size=3, **changes)


class VersionTests(unittest.TestCase):
    def test_compares_numerically_and_ignores_trailing_zeros(self) -> None:
        self.assertGreater(core.parse_version("v1.10.0"), core.parse_version("1.9.9"))
        self.assertEqual(core.parse_version("1.3"), core.parse_version("v1.3.0"))
        self.assertLess(core.parse_version("1.3.0"), core.parse_version("1.3.0.2"))


class ManifestTests(CoreTestCase):
    def data(self) -> dict:
        ready = {"id": "ready", "name": "준비됨", "version": "1.0.0", "kind": "portable", "url": "https://x/a.exe",
                 "sha256": "a" * 64, "size": 1, "exe": "a.exe"}
        later = dict(ready, id="later", url="")  # 아직 올리지 않은 앱
        return {"schema": 1, "hub": dict(ready, id="hub", url=""), "apps": [ready, later]}

    def test_skips_unpublished_entries(self) -> None:
        manifest = core.parse_manifest(self.data())
        self.assertEqual([app.id for app in manifest.apps], ["ready"])
        self.assertIsNone(manifest.hub)

    def test_rejects_unknown_schema_kind_and_missing_fields(self) -> None:
        data = self.data()
        with self.assertRaises(ValueError):
            core.parse_manifest(dict(data, schema=2))
        data["apps"][0]["kind"] = "zip"
        with self.assertRaises(ValueError):
            core.parse_manifest(data)
        del data["apps"][0]["exe"]
        with self.assertRaises(ValueError):
            core.parse_manifest(data)

    def test_installer_needs_uninstall_key(self) -> None:
        data = self.data()
        data["apps"][0]["kind"] = "installer"
        with self.assertRaises(ValueError):
            core.parse_manifest(data)

    def test_uses_last_copy_when_offline(self) -> None:
        source = self.tmp / "manifest.json"
        source.write_text(json.dumps(self.data()), encoding="utf-8")
        manifest, online = core.fetch_manifest(source.as_uri())
        self.assertTrue(online)
        source.unlink()
        cached, online = core.fetch_manifest(source.as_uri())
        self.assertFalse(online)
        self.assertEqual(cached, manifest)

    def test_offline_without_copy_is_an_error(self) -> None:
        with self.assertRaises(core.HubError):
            core.fetch_manifest((self.tmp / "none.json").as_uri())

    def test_icon_is_resolved_next_to_manifest_and_cached(self) -> None:
        (self.tmp / "assets").mkdir()
        (self.tmp / "assets" / "demo.png").write_bytes(b"png")
        url = (self.tmp / "manifest.json").as_uri()
        app = make_app(icon="assets/demo.png")
        path = core.icon_file(app, url)
        self.assertEqual(path.read_bytes(), b"png")
        (self.tmp / "assets" / "demo.png").unlink()
        self.assertEqual(core.icon_file(app, url), path)
        self.assertIsNone(core.icon_file(make_app(icon="assets/none.png"), url, fetch=False))


class DownloadTests(CoreTestCase):
    def test_hash_mismatch_leaves_nothing_behind(self) -> None:
        app = self.publish(b"new build")
        dest = self.tmp / "out" / "demo.exe"
        with self.assertRaises(core.HubError):
            core.download(app.url, dest, "0" * 64, app.size)
        self.assertEqual(list(dest.parent.iterdir()), [])

    def test_reports_progress_and_places_file(self) -> None:
        app = self.publish(b"new build")
        dest = self.tmp / "out" / "demo.exe"
        seen = []
        core.download(app.url, dest, app.sha256, app.size, progress=lambda done, total: seen.append((done, total)))
        self.assertEqual(dest.read_bytes(), b"new build")
        self.assertEqual(seen[-1], (9, 9))

    def test_cancel_stops_and_removes_partial_file(self) -> None:
        app = self.publish(b"x" * 10)
        cancel = threading.Event()
        cancel.set()
        with self.assertRaises(core.HubError):
            core.download(app.url, self.tmp / "out" / "demo.exe", app.sha256, app.size, cancel=cancel)
        self.assertEqual(list((self.tmp / "out").iterdir()), [])


class PortableTests(CoreTestCase):
    def setUp(self) -> None:
        super().setUp()
        patcher = patch.object(core, "launch")
        self.launch = patcher.start()
        self.addCleanup(patcher.stop)

    def test_installs_records_version_and_launches(self) -> None:
        app = self.publish(b"v1.2.0")
        self.assertIsNone(core.installed_exe(app))
        self.assertEqual(core.run(app), "")
        exe = core.portable_exe(app)
        self.launch.assert_called_once_with(exe)
        self.assertEqual(exe.read_bytes(), b"v1.2.0")
        self.assertEqual(core.installed_version(app), "1.2.0")
        self.assertFalse(core.needs_update(app))

    def test_update_replaces_only_the_exe(self) -> None:
        # CTQ는 exe 옆의 config.json과 DB\ 폴더를 쓰므로 폴더는 그대로 두어야 한다
        core.run(self.publish(b"old", version="1.0.0"))
        config = core.portable_exe(make_app()).parent / "config.json"
        config.write_text("{}", encoding="utf-8")
        new = self.publish(b"new", version="1.1.0")
        self.assertTrue(core.needs_update(new))
        core.run(new)
        self.assertEqual(core.portable_exe(new).read_bytes(), b"new")
        self.assertTrue(config.exists())
        self.assertEqual(sorted(p.name for p in config.parent.iterdir()), ["config.json", "데모.exe"])

    def test_running_app_is_launched_without_update(self) -> None:
        core.run(self.publish(b"old", version="1.0.0"))
        new = self.publish(b"new", version="1.1.0")
        with patch.object(core, "in_use", return_value=True):
            note = core.run(new)
        self.assertIn("다음 실행", note)
        self.assertEqual(core.portable_exe(new).read_bytes(), b"old")
        self.assertEqual(self.launch.call_count, 2)

    def test_failed_update_falls_back_to_installed_version(self) -> None:
        core.run(self.publish(b"old", version="1.0.0"))
        note = core.run(self.missing(version="1.1.0"))
        self.assertIn("설치된 버전으로 실행", note)
        self.assertEqual(self.launch.call_count, 2)
        self.assertEqual(core.installed_version(make_app()), "1.0.0")

    def test_failed_first_install_is_an_error(self) -> None:
        with self.assertRaises(core.HubError):
            core.run(self.missing())
        self.launch.assert_not_called()


class InstallerTests(CoreTestCase):
    """실제 NSIS 대신 /S를 받으면 설치 폴더와 Uninstall 키를 남기는 .cmd로 시험한다."""

    def setUp(self) -> None:
        super().setUp()
        patcher = patch.object(core, "UNINSTALL_KEY", TEST_KEY)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self._delete_key, r"Software\SelimToolsTest")
        patcher = patch.object(core, "launch")
        self.launch = patcher.start()
        self.addCleanup(patcher.stop)
        self.target = self.tmp / "installed"

    def _delete_key(self, path: str) -> None:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                while True:
                    try:
                        child = winreg.EnumKey(key, 0)
                    except OSError:
                        break
                    self._delete_key(rf"{path}\{child}")
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, path)
        except FileNotFoundError:
            pass

    def setup_app(self, version: str, exit_code: int = 0) -> core.App:
        script = (
            "@echo off\r\n"
            'if not "%~1"=="/S" exit /b 9\r\n'
            f'mkdir "{self.target}" 2>nul\r\n'
            f'copy /y "%~f0" "{self.target}\\demo.exe" >nul\r\n'
            f'reg add "HKCU\\{TEST_KEY}\\Demo" /v DisplayVersion /d {version} /f >nul\r\n'
            f'reg add "HKCU\\{TEST_KEY}\\Demo" /v InstallLocation /d "{self.target}" /f >nul\r\n'
            f"exit /b {exit_code}\r\n"
        )
        return self.publish(script.encode("ascii"), name="demo-setup.cmd", version=version, kind="installer",
                            exe="demo.exe", uninstall_key="Demo")

    def test_silent_install_then_version_from_registry(self) -> None:
        app = self.setup_app("2.0.0")
        self.assertIsNone(core.installed_exe(app))
        self.assertEqual(core.run(app), "")
        self.assertEqual(core.installed_version(app), "2.0.0")
        self.launch.assert_called_once_with(self.target / "demo.exe")
        self.assertEqual(list((core.DATA_DIR / "downloads").iterdir()), [])  # 설치 파일은 지운다

    def test_failing_installer_is_reported(self) -> None:
        with self.assertRaises(core.HubError) as caught:
            core.run(self.setup_app("2.0.0", exit_code=2))
        self.assertIn("종료 코드 2", str(caught.exception))
        self.launch.assert_not_called()

    def test_quoted_install_location(self) -> None:
        # FileRay(Tauri)는 InstallLocation을 "C:\...\FileRay"처럼 따옴표로 감싸 기록한다
        self.target.mkdir()
        (self.target / "demo.exe").write_bytes(b"")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, rf"{TEST_KEY}\Demo") as key:
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, f'"{self.target}"')
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "0.4.0")
        app = make_app(kind="installer", exe="demo.exe", uninstall_key="Demo", version="0.4.0")
        self.assertEqual(core.installed_exe(app), self.target / "demo.exe")
        self.assertFalse(core.needs_update(app))


class InUseTests(unittest.TestCase):
    def test_running_exe_is_locked(self) -> None:
        running = Path(sys._base_executable)  # 이 테스트를 돌리고 있는 인터프리터
        self.assertTrue(core.in_use(running))
        with tempfile.TemporaryDirectory() as folder:
            idle = Path(folder) / "idle.exe"
            shutil.copy(running, idle)
            self.assertFalse(core.in_use(idle))


if __name__ == "__main__":
    unittest.main()
