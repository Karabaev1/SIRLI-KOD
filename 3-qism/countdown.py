#!/usr/bin/env python3
"""
Countdown Timer — serial prop
═══════════════════════════════════════════
 SOZLASH (Configuration):
   TIMER_SECONDS — nechchi sekunddan boshlash
   WINDOW_W / WINDOW_H — oyna o'lchami
═══════════════════════════════════════════
"""

import tkinter as tk
from tkinter import ttk

# ╔══════════════════════════════════════════╗
# ║           SOZLAMALAR                     ║
# ╠══════════════════════════════════════════╣
TIMER_SECONDS = 46      # ← boshlang'ich vaqt (sekund)
WINDOW_W      = 760     # ← oyna kengligi (px)
WINDOW_H      = 370     # ← oyna balandligi (px)
# ╚══════════════════════════════════════════╝

# ── Ranglar ────────────────────────────────────
C_BG       = "#080810"
C_TBAR     = "#0e0e1a"
C_BORDER   = "#1a1a2e"
C_CARD     = "#0d0d18"
C_NORMAL   = "#dce3ef"
C_ORANGE   = "#e67e22"
C_RED      = "#e74c3c"
C_DIM      = "#2a2a3e"
C_DIM2     = "#444466"
C_FLASH_A  = "#7a0000"   # blink: dark red
C_FLASH_B  = "#cc0000"   # blink: bright red


