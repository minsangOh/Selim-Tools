"""Selim Tools — 세림전자 업무 프로그램을 항상 최신 버전으로 설치하고 실행하는 허브."""
from __future__ import annotations

import argparse
import logging
import logging.handlers
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QObject, QRectF, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtGui import QCloseEvent, QColor, QFont, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

import hub_core as core

APP_NAME = "Selim Tools"
APP_VERSION = "1.0.0"
RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
APP_ICON = RESOURCE_ROOT / "assets" / "icon.ico"
MANIFEST_JOB, HUB_JOB = "목록", "허브"  # 앱 작업은 앱 id를 키로 쓴다

STYLE = """
QWidget#root { background: #EEF2F7; }
QWidget#cards, QScrollArea { background: transparent; }
QWidget { color: #16181C; font-size: 13px; }
QLabel#title { font-size: 20px; font-weight: 700; }
QLabel#subtitle, QLabel#footer { color: #5B616A; font-size: 12px; }
QLabel#message { color: #5B616A; padding: 40px 0; }
QFrame#card { background: #FFFFFF; border: 1px solid rgba(20, 24, 32, 26); border-radius: 14px; }
QLabel#cardTitle { font-size: 15px; font-weight: 700; }
QLabel#cardText { color: #4A4F57; font-size: 12px; }
QLabel#cardStatus { color: #5B616A; font-size: 12px; font-weight: 600; }
QLabel#cardStatus[tone="accent"] { color: #0A58CA; }
QLabel#cardStatus[tone="ok"] { color: #0B6B2E; }
QLabel#cardStatus[tone="warn"] { color: #7A4F00; }
QLabel#cardStatus[tone="error"] { color: #A8231B; }
QLabel#link { font-size: 12px; }
QFrame#banner { background: rgba(10, 108, 255, 26); border: 1px solid rgba(10, 108, 255, 64); border-radius: 12px; }
QLabel#bannerText { color: #0A4AA8; font-weight: 600; }
QPushButton { color: #16181C; background: #FAFBFD; border: 1px solid rgba(20, 24, 32, 38); border-radius: 15px; padding: 0 14px; font-weight: 600; }
QPushButton:hover { background: #FFFFFF; border-color: rgba(20, 24, 32, 64); }
QPushButton:pressed { background: #EDEFF2; }
QPushButton:disabled { color: #9AA0A8; }
QPushButton#primaryButton { color: #FFFFFF; background: #0A6CFF; border: 1px solid #0A6CFF; border-radius: 15px; }
QPushButton#primaryButton:hover { background: #0058D6; border-color: #0058D6; }
QPushButton#primaryButton:pressed { background: #004CBA; border-color: #004CBA; }
QPushButton#primaryButton:disabled { color: #FFFFFF; background: #8DB7F5; border-color: #8DB7F5; }
QProgressBar#cardProgress { background: rgba(20, 24, 32, 20); border: none; border-radius: 2px; }
QProgressBar#cardProgress::chunk { background: #0A6CFF; border-radius: 2px; }
"""


class WorkerSignals(QObject):
    progress = Signal(int, int)
    succeeded = Signal(object)
    failed = Signal(str)
    finished = Signal(str)


class Worker(QRunnable):
    """callback(progress)을 스레드 풀에서 실행하고 결과를 시그널로 알린다."""

    def __init__(self, key: str, callback: Callable[[core.Progress], object]):
        super().__init__()
        self.key = key
        self.callback = callback
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = self.callback(self.signals.progress.emit)
        except core.HubError as exc:
            core.log.warning("%s: %s", self.key, exc)
            self.signals.failed.emit(str(exc))
        except Exception as exc:
            core.log.exception("%s: 예상하지 못한 오류", self.key)
            self.signals.failed.emit(f"예상하지 못한 오류가 났습니다. ({exc})")
        else:
            self.signals.succeeded.emit(result)
        finally:
            self.signals.finished.emit(self.key)


