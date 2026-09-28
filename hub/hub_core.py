"""Selim Tools 허브의 동작: 목록(manifest) 받기, 설치 상태 확인, 내려받기·설치·실행.

Qt를 쓰지 않으므로 화면 없이 테스트할 수 있다.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import urllib.request
import winreg
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Callable
from urllib.parse import urljoin, urlparse

MANIFEST_URL = "https://raw.githubusercontent.com/minsangOh/Selim-Tools/master/manifest.json"
# 설치형 앱의 NSIS 설치 파일은 HKCU의 이 키 아래 <uninstall_key>에 버전과 설치 위치를 남긴다
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
# 허브가 받은 앱·캐시·상태를 두는 폴더 (테스트에서 바꾼다)
DATA_DIR = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "SelimTools"
CHUNK = 1 << 20  # 1MB씩 받으며 진행률과 취소를 확인한다

log = logging.getLogger("selimtools")
_state_lock = threading.Lock()

Progress = Callable[[int, int], None]


class HubError(Exception):
    """사용자에게 그대로 보여 줄 실패 사유."""


@dataclass(frozen=True)
class App:
    id: str
    name: str
    version: str
    kind: str  # "portable": exe 하나를 허브 폴더에 둔다, "installer": 설치 파일을 /S(무인)로 실행한다
    url: str
    sha256: str
    size: int
    exe: str  # portable: 저장할 파일 이름, installer: 설치 폴더 안의 실행 파일 이름
    description: str = ""
    uninstall_key: str = ""  # installer 전용
    icon: str = ""  # manifest 위치 기준 상대 경로
    notes: str = ""  # 릴리스 페이지 주소

    @classmethod
    def from_dict(cls, data: dict) -> App:
        app = cls(**{field.name: data[field.name] for field in fields(cls) if field.name in data})
        if app.kind not in ("portable", "installer"):
            raise ValueError(f"{app.id}: 알 수 없는 kind {app.kind!r}")
        if app.kind == "installer" and not app.uninstall_key:
            raise ValueError(f"{app.id}: installer에는 uninstall_key가 필요합니다")
        return app


@dataclass(frozen=True)
class Manifest:
    apps: tuple[App, ...]
    hub: App | None


def parse_manifest(data: dict) -> Manifest:
    if data.get("schema") != 1:
        raise ValueError("지원하지 않는 manifest 형식입니다")
    try:
        # url이 빈 항목은 아직 한 번도 올리지 않은 앱이다
        apps = tuple(App.from_dict(item) for item in data["apps"] if item.get("url"))
        hub = App.from_dict(data["hub"]) if data.get("hub", {}).get("url") else None
    except (KeyError, TypeError) as exc:
        raise ValueError(f"manifest 항목이 올바르지 않습니다: {exc!r}") from exc
    return Manifest(apps, hub)


def _open(url: str, timeout: float):
    request = urllib.request.Request(url, headers={"User-Agent": "SelimTools-Hub"})
    return urllib.request.urlopen(request, timeout=timeout)


def _write_atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def _remove(path: Path) -> None:
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass  # 백신 검사 등으로 잠시 잠긴 파일은 다음에 지운다


def fetch_manifest(url: str = MANIFEST_URL) -> tuple[Manifest, bool]:
    """목록을 받는다. 받지 못하면 마지막으로 받은 사본을 쓴다. 두 번째 값은 새로 받았는지 여부다."""
    cache = DATA_DIR / "cache" / "manifest.json"
    try:
        with _open(url, timeout=10) as response:
            raw = response.read()
        manifest = parse_manifest(json.loads(raw))
    except (OSError, ValueError) as exc:
        log.warning("목록을 받지 못했습니다: %s", exc)
        if not cache.exists():
            raise HubError("프로그램 목록을 받지 못했습니다. 인터넷 연결을 확인하세요.") from exc
        return parse_manifest(json.loads(cache.read_bytes())), False
    _write_atomic(cache, raw)
    return manifest, True


def icon_file(app: App, manifest_url: str = MANIFEST_URL, fetch: bool = True) -> Path | None:
    """앱 아이콘 파일. 캐시에 없으면 받아 둔다. 아이콘이 없거나 받지 못하면 None."""
    if not app.icon:
        return None
    url = urljoin(manifest_url, app.icon)
    path = DATA_DIR / "cache" / "icons" / Path(urlparse(url).path).name
    if not path.exists() and fetch:
        try:
            with _open(url, timeout=10) as response:
                _write_atomic(path, response.read())
        except OSError as exc:
            log.warning("아이콘을 받지 못했습니다 (%s): %s", url, exc)
    return path if path.exists() else None


def portable_exe(app: App) -> Path:
    return DATA_DIR / "apps" / app.id / app.exe


def _uninstall_values(app: App) -> dict[str, str]:
    values = {}
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, rf"{UNINSTALL_KEY}\{app.uninstall_key}") as key:
            for name in ("DisplayVersion", "InstallLocation"):
                try:
                    values[name] = str(winreg.QueryValueEx(key, name)[0])
                except OSError:
                    pass
    except OSError:
        pass
    return values


def installed_exe(app: App) -> Path | None:
    if app.kind == "portable":
        exe = portable_exe(app)
    else:
        # FileRay(Tauri) 설치 파일은 설치 위치를 따옴표로 감싸 기록한다
        location = _uninstall_values(app).get("InstallLocation", "").strip().strip('"')
        if not location:
            return None
        exe = Path(location) / app.exe
    return exe if exe.is_file() else None


def _load_state() -> dict[str, str]:
    try:
        return json.loads((DATA_DIR / "state.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _save_version(app_id: str, version: str) -> None:
    with _state_lock:
        state = _load_state()
        state[app_id] = version
        _write_atomic(DATA_DIR / "state.json", json.dumps(state, ensure_ascii=False, indent=1).encode("utf-8"))


def installed_version(app: App) -> str | None:
    if app.kind == "portable":
        return _load_state().get(app.id)
    return _uninstall_values(app).get("DisplayVersion")


def parse_version(text: str) -> tuple[int, ...]:
    """'v1.3.0' → (1, 3). 뒤쪽 0을 떼어 1.3과 1.3.0을 같은 버전으로 본다."""
    parts = [int(re.match(r"\d*", piece).group() or 0) for piece in text.strip().lstrip("vV").split(".")]
    while parts and parts[-1] == 0:
        parts.pop()
    return tuple(parts)


def needs_update(app: App) -> bool:
    current = installed_version(app)
    return current is None or parse_version(app.version) > parse_version(current)


def download(url: str, dest: Path, sha256: str, size: int,
             progress: Progress | None = None, cancel: threading.Event | None = None) -> None:
    """url을 dest로 받는다. 크기나 sha256이 목록과 다르면 받은 파일을 지우고 HubError를 낸다."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    digest = hashlib.sha256()
    done = 0
    try:
        with _open(url, timeout=30) as response, open(part, "wb") as out:
            while chunk := response.read(CHUNK):
                if cancel is not None and cancel.is_set():
                    raise HubError("취소했습니다.")
                out.write(chunk)
                digest.update(chunk)
                done += len(chunk)
                if progress is not None:
                    progress(done, size)
        if done != size or digest.hexdigest() != sha256.lower():
            raise HubError("받은 파일이 목록의 정보와 다릅니다. 잠시 후 다시 시도하세요.")
        os.replace(part, dest)
    except OSError as exc:
        raise HubError(f"내려받지 못했습니다. ({exc})") from exc
    finally:
        _remove(part)


