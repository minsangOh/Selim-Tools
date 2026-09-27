from __future__ import annotations

import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

import hub_core as core
from main import MainWindow


def entry(app_id: str, version: str) -> dict:
    return {"id": app_id, "name": app_id.upper(), "description": f"{app_id} 설명", "version": version,
            "kind": "portable", "url": f"https://example.invalid/{app_id}.exe", "sha256": "a" * 64,
            "size": 48_000_000, "exe": f"{app_id}.exe"}


class MainWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def wait_for(self, condition, timeout: float = 10) -> None:
        deadline = time.monotonic() + timeout
        while not condition():
            self.assertLess(time.monotonic(), deadline, "목록을 불러오지 못했습니다")
            QApplication.processEvents()
            time.sleep(0.01)

    def test_cards_follow_install_state_and_hub_update_is_offered(self) -> None:
        with tempfile.TemporaryDirectory() as folder, patch.object(core, "DATA_DIR", Path(folder) / "data"):
            manifest = Path(folder) / "manifest.json"
            manifest.write_text(json.dumps({
                "schema": 1,
                "hub": dict(entry("hub", "9.0.0"), kind="installer", uninstall_key="SelimTools"),
                "apps": [entry("fresh", "1.0.0"), entry("stale", "2.0.0"), entry("missing", "1.0.0")],
            }), encoding="utf-8")
            for app_id, version in (("fresh", "1.0.0"), ("stale", "1.5.0")):
                exe = core.DATA_DIR / "apps" / app_id / f"{app_id}.exe"
                exe.parent.mkdir(parents=True)
                exe.write_bytes(b"")
                core._save_version(app_id, version)

            window = MainWindow(manifest.as_uri())
            try:
                self.wait_for(lambda: window.cards and window.refresh_button.isEnabled())
                self.assertEqual([card.button.text() for card in window.cards], ["실행", "업데이트 후 실행", "설치"])
                self.assertIn("v1.5.0 설치됨", window.cards[1].status.text())
                self.assertIn("48MB", window.cards[2].status.text())
                self.assertFalse(window.banner.isHidden())
                self.assertIn("v9.0.0", window.banner_text.text())
            finally:
                window.close()

    def test_offline_without_copy_shows_message(self) -> None:
        with tempfile.TemporaryDirectory() as folder, patch.object(core, "DATA_DIR", Path(folder) / "data"):
            window = MainWindow((Path(folder) / "none.json").as_uri())
            try:
                self.wait_for(window.refresh_button.isEnabled)
                self.assertEqual(window.cards, [])
                self.assertIn("인터넷 연결", window.message.text())
                self.assertTrue(window.banner.isHidden())
            finally:
                window.close()


if __name__ == "__main__":
    unittest.main()