def letter_tile(name: str, size: int) -> QPixmap:
    """아이콘이 없을 때 쓰는 이름 첫 글자 타일."""
    ratio = 2
    pixmap = QPixmap(size * ratio, size * ratio)
    pixmap.setDevicePixelRatio(ratio)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#0A6CFF"))
    painter.drawRoundedRect(QRectF(0, 0, size, size), size * 0.22, size * 0.22)
    font = QFont(painter.font())
    font.setPixelSize(int(size * 0.45))
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor("#FFFFFF"))
    painter.drawText(QRectF(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, name[:1])
    painter.end()
    return pixmap


class AppCard(QFrame):
    """앱 하나: 아이콘, 이름, 설명, 설치 상태, 실행 버튼."""

    def __init__(self, app: core.App, icon: Path | None, owner: MainWindow):
        super().__init__()
        self.setObjectName("card")
        self.app = app
        self.owner = owner

        icon_label = QLabel()
        icon_label.setFixedSize(48, 48)
        icon_label.setPixmap(QIcon(str(icon)).pixmap(48, 48) if icon else letter_tile(app.name, 48))
        name = QLabel(app.name)
        name.setObjectName("cardTitle")
        description = QLabel(app.description)
        description.setObjectName("cardText")
        description.setWordWrap(True)
        self.status = QLabel()
        self.status.setObjectName("cardStatus")
        self.status.setWordWrap(True)
        self.progress = QProgressBar()
        self.progress.setObjectName("cardProgress")
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(4)
        self.progress.hide()
        self.button = QPushButton()
        self.button.setObjectName("primaryButton")
        self.button.setFixedSize(140, 34)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.button.clicked.connect(self.start)
        notes = QLabel(f'<a href="{app.notes}">변경 내용</a>' if app.notes else "")
        notes.setObjectName("link")
        notes.setOpenExternalLinks(True)

        text = QVBoxLayout()
        text.setSpacing(3)
        text.addWidget(name)
        text.addWidget(description)
        text.addWidget(self.status)
        text.addWidget(self.progress)
        side = QVBoxLayout()
        side.setSpacing(6)
        side.addWidget(self.button)
        side.addWidget(notes, alignment=Qt.AlignmentFlag.AlignHCenter)
        side.addStretch()
        row = QHBoxLayout(self)
        row.setContentsMargins(16, 14, 16, 14)
        row.setSpacing(14)
        row.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignTop)
        row.addLayout(text, 1)
        row.addLayout(side)
        self.refresh()

    def refresh(self) -> None:
        """설치 상태를 다시 읽어 버튼과 상태 문구를 맞춘다."""
        app = self.app
        current = core.installed_version(app)
        if core.installed_exe(app) is None:
            self._show("설치", f"설치되지 않음 · 최신 v{app.version} · {app.size / 1_000_000:.0f}MB", "muted")
        elif core.needs_update(app):
            self._show("업데이트 후 실행", f"v{current or '?'} 설치됨 → 새 버전 v{app.version}", "accent")
        else:
            self._show("실행", f"v{current} · 최신 버전", "ok")

    def _show(self, button: str, status: str, tone: str) -> None:
        self.button.setText(button)
        self.button.setEnabled(True)
        self.set_status(status, tone)

    def set_status(self, text: str, tone: str) -> None:
        self.status.setText(text)
        self.status.setProperty("tone", tone)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)

    def start(self) -> None:
        self.button.setEnabled(False)
        self.button.setText("준비 중…")
        cancel = self.owner.cancel
        worker = Worker(self.app.id, lambda progress: core.run(self.app, progress, cancel))
        worker.signals.progress.connect(self.on_progress)
        worker.signals.succeeded.connect(self.on_done)
        worker.signals.failed.connect(self.on_failed)
        self.owner.submit(worker)

    def on_progress(self, done: int, total: int) -> None:
        self.progress.show()
        if done < total:
            self.progress.setRange(0, total)
            self.progress.setValue(done)
            self.button.setText(f"받는 중 {done * 100 // total}%")
        else:
            self.progress.setRange(0, 0)  # 무인 설치는 진행률을 알 수 없다
            self.button.setText("설치 중…")

    def on_done(self, note: str) -> None:
        self.progress.hide()
        self.refresh()
        if note:
            self.set_status(note, "warn")

    def on_failed(self, message: str) -> None:
        self.progress.hide()
        self.refresh()
        self.set_status(message, "error")


