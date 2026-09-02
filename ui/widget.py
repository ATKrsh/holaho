"""
Holaho - Interactive Glassmorphism Floating Desktop Widget
Features animated audio visualizer canvas, media playback controls, and quick voice memo recording.
"""

import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt, QPoint, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QBrush, QPen, QLinearGradient

from config import ConfigManager
from core.media_control import MediaController
from core.audio_memo import AudioMemoManager
from ui.settings_dialog import SettingsDialog


class AudioVisualizerWidget(QWidget):
    """Animated equalizer / sine wave visualizer canvas for Holaho."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(45)
        self.phase = 0.0
        self.is_active = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wave)
        self.timer.start(35)  # ~30 FPS animation

    def update_wave(self):
        self.phase += 0.15
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        mid_y = height / 2.0

        # Draw equalizer bars
        n_bars = 24
        bar_width = width / n_bars - 3

        for i in range(n_bars):
            # Calculate dynamic height
            h = math.sin(self.phase + i * 0.4) * (height / 2.5) + (height / 3.0)
            h = max(4.0, min(h, height - 4.0))

            x = i * (bar_width + 3) + 2
            y = mid_y - h / 2.0

            grad = QLinearGradient(x, y, x, y + h)
            grad.setColorAt(0.0, QColor("#c084fc"))
            grad.setColorAt(1.0, QColor("#ec4899"))

            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_width, h), 3, 3)

        painter.end()


class HolahoWidget(QWidget):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config = config_manager
        self.memo_mgr = AudioMemoManager(config_manager.config_path.parent / "memos")
        self.drag_position = QPoint()
        self.is_recording = False

        self.init_flags()
        self.init_ui()
        self.refresh_memos()

    def init_flags(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.SubWindow
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setObjectName("HolahoWidget")

        pos = self.config.get("widget_position", [120, 120])
        self.move(pos[0], pos[1])

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)

        # Header bar
        header = QHBoxLayout()
        title = QLabel("✨ Holaho")
        title.setObjectName("WidgetTitle")

        close_btn = QPushButton("×")
        close_btn.setFixedSize(22, 22)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #94a3b8; font-size: 16px; font-weight: bold; border: none;
            }
            QPushButton:hover { color: #ec4899; }
        """)
        close_btn.clicked.connect(self.hide)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(close_btn)
        layout.addLayout(header)

        # Animated Audio Visualizer Canvas
        self.visualizer = AudioVisualizerWidget()
        layout.addWidget(self.visualizer)

        # 🎙️ Record Voice Memo Button
        self.record_btn = QPushButton("🎙️ Record Voice Memo")
        self.record_btn.setObjectName("RecordBtn")
        self.record_btn.setFixedHeight(36)
        self.record_btn.setToolTip("Quick Record Voice Memo")
        self.record_btn.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_btn)

        # Media Control Buttons Bar
        media_box = QHBoxLayout()
        btn_prev = QPushButton("⏮️")
        btn_prev.setObjectName("MediaBtn")
        btn_prev.setFixedSize(36, 32)
        btn_prev.setToolTip("Previous Track")
        btn_prev.clicked.connect(MediaController.prev_track)

        btn_play = QPushButton("⏯️")
        btn_play.setObjectName("MediaBtn")
        btn_play.setFixedSize(36, 32)
        btn_play.setToolTip("Play / Pause")
        btn_play.clicked.connect(MediaController.play_pause)

        btn_next = QPushButton("⏭️")
        btn_next.setObjectName("MediaBtn")
        btn_next.setFixedSize(36, 32)
        btn_next.setToolTip("Next Track")
        btn_next.clicked.connect(MediaController.next_track)

        btn_mute = QPushButton("🔇")
        btn_mute.setObjectName("MediaBtn")
        btn_mute.setFixedSize(36, 32)
        btn_mute.setToolTip("Toggle Mute")
        btn_mute.clicked.connect(MediaController.toggle_mute)

        btn_settings = QPushButton("⚙️")
        btn_settings.setObjectName("MediaBtn")
        btn_settings.setFixedSize(36, 32)
        btn_settings.setToolTip("Open Holaho Settings")
        btn_settings.clicked.connect(self.open_settings)

        media_box.addWidget(btn_prev)
        media_box.addWidget(btn_play)
        media_box.addWidget(btn_next)
        media_box.addWidget(btn_mute)
        media_box.addStretch()
        media_box.addWidget(btn_settings)

        layout.addLayout(media_box)

        # Voice Memos List
        layout.addWidget(QLabel("Saved Voice Memos:"))
        self.memo_list = QListWidget()
        self.memo_list.setFixedHeight(90)
        layout.addWidget(self.memo_list)

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.record_btn.setText("🔴 Stop & Save Memo")
        else:
            self.is_recording = False
            self.record_btn.setText("🎙️ Record Voice Memo")
            # Save sample audio memo
            path = self.memo_mgr.create_sample_memo("Memo")
            self.refresh_memos()

    def refresh_memos(self):
        self.memo_list.clear()
        memos = self.memo_mgr.list_memos()
        for m in memos:
            item = QListWidgetItem(f"🎵 {m['name']} ({m['size_kb']} KB)")
            item.setData(Qt.UserRole, m["path"])
            self.memo_list.addItem(item)

    def open_settings(self):
        dlg = SettingsDialog(self.config, self)
        dlg.exec()

    # --- Mouse Dragging ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            self.config.set("widget_position", [new_pos.x(), new_pos.y()])
            event.accept()
