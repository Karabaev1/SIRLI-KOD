#!/usr/bin/env python3
"""ISHROQAI-45xFA — Setup Wizard"""
import tkinter as tk
import threading, random, time, subprocess, sys, os

DIR      = os.path.dirname(os.path.abspath(__file__))
APP      = os.path.join(DIR, 'app.py')
ICON_PNG = os.path.join(DIR, 'icon.png')

DARK  = '#0d1117'
DARK2 = '#010409'
CYAN  = '#00e5ff'
GREEN = '#00ff88'
WHITE = '#f0f6fc'
DIM   = '#8b949e'
RED   = '#ff3b3b'


# ── Helpers ────────────────────────────────────────────────────────────────

def _hex_line():
    return '  ' + ' '.join(f'{random.randint(0,255):02x}' for _ in range(20))

def _code_line():
    tpls = [
        '0x{a:08x}  →  0x{b:08x}   [{m}]',
        '[+] module <{m}> mapped  base=0x{a:08x}',
        'SYS_{m}  eax=0x{a:08x}  ecx=0x{b:04x}',
        'INJECT  offset={a:04x}  len={b:03x}  flags={c:02x}',
        'RECV {b} bytes  pipe/{m} → fd/{a:02x}',
        'MAP  0x{a:08x}-0x{b:08x}  [{m}]',
        'AUTH  token={a:016x}  uid={b}',
        '[*] scanning 192.168.{b}.{c}:{a}',
    ]
    mods = ['net','auth','crypt','mem','krnl','io','sys','ipc','payload','shell']
    t = random.choice(tpls)
    return t.format(
        a=random.randint(0, 0xffffffff),
        b=random.randint(0, 0xffff),
        c=random.randint(0, 0xff),
        m=random.choice(mods),
    )[:64]


# ── Installer ──────────────────────────────────────────────────────────────

