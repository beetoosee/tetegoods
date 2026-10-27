"""Build the print-ready PDF of "Colorindo com a Estela".

Inputs (next to this script):
  cover.jpg          color cover art, 3:4
  pages/01..40.png   black and white drawings, 3:4 (made by prepare_pages.py)
  pages/owner.png    small drawing for the "this book belongs to" page
  fonts/             Fredoka (numbers) and Pacifico (titles), from Google Fonts

Outputs (in output/):
  Colorindo-com-a-Estela.pdf             A4, cover + owner page + 40 drawings
  Colorindo-com-a-Estela-capa-sangria.pdf cover alone with 3 mm bleed, for print shops
"""
from pathlib import Path

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

HERE = Path(__file__).parent
OUT = HERE / "output"
TITLE = "Colorindo com a Estela"
PAGE_W, PAGE_H = A4
BLEED = 3 * mm

# Drawing area: 3:4 box centered on the page, inside a rounded frame.
DRAW_W = 182 * mm
DRAW_H = DRAW_W * 4 / 3
FRAME_PAD = 4 * mm
FRAME_TOP = 14 * mm  # gap between page top and frame
INK = (0.17, 0.12, 0.12)  # soft near-black for frame and text

pdfmetrics.registerFont(TTFont("Fredoka", str(HERE / "fonts" / "Fredoka.ttf")))
pdfmetrics.registerFont(TTFont("Pacifico", str(HERE / "fonts" / "Pacifico.ttf")))


def crop_to_ratio(img: Image.Image, ratio: float) -> Image.Image:
    """Center-crop img to width/height == ratio."""
    w, h = img.size
    if w / h > ratio:
        new_w = round(h * ratio)
        left = (w - new_w) // 2
        return img.crop((left, 0, left + new_w, h))
    new_h = round(w / ratio)
    top = (h - new_h) // 2
    return img.crop((0, top, w, top + new_h))


def cover_file(page_w: float, page_h: float) -> Path:
    """Write the cover cropped to the page shape and return its path."""
    img = crop_to_ratio(Image.open(HERE / "cover.jpg").convert("RGB"), page_w / page_h)
    path = OUT / f"_cover_{round(page_w)}x{round(page_h)}.jpg"
    img.save(path, quality=95, subsampling=0)
    return path


def line_art(path: Path) -> ImageReader:
    """Load a black and white drawing as grayscale so it prints with black ink only."""
    return ImageReader(Image.open(path).convert("L"))


def new_canvas(path: Path, size: tuple[float, float]) -> canvas.Canvas:
    # Start with an embedded font so the PDF lists no unembedded Helvetica.
    return canvas.Canvas(str(path), pagesize=size, initialFontName="Fredoka")


def heart(c: canvas.Canvas, cx: float, cy: float, size: float) -> None:
    """Outline heart centered at (cx, cy), about size wide."""
    s = size / 2
    p = c.beginPath()
    p.moveTo(cx, cy - s * 0.9)
    p.curveTo(cx - s * 0.2, cy - s * 0.55, cx - s, cy - s * 0.15, cx - s, cy + s * 0.3)
    p.curveTo(cx - s, cy + s * 0.75, cx - s * 0.45, cy + s * 0.95, cx, cy + s * 0.5)
    p.curveTo(cx + s * 0.45, cy + s * 0.95, cx + s, cy + s * 0.75, cx + s, cy + s * 0.3)
    p.curveTo(cx + s, cy - s * 0.15, cx + s * 0.2, cy - s * 0.55, cx, cy - s * 0.9)
    p.close()
    c.drawPath(p, stroke=1, fill=0)


def frame_box() -> tuple[float, float, float, float]:
    fw = DRAW_W + 2 * FRAME_PAD
    fh = DRAW_H + 2 * FRAME_PAD
    fx = (PAGE_W - fw) / 2
    fy = PAGE_H - FRAME_TOP - fh
    return fx, fy, fw, fh


def drawing_page(c: canvas.Canvas, img: Path, number: int) -> None:
    fx, fy, fw, fh = frame_box()
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1.6)
    c.roundRect(fx, fy, fw, fh, 6 * mm, stroke=1, fill=0)
    c.drawImage(line_art(img), fx + FRAME_PAD, fy + FRAME_PAD, DRAW_W, DRAW_H)
    # Page number inside a small heart, centered under the frame.
    hy = fy / 2
    c.setLineWidth(1.2)
    heart(c, PAGE_W / 2, hy, 11 * mm)
    c.setFillColorRGB(*INK)
    c.setFont("Fredoka", 9)
    c.drawCentredString(PAGE_W / 2, hy - 0.6 * mm, str(number))


def owner_page(c: canvas.Canvas) -> None:
    fx, fy, fw, fh = frame_box()
    c.setStrokeColorRGB(*INK)
    c.setFillColorRGB(*INK)
    c.setLineWidth(1.6)
    c.roundRect(fx, fy, fw, fh, 6 * mm, stroke=1, fill=0)
    c.setFont("Pacifico", 34)
    c.drawCentredString(PAGE_W / 2, fy + fh - 34 * mm, "Este livro pertence a:")
    c.setLineWidth(1.2)
    line_y = fy + fh - 58 * mm
    c.line(fx + 25 * mm, line_y, fx + fw - 25 * mm, line_y)
    hearts_y = line_y - 14 * mm
    for dx in (-30 * mm, 0, 30 * mm):
        heart(c, PAGE_W / 2 + dx, hearts_y, 9 * mm)
    # Drawing fills the space left between the hearts and the frame bottom.
    art_bottom = fy + 8 * mm
    art_h = hearts_y - 10 * mm - art_bottom
    art_w = art_h * 3 / 4
    c.drawImage(line_art(HERE / "pages" / "owner.png"), (PAGE_W - art_w) / 2, art_bottom, art_w, art_h)


def build_book() -> Path:
    path = OUT / "Colorindo-com-a-Estela.pdf"
    c = new_canvas(path, A4)
    c.setTitle(TITLE)
    c.setAuthor("TeteGoods")
    c.setSubject("Livro de colorir: a Estela e o unicórnio")
    c.drawImage(str(cover_file(PAGE_W, PAGE_H)), 0, 0, PAGE_W, PAGE_H)
    c.showPage()
    owner_page(c)
    c.showPage()
    for n in range(1, 41):
        drawing_page(c, HERE / "pages" / f"{n:02d}.png", n)
        c.showPage()
    c.save()
    return path


def build_cover_with_bleed() -> Path:
    w, h = PAGE_W + 2 * BLEED, PAGE_H + 2 * BLEED
    path = OUT / "Colorindo-com-a-Estela-capa-sangria.pdf"
    c = new_canvas(path, (w, h))
    c.setTitle(f"{TITLE} - capa com sangria de 3 mm")
    c.drawImage(str(cover_file(w, h)), 0, 0, w, h)
    # Trim box tells print software where to cut.
    c.setTrimBox((BLEED, BLEED, BLEED + PAGE_W, BLEED + PAGE_H))
    c.showPage()
    c.save()
    return path


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for p in (build_book(), build_cover_with_bleed()):
        print(p)
    for tmp in OUT.glob("_cover_*.jpg"):
        tmp.unlink()


if __name__ == "__main__":
    main()
