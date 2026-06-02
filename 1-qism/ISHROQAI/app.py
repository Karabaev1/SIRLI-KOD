#!/usr/bin/env python3
"""ISHROQAI-45xFA — launches the main NEXUS AI interface"""
import subprocess, sys, os

NEXUS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'nexus_ai', 'main.py'
)

if __name__ == '__main__':
    subprocess.Popen([sys.executable, NEXUS])
