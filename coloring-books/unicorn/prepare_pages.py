"""Turn raw generated drawings into clean print-ready line art.

Each raw drawing (1792 x 2400 px, 3:4) is enlarged 2x, softened slightly so
edges stay smooth, then turned into pure black and white (no gray).
The result is 3584 x 4800 px, about 490 dpi on an A4 page.

Usage: python3 prepare_pages.py RAW_DIR
RAW_DIR holds p01.png ... p40.png. Output goes to pages/01.png ... 40.png.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter

HERE = Path(__file__).parent
SCALE = 2
THRESHOLD = 150  # gray values above this become white
COLOR_SPREAD = 30  # a pixel whose channels differ more than this counts as colored


def clean(src: Path, dst: Path) -> None:
    rgb = Image.open(src).convert("RGB")
    # Some drawings come back with pink cheeks: turn any colored pixel white.
    r, g, b = rgb.split()
    spread = ImageChops.subtract(ImageChops.lighter(ImageChops.lighter(r, g), b),
                                 ImageChops.darker(ImageChops.darker(r, g), b))
    colored = spread.point(lambda v: 255 if v > COLOR_SPREAD else 0)
    gray = rgb.convert("L")
    gray.paste(255, mask=colored)
    big = gray.resize((gray.width * SCALE, gray.height * SCALE), Image.LANCZOS)
    big = big.filter(ImageFilter.GaussianBlur(1.0))
    bw = big.point(lambda v: 255 if v > THRESHOLD else 0).convert("1")
    bw.save(dst, optimize=True)


def main() -> None:
    raw = Path(sys.argv[1])
    out = HERE / "pages"
    out.mkdir(exist_ok=True)
    for n in range(1, 41):
        src = raw / f"p{n:02d}.png"
        clean(src, out / f"{n:02d}.png")
        print("ok", src.name)


if __name__ == "__main__":
    main()
