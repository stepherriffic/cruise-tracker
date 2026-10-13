#!/usr/bin/env python3
"""Create share-card + apple icon for the Norwegian Bliss voyage.

Photo: Andrew Bone, 'Norwegian Bliss (50505494088).jpg', CC BY 2.0.
https://commons.wikimedia.org/wiki/File:Norwegian_Bliss_(50505494088).jpg
Modified: cropped, graded, and overlaid with text for this share-card.
"""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets"
DEST.mkdir(exist_ok=True)
PHOTO = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Norwegian_Bliss_%2850505494088%29.jpg/1280px-Norwegian_Bliss_%2850505494088%29.jpg"
W, H = 1200, 630
NAVY = (8, 23, 41)

def font(size, bold=True):
    path = "/usr/share/fonts/truetype/dejavu/" + ("DejaVuSansCondensed-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)

def load_ship():
    req = Request(PHOTO, headers={"User-Agent": "NorwegianBlissCruiseTracker/1.0 (https://stepherriffic.github.io/cruise-tracker/)"})
    try:
        with urlopen(req, timeout=25) as response:
            return Image.open(BytesIO(response.read())).convert("RGB")
    except Exception as ex:
        raise RuntimeError("Licensed ship photograph could not be downloaded. Refusing to publish a mislabeled substitute.") from ex

def create_share():
    ship = load_ship()
    base = Image.new("RGB", (W, H), NAVY)
    crop = ImageOps.fit(ship, (795, 560), method=Image.Resampling.LANCZOS, centering=(0.54, 0.49))
    crop = ImageEnhance.Color(crop).enhance(1.12)
    # The photo fills the right side, fading gently into the dark title panel.
    base.paste(crop, (415, 35))
    px = base.load()
    for x in range(370, 820):
        opacity = max(0, min(1, (820 - x) / 450))
        for y in range(H):
            r, g, b = px[x, y]
            px[x, y] = tuple(round(c * (1 - opacity) + n * opacity) for c, n in zip((r, g, b), NAVY))
    draw = ImageDraw.Draw(base)
    draw.rectangle((0, 0, W, 9), fill=(17, 188, 221))
    draw.line((64, 143, 222, 143), fill=(34, 211, 238), width=5)
    draw.text((64, 95), "THE 2026 PANAMA CANAL VOYAGE", fill=(103, 232, 249), font=font(19))
    draw.text((56, 182), "NORWEGIAN", fill=(255, 255, 255), font=font(65))
    draw.text((48, 258), "BLISS", fill=(255, 255, 255), font=font(137))
    draw.text((64, 467), "LOS ANGELES  →  MIAMI", fill=(224, 242, 254), font=font(26))
    draw.text((64, 510), "OCTOBER 13–29, 2026  •  16 NIGHTS", fill=(103, 232, 249), font=font(17))
    draw.rectangle((0, 604, W, H), fill=(5, 16, 29))
    draw.text((735, 608), "Ship photo: Andrew Bone · CC BY 2.0 · cropped & color graded", fill=(192, 209, 223), font=font(11, False))
    base.save(DEST / "norwegian-bliss-share.jpg", quality=90, subsampling=0, optimize=True, progressive=True)

def create_touch_icon():
    im = Image.new("RGB", (180, 180), (9, 24, 43))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, 179, 179), radius=36, fill=(9, 24, 43))
    d.polygon([(0, 119), (55, 111), (108, 120), (180, 111), (180, 180), (0, 180)], fill=(7, 116, 145))
    d.polygon([(23, 99), (162, 99), (141, 134), (53, 134)], fill=(249, 250, 251))
    d.rectangle((46, 58, 139, 99), fill=(249, 250, 251))
    d.rectangle((62, 40, 128, 60), fill=(226, 232, 240))
    d.rectangle((107, 28, 127, 42), fill=(20, 184, 220))
    for x in (56, 78, 100, 122):
        d.rectangle((x, 69, x+12, 80), fill=(3, 105, 161))
    d.line((23, 101, 162, 101), fill=(22, 185, 221), width=8)
    d.arc((2, 115, 92, 150), 5, 170, fill=(103, 232, 249), width=5)
    d.arc((88, 116, 178, 151), 5, 170, fill=(103, 232, 249), width=5)
    im.save(DEST / "apple-touch-icon.png", optimize=True)

if __name__ == "__main__":
    create_share()
    create_touch_icon()
    print("Wrote ship photo share image (1200×630) and touch icon (180×180).")
