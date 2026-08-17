"""
Generate a stylized preview GIF for the README (not a real screen recording).
It uses Curb's visual language: dark map, signage-style markers, time scrubber.
Replace docs/demo.gif with an actual screen capture whenever you like.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 900, 480
BG = (14, 17, 22)
PANEL = (22, 27, 34)
LINE = (42, 49, 59)
INK = (230, 234, 240)
MUT = (139, 150, 165)
GREEN = (53, 196, 106); BLUE = (79, 155, 255); AMBER = (242, 178, 58)
RED = (240, 80, 60); ORANGE = (255, 122, 26)

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz, bold=True): return ImageFont.truetype(FB if bold else F, sz)

DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
DAY2 = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

# signs: (x, y, kind, text, cleaning_day_indices)
SIGNS = [
    (150, 120, "clean", "Mo Th", [0, 3]),
    (360, 90,  "clean", "Tu Fr", [1, 4]),
    (600, 130, "warn",  "\u2298", []),
    (760, 100, "clean", "We",    [2]),
    (230, 250, "clean", "Tu Th", [1, 3]),
    (520, 260, "warn",  "\u2298", []),
    (690, 250, "clean", "Mo We Fr", [0, 2, 4]),
    (420, 330, "clean", "Th",    [3]),
]


def rounded(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def draw_sign(d, x, y, kind, text, active):
    fnt = font(15)
    tw = d.textlength(text, font=fnt)
    pad = 7
    w = int(tw) + pad * 2
    h = 24
    if kind == "warn":
        border, col, bg = RED, RED, (255, 255, 255)
    elif active:
        border, col, bg = ORANGE, (150, 60, 0), (255, 236, 214)
    else:
        border, col, bg = BLUE, (18, 80, 127), (255, 255, 255)
    box = (x - w // 2, y - h, x + w // 2, y)
    rounded(d, box, 6, fill=bg, outline=border, width=3)
    d.polygon([(x - 5, y), (x + 5, y), (x, y + 6)], fill=border)  # pointer
    d.text((x - tw // 2, y - h + 5), text, font=fnt, fill=col)


def frame(i, n):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # faint street grid
    for gx in range(60, W, 90):
        d.line([(gx, 60), (gx, H - 90)], fill=(26, 31, 38), width=6)
    for gy in range(80, H - 90, 70):
        d.line([(40, gy), (W - 40, gy)], fill=(26, 31, 38), width=6)

    active_day = i % 7
    for (x, y, kind, text, days) in SIGNS:
        draw_sign(d, x, y, kind, text, active=(active_day in days))

    # brand panel
    rounded(d, (24, 24, 360, 96), 12, fill=PANEL, outline=LINE, width=1)
    d.text((40, 34), "CURB", font=font(30), fill=INK)
    for k in range(4):
        d.rectangle((150 + k * 12, 40, 158 + k * 12, 58), fill=ORANGE)
    d.text((40, 70), "Where you can park in NYC", font=font(13, False), fill=MUT)

    # bottom time scrubber
    cy = H - 54
    rounded(d, (24, H - 84, W - 24, H - 14), 12, fill=PANEL, outline=LINE, width=1)
    cellw = (W - 80) / 7
    for k, dname in enumerate(DAYS):
        bx = 40 + k * cellw
        box = (bx, cy - 16, bx + cellw - 8, cy + 14)
        if k == active_day:
            rounded(d, box, 7, fill=(60, 32, 10), outline=ORANGE, width=2)
            d.text((bx + 12, cy - 9), dname, font=font(13), fill=(255, 178, 122))
        else:
            rounded(d, box, 7, fill=(28, 37, 48), outline=LINE, width=1)
            d.text((bx + 12, cy - 9), dname, font=font(13), fill=MUT)
    # slider line + moving knob
    ly = H - 26
    d.line([(44, ly), (W - 44, ly)], fill=(36, 48, 65), width=4)
    kx = 44 + (W - 88) * (i / (n - 1))
    d.ellipse((kx - 8, ly - 8, kx + 8, ly + 8), fill=ORANGE, outline=BG, width=3)

    # readout
    rounded(d, (390, 34, 560, 74), 8, fill=(10, 13, 18), outline=LINE, width=1)
    d.text((404, 44), f"{DAYS[active_day]}  9:30 AM", font=font(18), fill=(255, 154, 77))
    return img


def main():
    n = 28
    frames = [frame(i, n) for i in range(n)]
    frames[0].save("docs/demo.gif", save_all=True, append_images=frames[1:],
                   duration=140, loop=0, optimize=True)
    print("wrote docs/demo.gif")


if __name__ == "__main__":
    main()
