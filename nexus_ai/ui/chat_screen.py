"""Main chat interface — NEXUS AI matrix style"""
import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QPushButton, QFrame, QSizePolicy, QLineEdit, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QUrl
from PyQt6.QtGui import QColor, QPainter, QFont, QTextCharFormat, QTextCursor, QDesktopServices

_URL_RE = re.compile(r'(https?://\S+)')

def _linkify(text):
    parts = _URL_RE.split(text)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            result.append(part.replace('\n', '<br>'))
        else:
            result.append(
                f'<a href="{part}" style="color:#00DDFF;text-decoration:underline;">{part}</a>'
            )
    return ''.join(result)


# ── Small helper widgets ──────────────────────────────────────────────────────

class BlinkingDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(10, 10)
        self._on = True
        t = QTimer(self)
        t.timeout.connect(self._blink)
        t.start(600)

    def _blink(self):
        self._on = not self._on
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("#00FF46") if self._on else QColor("#003A14")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(0, 0, 10, 10)
        painter.end()


class MessageBubble(QLabel):
    def __init__(self, text, is_ai=True, parent=None):
        super().__init__(parent)
        self.setWordWrap(True)
        self.setOpenExternalLinks(True)
        self.setTextFormat(Qt.TextFormat.RichText)
        self.setText(_linkify(text))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        if is_ai:
            self.setStyleSheet("""
                QLabel {
                    color: #00FF46;
                    font-family: 'Monospace';
                    font-size: 13px;
                    background: #000D04;
                    border-left: 2px solid #00FF46;
                    padding: 12px 16px;
                    margin: 4px 60px 4px 0px;
                    line-height: 1.6;
                }
            """)
        else:
            self.setStyleSheet("""
                QLabel {
                    color: #AAFFCC;
                    font-family: 'Monospace';
                    font-size: 13px;
                    background: #001A0A;
                    border-right: 2px solid #AAFFCC;
                    padding: 10px 16px;
                    margin: 4px 0px 4px 60px;
                    font-style: italic;
                }
            """)


class TypingIndicator(QLabel):
    def __init__(self, name="ISHROQ AI", parent=None):
        super().__init__(parent)
        self._name = name
        self._dots = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(400)
        self.setStyleSheet("""
            color: #007A22;
            font-family: 'Monospace';
            font-size: 13px;
            padding: 8px 16px;
        """)
        self._animate()

    def _animate(self):
        self._dots = (self._dots + 1) % 4
        self.setText(self._name + "." * self._dots)


# ── Inline action buttons (DARK WEB / CLEAR WEB) ─────────────────────────────

class ActionButtonsWidget(QWidget):
    """Chat ichida markazda ko'rinadigan 2 ta tanlov tugmasi"""
    choice = pyqtSignal(str)   # 'dark' or 'clear'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)

        label = QLabel("< SELECT DIRECTION >")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("""
            color: #007A22;
            font-family: 'Monospace';
            font-size: 11px;
            letter-spacing: 2px;
            margin-bottom: 10px;
        """)
        outer.addWidget(label)

        row = QHBoxLayout()
        row.setSpacing(16)
        row.addStretch()

        dark_btn = QPushButton("◈  DARK WEB")
        dark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        dark_btn.setFixedSize(160, 50)
        dark_btn.setStyleSheet("""
            QPushButton {
                background: #0A0000;
                color: #FF4444;
                border: 1px solid #660000;
                font-family: 'Monospace';
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 3px;
            }
            QPushButton:hover {
                background: #1A0000;
                border-color: #FF4444;
                color: #FF6666;
            }
            QPushButton:pressed { background: #330000; }
        """)
        dark_btn.clicked.connect(lambda: self.choice.emit('dark'))
        row.addWidget(dark_btn)

        clear_btn = QPushButton("◈  CLEAR WEB")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setFixedSize(160, 50)
        clear_btn.setStyleSheet("""
            QPushButton {
                background: #000A0A;
                color: #00DDFF;
                border: 1px solid #006677;
                font-family: 'Monospace';
                font-size: 13px;
                font-weight: bold;
                letter-spacing: 3px;
            }
            QPushButton:hover {
                background: #001A1A;
                border-color: #00DDFF;
                color: #44EEFF;
            }
            QPushButton:pressed { background: #003333; }
        """)
        clear_btn.clicked.connect(lambda: self.choice.emit('clear'))
        row.addWidget(clear_btn)

        row.addStretch()
        outer.addLayout(row)


# ── Inline terminal widget ────────────────────────────────────────────────────