class Installer(tk.Tk):
    STEPS = [
        ('Verifying system compatibility...',           0.08),
        ('Connecting to ISHROQAI update server...',     0.16),
        ('Authenticating license 45xFA-CORE-7731...',   0.23),
        ('Downloading neural core (1.2 GB)...',         0.38),
        ('Downloading language model weights...',       0.51),
        ('Downloading security module...',              0.60),
        ('Extracting AI inference engine...',           0.70),
        ('Installing NEXUS-45 neural backend...',       0.79),
        ('Configuring security protocols...',           0.87),
        ('Integrating system services...',              0.93),
        ('Running post-install validation...',          0.97),
        ('Finalizing — writing system registry...',     1.00),
    ]

    LOG_INIT = [
        '[*] ISHROQAI-45xFA Setup Wizard v7731',
        '[*] Checking operating system...',
        '[✓] Linux x86_64 — fully supported',
        '[*] Checking Python runtime...',
        '[✓] Python 3.10+ — OK',
        '[*] Verifying disk space...',
        '[✓] Available: 18.4 GB — sufficient',
        '[*] Verifying RAM...',
        '[✓] RAM 16 GB — sufficient',
        '[*] Establishing connection to ai-core.ishroq.net...',
        '[✓] TLS 1.3 secure channel established',
        '[*] Validating product license...',
        '[✓] License 45xFA-CORE-7731 — VALID  (perpetual)',
        '[*] Starting installation sequence...',
        '',
    ]

    def __init__(self):
        super().__init__()
        self.title('ISHROQAI-45xFA — Setup Wizard')
        self.resizable(False, False)
        self.configure(bg=DARK)

        W, H = 640, 420
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f'{W}x{H}+{(sw-W)//2}+{(sh-H)//2}')

        self._set_icon()
        self._build()
        self.after(700, self._start)

    def _set_icon(self):
        try:
            img = tk.PhotoImage(file=ICON_PNG)
            self.iconphoto(True, img)
            self._icon_ref = img
        except Exception:
            pass

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=DARK2, pady=20)
        hdr.pack(fill='x')
        try:
            img = tk.PhotoImage(file=ICON_PNG).subsample(4, 4)
            tk.Label(hdr, image=img, bg=DARK2).pack()
            self._hdr_icon = img
        except Exception:
            pass
        tk.Label(hdr, text='ISHROQAI-45xFA',
                 font=('Courier New', 22, 'bold'), fg=CYAN, bg=DARK2).pack()
        tk.Label(hdr, text='Advanced Intelligence Assistant  ·  Setup Wizard',
                 font=('Courier New', 9), fg=DIM, bg=DARK2).pack(pady=(2, 0))

        tk.Frame(self, height=1, bg='#21262d').pack(fill='x')

        body = tk.Frame(self, bg=DARK, padx=40, pady=22)
        body.pack(fill='both', expand=True)

        tk.Label(body, text='Installation Progress',
                 font=('Segoe UI', 10, 'bold'), fg=WHITE, bg=DARK,
                 anchor='w').pack(anchor='w', pady=(0, 10))

        self._step_var = tk.StringVar(value='Preparing installer...')
        tk.Label(body, textvariable=self._step_var,
                 font=('Courier New', 9), fg=CYAN, bg=DARK, anchor='w').pack(anchor='w', pady=(0, 6))

        self._bar_cv = tk.Canvas(body, height=8, bg='#21262d', highlightthickness=0)
        self._bar_cv.pack(fill='x')
        self._bar_r = self._bar_cv.create_rectangle(0, 0, 0, 8, fill=CYAN, outline='')

        self._pct_var = tk.StringVar(value='0%')
        tk.Label(body, textvariable=self._pct_var,
                 font=('Courier New', 8), fg=DIM, bg=DARK, anchor='e').pack(anchor='e', pady=(3, 0))

        log_frame = tk.Frame(body, bg='#010409')
        log_frame.pack(fill='both', expand=True, pady=(10, 0))
        self._log = tk.Text(log_frame, height=8, bg='#010409', fg='#3fb950',
                            font=('Courier New', 8), relief='flat',
                            state='disabled', padx=10, pady=8)
        self._log.pack(fill='both', expand=True)

        tk.Frame(self, height=1, bg='#21262d').pack(fill='x')
        foot = tk.Frame(self, bg=DARK2, pady=10)
        foot.pack(fill='x', padx=20)
        tk.Label(foot, text='© 2025 ISHROQAI Technologies — All rights reserved.',
                 font=('Segoe UI', 8), fg='#3d444d', bg=DARK2).pack(side='left')
        self._ok_lbl = tk.Label(foot, text='', font=('Segoe UI', 8, 'bold'),
                                 fg=GREEN, bg=DARK2)
        self._ok_lbl.pack(side='right')

    def _log_add(self, line):
        self._log.config(state='normal')
        self._log.insert('end', line + '\n')
        self._log.see('end')
        self._log.config(state='disabled')

    def _set_pct(self, v):
        self._pct_var.set(f'{int(v*100)}%')
        w = self._bar_cv.winfo_width()
        self._bar_cv.coords(self._bar_r, 0, 0, int(w * v), 8)

    def _start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        for line in self.LOG_INIT:
            time.sleep(0.18)
            self.after(0, self._log_add, line)

        for label, target in self.STEPS:
            self.after(0, self._step_var.set, f'▶  {label}')
            cur = self._bar_cv.coords(self._bar_r)[2] / max(self._bar_cv.winfo_width(), 1)
            for i in range(40):
                pct = cur + (target - cur) * (i / 39)
                self.after(0, self._set_pct, pct)
                time.sleep(0.06)
            for _ in range(random.randint(3, 7)):
                time.sleep(random.uniform(0.1, 0.35))
                self.after(0, self._log_add, _hex_line())
            time.sleep(random.uniform(0.4, 0.9))

        self.after(0, self._log_add, '')
        self.after(0, self._log_add, '[✓] All components installed successfully.')
        self.after(0, self._ok_lbl.config, {'text': '✓  SUCCESS'})
        self.after(0, self._step_var.set, '✓  Installation complete — launching ISHROQAI-45xFA...')
        time.sleep(1.8)
        self.after(0, self._to_hack)

    def _to_hack(self):
        self.withdraw()
        HackEffect(on_done=self._finish)

    def _finish(self):
        subprocess.Popen([sys.executable, APP])
        self.after(300, self.destroy)


# ── Hack Effect — 30 seconds ───────────────────────────────────────────────

