"""Draw the home-screen icon for the Nyx phone page.

    python tools/make_icons.py

Writes icon-192.png, icon-512.png and apple-touch-icon.png next to index.html.
An icon is the difference between "a website I saved" and "an app on my phone",
and it is the only part of that the PWA manifest cannot invent for you.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BG_OUTER = (8, 8, 10)
BG_INNER = (34, 24, 66)
ACCENT = (124, 92, 255)
ACCENT_SOFT = (168, 148, 255)
STAR = (236, 236, 241)


def crescent(size: int) -> Image.Image:
    """A night mark: crescent moon over a soft glow, on the page's own palette."""
    scale = 4  # draw big, then downsample — free antialiasing
    s = size * scale
    img = Image.new("RGBA", (s, s), BG_OUTER + (255,))

    # radial-ish background: a big soft disc of the inner colour
    grad = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    gd.ellipse([-s * 0.25, -s * 0.55, s * 1.25, s * 0.95], fill=BG_INNER + (255,))
    grad = grad.filter(ImageFilter.GaussianBlur(s * 0.10))
    img.alpha_composite(grad)

    # glow behind the moon
    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    cx, cy, r = s * 0.52, s * 0.50, s * 0.26
    gdraw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT + (150,))
    glow = glow.filter(ImageFilter.GaussianBlur(s * 0.06))
    img.alpha_composite(glow)

    # the moon: a full disc, minus an offset disc cut back out of it
    moon = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    md = ImageDraw.Draw(moon)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT_SOFT + (255,))
    cut_r = r * 0.94
    cut_cx, cut_cy = cx + r * 0.42, cy - r * 0.20
    md.ellipse([cut_cx - cut_r, cut_cy - cut_r, cut_cx + cut_r, cut_cy + cut_r], fill=(0, 0, 0, 0))
    img.alpha_composite(moon)

    # one small star, high and to the left, so the mark reads as night
    star = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    sd = ImageDraw.Draw(star)
    sx, sy, sr = s * 0.30, s * 0.26, s * 0.022
    sd.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=STAR + (235,))
    star = star.filter(ImageFilter.GaussianBlur(s * 0.004))
    img.alpha_composite(star)

    return img.resize((size, size), Image.LANCZOS)


def main() -> int:
    sizes = {"icon-192.png": 192, "icon-512.png": 512, "apple-touch-icon.png": 180}
    for name, size in sizes.items():
        path = ROOT / name
        # flatten to RGB: iOS puts a white plate behind transparent icons
        crescent(size).convert("RGB").save(path, "PNG", optimize=True)
        print(f"wrote {path.name}  {size}x{size}  {path.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
