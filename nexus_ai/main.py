#!/usr/bin/env python3
"""ISHROQAI-45xFA — Hacker AI Interface"""
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase

from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ISHROQAI-45xFA")
    app.setStyle('Fusion')

    # Qahramonni argumentdan olish: python main.py umid
    character = sys.argv[1].lower() if len(sys.argv) > 1 else 'default'

    window = MainWindow(character=character)
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