class MainWindow(QMainWindow):
    def __init__(self, manifest_url: str = core.MANIFEST_URL):
        super().__init__()
        self.manifest_url = manifest_url
        self.cancel = threading.Event()
        self.jobs: dict[str, Worker] = {}  # 끝날 때까지 참조를 잡아 두어 시그널 객체가 먼저 사라지지 않게 한다
        self.cards: list[AppCard] = []
        self.hub_update: core.App | None = None
        self.setWindowTitle(APP_NAME)
        self.resize(760, 640)
        self.setMinimumSize(620, 480)

        brand = QLabel()
        brand.setPixmap(QIcon(str(APP_ICON)).pixmap(40, 40))
        title = QLabel(APP_NAME)
        title.setObjectName("title")
        subtitle = QLabel("세림전자 업무 프로그램을 항상 최신 버전으로 실행합니다")
        subtitle.setObjectName("subtitle")
        self.refresh_button = QPushButton("새로 고침")
        self.refresh_button.setFixedHeight(30)
        self.refresh_button.clicked.connect(self.load_manifest)
        self.list_status = QLabel()
        self.list_status.setObjectName("subtitle")
        heading = QVBoxLayout()
        heading.setSpacing(2)
        heading.addWidget(title)
        heading.addWidget(subtitle)
        tools = QVBoxLayout()
        tools.setSpacing(4)
        tools.addWidget(self.refresh_button, alignment=Qt.AlignmentFlag.AlignRight)
        tools.addWidget(self.list_status, alignment=Qt.AlignmentFlag.AlignRight)
        header = QHBoxLayout()
        header.setSpacing(12)
        header.addWidget(brand)
        header.addLayout(heading, 1)
        header.addLayout(tools)

        self.banner = QFrame()
        self.banner.setObjectName("banner")
        self.banner_text = QLabel()
        self.banner_text.setObjectName("bannerText")
        self.banner_text.setWordWrap(True)
        self.banner_button = QPushButton("지금 업데이트")
        self.banner_button.setObjectName("primaryButton")
        self.banner_button.setFixedHeight(30)
        self.banner_button.clicked.connect(self.update_hub)
        banner_row = QHBoxLayout(self.banner)
        banner_row.setContentsMargins(14, 8, 8, 8)
        banner_row.addWidget(self.banner_text, 1)
        banner_row.addWidget(self.banner_button)
        self.banner.hide()

        self.message = QLabel()
        self.message.setObjectName("message")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message.setWordWrap(True)
        self.card_box = QVBoxLayout()
        self.card_box.setContentsMargins(0, 0, 0, 0)
        self.card_box.setSpacing(10)
        self.card_box.addWidget(self.message)
        self.card_box.addStretch()
        cards = QWidget()
        cards.setObjectName("cards")
        cards.setLayout(self.card_box)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setWidget(cards)
        footer = QLabel(f"{APP_NAME} v{APP_VERSION}")
        footer.setObjectName("footer")

        root = QWidget()
        root.setObjectName("root")
        layout = QVBoxLayout(root)
        layout.setContentsMargins(24, 20, 24, 14)
        layout.setSpacing(14)
        layout.addLayout(header)
        layout.addWidget(self.banner)
        layout.addWidget(scroll, 1)
        layout.addWidget(footer)
        self.setCentralWidget(root)
        self.setStyleSheet(STYLE)
        self.load_manifest()

    def submit(self, worker: Worker) -> None:
        self.jobs[worker.key] = worker
        worker.signals.finished.connect(self.job_finished)
        self._update_controls()
        QThreadPool.globalInstance().start(worker)

    def job_finished(self, key: str) -> None:
        self.jobs.pop(key, None)
        self._update_controls()

    def _update_controls(self) -> None:
        # 작업 중에 목록을 다시 그리거나 허브를 바꾸면 진행 중인 작업을 잃는다
        idle = not self.jobs
        self.refresh_button.setEnabled(idle)
        self.banner_button.setEnabled(idle)

    def load_manifest(self) -> None:
        self.list_status.setText("목록을 확인하는 중…")
        url = self.manifest_url

        def job(progress: core.Progress):
            manifest, online = core.fetch_manifest(url)
            icons = {app.id: core.icon_file(app, url, fetch=online) for app in manifest.apps}
            return manifest, online, icons

        worker = Worker(MANIFEST_JOB, job)
        worker.signals.succeeded.connect(self.show_manifest)
        worker.signals.failed.connect(self.show_manifest_error)
        self.submit(worker)

    def show_manifest(self, result: tuple[core.Manifest, bool, dict[str, Path | None]]) -> None:
        manifest, online, icons = result
        for card in self.cards:
            self.card_box.removeWidget(card)
            card.deleteLater()
        self.cards = [AppCard(app, icons.get(app.id), self) for app in manifest.apps]
        for index, card in enumerate(self.cards):
            self.card_box.insertWidget(index, card)
        self.message.setText("" if self.cards else "표시할 프로그램이 없습니다.")
        self.message.setVisible(not self.cards)
        self.list_status.setText(f"{datetime.now():%H:%M} 확인" if online else "오프라인 · 마지막으로 받은 목록")
        hub = manifest.hub
        self.hub_update = hub if hub and core.parse_version(hub.version) > core.parse_version(APP_VERSION) else None
        if self.hub_update:
            self.banner_text.setText(f"{APP_NAME} 새 버전 v{hub.version}이 있습니다.")
            self.banner_button.setText("지금 업데이트")
        self.banner.setVisible(self.hub_update is not None)

    def show_manifest_error(self, message: str) -> None:
        self.list_status.setText("목록을 받지 못했습니다")
        if not self.cards:
            self.message.setText(message)
            self.message.show()

    def update_hub(self) -> None:
        hub = self.hub_update
        if hub is None:
            return
        self.banner_button.setText("받는 중…")
        worker = Worker(HUB_JOB, lambda progress: core.download_hub(hub, progress, self.cancel))
        worker.signals.progress.connect(self.hub_progress)
        worker.signals.succeeded.connect(self.install_hub)
        worker.signals.failed.connect(self.hub_update_failed)
        self.submit(worker)

    def hub_progress(self, done: int, total: int) -> None:
        self.banner_button.setText(f"받는 중 {done * 100 // total}%")

    def install_hub(self, setup: Path) -> None:
        # 설치 파일은 이 창이 닫혀 실행 파일 잠금이 풀리길 기다렸다가 덮어쓰고 허브를 다시 연다
        try:
            subprocess.Popen([str(setup), "/S"], close_fds=True)
        except OSError as exc:
            self.hub_update_failed(f"설치 프로그램을 실행하지 못했습니다. ({exc})")
            return
        self.jobs.pop(HUB_JOB, None)  # 닫을 때 "설치 진행 중"으로 묻지 않게 한다
        self.close()

    def hub_update_failed(self, message: str) -> None:
        self.banner_text.setText(message)
        self.banner_button.setText("다시 시도")

    def closeEvent(self, event: QCloseEvent) -> None:
        busy = [key for key in self.jobs if key != MANIFEST_JOB]
        if busy:
            answer = QMessageBox.question(self, APP_NAME, "설치가 진행 중입니다. 중단하고 닫을까요?")
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
        self.cancel.set()  # 내려받기는 다음 조각에서 멈춘다. 이미 시작한 무인 설치는 끝까지 간다
        event.accept()


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--manifest", default=core.MANIFEST_URL)  # 시험용 목록 주소 (file:// 도 된다)
    args, _ = parser.parse_known_args()
    core.DATA_DIR.mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        core.DATA_DIR / "hub.log", maxBytes=1_000_000, backupCount=1, encoding="utf-8"
    )
    logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s %(levelname)s %(message)s")
    core.clean_downloads()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")
    font = QFont()
    # 작업지도서·CTQ 앱과 같은 글꼴: 영문은 Segoe UI, 한글은 맑은 고딕
    font.setFamilies(["Segoe UI Variable Text", "Segoe UI", "Malgun Gothic"])
    font.setPixelSize(13)
    app.setFont(font)
    app.setWindowIcon(QIcon(str(APP_ICON)))
    window = MainWindow(args.manifest)
    window.show()
    code = app.exec()
    QThreadPool.globalInstance().waitForDone()  # 멈춘 내려받기와 진행 중인 무인 설치를 마무리한다
    return code


if __name__ == "__main__":
    raise SystemExit(main())