class HackEffect(tk.Tk):

    MSGS = [
        ('INITIALIZING PAYLOAD DELIVERY...',           '#00ff88'),
        ('PROBING SYSTEM ARCHITECTURE...',             '#00e5ff'),
        ('ESTABLISHING ENCRYPTED TUNNEL...',           '#00ff88'),
        ('BYPASSING FIREWALL — RULES FLUSHED',         '#ffd700'),
        ('KERNEL MODULE INJECTION: IN PROGRESS...',    '#ffd700'),
        ('ESCALATING PRIVILEGES  →  [root] ✓',        '#ff9800'),
        ('LOADING PERSISTENCE MODULE...',              '#00e5ff'),
        ('WRITING TO /etc/cron.d/ishroq...',           '#00ff88'),
        ('MAPPING INTERNAL NETWORK TOPOLOGY...',       '#00e5ff'),
        ('DEPLOYING KEYLOGGER MODULE...',              '#ff4444'),
        ('INTERCEPTING MEMORY SEGMENTS...',            '#ffd700'),
        ('EXFILTRATING CREDENTIAL STORE...',           '#ff4444'),
        ('BACKDOOR CHANNEL OPEN — PORT 4444',          '#ff4444'),
        ('COVERING TRACKS — CLEARING LOGS...',         '#00ff88'),
        ('REMOVING INSTALL ARTIFACTS...',              '#00e5ff'),
        ('STAGING C2 COMMUNICATION...',                '#ffd700'),
        ('PAYLOAD FULLY DEPLOYED ✓',                   '#ff4444'),
        ('PERSISTENCE CONFIRMED ✓',                    '#00ff88'),
        ('✓  SYSTEM FULLY COMPROMISED',                '#ff0000'),
    ]

    # 10 terminal pozitsiyasi
    POSITIONS = [
        (20,   80,  400, 200),   # top-left
        (450,  60,  420, 220),   # top-center
        (900,  80,  380, 200),   # top-right
        (20,  330,  360, 210),   # mid-left
        (420, 310,  440, 230),   # center
        (900, 320,  380, 220),   # mid-right
        (20,  580,  420, 200),   # bottom-left
        (470, 590,  400, 190),   # bottom-center
        (910, 570,  360, 200),   # bottom-right
        (350, 160,  380, 180),   # extra center-top
    ]

    COLORS = ['#00ff88', '#00e5ff', '#ffd700', '#ff4444',
              '#ff00ff', '#ffffff', '#ff9800', '#00ffaa']

    def __init__(self, on_done):
        super().__init__()
        self._on_done  = on_done
        self._running  = True
        self._msg_idx  = 0
        self._prog     = 0.0
        self._terms    = []
        self._blink_on = True

        self.attributes('-fullscreen', True)
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.configure(bg='black')

        self._c = tk.Canvas(self, bg='black', highlightthickness=0)
        self._c.pack(fill='both', expand=True)

        self.after(100, self._build)

        # 30 soniya ushlab turadi
        self.after(30000, self._end)

    # ── Build ──────────────────────────────────────────────────────────────

    def _build(self):
        c   = self._c
        sw  = self.winfo_screenwidth()
        sh  = self.winfo_screenheight()
        self._sw, self._sh = sw, sh

        # Warning title (miltillaydi)
        self._title_id = c.create_text(
            sw // 2, 34,
            text='⚠   SYSTEM OVERRIDE — ISHROQAI-45xFA   ⚠',
            font=('Courier New', 26, 'bold'),
            fill='#ff3b3b', anchor='center')

        self._sub_id = c.create_text(
            sw // 2, 68,
            text='CORE INJECTION IN PROGRESS — DO NOT POWER OFF',
            font=('Courier New', 11),
            fill='#550000', anchor='center')

        # Terminal oynalar
        for i, (x, y, w, h) in enumerate(self.POSITIONS):
            c.create_rectangle(x, y, x+w, y+h,
                               fill='#040804', outline='#1a3a1a', width=1,
                               tags=f'term_box_{i}')
            c.create_rectangle(x, y, x+w, y+20,
                               fill='#0a1f0a', outline='', tags=f'term_hdr_{i}')
            c.create_text(x+10, y+10,
                          text=f'root@ISHROQ [{i+1}]:~#',
                          font=('Courier New', 7, 'bold'),
                          fill='#00c853', anchor='w', tags=f'term_lbl_{i}')
            txt = tk.Text(self,
                          bg='#020602', fg='#00e676',
                          font=('Courier New', 7),
                          relief='flat', state='disabled',
                          padx=4, pady=4, highlightthickness=0)
            c.create_window(x, y+22, anchor='nw', window=txt,
                            width=w, height=h-22, tags=f'term_win_{i}')
            self._terms.append(txt)

        # Status maydoni
        self._status_id = c.create_text(
            sw // 2, sh - 180,
            text='', font=('Courier New', 13, 'bold'),
            fill='#00ff88', anchor='center')

        # Progress bar
        by = sh - 110
        c.create_rectangle(sw//2-360, by, sw//2+360, by+16,
                           fill='#040a04', outline='#1a3a1a', width=1)
        self._prog_r   = c.create_rectangle(sw//2-360, by, sw//2-360, by+16,
                                            fill='#00c853', outline='')
        self._prog_lbl = c.create_text(
            sw//2, by + 28,
            text='SYSTEM COMPROMISE: 0%',
            font=('Courier New', 11, 'bold'),
            fill='#00c853', anchor='center')

        # Vaqt ko'rsatkichi
        self._timer_id = c.create_text(
            sw - 20, sh - 20,
            text='', font=('Courier New', 10),
            fill='#1a3a1a', anchor='se')

        self._start_time = time.time()

        # Animatsiyalar
        self._scroll_terms()
        self._show_msgs()
        self._anim_prog()
        self._blink_title()
        self._cycle_term_colors()
        self._update_timer()
        self._flicker_terms()

    # ── Animations ─────────────────────────────────────────────────────────

    def _scroll_terms(self):
        if not self._running:
            return
        for t in self._terms:
            if not t.winfo_exists():
                continue
            t.config(state='normal')
            t.insert('end', _code_line() + '\n')
            t.see('end')
            if int(t.index('end-1c').split('.')[0]) > 60:
                t.delete('1.0', '4.0')
            t.config(state='disabled')
        self.after(50, self._scroll_terms)

    def _show_msgs(self):
        if not self._running or self._msg_idx >= len(self.MSGS):
            return
        text, color = self.MSGS[self._msg_idx]
        self._c.itemconfig(self._status_id, text=text, fill=color)
        self._msg_idx += 1
        interval = 1400 if self._msg_idx < 5 else 1100
        self.after(interval, self._show_msgs)

    def _anim_prog(self):
        if not self._running:
            return
        self._prog = min(self._prog + random.uniform(0.3, 1.2), 100)
        sw, sh = self._sw, self._sh
        by = sh - 110
        filled = int((sw//2 - 360) + 720 * (self._prog / 100))
        # Rang progress ga qarab o'zgaradi
        if self._prog < 40:
            color = '#00c853'
        elif self._prog < 70:
            color = '#ffd700'
        elif self._prog < 90:
            color = '#ff9800'
        else:
            color = '#ff3b3b'
        self._c.coords(self._prog_r, sw//2-360, by, filled, by+16)
        self._c.itemconfig(self._prog_r, fill=color)
        self._c.itemconfig(self._prog_lbl,
                           text=f'SYSTEM COMPROMISE: {int(self._prog)}%',
                           fill=color)
        if self._prog < 100:
            self.after(30, self._anim_prog)

    def _blink_title(self):
        if not self._running:
            return
        colors = ['#ff3b3b', '#ff0000', '#cc0000', '#ff6666']
        self._c.itemconfig(self._title_id,
                           fill=random.choice(colors))
        self.after(400, self._blink_title)

    def _cycle_term_colors(self):
        if not self._running:
            return
        for i in range(len(self.POSITIONS)):
            border_color = random.choice(['#1a3a1a', '#003300', '#005500',
                                          '#003322', '#001a00'])
            txt_color    = random.choice(['#00e676', '#00ff88', '#00c853',
                                          '#69f0ae', '#00bfa5'])
            try:
                self._c.itemconfig(f'term_box_{i}', outline=border_color)
                self._terms[i].config(fg=txt_color)
            except Exception:
                pass
        self.after(600, self._cycle_term_colors)

    def _flicker_terms(self):
        """Terminallar o'chib-yonib turadi"""
        if not self._running:
            return
        i = random.randint(0, len(self.POSITIONS) - 1)
        try:
            self._c.itemconfig(f'term_win_{i}', state='hidden')
            self.after(random.randint(80, 300),
                       lambda: self._c.itemconfig(f'term_win_{i}', state='normal'))
        except Exception:
            pass
        self.after(random.randint(200, 700), self._flicker_terms)

    def _update_timer(self):
        if not self._running:
            return
        elapsed = time.time() - self._start_time
        self._c.itemconfig(self._timer_id,
                           text=f'{elapsed:.1f}s')
        self.after(100, self._update_timer)

    # ── Color flash phase (son'gi 5 soniya) ───────────────────────────────

    def _color_chaos(self, step=0):
        """Oxirida rang chaos"""
        colors = ['#ff0000', 'black', '#00ff00', 'black',
                  '#0000ff', 'black', '#ffff00', 'black',
                  '#ff00ff', 'black', '#00ffff', 'black',
                  'white', 'black', '#ff4444', 'black']
        if step < len(colors):
            self._c.config(bg=colors[step])
            self.after(90, lambda: self._color_chaos(step + 1))
        else:
            self._c.config(bg='black')
            self._show_final_msg()

    def _show_final_msg(self):
        sw, sh = self._sw, self._sh
        # Katta yashil matn
        self._c.create_text(
            sw // 2, sh // 2 - 20,
            text='BACKDOOR INSTALLED',
            font=('Courier New', 48, 'bold'),
            fill='#00ff88', anchor='center')
        self._c.create_text(
            sw // 2, sh // 2 + 60,
            text='✓   CONNECTION ESTABLISHED   ✓',
            font=('Courier New', 22, 'bold'),
            fill='#00e5ff', anchor='center')
        self.after(2000, self._fade_out)

    # ── End sequence ───────────────────────────────────────────────────────

    def _end(self):
        self._running = False
        self._color_chaos()

    def _fade_out(self, step=10):
        if step >= 0:
            self.attributes('-alpha', step / 10)
            self.after(35, lambda: self._fade_out(step - 1))
        else:
            self.destroy()
            self._on_done()


# ── Entry ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    Installer().mainloop()
