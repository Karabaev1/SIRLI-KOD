"""Main window — screen manager, state machine controller"""
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PyQt6.QtCore import Qt, QTimer

from ui.boot_screen import BootScreen
from ui.chat_screen import ChatScreen
from ui.virtual_world import VirtualWorldScreen
from data.dialogue import VIRTUAL_SEQUENCES
from data.qa_scripts import QA_SCRIPTS
from data.characters import CHARACTERS

AI_NAME = "ISHROQ AI"

DEFAULT_GREETING = (
    'Identifikatsiya tasdiqlandi.\n\n'
    'Salom.\n'
    'Men barcha savollarga va hacking qilishga\n'
    'yordam beruvchi sun\'iy intellektman.\n\n'
    'Tayyor. Buyruqlaringizni kuting.'
)


class MainWindow(QMainWindow):

    def __init__(self, character='default', parent=None):
        super().__init__(parent)

        # Qahramonni CHARACTERS dan olish
        char_cfg = CHARACTERS.get(character, {})
        self.ai_name       = AI_NAME
        self.operator_name = char_cfg.get('operator_name', 'OPERATOR')
        self._greeting     = char_cfg.get('greeting', DEFAULT_GREETING)
        window_title       = char_cfg.get('window_title', f'{AI_NAME} v1.0')

        self.setWindowTitle(window_title)
        self.setMinimumSize(900, 650)
        self.resize(1100, 720)
        self._center_window()
        self.setStyleSheet("QMainWindow { background: #000000; }")

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.boot_screen   = BootScreen(ai_name=self.ai_name)
        self.chat_screen   = ChatScreen(self.ai_name, self.operator_name)
        self.virtual_screen = VirtualWorldScreen()

        self.stack.addWidget(self.boot_screen)    # 0
        self.stack.addWidget(self.chat_screen)    # 1
        self.stack.addWidget(self.virtual_screen) # 2

        self.boot_screen.boot_complete.connect(self._on_boot_complete)
        self.chat_screen.user_message.connect(self._on_user_message)
        self.chat_screen.action_choice.connect(self._on_action_choice)

        self.stack.setCurrentIndex(0)

    # ── Window ────────────────────────────────────────────────────────────────

    def _center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    # ── Boot flow ─────────────────────────────────────────────────────────────

    def _on_boot_complete(self):
        self.stack.setCurrentIndex(1)
        self._play_intro()

    def _play_intro(self):
        """Boot tugagach — qisqa animatsiya, so'ng qahramonning salomi"""
        steps = [
            ('.', 700, False),
            ('. .', 700, False),
            ('. . .', 900, False),
            ('Foydalanuvchi identifikatsiyasi tekshirilmoqda...', 0, True),
        ]
        self._play_step(steps, 0)

    def _play_step(self, steps, idx):
        if idx >= len(steps):
            # Barcha qadamlar tugadi — asosiy salom xabari
            self.chat_screen.add_ai_message(
                self._greeting,
                with_typing=True,
                callback=lambda: self.chat_screen.enable_input(True)
            )
            return

        text, delay, with_typing = steps[idx]
        self.chat_screen.add_ai_message(
            text,
            with_typing=with_typing,
            callback=(
                lambda: self.chat_screen.add_ai_message(
                    self._greeting,
                    with_typing=True,
                    callback=lambda: self.chat_screen.enable_input(True)
                )
            ) if idx == len(steps) - 1 else None
        )
        if idx < len(steps) - 1:
            QTimer.singleShot(delay, lambda: self._play_step(steps, idx + 1))

    # ── User message ──────────────────────────────────────────────────────────

    def _on_user_message(self, text):
        self.chat_screen.enable_input(False)
        answer = self._find_answer(text)
        if answer:
            self.chat_screen.add_ai_message(
                answer,
                with_typing=True,
                callback=lambda: self.chat_screen.show_action_buttons()
            )
        else:
            self.chat_screen.add_ai_message(
                'Buyruq aniqlanmadi.\nQayta urinib ko\'ring yoki boshqa so\'z ishlating.',
                with_typing=True,
                callback=lambda: self.chat_screen.enable_input(True)
            )

    def _find_answer(self, text):
        text_lower = text.lower().strip()
        for script in QA_SCRIPTS:
            for trigger in script['triggers']:
                if trigger.lower() in text_lower:
                    return script['answer']
        return None

    # ── Action choice (DARK / CLEAR) ──────────────────────────────────────────

    def _on_action_choice(self, which):
        if which == 'dark':
            label = ">> DARK WEB — Anonim yo'l tanlandi"
            seq_key = 'darknet_hack'
        else:
            label = ">> CLEAR WEB — Avtorizatsiyalangan yo'l"
            seq_key = 'cleannet_hack'

        self.chat_screen.add_user_message(label)
        sequence = VIRTUAL_SEQUENCES.get(seq_key, [])
        self.chat_screen.start_inline_terminal(
            sequence,
            on_complete=lambda: self.chat_screen.enable_input(True)
        )

    # ── Keyboard ──────────────────────────────────────────────────────────────

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
        elif event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        else:
            super().keyPressEvent(event)
