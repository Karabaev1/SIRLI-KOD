"""Virtual world screen — terminal animation sequence"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor


class VirtualWorldScreen(QWidget):
    """Terminal animatsiya ekrani — virtual hayot simulyatsiyasi"""
    sequence_complete = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lines = []
        self._line_idx = 0
        self._char_idx = 0
        self._current_line = ""
        self._delay = 0.05
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._type_next)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("background: #000000;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(0)

        # Top bar
        top_bar = QLabel("[ ISHROQ AI — VIRTUAL INTERFACE ACTIVE ]")
        top_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_bar.setStyleSheet("""
            color: #00FF46;
            font-family: 'Monospace';
            font-size: 11px;
            letter-spacing: 4px;
            border-bottom: 1px solid #003A14;
            padding: 8px;
            margin-bottom: 10px;
        """)
        layout.addWidget(top_bar)

        # Terminal output
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("Monospace", 12))
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: #000000;
                color: #00FF46;
                border: none;
                padding: 10px;
                selection-background-color: #003A14;
            }
        """)
        layout.addWidget(self.terminal)

        # Return button (hidden until done)
        self.return_btn = QPushButton("[ BAZAGA QAYTISH — ENTER ]")
        self.return_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.return_btn.hide()
        self.return_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #00FF46;
                border: 1px solid #00FF46;
                font-family: 'Monospace';
                font-size: 13px;
                font-weight: bold;
                padding: 12px;
                letter-spacing: 3px;
            }
            QPushButton:hover {
                background: #001A0A;
                border-color: #00FF88;
                color: #00FF88;
            }
            QPushButton:pressed {
                background: #003A14;
            }
        """)
        self.return_btn.clicked.connect(self.sequence_complete.emit)
        layout.addWidget(self.return_btn)

    def play_sequence(self, sequence_lines):
        """Sequence ni boshlash: list of (text, delay) tuples"""
        self.terminal.clear()
        self.return_btn.hide()
        self._lines = sequence_lines
        self._line_idx = 0
        self._next_line()

    def _next_line(self):
        if self._line_idx >= len(self._lines):
            self._on_complete()
            return

        text, delay = self._lines[self._line_idx]
        self._line_idx += 1
        self._delay_ms = max(10, int(delay * 1000))

        if text == "":
            self._append_text("\n")
            QTimer.singleShot(100, self._next_line)
        else:
            self._current_line = text
            self._char_idx = 0
            self._timer.start(18)

    def _type_next(self):
        if self._char_idx < len(self._current_line):
            ch = self._current_line[self._char_idx]
            self._append_char(ch)
            self._char_idx += 1
        else:
            self._timer.stop()
            self._append_text("\n")
            QTimer.singleShot(self._delay_ms, self._next_line)

    def _append_char(self, ch):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        fmt = QTextCharFormat()

        # Color based on content
        line = self._current_line
        if line.startswith(">>>"):
            if "ALERT" in line or "ERROR" in line or "DETECTED" in line:
                fmt.setForeground(QColor("#FF4444"))
            elif "COMPLETE" in line or "SUCCESS" in line or "GRANTED" in line:
                fmt.setForeground(QColor("#00FF88"))
            else:
                fmt.setForeground(QColor("#00DDFF"))
        elif line.strip().startswith("["):
            if "OPEN" in line or "✓" in line or "ACTIVE" in line:
                fmt.setForeground(QColor("#00FF46"))
            elif "CLOSED" in line or "FILTERED" in line:
                fmt.setForeground(QColor("#FF4444"))
            else:
                fmt.setForeground(QColor("#AAAAAA"))
        elif line.startswith("    "):
            fmt.setForeground(QColor("#888888"))
        else:
            fmt.setForeground(QColor("#00FF46"))

        cursor.insertText(ch, fmt)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()

    def _append_text(self, text):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        fmt.setForeground(QColor("#00FF46"))
        cursor.insertText(text, fmt)
        self.terminal.setTextCursor(cursor)

    def _on_complete(self):
        self._append_text("\n")
        self._append_text("_" * 50 + "\n")
        self._append_text("\n")
        self.return_btn.show()
