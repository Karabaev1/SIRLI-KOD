import tkinter as tk

BG          = "#4B5463"
BG_LEFT     = "#3a4150"
BORDER      = "#5c6475"
WHITE       = "#ffffff"
WHITE_DIM   = "#cccccc"

TOP_INFO = [
    ("Ism",   "Umid Kenjayev"),
    ("Yoshi", "14"),
]

EXTRA_INFO = [
    "Matematika, fizika va boshqa aniq fanlarni yaxshi o'zlashtiradi.",
    "Tarbiyasi va xulqida nuqsonlar kuzatilmagan.",
    "IT sohasiga juda ham qattiq qiziqadi.",
    "Provayder kompaniyada internet texniki bo'lib ishlaydi.",
    "Uy bekasi.",
]

root = tk.Tk()
root.title("Candidate #7")
root.configure(bg=BG)
root.geometry("1280x720")
root.minsize(800, 500)

root.bind("<Escape>", lambda e: root.destroy())
root.bind("<F11>", lambda e: root.attributes(
    "-fullscreen", not root.attributes("-fullscreen")))

canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def draw(event=None):
    canvas.delete("all")
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    if W < 2 or H < 2:
        return

    left_w = int(W * 0.40)

    # ── Chap panel ──
    canvas.create_rectangle(0, 0, left_w, H, fill=BG_LEFT, outline="")
    canvas.create_line(left_w, 0, left_w, H, fill=BORDER, width=2)

    ph_w = int(left_w * 0.65)
    ph_h = int(H * 0.50)
    ph_x1 = (left_w - ph_w) // 2
    ph_y1 = (H - ph_h) // 2
    canvas.create_rectangle(ph_x1, ph_y1, ph_x1 + ph_w, ph_y1 + ph_h,
                            outline=BORDER, width=2, dash=(10, 6))
    canvas.create_text((ph_x1 * 2 + ph_w) // 2, (ph_y1 * 2 + ph_h) // 2,
                       text="RASM", fill=BORDER,
                       font=("Arial", int(H * 0.018), "bold"))

    # ── O'ng panel ──
    px        = left_w + int(W * 0.05)
    cy        = int(H * 0.12)
    right_lim = int(W * 0.50)

    fs_badge = max(13, int(H * 0.024))
    fs_info  = max(12, int(H * 0.022))
    label_w  = int(W * 0.09)

    # CANDIDATE #7 badge — kattaroq
    badge_text = "  CANDIDATE  #7  "
    tmp = canvas.create_text(0, 0, text=badge_text,
                             font=("Arial", fs_badge, "bold"), anchor="nw")
    bb = canvas.bbox(tmp)
    canvas.delete(tmp)
    bw = bb[2] - bb[0]
    bh = bb[3] - bb[1]
    pad = int(H * 0.013)

    rx1, ry1 = px - pad, cy - pad
    rx2, ry2 = px + bw + pad, cy + bh + pad
    canvas.create_rectangle(rx1, ry1, rx2, ry2,
                            outline=WHITE, width=2, fill="")
    canvas.create_text(px, cy, text=badge_text,
                       fill=WHITE, font=("Arial", fs_badge, "bold"),
                       anchor="nw")
    cy = ry2 + int(H * 0.045)

    # Ajratuvchi chiziq
    canvas.create_line(px, cy, px + 80, cy, fill=WHITE_DIM, width=2)
    cy += int(H * 0.035)

    # Ism va Yoshi
    for label, value in TOP_INFO:
        canvas.create_text(px, cy,
                           text=label + ":",
                           fill=WHITE,
                           font=("Arial", fs_info, "bold"),
                           anchor="nw",
                           width=label_w)
        canvas.create_text(px + label_w + 10, cy,
                           text=value,
                           fill=WHITE_DIM,
                           font=("Arial", fs_info),
                           anchor="nw",
                           width=right_lim - label_w - 10)
        cy += int(fs_info * 2.2)

    cy += int(H * 0.01)

    # Boshqa ma'lumotlar
    canvas.create_text(px, cy,
                       text="Boshqa ma'lumotlar:",
                       fill=WHITE,
                       font=("Arial", fs_info, "bold"),
                       anchor="nw")
    cy += int(fs_info * 1.7)

    for item in EXTRA_INFO:
        canvas.create_text(px + 14, cy,
                           text="— " + item,
                           fill=WHITE_DIM,
                           font=("Arial", fs_info),
                           anchor="nw",
                           width=right_lim - 14)
        cy += int(fs_info * 2.0)

canvas.bind("<Configure>", draw)
root.mainloop()
