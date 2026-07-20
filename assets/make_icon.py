"""Generate the One-Liner app icon.

Draws the 1024px master PNG with Pillow, then emits every size macOS
wants and packs them into One-Liner.icns via iconutil.

Usage:  python3 assets/make_icon.py
"""

import os
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SS = 4  # supersample factor for crisp edges
CANVAS = 1024

# macOS icon grid: the squircle occupies 824x824 centered on a 1024 canvas
SHAPE = 824
RADIUS = 186

BG_TOP = (38, 50, 66)
BG_BOTTOM = (18, 24, 33)
GRAY = (138, 151, 165)
GREEN = (78, 207, 168)  # matches the app's #4ECFA8 accent
CHEVRON = (94, 168, 220)


def rounded_bar(draw, x0, y0, x1, y1, color):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=(y1 - y0) / 2, fill=color)


def build_master() -> Image.Image:
    size = CANVAS * SS
    off = (CANVAS - SHAPE) // 2 * SS
    shape = SHAPE * SS

    # Vertical gradient, masked to the squircle
    grad = Image.new("RGB", (1, shape))
    for y in range(shape):
        t = y / (shape - 1)
        grad.putpixel((0, y), tuple(
            round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)
        ))
    grad = grad.resize((shape, shape))

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [off, off, off + shape, off + shape], radius=RADIUS * SS, fill=255
    )

    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img.paste(grad, (off, off), mask.crop((off, off, off + shape, off + shape)))

    draw = ImageDraw.Draw(img)

    # Glyph: three ragged gray lines funnel into one clean green line
    cx = size / 2
    bar_h = 58 * SS
    left = off + 150 * SS
    right = off + shape - 150 * SS

    rows = [  # (y-center offset from shape top, x0, x1)
        (250, left, left + 380 * SS),
        (360, left, left + 500 * SS),
        (470, left, left + 300 * SS),
    ]
    for ycen, x0, x1 in rows:
        y = off + ycen * SS
        rounded_bar(draw, x0, y - bar_h / 2, x1, y + bar_h / 2, GRAY)

    # Downward chevron between the stack and the result line
    ch_y = off + 583 * SS
    ch_w, ch_h, ch_t = 96 * SS, 52 * SS, 30 * SS
    draw.line(
        [(cx - ch_w / 2, ch_y), (cx, ch_y + ch_h), (cx + ch_w / 2, ch_y)],
        fill=CHEVRON, width=ch_t, joint="curve",
    )
    for px in (cx - ch_w / 2, cx, cx + ch_w / 2):
        py = ch_y + (ch_h if px == cx else 0)
        draw.ellipse(
            [px - ch_t / 2, py - ch_t / 2, px + ch_t / 2, py + ch_t / 2],
            fill=CHEVRON,
        )

    # The one clean line
    y = off + 700 * SS
    glow_h = int(bar_h * 2.2)
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rounded_bar(
        ImageDraw.Draw(glow), left, y - glow_h / 2, right, y + glow_h / 2,
        GREEN + (90,),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(28 * SS))
    glow.putalpha(Image.composite(glow.getchannel("A"), Image.new("L", (size, size), 0), mask))
    img.alpha_composite(glow)
    rounded_bar(draw, left, y - bar_h / 2, right, y + bar_h / 2, GREEN)

    return img.resize((CANVAS, CANVAS), Image.LANCZOS)


def main():
    master = build_master()
    master_path = os.path.join(HERE, "icon-1024.png")
    master.save(master_path)

    iconset = os.path.join(HERE, "One-Liner.iconset")
    shutil.rmtree(iconset, ignore_errors=True)
    os.makedirs(iconset)
    for pt in (16, 32, 128, 256, 512):
        for scale in (1, 2):
            px = pt * scale
            suffix = "" if scale == 1 else "@2x"
            master.resize((px, px), Image.LANCZOS).save(
                os.path.join(iconset, f"icon_{pt}x{pt}{suffix}.png")
            )

    icns = os.path.join(HERE, "One-Liner.icns")
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", icns], check=True)
    shutil.rmtree(iconset)
    print(f"wrote {master_path}\nwrote {icns}")


if __name__ == "__main__":
    main()