def install(app: App, progress: Progress | None = None, cancel: threading.Event | None = None) -> None:
    """앱을 목록의 버전으로 설치하거나 바꾼다."""
    if app.kind == "portable":
        # 폴더는 그대로 두고 exe만 바꾼다. CTQ는 exe 옆의 config.json과 DB\ 폴더를 쓴다
        exe = portable_exe(app)
        new = exe.with_name(exe.name + ".new")
        download(app.url, new, app.sha256, app.size, progress, cancel)
        try:
            os.replace(new, exe)
        except PermissionError as exc:
            _remove(new)
            raise HubError(f"{app.name}이(가) 실행 중이라 바꾸지 못했습니다. 종료한 뒤 다시 시도하세요.") from exc
        _save_version(app.id, app.version)
        return
    setup = DATA_DIR / "downloads" / Path(urlparse(app.url).path).name
    download(app.url, setup, app.sha256, app.size, progress, cancel)
    # FileRay·PDF Diff 설치 파일은 모두 사용자 단위 NSIS라 관리자 권한 없이 /S로 조용히 설치된다.
    # 업데이트면 /UPDATE도 넘긴다. FileRay(Tauri) 설치 파일은 무인 설치 때마다 바탕 화면 바로가기를 새로 만드는데,
    # /UPDATE가 있으면 사용자가 지운 바로가기를 되살리지 않는다. 이 옵션을 모르는 설치 파일은 무시한다
    args = [str(setup), "/S"] + (["/UPDATE"] if installed_exe(app) is not None else [])
    try:
        code = subprocess.run(args, check=False).returncode
    except OSError as exc:
        raise HubError(f"{app.name} 설치 프로그램을 실행하지 못했습니다. ({exc})") from exc
    finally:
        _remove(setup)
    if code != 0:
        raise HubError(f"{app.name} 설치가 실패했습니다 (종료 코드 {code}).")
    if needs_update(app):
        raise HubError(f"{app.name}을(를) 설치했지만 설치된 버전을 확인하지 못했습니다.")


