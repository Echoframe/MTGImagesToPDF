import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black
from PIL import Image, ImageFilter, ImageEnhance

# =========================
# CONFIG
# =========================

INPUT_DIR = "cards"
OUTPUT_PDF = "mtg_a4_print_ready.pdf"

CARD_W_MM = 63
CARD_H_MM = 88
BLEED_MM = 3

CARDS_X = 3
CARDS_Y = 3

MIN_DPI = 600

CROP_LEN = 5 * mm
CROP_OFFSET = 1.5 * mm

SUPPORTED = (".png", ".jpg", ".jpeg", ".tif", ".tiff")

# =========================
# DERIVED
# =========================

PRINT_W_MM = CARD_W_MM + BLEED_MM * 2
PRINT_H_MM = CARD_H_MM + BLEED_MM * 2

PAGE_W, PAGE_H = A4

print_w = PRINT_W_MM * mm
print_h = PRINT_H_MM * mm

grid_w = CARDS_X * print_w
grid_h = CARDS_Y * print_h

margin_x = (PAGE_W - grid_w) / 2
margin_y = (PAGE_H - grid_h) / 2

# =========================
# HELPERS
# =========================

def effective_dpi(img, w_mm, h_mm):
    px_w, px_h = img.size
    return min(
        px_w / (w_mm / 25.4),
        px_h / (h_mm / 25.4)
    )

def upscale_if_needed(img):
    dpi = effective_dpi(img, PRINT_W_MM, PRINT_H_MM)
    if dpi >= MIN_DPI:
        return img

    scale = MIN_DPI / dpi
    new_size = (
        int(img.width * scale),
        int(img.height * scale)
    )

    img = img.resize(new_size, Image.LANCZOS)
    img = img.filter(ImageFilter.UnsharpMask(
        radius=1.2,
        percent=120,
        threshold=2
    ))
    return img

def glossy_compensation(img):
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.05)
    return img

def micro_black_boost(img):
    r, g, b = img.split()
    r = r.point(lambda x: max(0, x - 3))
    g = g.point(lambda x: max(0, x - 3))
    b = b.point(lambda x: max(0, x - 3))
    return Image.merge("RGB", (r, g, b))

def draw_crop_marks(c, x, y, w, h):
    c.setStrokeColor(black)
    c.setLineWidth(0.3)

    # Top-left
    c.line(x - CROP_OFFSET, y, x - CROP_OFFSET - CROP_LEN, y)
    c.line(x, y + h + CROP_OFFSET, x, y + h + CROP_OFFSET + CROP_LEN)

    # Top-right
    c.line(x + w + CROP_OFFSET, y, x + w + CROP_OFFSET + CROP_LEN, y)
    c.line(x + w, y + h + CROP_OFFSET, x + w, y + h + CROP_OFFSET + CROP_LEN)

    # Bottom-left
    c.line(x - CROP_OFFSET, y + h, x - CROP_OFFSET - CROP_LEN, y + h)
    c.line(x, y - CROP_OFFSET, x, y - CROP_OFFSET - CROP_LEN)

    # Bottom-right
    c.line(x + w + CROP_OFFSET, y + h, x + w + CROP_OFFSET + CROP_LEN, y + h)
    c.line(x + w, y - CROP_OFFSET, x + w, y - CROP_OFFSET - CROP_LEN)

# =========================
# LOAD FILES
# =========================

files = sorted(
    f for f in os.listdir(INPUT_DIR)
    if f.lower().endswith(SUPPORTED)
)

if not files:
    raise RuntimeError("No card images found.")

# =========================
# PDF
# =========================

c = canvas.Canvas(OUTPUT_PDF, pagesize=A4)
idx = 0

while idx < len(files):
    for row in range(CARDS_Y):
        for col in range(CARDS_X):
            if idx >= len(files):
                break

            path = os.path.join(INPUT_DIR, files[idx])
            img = Image.open(path)

            if img.mode != "RGB":
                img = img.convert("RGB")

            img = upscale_if_needed(img)
            img = micro_black_boost(img)
            img = glossy_compensation(img)

            temp = path + "_tmp.tif"
            img.save(temp, format="JPEG", quality=95, dpi=(1200,1200))

            x = margin_x + col * print_w
            y = PAGE_H - margin_y - (row + 1) * print_h

            c.drawImage(
                temp,
                x, y,
                width=print_w,
                height=print_h
            )

            draw_crop_marks(c, x, y, print_w, print_h)
            print(f"Processing card {idx + 1} / {len(files)}: {files[idx]}")

            os.remove(temp)
            idx += 1

    c.showPage()

c.save()
print(f"✔ Print-ready PDF created: {OUTPUT_PDF}")