class CountdownApp:
    def __init__(self, root: tk.Tk):
        self.root      = root
        self.total     = TIMER_SECONDS
        self.remaining = TIMER_SECONDS
        self.blinking  = False
        self._blink_id = None
        self._drag_x   = 0
        self._drag_y   = 0

        self._setup_window()
        self._build_ui()
        self._tick()

    # ── Window setup ───────────────────────────
    def _setup_window(self):
        self.root.overrideredirect(True)
        self.root.configure(bg=C_BG)
        self.root.resizable(False, False)
        # Center on screen
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x  = (sw - WINDOW_W) // 2
        y  = (sh - WINDOW_H) // 2
        self.root.geometry(f"{WINDOW_W}x{WINDOW_H}+{x}+{y}")
        self.root.attributes('-topmost', True)

    # ── UI ─────────────────────────────────────
    def _build_ui(self):
        # Title bar
        self._tbar = tk.Frame(self.root, bg=C_TBAR, height=34)
        self._tbar.pack(fill='x')
        self._tbar.pack_propagate(False)
        self._tbar.bind("<Button-1>",  self._drag_start)
        self._tbar.bind("<B1-Motion>", self._drag_move)

        self._tbar_lbl = tk.Label(
            self._tbar, text="  COUNTDOWN TIMER",
            font=("Courier", 10), fg="#333355", bg=C_TBAR
        )
        self._tbar_lbl.pack(side='left', padx=6, pady=8)
        self._tbar_lbl.bind("<Button-1>",  self._drag_start)
        self._tbar_lbl.bind("<B1-Motion>", self._drag_move)

        tk.Button(
            self._tbar, text="✕",
            font=("Arial", 11, "bold"), fg="#444466", bg=C_TBAR,
            activebackground=C_RED, activeforeground="white",
            relief='flat', padx=12, bd=0, cursor='hand2',
            command=self.root.destroy
        ).pack(side='right', fill='y')

        tk.Frame(self.root, bg=C_BORDER, height=1).pack(fill='x')

        # ── Content ──────────────────────────────
        self._body = tk.Frame(self.root, bg=C_BG)
        self._body.pack(fill='both', expand=True)

        # Top spacer
        tk.Frame(self._body, bg=C_BG, height=14).pack()

        # Card frame around timer
        self._card = tk.Frame(
            self._body, bg=C_CARD,
            highlightbackground=C_BORDER,
            highlightthickness=1
        )
        self._card.pack(padx=38, fill='x')

        # Timer label
        self._timer_lbl = tk.Label(
            self._card,
            text=self._fmt(self.remaining),
            font=("Courier", 88, "bold"),
            fg=C_NORMAL, bg=C_CARD,
            pady=4
        )
        self._timer_lbl.pack()

        # Thin divider inside card
        tk.Frame(self._card, bg=C_BORDER, height=1).pack(fill='x')

        # Sub info row inside card
        sub_row = tk.Frame(self._card, bg=C_CARD)
        sub_row.pack(fill='x', padx=14, pady=6)

        self._status_lbl = tk.Label(
            sub_row, text="● ARMED",
            font=("Courier", 11), fg=C_DIM2, bg=C_CARD, anchor='w'
        )
        self._status_lbl.pack(side='left')

        self._remain_lbl = tk.Label(
            sub_row,
            text=f"{self.remaining}s remaining",
            font=("Courier", 11), fg=C_DIM2, bg=C_CARD, anchor='e'
        )
        self._remain_lbl.pack(side='right')

        # Progress bar
        sty = ttk.Style()
        sty.theme_use('clam')
        sty.configure(
            "CD.Horizontal.TProgressbar",
            troughcolor=C_DIM, background=C_RED,
            borderwidth=0, lightcolor=C_RED, darkcolor=C_RED,
            relief='flat'
        )
        self._prog_var = tk.DoubleVar(value=100.0)
        ttk.Progressbar(
            self._body,
            variable=self._prog_var,
            maximum=100,
            style="CD.Horizontal.TProgressbar"
        ).pack(fill='x', padx=38, pady=(10, 0))

        # Bottom spacer
        tk.Frame(self._body, bg=C_BG, height=12).pack()

        # Keep track of widgets that change color on blink
        self._blinkable_bg = [
            self._body, self._card, self._timer_lbl,
            self._status_lbl, self._remain_lbl, sub_row
        ]
        self._blinkable_sub = sub_row   # store sub_row ref

    # ── Drag ───────────────────────────────────
    def _drag_start(self, e):
        self._drag_x = e.x_root - self.root.winfo_x()
        self._drag_y = e.y_root - self.root.winfo_y()

    def _drag_move(self, e):
        x = e.x_root - self._drag_x
        y = e.y_root - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    # ── Helpers ────────────────────────────────
    @staticmethod
    def _fmt(s: int) -> str:
        h   = s // 3600
        m   = (s % 3600) // 60
        sec = s % 60
        return f"{h:02d}:{m:02d}:{sec:02d}"

    def _set_timer_color(self, fg):
        self._timer_lbl.config(fg=fg)

    # ── Countdown tick ─────────────────────────
    def _tick(self):
        if self.blinking:
            return

        if self.remaining > 0:
            self.remaining -= 1
            self._timer_lbl.config(text=self._fmt(self.remaining))
            self._remain_lbl.config(text=f"{self.remaining}s remaining")

            pct = self.remaining / self.total * 100
            self._prog_var.set(pct)

            # Color stages
            if self.remaining <= 5:
                self._set_timer_color(C_RED)
                self._status_lbl.config(text="● CRITICAL", fg=C_RED)
                self._remain_lbl.config(fg=C_RED)
            elif self.remaining <= 15:
                self._set_timer_color(C_ORANGE)
                self._status_lbl.config(text="● WARNING", fg=C_ORANGE)
                self._remain_lbl.config(fg=C_ORANGE)

            self.root.after(1000, self._tick)
        else:
            self._on_zero()

    # ── Zero reached ───────────────────────────
    def _on_zero(self):
        self.blinking = True
        self._timer_lbl.config(text="00:00:00")
        self._prog_var.set(0)
        self._status_lbl.config(text="● TRIGGERED", fg=C_RED)
        self._remain_lbl.config(text="0s remaining", fg=C_RED)
        self._blink(True)

    def _blink(self, phase: bool):
        if phase:
            # Bright red flash
            body_bg  = C_FLASH_B
            card_bg  = C_FLASH_B
            timer_fg = "#ffffff"
        else:
            # Dark red
            body_bg  = C_FLASH_A
            card_bg  = C_FLASH_A
            timer_fg = C_RED

        self.root.configure(bg=body_bg)
        for w in self._blinkable_bg:
            w.configure(bg=card_bg)
        self._timer_lbl.configure(fg=timer_fg, bg=card_bg)
        self._card.configure(
            highlightbackground=C_FLASH_B if phase else C_FLASH_A
        )

        self._blink_id = self.root.after(380, lambda: self._blink(not phase))


# ── Entry point ────────────────────────────────
def main():
    root = tk.Tk()
    CountdownApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
