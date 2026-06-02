"""Boot screen — matrix rain animation + loading sequence"""
import random
import string
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen


class MatrixRain(QWidget):
    """Matrix yomg'ir animatsiyasi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.chars = string.ascii_letters + string.digits + "!@#$%^&*<>?/|\\~`"
        self.columns = []
        self.cell_size = 16
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(60)
        self._init_columns()

    def _init_columns(self):
        num_cols = max(1, self.width() // self.cell_size)
        self.columns = [
            {
                'y': random.randint(-40, 0),
                'speed': random.uniform(0.3, 1.0),
                'length': random.randint(5, 25),
                'chars': [random.choice(self.chars) for _ in range(30)],
            }
            for _ in range(num_cols)
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._init_columns()

    def _update(self):
        for col in self.columns:
            col['y'] += col['speed']
            if random.random() < 0.1:
                idx = random.randint(0, len(col['chars']) - 1)
                col['chars'][idx] = random.choice(self.chars)
            if col['y'] - col['length'] > self.height() // self.cell_size:
                col['y'] = random.randint(-20, 0)
                col['speed'] = random.uniform(0.3, 1.0)
                col['length'] = random.randint(5, 25)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0))
        font = QFont("Monospace", 10, QFont.Weight.Bold)
        painter.setFont(font)
        for x_idx, col in enumerate(self.columns):
            x = x_idx * self.cell_size
            head_y = int(col['y'])
            for i in range(col['length']):
                y = head_y - i
                if y < 0 or y * self.cell_size > self.height():
                    continue
                char = col['chars'][i % len(col['chars'])]
                if i == 0:
                    painter.setPen(QColor(200, 255, 200))
                elif i < 3:
                    painter.setPen(QColor(0, 255, 70))
                else:
                    alpha = max(30, 180 - i * 8)
                    painter.setPen(QColor(0, 140, 30, alpha))
                painter.drawText(x, y * self.cell_size, char)
        painter.end()


class BootScreen(QWidget):
    """Boot screen: matrix rain + loading bar + status messages"""
    boot_complete = pyqtSignal()

    BOOT_MESSAGES = [
        "BIOS v3.14 — System check...",
        "CPU: Intel Core i7-13700K [OK]",
        "RAM: 32GB DDR5 [OK]",
        "ISHROQAI-45xFA kernel loading...",
        "Neural network: initializing...",
        "Encryption module: AES-256 [ACTIVE]",
        "TOR client: connecting...",
        "VPN tunnel: establishing...",
        "Proxy chains: 7 hops [READY]",
        "Database: 2.4TB encrypted [MOUNTED]",
        "User identity: VERIFIED",
        "ISHROQAI-45xFA v1.0 — ONLINE",
    ]

    def __init__(self, ai_name="ISHROQ AI", parent=None):
        super().__init__(parent)
        self.ai_name = ai_name
        self._setup_ui()
        self._msg_idx = 0
        self._progress = 0

        self._msg_timer = QTimer(self)
        self._msg_timer.timeout.connect(self._next_message)
        self._msg_timer.start(350)

    def _setup_ui(self):
        self.setStyleSheet("background: #000000;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(0)

        self.matrix = MatrixRain(self)
        self.matrix.setFixedHeight(300)
        layout.addWidget(self.matrix)

        layout.addSpacing(30)

        # Title
        title = QLabel(self.ai_name if hasattr(self, 'ai_name') else "ISHROQ AI")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: #00FF46;
            font-family: 'Monospace';
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 8px;
        """)
        layout.addWidget(title)

        subtitle = QLabel("Intelligent Security Assistant")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            color: #007A22;
            font-family: 'Monospace';
            font-size: 13px;
            letter-spacing: 4px;
            margin-bottom: 30px;
        """)
        layout.addWidget(subtitle)

        layout.addSpacing(40)

        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.status_label.setStyleSheet("""
            color: #00CC3A;
            font-family: 'Monospace';
            font-size: 12px;
            padding-left: 20px;
        """)
        layout.addWidget(self.status_label)

        layout.addSpacing(8)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #001A0A;
                border: 1px solid #003A14;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00FF46, stop:1 #00CC3A);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)

        layout.addStretch()

        bottom = QLabel("[ AUTHORIZED ACCESS ONLY ]")
        bottom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bottom.setStyleSheet("""
            color: #003A14;
            font-family: 'Monospace';
            font-size: 10px;
            letter-spacing: 3px;
        """)
        layout.addWidget(bottom)

    def _next_message(self):
        if self._msg_idx >= len(self.BOOT_MESSAGES):
            self._msg_timer.stop()
            QTimer.singleShot(600, self.boot_complete.emit)
            return
        msg = self.BOOT_MESSAGES[self._msg_idx]
        self.status_label.setText(f"> {msg}")
        self._msg_idx += 1
        self._progress = int((self._msg_idx / len(self.BOOT_MESSAGES)) * 100)
        self.progress_bar.setValue(self._progress)
