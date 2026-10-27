# Colorindo com a Estela

A coloring book with a color cover and 40 black-and-white pages. Estela, a chibi girl with long curly hair, has adventures with her baby unicorn. Her younger sister, who has two pigtails tied with flowers, shows up on 8 pages.

**Print file:** `output/Colorindo-com-a-Estela.pdf`

## What is in the PDF

| PDF page | Content |
|---|---|
| 1 | Color cover |
| 2 | "Este livro pertence a:" (a line for the child's name) |
| 3–42 | Drawings 1–40, each in a rounded frame with its number in a heart |

- Size: A4 (210 × 297 mm).
- Drawings: pure black and white, gray only (no color ink), about 500 dpi.
- Cover: about 350 dpi.
- Fonts are embedded.

`output/Colorindo-com-a-Estela-capa-sangria.pdf` is the cover alone with 3 mm of extra art on each side ("bleed"), for print shops that cut the cover to size.

### Printing tips

- Print on one side only, so markers don't show through on the next drawing.
- Use thick paper (120–180 g/m²) for the drawings and 240–300 g/m² for the cover.
- If the printer can't print to the edge, choose "fit to page". The cover will get a thin white border.

## Pages

| # | Scene | # | Scene |
|---|---|---|---|
| 1 | Hug in the meadow | 21 | Birthday party (with sister) |
| 2 | Riding over a rainbow | 22 | Making strawberry jam |
| 3 | Princess hug | 23 | Garden walk in a bucket hat and sunglasses |
| 4 | Daydreaming on a cloud | 24 | Painting a rainbow |
| 5 | Little witch with a wand | 25 | Tea party (with sister) |
| 6 | Mermaid | 26 | Watering the flowers |
| 7 | Nap in a unicorn hoodie | 27 | Flying a kite |
| 8 | Beach day | 28 | Building a snowman (with sister) |
| 9 | Ice cream picnic | 29 | Camping and marshmallows |
| 10 | Flower swing | 30 | Hot air balloon |
| 11 | Hug with hearts | 31 | Playground (with sister) |
| 12 | Princess and castle | 32 | Ballet |
| 13 | Sleeping under the moon | 33 | Christmas tree (with sister) |
| 14 | Galloping by the rainbow | 34 | Bicycle ride |
| 15 | Reading in pajamas | 35 | Rainy day (with sister) |
| 16 | Baking a cake | 36 | Brushing the unicorn's mane |
| 17 | Flying on a winged unicorn | 37 | Making music (with sister) |
| 18 | Flower crown | 38 | Space trip |
| 19 | Pool float | 39 | Bedtime |
| 20 | Fairy with a wand | 40 | Group hug in a heart (with sister) |

Pages 1–20 are the `references/pagina_chibi_01` to `20` drawings, redrawn by AI in a 3:4 shape so they fill an A4 page. Pages 21–40 are new scenes drawn in the same style. Scenes 21–23 bring the `ref-03`, `ref-05` and `ref-02`/`ref-04` themes into the chibi style. The `ref-*` drawings were not used as-is, because they are square, much denser, and show a different girl.

All art was made with Higgsfield (Nano Banana Pro at 2K). The cover was then enlarged to 4K.

## Folders

| Path | What it holds |
|---|---|
| `references/` | Source drawings, plus `sister.png` (the younger sister) |
| `pages/` | Final drawings `01`–`40` and `owner.png` (drawing on PDF page 2), 3584 × 4800 px, pure black and white |
| `cover.jpg` | Final cover, 3072 × 4096 px |
| `fonts/` | Fredoka and Pacifico (SIL Open Font License) |
| `output/` | The print PDFs |

## Rebuild

```bash
pip install pillow reportlab
python3 prepare_pages.py RAW_DIR   # only for new raw drawings: RAW_DIR/p01.png..p40.png -> pages/
python3 build_book.py              # pages/ + cover.jpg -> output/*.pdf
```

`prepare_pages.py` enlarges each 1792 × 2400 drawing 2×, removes any color (some drawings came with pink cheeks) and makes it pure black and white.