def in_use(exe: Path) -> bool:
    """실행 중인 exe는 Windows가 잠가 두므로 쓰기 모드로 열리지 않는다."""
    try:
        with open(exe, "r+b"):
            return False
    except PermissionError:
        return True


def launch(exe: Path) -> None:
    try:
        os.startfile(exe, cwd=str(exe.parent))
    except OSError as exc:
        raise HubError(f"실행하지 못했습니다. ({exc})") from exc


def run(app: App, progress: Progress | None = None, cancel: threading.Event | None = None) -> str:
    """최신 버전으로 맞춘 뒤 실행한다. 업데이트를 건너뛰었다면 그 이유를 돌려준다."""
    exe = installed_exe(app)
    note = ""
    if exe is None or needs_update(app):
        if exe is not None and in_use(exe):
            note = "실행 중이라 업데이트는 다음 실행 때 합니다."
        else:
            try:
                install(app, progress, cancel)
            except HubError as exc:
                # 설치된 버전이 있으면 업데이트에 실패해도 그 버전으로 실행한다
                if exe is None or (cancel is not None and cancel.is_set()):
                    raise
                note = f"업데이트하지 못해 설치된 버전으로 실행합니다. {exc}"
            exe = installed_exe(app)
    if exe is None:
        raise HubError(f"{app.name} 실행 파일을 찾지 못했습니다.")
    launch(exe)
    return note


def download_hub(hub: App, progress: Progress | None = None, cancel: threading.Event | None = None) -> Path:
    """허브 새 버전의 설치 파일을 받는다. 실행은 허브가 스스로 종료하면서 한다."""
    setup = DATA_DIR / "downloads" / Path(urlparse(hub.url).path).name
    download(hub.url, setup, hub.sha256, hub.size, progress, cancel)
    return setup


def clean_downloads() -> None:
    """지난번에 남은 설치 파일을 지운다. 아직 쓰이는 파일은 다음에 지운다."""
    for path in (DATA_DIR / "downloads").glob("*"):
        _remove(path)