class InlineTerminal(QWidget):
    """Chat ichiga embed qilinadigan terminal animatsiyasi"""
    complete = pyqtSignal()

    def __init__(self, sequence, ai_name="ISHROQ AI", parent=None):
        super().__init__(parent)
        self._ai_name = ai_name
        self._lines = sequence
        self._line_idx = 0
        self._char_idx = 0
        self._current_line = ""
        self._delay_ms = 50
        self._char_timer = QTimer(self)
        self._char_timer.timeout.connect(self._type_next_char)
        self._setup_ui()
        QTimer.singleShot(300, self._next_line)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(0)

        header = QLabel(f"[ {self._ai_name} — TERMINAL ACTIVE ]")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            color: #00DDFF;
            font-family: 'Monospace';
            font-size: 10px;
            letter-spacing: 3px;
            border: 1px solid #003A14;
            border-bottom: none;
            padding: 4px;
            background: #000500;
        """)
        layout.addWidget(header)

        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("Monospace", 11))
        self.terminal.setMinimumHeight(220)
        self.terminal.setMaximumHeight(320)
        self.terminal.setStyleSheet("""
            QTextEdit {
                background: #000500;
                color: #00FF46;
                border: 1px solid #003A14;
                padding: 10px;
                selection-background-color: #003A14;
            }
            QScrollBar:vertical {
                background: #000500;
                width: 4px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #003A14;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)
        layout.addWidget(self.terminal)

    def _next_line(self):
        if self._line_idx >= len(self._lines):
            self._on_complete()
            return
        text, delay = self._lines[self._line_idx]
        self._line_idx += 1
        self._delay_ms = max(80, int(delay * 1200))

        if text == "":
            self._append_text("\n")
            QTimer.singleShot(60, self._next_line)
        else:
            self._current_line = text
            self._char_idx = 0
            self._char_timer.start(14)

    def _type_next_char(self):
        if self._char_idx < len(self._current_line):
            self._append_char(self._current_line[self._char_idx])
            self._char_idx += 1
        else:
            self._char_timer.stop()
            self._append_text("\n")
            QTimer.singleShot(self._delay_ms, self._next_line)

    def _append_char(self, ch):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        fmt = QTextCharFormat()
        line = self._current_line
        if line.startswith(">>>"):
            if any(w in line for w in ("ALERT", "ERROR", "DETECTED", "WARNING")):
                fmt.setForeground(QColor("#FF4444"))
            elif any(w in line for w in ("COMPLETE", "SUCCESS", "GRANTED", "ACTIVATED")):
                fmt.setForeground(QColor("#00FF88"))
            else:
                fmt.setForeground(QColor("#00DDFF"))
        elif line.strip().startswith("["):
            if any(w in line for w in ("OPEN", "✓", "ACTIVE")):
                fmt.setForeground(QColor("#00FF46"))
            elif any(w in line for w in ("CLOSED", "FILTERED")):
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
        fmt.setForeground(QColor("#003A14"))
        cursor.insertText(text, fmt)
        self.terminal.setTextCursor(cursor)

    def _on_complete(self):
        self._append_text("\n" + "─" * 42 + "\n")
        self.complete.emit()


# ── Main ChatScreen ───────────────────────────────────────────────────────────

class ChatScreen(QWidget):
    choice_made = pyqtSignal(str)
    web_choice = pyqtSignal(str)
    user_message = pyqtSignal(str)
    action_choice = pyqtSignal(str)   # 'dark' or 'clear'

    def __init__(self, ai_name="NEXUS", operator_name="OPERATOR", parent=None):
        super().__init__(parent)
        self.ai_name = ai_name
        self.operator_name = operator_name
        self._typing_indicator = None
        self._action_buttons = None
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet("background: #000000;")

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # LEFT PANEL (40%) — bo'sh joy
        left_panel = QWidget()
        left_panel.setStyleSheet("background: #000000;")
        left_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        root.addWidget(left_panel, 40)

        # Vertikal ajratuvchi chiziq
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.VLine)
        divider.setFixedWidth(1)
        divider.setStyleSheet("background: #003A14; border: none;")
        root.addWidget(divider)

        # RIGHT PANEL (60%) — chat interfeysi
        right_panel = QWidget()
        right_panel.setStyleSheet("background: #000000;")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # TOP BAR
        top_bar = QWidget()
        top_bar.setFixedHeight(52)
        top_bar.setStyleSheet("background: #000D04; border-bottom: 1px solid #003A14;")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        status_dot = BlinkingDot()
        top_layout.addWidget(status_dot)
        top_layout.addSpacing(10)

        ai_label = QLabel(self.ai_name)
        ai_label.setStyleSheet("""
            color: #00FF46;
            font-family: 'Monospace';
            font-size: 16px;
            font-weight: bold;
            letter-spacing: 4px;
        """)
        top_layout.addWidget(ai_label)

        version_label = QLabel("v2.1")
        version_label.setStyleSheet("""
            color: #003A14;
            font-family: 'Monospace';
            font-size: 11px;
            padding-top: 4px;
        """)
        top_layout.addWidget(version_label)
        top_layout.addStretch()

        op_label = QLabel(f"[ {self.operator_name} ]")
        op_label.setStyleSheet("""
            color: #007A22;
            font-family: 'Monospace';
            font-size: 11px;
            letter-spacing: 2px;
        """)
        top_layout.addWidget(op_label)

        right_layout.addWidget(top_bar)

        # CHAT SCROLL AREA
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: #000000; }
            QScrollBar:vertical {
                background: #000D04;
                width: 6px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #003A14;
                border-radius: 3px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        """)

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background: #000000;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(20, 20, 20, 20)
        self.chat_layout.setSpacing(6)
        self.chat_layout.addStretch()

        self.scroll_area.setWidget(self.chat_container)
        right_layout.addWidget(self.scroll_area)

        # INPUT PANEL
        input_panel = QWidget()
        input_panel.setFixedHeight(60)
        input_panel.setStyleSheet("background: #000D04; border-top: 1px solid #003A14;")
        input_layout = QHBoxLayout(input_panel)
        input_layout.setContentsMargins(16, 10, 16, 10)
        input_layout.setSpacing(10)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("> Type a message...")
        self.text_input.setEnabled(False)
        self.text_input.setStyleSheet("""
            QLineEdit {
                background: #000000;
                color: #00FF46;
                border: 1px solid #003A14;
                font-family: 'Monospace';
                font-size: 13px;
                padding: 6px 12px;
            }
            QLineEdit:focus { border-color: #00FF46; }
            QLineEdit:disabled {
                color: #002A10;
                border-color: #001A0A;
                background: #000300;
            }
        """)
        self.text_input.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.text_input)

        self.send_btn = QPushButton("SEND")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setFixedSize(70, 36)
        self.send_btn.setEnabled(False)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #003A14;
                border: 1px solid #001A0A;
                font-family: 'Monospace';
                font-size: 11px;
                letter-spacing: 2px;
            }
            QPushButton:enabled { color: #007A22; border-color: #003A14; }
            QPushButton:enabled:hover {
                background: #001A0A;
                border-color: #00FF46;
                color: #00FF46;
            }
            QPushButton:enabled:pressed { background: #002A0A; }
        """)
        self.send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(self.send_btn)

        right_layout.addWidget(input_panel)
        root.addWidget(right_panel, 60)

    # ── Public API ────────────────────────────────────────────────────────────

    def enable_input(self, enabled=True):
        self.text_input.setEnabled(enabled)
        self.send_btn.setEnabled(enabled)
        if enabled:
            self.text_input.setFocus()

    def add_ai_message(self, text, with_typing=True, callback=None):
        if with_typing:
            self._show_typing_indicator()
            delay = min(2500, max(800, len(text) * 15))
            QTimer.singleShot(delay, lambda: self._show_ai_message(text, callback))
        else:
            self._show_ai_message(text, callback)

    def add_user_message(self, text):
        bubble = MessageBubble(text, is_ai=False)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self._scroll_to_bottom()

    def show_action_buttons(self):
        """DARK WEB / CLEAR WEB tugmalarini chat ichiga qo'sh"""
        self._remove_action_buttons()
        btn_widget = ActionButtonsWidget()
        btn_widget.choice.connect(self._on_action_choice)
        self._action_buttons = btn_widget
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, btn_widget)
        self._scroll_to_bottom()

    def start_inline_terminal(self, sequence, on_complete=None):
        """Terminal animatsiyasini chat ichida ishga tushir"""
        terminal = InlineTerminal(sequence, ai_name=self.ai_name)
        if on_complete:
            terminal.complete.connect(on_complete)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, terminal)
        self._scroll_to_bottom()

    # ── Private ───────────────────────────────────────────────────────────────

    def _send_message(self):
        text = self.text_input.text().strip()
        if text and self.text_input.isEnabled():
            self.text_input.clear()
            self.add_user_message(text)
            self.user_message.emit(text)

    def _on_action_choice(self, which):
        self._remove_action_buttons()
        self.action_choice.emit(which)

    def _remove_action_buttons(self):
        if self._action_buttons:
            self._action_buttons.setParent(None)
            self._action_buttons = None

    def _show_ai_message(self, text, callback=None):
        self._remove_typing_indicator()
        bubble = MessageBubble(text, is_ai=True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)
        self._scroll_to_bottom()
        if callback:
            callback()

    def _show_typing_indicator(self):
        if self._typing_indicator:
            return
        self._typing_indicator = TypingIndicator(self.ai_name)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, self._typing_indicator)
        self._scroll_to_bottom()

    def _remove_typing_indicator(self):
        if self._typing_indicator:
            self._typing_indicator.setParent(None)
            self._typing_indicator = None

    def _scroll_to_bottom(self):
        QTimer.singleShot(80, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))

    # ── Legacy stubs (scripted dialogue bilan compat) ────────────────────────
    def show_choices(self, choices): pass
    def show_web_choice(self): pass
    def clear_and_shutdown(self): pass
