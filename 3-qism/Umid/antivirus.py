#!/usr/bin/env python3
"""AegisGuard Security Suite v4.2 — serial demo"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

# ─────────────────────────────────────────────
#  COLORS  (dark navy, professional look)
# ─────────────────────────────────────────────
BG       = "#12151e"
PANEL    = "#1a1e2a"
CARD     = "#1e2433"
BORDER   = "#2a3040"
ACCENT   = "#2b7de9"
ACCENT_L = "#4d9ef5"
GREEN    = "#22c55e"
GREEN_D  = "#15803d"
GREEN_BG = "#052e16"
TEXT     = "#e8ecf4"
TEXT2    = "#8594b0"
TEXT3    = "#5a6a82"
RED      = "#ef4444"
YELLOW   = "#f59e0b"

# ─────────────────────────────────────────────
#  INSTALL STEPS
# ─────────────────────────────────────────────
INSTALL_STEPS = [
    ("Preparing installation environment...",    10),
    ("Extracting core components...",            14),
    ("Installing real-time protection engine...", 16),
    ("Updating virus signature database...",      20),
    ("Configuring firewall module...",            12),
    ("Registering system services...",            10),
    ("Setting up scheduled scans...",             8),
    ("Applying security policies...",             6),
    ("Finalizing installation...",                4),
]

# ─────────────────────────────────────────────
#  SCAN LOG ITEMS
# ─────────────────────────────────────────────
SCAN_ITEMS = [
    # System binaries
    ("/usr/bin/bash",                              "clean"),
    ("/usr/bin/python3.11",                        "clean"),
    ("/usr/bin/wget",                              "clean"),
    ("/usr/bin/curl",                              "clean"),
    ("/usr/bin/ssh",                               "clean"),
    ("/usr/bin/nmap",                              "clean"),
    ("/usr/lib/systemd/systemd",                   "clean"),
    ("/usr/lib/x86_64-linux-gnu/libssl.so.3",      "clean"),
    ("/usr/sbin/NetworkManager",                   "clean"),
    ("/usr/sbin/sshd",                             "clean"),
    # Config
    ("/etc/passwd",                                "clean"),
    ("/etc/shadow",                                "clean"),
    ("/etc/hosts",                                 "clean"),
    ("/etc/resolv.conf",                           "clean"),
    ("/etc/ssh/sshd_config",                       "clean"),
    ("/etc/crontab",                               "clean"),
    ("/etc/apt/sources.list",                      "clean"),
    # Logs
    ("/var/log/syslog",                            "clean"),
    ("/var/log/auth.log",                          "clean"),
    ("/var/log/kern.log",                          "clean"),
    ("/var/lib/dpkg/status",                       "clean"),
    # Home
    ("/home/umid/.bashrc",                         "clean"),
    ("/home/umid/.profile",                        "clean"),
    ("/home/umid/.ssh/authorized_keys",            "clean"),
    ("/home/umid/Documents/",                      "clean"),
    ("/home/umid/Downloads/",                      "clean"),
    ("/tmp/",                                      "clean"),
    ("/boot/vmlinuz-6.1.0-kali5-amd64",           "clean"),
    # Processes
    ("Process: systemd [PID 1]",                   "ok"),
    ("Process: NetworkManager [PID 847]",          "ok"),
    ("Process: sshd [PID 1203]",                   "ok"),
    ("Process: xfce4-session [PID 2341]",          "ok"),
    ("Process: python3 [PID 4219]",                "ok"),
    # Memory
    ("Memory: kernel space",                       "ok"),
    ("Memory: user space",                         "ok"),
    ("Memory: shared libraries",                   "ok"),
    # Misc
    ("Startup services: 14 entries",               "ok"),
    ("Browser extensions: 4 entries",              "ok"),
    ("Network connections: 8 active",              "ok"),
    # ── Device separator ──
    ("────────────────────────────────────────────────────────", "sep"),
    ("   CONNECTED DEVICE DETECTED",                "device_title"),
    ("   Device  : Android [/dev/bus/usb/001/004]", "device"),
    ("   Model   : Samsung Galaxy A54",             "device"),
    ("   Protocol: MTP bridge established",         "device"),
    ("────────────────────────────────────────────────────────", "sep"),
    ("   Scanning /sdcard/DCIM/Camera/     [312 files]",  "scan_dev"),
    ("   Scanning /sdcard/Android/data/    [1,847 items]", "scan_dev"),
    ("   Scanning /sdcard/WhatsApp/Media/  [423 files]",  "scan_dev"),
    ("   Scanning /sdcard/Download/        [89 files]",   "scan_dev"),
    ("   Scanning accessible app partitions...",          "scan_dev"),
    ("   Device scan: 2,671 items — no threats found",    "device_ok"),
    ("────────────────────────────────────────────────────────", "sep"),
    # Final
    ("Scheduled tasks: 6 entries",                 "ok"),
    ("Final verification pass...",                 "ok"),
]

TOTAL_FILES = 24_392


# ─────────────────────────────────────────────
#  SHIELD DRAWING
# ─────────────────────────────────────────────
def shield_pts(cx, cy, w, h):
    hw, hh = w / 2, h / 2
    return [
        cx - hw,        cy - hh,
        cx + hw,        cy - hh,
        cx + hw,        cy + hh * 0.05,
        cx + hw * 0.42, cy + hh * 0.72,
        cx,             cy + hh,
        cx - hw * 0.42, cy + hh * 0.72,
        cx - hw,        cy + hh * 0.05,
    ]


def draw_shield(canvas, cx, cy, w, h, fill, outline, stroke_w=2, check_color="white", check_w=3):
    pts = shield_pts(cx, cy, w, h)
    canvas.create_polygon(pts, fill=fill, outline=outline, width=stroke_w, smooth=False)
    # Checkmark
    sc = min(w, h) * 0.22
    x0, y0 = cx - sc * 0.9, cy + sc * 0.05
    xm, ym = cx - sc * 0.2, cy + sc * 0.85
    x1, y1 = cx + sc * 1.0, cy - sc * 0.7
    canvas.create_line(x0, y0, xm, ym, x1, y1,
                       fill=check_color, width=check_w,
                       capstyle="round", joinstyle="round")


# ─────────────────────────────────────────────
#  INSTALLER WINDOW
# ─────────────────────────────────────────────
class InstallerWindow:
    def __init__(self, root):
        self.root = root
        self.completed = False
        self.root.title("AegisGuard Security Suite — Setup")
        self.root.geometry("590x450")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)
        self._center(590, 450)

        self._drag_x = 0
        self._drag_y = 0
        self._build()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # ── UI ──────────────────────────────────
    def _build(self):
        # Title bar
        tbar = tk.Frame(self.root, bg=PANEL, height=36)
        tbar.pack(fill="x")
        tbar.pack_propagate(False)
        tbar.bind("<Button-1>",   self._drag_start)
        tbar.bind("<B1-Motion>",  self._drag_move)

        tk.Label(tbar, text="  AegisGuard Security Suite — Setup",
                 font=("Sans", 10), fg=TEXT2, bg=PANEL).pack(side="left", padx=4, pady=8)
        tk.Button(tbar, text="✕", font=("Sans", 11, "bold"), fg=TEXT2, bg=PANEL,
                  activebackground=RED, activeforeground="white",
                  relief="flat", padx=10, bd=0, cursor="hand2",
                  command=self.root.destroy).pack(side="right")

        # Separator
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # Header
        hdr = tk.Frame(self.root, bg=PANEL, height=90)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        sh_c = tk.Canvas(hdr, width=58, height=68, bg=PANEL, highlightthickness=0)
        sh_c.pack(side="left", padx=22, pady=11)
        draw_shield(sh_c, 29, 34, 44, 52, ACCENT, ACCENT_L, 2, "white", 3)

        info = tk.Frame(hdr, bg=PANEL)
        info.pack(side="left", pady=18)
        tk.Label(info, text="AegisGuard Security Suite",
                 font=("Sans", 15, "bold"), fg=TEXT, bg=PANEL).pack(anchor="w")
        tk.Label(info, text="Version 4.2.1  ·  Setup Wizard",
                 font=("Sans", 10), fg=TEXT2, bg=PANEL).pack(anchor="w", pady=2)

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=32, pady=18)

        tk.Label(body, text="Welcome to AegisGuard Security Suite",
                 font=("Sans", 13, "bold"), fg=TEXT, bg=BG).pack(anchor="w")
        tk.Label(body,
                 text="This wizard will install AegisGuard on your system.\n"
                      "AegisGuard provides real-time protection, advanced threat detection,\n"
                      "and comprehensive scanning for all connected devices.",
                 font=("Sans", 10), fg=TEXT2, bg=BG, justify="left").pack(anchor="w", pady=(6, 16))

        self.status_lbl = tk.Label(body, text="Ready to install.",
                                   font=("Sans", 10), fg=TEXT2, bg=BG, anchor="w")
        self.status_lbl.pack(fill="x")

        # Progress
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("I.Horizontal.TProgressbar",
                        troughcolor=CARD, background=ACCENT,
                        borderwidth=0, lightcolor=ACCENT, darkcolor=ACCENT)
        self.prog_var = tk.DoubleVar(value=0)
        ttk.Progressbar(body, variable=self.prog_var, maximum=100,
                        style="I.Horizontal.TProgressbar",
                        length=526).pack(anchor="w", pady=(8, 4))
        self.pct_lbl = tk.Label(body, text="0%", font=("Sans", 9), fg=TEXT3, bg=BG, anchor="w")
        self.pct_lbl.pack(fill="x")

        # Bottom bar
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")
        bot = tk.Frame(self.root, bg=PANEL, height=56)
        bot.pack(fill="x")
        bot.pack_propagate(False)

        self.launch_btn = tk.Button(bot, text="  Launch AegisGuard  ",
                                    font=("Sans", 10, "bold"),
                                    bg=GREEN_D, fg="white",
                                    activebackground=GREEN, activeforeground="white",
                                    relief="flat", padx=4, pady=6, cursor="hand2",
                                    command=self._launch, state="disabled")
        self.launch_btn.pack(side="right", padx=14, pady=10)

        self.install_btn = tk.Button(bot, text="  Install  ",
                                     font=("Sans", 10, "bold"),
                                     bg=ACCENT, fg="white",
                                     activebackground=ACCENT_L, activeforeground="white",
                                     relief="flat", padx=4, pady=6, cursor="hand2",
                                     command=self._start_install)
        self.install_btn.pack(side="right", padx=4, pady=10)

        tk.Button(bot, text="Cancel",
                  font=("Sans", 10), bg=CARD, fg=TEXT2,
                  activebackground=BORDER, activeforeground=TEXT,
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  command=self.root.destroy).pack(side="right", padx=4, pady=10)

    # ── Drag ────────────────────────────────
    def _drag_start(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()

    def _drag_move(self, e):
        self.root.geometry(f"+{e.x_root - self._drag_x}+{e.y_root - self._drag_y}")

    # ── Install logic ───────────────────────
    def _start_install(self):
        self.install_btn.config(state="disabled")
        threading.Thread(target=self._install_thread, daemon=True).start()

    def _install_thread(self):
        total = sum(s[1] for s in INSTALL_STEPS)
        done = 0
        for msg, inc in INSTALL_STEPS:
            self.root.after(0, lambda m=msg: self.status_lbl.config(text=m))
            for _ in range(inc):
                done += 1
                pct = done / total * 100
                self.root.after(0, lambda p=pct: self.prog_var.set(p))
                self.root.after(0, lambda p=pct: self.pct_lbl.config(text=f"{int(p)}%"))
                time.sleep(0.18 + random.uniform(0, 0.08))
        self.root.after(0, self._install_done)

    def _install_done(self):
        self.prog_var.set(100)
        self.pct_lbl.config(text="100%")
        self.status_lbl.config(
            text="✓  Installation complete!  AegisGuard is ready.", fg=GREEN)
        self.launch_btn.config(state="normal")

    def _launch(self):
        self.completed = True
        self.root.destroy()


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("AegisGuard Security Suite")
        self.root.geometry("940x670")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self.root.overrideredirect(True)
        self._center(940, 670)

        self._drag_x = 0
        self._drag_y = 0
        self.scan_done = False
        self.content = None

        self._build_shell()
        self.show_dashboard()

    def _center(self, w, h):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    # ── Shell (title bar + nav) ──────────────
    def _build_shell(self):
        # Title bar
        tbar = tk.Frame(self.root, bg=PANEL, height=46)
        tbar.pack(fill="x")
        tbar.pack_propagate(False)
        tbar.bind("<Button-1>",   self._drag_start)
        tbar.bind("<B1-Motion>",  self._drag_move)

        sh_c = tk.Canvas(tbar, width=32, height=40, bg=PANEL, highlightthickness=0)
        sh_c.pack(side="left", padx=14, pady=3)
        draw_shield(sh_c, 16, 20, 24, 30, ACCENT, ACCENT_L, 1, "white", 2)

        title_lbl = tk.Label(tbar, text="AegisGuard Security Suite",
                             font=("Sans", 12, "bold"), fg=TEXT, bg=PANEL)
        title_lbl.pack(side="left")
        title_lbl.bind("<Button-1>",  self._drag_start)
        title_lbl.bind("<B1-Motion>", self._drag_move)

        tk.Label(tbar, text=" v4.2.1", font=("Sans", 9), fg=TEXT3, bg=PANEL).pack(
            side="left", anchor="s", pady=10)

        tk.Button(tbar, text="✕", font=("Sans", 12, "bold"), fg=TEXT3, bg=PANEL,
                  activebackground=RED, activeforeground="white",
                  relief="flat", padx=14, pady=0, bd=0, cursor="hand2",
                  command=self.root.destroy).pack(side="right", fill="y")
        tk.Button(tbar, text="─", font=("Sans", 12), fg=TEXT3, bg=PANEL,
                  activebackground=CARD, activeforeground=TEXT,
                  relief="flat", padx=14, pady=0, bd=0, cursor="hand2",
                  command=lambda: self.root.iconify()).pack(side="right", fill="y")

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # Nav
        nav = tk.Frame(self.root, bg=PANEL, height=42)
        nav.pack(fill="x")
        nav.pack_propagate(False)

        self.nav_btns = {}
        for label, cmd in [
            ("Dashboard",  self.show_dashboard),
            ("Scan",       self._start_scan),
            ("Quarantine", None),
            ("Settings",   None),
        ]:
            btn = tk.Button(nav, text=f"  {label}  ",
                            font=("Sans", 10), fg=TEXT2, bg=PANEL,
                            activebackground=CARD, activeforeground=TEXT,
                            relief="flat", pady=10, cursor="hand2",
                            command=(cmd or (lambda: None)))
            btn.pack(side="left")
            self.nav_btns[label] = btn

        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")

        # Content area
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill="both", expand=True)

        # Status bar
        tk.Frame(self.root, bg=BORDER, height=1).pack(fill="x")
        sbar = tk.Frame(self.root, bg=PANEL, height=26)
        sbar.pack(fill="x")
        tk.Label(sbar,
                 text="  ●  Real-time Protection: Active     ●  Virus DB: Up to date     ●  Firewall: On",
                 font=("Sans", 8), fg=GREEN, bg=PANEL).pack(side="left", pady=4)

    def _drag_start(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()

    def _drag_move(self, e):
        self.root.geometry(f"+{e.x_root - self._drag_x}+{e.y_root - self._drag_y}")

    # ── Nav helper ──────────────────────────
    def _set_nav(self, active):
        for name, btn in self.nav_btns.items():
            if name == active:
                btn.config(fg=TEXT, bg=CARD)
            else:
                btn.config(fg=TEXT2, bg=PANEL)

    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    # ── Dashboard ───────────────────────────
    def show_dashboard(self):
        self._clear()
        self._set_nav("Dashboard")

        wrap = tk.Frame(self.content, bg=BG)
        wrap.pack(expand=True)

        # Big shield
        shc = tk.Canvas(wrap, width=130, height=152, bg=BG, highlightthickness=0)
        shc.pack(pady=(28, 6))
        draw_shield(shc, 65, 76, 96, 118, ACCENT, ACCENT_L, 3, "white", 5)

        tk.Label(wrap, text="YOUR DEVICE IS PROTECTED",
                 font=("Sans", 15, "bold"), fg=GREEN, bg=BG).pack()
        tk.Label(wrap, text="All systems operational. No threats detected.",
                 font=("Sans", 10), fg=TEXT2, bg=BG).pack(pady=(4, 18))

        # Cards row
        cards = tk.Frame(wrap, bg=BG)
        cards.pack()
        self._card(cards, "Real-time Protection", "Active",   GREEN,    "●")
        tk.Frame(cards, width=14, bg=BG).pack(side="left")
        self._card(cards, "Firewall",             "Enabled",  GREEN,    "●")
        tk.Frame(cards, width=14, bg=BG).pack(side="left")
        self._card(cards, "Virus Database",       "Updated",  ACCENT_L, "↑")

        scan_btn = tk.Button(wrap, text="   RUN FULL SCAN   ",
                             font=("Sans", 12, "bold"),
                             bg=ACCENT, fg="white",
                             activebackground=ACCENT_L, activeforeground="white",
                             relief="flat", padx=8, pady=12, cursor="hand2",
                             command=self._start_scan)
        scan_btn.pack(pady=24)

        last = "Never scanned" if not self.scan_done else "Last scan: Today  —  System clean"
        tk.Label(wrap, text=last, font=("Sans", 9), fg=TEXT3, bg=BG).pack()

    def _card(self, parent, title, value, color, icon):
        f = tk.Frame(parent, bg=CARD, padx=20, pady=14)
        f.pack(side="left")
        tk.Label(f, text=title, font=("Sans", 9), fg=TEXT2, bg=CARD).pack(anchor="w")
        row = tk.Frame(f, bg=CARD)
        row.pack(anchor="w", pady=(5, 0))
        tk.Label(row, text=icon + "  ", font=("Sans", 13), fg=color, bg=CARD).pack(side="left")
        tk.Label(row, text=value, font=("Sans", 12, "bold"), fg=color, bg=CARD).pack(side="left")

    # ── Scan ────────────────────────────────
    def _start_scan(self):
        self._clear()
        self._set_nav("Scan")

        outer = tk.Frame(self.content, bg=BG)
        outer.pack(fill="both", expand=True, padx=32, pady=22)

        tk.Label(outer, text="Full System Scan — In Progress",
                 font=("Sans", 13, "bold"), fg=TEXT, bg=BG).pack(anchor="w")
        tk.Label(outer, text="Scanning system files, processes, and connected devices...",
                 font=("Sans", 10), fg=TEXT2, bg=BG).pack(anchor="w", pady=(3, 14))

        self.cur_lbl = tk.Label(outer, text="Initializing scan engine...",
                                font=("Monospace", 9), fg=TEXT2, bg=BG, anchor="w")
        self.cur_lbl.pack(fill="x")

        style = ttk.Style()
        style.configure("S.Horizontal.TProgressbar",
                        troughcolor=CARD, background=ACCENT,
                        borderwidth=0, lightcolor=ACCENT, darkcolor=ACCENT)
        self.scan_var = tk.DoubleVar(value=0)
        self.scan_pb  = ttk.Progressbar(outer, variable=self.scan_var, maximum=100,
                                         style="S.Horizontal.TProgressbar")
        self.scan_pb.pack(fill="x", pady=(6, 3))

        self.stat_lbl = tk.Label(outer,
            text="0%   |   Files scanned: 0   |   Threats found: 0",
            font=("Sans", 9), fg=TEXT3, bg=BG, anchor="w")
        self.stat_lbl.pack(fill="x", pady=(0, 10))

        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=(0, 6))
        tk.Label(outer, text="Scan Log", font=("Sans", 10, "bold"), fg=TEXT2,
                 bg=BG, anchor="w").pack(fill="x")

        # Log area
        log_wrap = tk.Frame(outer, bg=CARD)
        log_wrap.pack(fill="both", expand=True, pady=(6, 0))

        self.log = tk.Text(log_wrap, bg=CARD, fg=TEXT2,
                           font=("Monospace", 9), relief="flat",
                           padx=12, pady=8, state="disabled",
                           wrap="none", cursor="arrow",
                           selectbackground=CARD)
        vsb = ttk.Scrollbar(log_wrap, orient="vertical", command=self.log.yview)
        self.log.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.log.pack(side="left", fill="both", expand=True)

        # Text tags
        self.log.tag_configure("clean",        foreground=TEXT2)
        self.log.tag_configure("ok",           foreground=TEXT2)
        self.log.tag_configure("sep",          foreground=TEXT3)
        self.log.tag_configure("device_title", foreground=ACCENT_L,
                               font=("Monospace", 9, "bold"))
        self.log.tag_configure("device",       foreground=ACCENT_L)
        self.log.tag_configure("scan_dev",     foreground=TEXT2)
        self.log.tag_configure("device_ok",    foreground=GREEN,
                               font=("Monospace", 9, "bold"))

        threading.Thread(target=self._scan_thread, daemon=True).start()

    def _log_append(self, line, tag):
        def _do():
            self.log.config(state="normal")
            self.log.insert("end", line + "\n", tag)
            self.log.see("end")
            self.log.config(state="disabled")
        self.root.after(0, _do)

    def _scan_thread(self):
        start    = time.time()
        total    = len(SCAN_ITEMS)
        suffixes = {"clean": "  →  OK", "ok": "  →  OK"}

        for i, (item, tag) in enumerate(SCAN_ITEMS):
            pct   = i / total * 100
            files = int(i / total * TOTAL_FILES)

            self.root.after(0, lambda p=pct: self.scan_var.set(p))
            self.root.after(0, lambda p=pct, f=files: self.stat_lbl.config(
                text=f"{int(p)}%   |   Files scanned: {f:,}   |   Threats found: 0"))
            self.root.after(0, lambda it=item: self.cur_lbl.config(
                text=f"Scanning: {it}"))

            suffix = suffixes.get(tag, "")
            self._log_append(f"  {item}{suffix}", tag)

            # Variable delays — device section slower
            if tag in ("scan_dev", "device", "device_title"):
                delay = random.uniform(0.75, 1.25)
            elif tag == "sep":
                delay = 0.15
            else:
                delay = random.uniform(0.35, 0.70)
            time.sleep(delay)

        # Pad to at least 32 seconds total
        elapsed = time.time() - start
        if elapsed < 32:
            pad = 32 - elapsed
            steps = 12
            for j in range(steps):
                p = 95 + (j / steps) * 5
                self.root.after(0, lambda v=p: self.scan_var.set(v))
                time.sleep(pad / steps)

        self.root.after(0, self.scan_var.set, 100)
        self.root.after(0, self.stat_lbl.config, {
            "text": f"100%   |   Files scanned: {TOTAL_FILES:,}   |   Threats found: 0"})
        time.sleep(0.6)
        self.scan_done = True
        self.root.after(0, self._show_complete)

    # ── Complete ─────────────────────────────
    def _show_complete(self):
        self._clear()
        self._set_nav("Dashboard")

        wrap = tk.Frame(self.content, bg=BG)
        wrap.pack(expand=True)

        # Green shield
        shc = tk.Canvas(wrap, width=140, height=164, bg=BG, highlightthickness=0)
        shc.pack(pady=(24, 4))
        draw_shield(shc, 70, 82, 104, 128, GREEN_D, GREEN, 3, GREEN, 6)
        shc.create_line(
            70 - 22, 82 + 2,
            70 - 5,  82 + 24,
            70 + 25, 82 - 22,
            fill="white", width=6, capstyle="round", joinstyle="round")

        tk.Label(wrap, text="SCAN COMPLETE",
                 font=("Sans", 17, "bold"), fg=GREEN, bg=BG).pack(pady=(4, 0))
        tk.Label(wrap, text="No threats detected. Your system is clean.",
                 font=("Sans", 11), fg=TEXT, bg=BG).pack(pady=(5, 2))
        tk.Label(wrap, text="Connected device (Samsung Galaxy A54) — no threats found",
                 font=("Sans", 10), fg=GREEN, bg=BG).pack(pady=(0, 20))

        # Stats table
        tbl = tk.Frame(wrap, bg=CARD, padx=36, pady=18)
        tbl.pack()
        for label, val, highlight in [
            ("Files scanned",     f"{TOTAL_FILES:,}", False),
            ("Threats found",     "0",                True),
            ("Scan duration",     "00:38",            False),
            ("Connected devices", "1  —  clean",      True),
        ]:
            row = tk.Frame(tbl, bg=CARD)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label + ":",
                     font=("Sans", 10), fg=TEXT2, bg=CARD,
                     width=22, anchor="w").pack(side="left")
            color = GREEN if highlight else TEXT
            tk.Label(row, text=val,
                     font=("Sans", 10, "bold"), fg=color, bg=CARD).pack(side="left")

        # Buttons
        btns = tk.Frame(wrap, bg=BG)
        btns.pack(pady=22)

        tk.Button(btns, text="  Scan Again  ",
                  font=("Sans", 10), bg=CARD, fg=TEXT,
                  activebackground=BORDER, activeforeground=TEXT,
                  relief="flat", padx=6, pady=8, cursor="hand2",
                  command=self._start_scan).pack(side="left", padx=8)

        tk.Button(btns, text="  Done  ",
                  font=("Sans", 10, "bold"), bg=ACCENT, fg="white",
                  activebackground=ACCENT_L, activeforeground="white",
                  relief="flat", padx=18, pady=8, cursor="hand2",
                  command=self.show_dashboard).pack(side="left", padx=8)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    # Phase 1 — Installer
    root1 = tk.Tk()
    installer = InstallerWindow(root1)
    root1.mainloop()

    if not installer.completed:
        return

    # Phase 2 — Main app
    root2 = tk.Tk()
    MainWindow(root2)
    root2.mainloop()


if __name__ == "__main__":
    main()
