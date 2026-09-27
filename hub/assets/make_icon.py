"""허브 아이콘(hub/assets/icon.ico)과 README용 그림(assets/hub.png)을 그린다.

모양을 바꿀 때만 실행한다: python assets/make_icon.py (PySide6만 있으면 된다)
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QRectF, Qt
from PySide6.QtGui import QColor, QGuiApplication, QImage, QLinearGradient, QPainter

HERE = Path(__file__).resolve().parent
SIZES = (16, 20, 24, 32, 40, 48, 64, 128, 256)


def draw(size: int) -> QImage:
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    # 작업지도서 앱의 로고와 같은 파란 타일
    tile = QRectF(0, 0, size, size).adjusted(size * 0.03, size * 0.03, -size * 0.03, -size * 0.03)
    gradient = QLinearGradient(tile.topLeft(), tile.bottomRight())
    gradient.setColorAt(0.0, QColor("#3D8BFF"))
    gradient.setColorAt(1.0, QColor("#0A56D6"))
    painter.setBrush(gradient)
    painter.drawRoundedRect(tile, size * 0.22, size * 0.22)
    # 2×2 격자: 여러 프로그램을 모아 둔 곳. 오른쪽 아래 한 칸은 "최신"을 뜻하는 초록
    gap = size * 0.09
    cell = (size * 0.56 - gap) / 2
    origin = size * 0.22
    for row in range(2):
        for col in range(2):
            painter.setBrush(QColor("#5BE39A" if (row, col) == (1, 1) else "#FFFFFF"))
            rect = QRectF(origin + col * (cell + gap), origin + row * (cell + gap), cell, cell)
            painter.drawRoundedRect(rect, cell * 0.28, cell * 0.28)
    painter.end()
    return image


def png_bytes(image: QImage) -> bytes:
    data = QByteArray()
    buffer = QBuffer(data)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    image.save(buffer, "PNG")
    return bytes(data)


def write_ico(path: Path, images: dict[int, bytes]) -> None:
    """PNG 조각을 담은 ICO (Windows Vista 이후 모든 크기에서 읽는다)."""
    header = struct.pack("<HHH", 0, 1, len(images))
    offset = len(header) + 16 * len(images)
    entries, blobs = b"", b""
    for size, png in images.items():
        entries += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(png), offset)
        offset += len(png)
        blobs += png
    path.write_bytes(header + entries + blobs)


def main() -> int:
    app = QGuiApplication(sys.argv)  # noqa: F841 — QPainter가 쓰는 Qt 초기화
    write_ico(HERE / "icon.ico", {size: png_bytes(draw(size)) for size in SIZES})
    draw(128).save(str(HERE.parents[1] / "assets" / "hub.png"))
    print("icon.ico, assets/hub.png를 만들었습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
