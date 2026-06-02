#!/usr/bin/env python3
"""Generates ISHROQAI-45xFA icon.png"""
from PIL import Image, ImageDraw, ImageFont
import math, os

SIZE = 256
OUT  = os.path.join(os.path.dirname(__file__), 'icon.png')

img  = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Background circle
draw.ellipse([4, 4, SIZE-4, SIZE-4], fill=(10, 15, 30, 255))

# Outer glow ring
for i in range(6, 0, -1):
    alpha = int(40 * (i / 6))
    draw.ellipse([4-i*2, 4-i*2, SIZE-4+i*2, SIZE-4+i*2],
                  outline=(0, 220, 255, alpha), width=2)

# Hexagon
cx, cy = SIZE // 2, SIZE // 2
r = 90
pts = [(int(cx + r * math.cos(math.radians(60*i - 30))),
        int(cy + r * math.sin(math.radians(60*i - 30)))) for i in range(6)]
draw.polygon(pts, outline=(0, 220, 255, 200), fill=(0, 20, 40, 180))

# Inner hexagon
r2 = 70
pts2 = [(int(cx + r2 * math.cos(math.radians(60*i - 30))),
         int(cy + r2 * math.sin(math.radians(60*i - 30)))) for i in range(6)]
draw.polygon(pts2, outline=(0, 200, 255, 100), fill=None)

# Circuit lines
for angle in [0, 60, 120, 180, 240, 300]:
    rad = math.radians(angle)
    x1  = int(cx + 70 * math.cos(rad))
    y1  = int(cy + 70 * math.sin(rad))
    x2  = int(cx + 90 * math.cos(rad))
    y2  = int(cy + 90 * math.sin(rad))
    draw.line([x1, y1, x2, y2], fill=(0, 255, 200, 180), width=2)
    draw.ellipse([x2-4, y2-4, x2+4, y2+4], fill=(0, 255, 200, 200))

# "IQ" text in center
try:
    fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 56)
except Exception:
    fnt = ImageFont.load_default()

bbox = draw.textbbox((0, 0), 'IQ', font=fnt)
tw   = bbox[2] - bbox[0]
th   = bbox[3] - bbox[1]
draw.text((cx - tw//2, cy - th//2 - 4), 'IQ',
          font=fnt, fill=(0, 230, 255, 255))

# Small subtitle
try:
    fnt2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
except Exception:
    fnt2 = ImageFont.load_default()
draw.text((cx - 22, cy + 36), '45xFA', font=fnt2, fill=(0, 180, 200, 160))

img.save(OUT)
print(f'Icon saved: {OUT}')
