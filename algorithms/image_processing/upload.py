import base64
import io
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

import fitz          # PyMuPDF  — pip install pymupdf
import pdfplumber    # text extraction
from PIL import Image


# ── configuration ────────────────────────────────────────────────────────────

@dataclass
class ReaderConfig:
    """Tune extraction and image-optimisation behaviour."""

    # --- text ---
    text_layout: bool = True          # preserve spatial layout (pdfplumber)

    # --- page rasterisation (for scanned pages / visual fallback) ---
    raster_dpi: int = 150             # DPI for full-page raster (if needed)

    # --- embedded image extraction ---
    extract_images: bool = True       # pull raster images embedded in the PDF
    min_image_px: int = 50           # ignore images smaller than this in either dimension
    max_image_px: int = 1800         # downscale images larger than this
    image_format: str = "JPEG"       # output format: JPEG | PNG | WEBP
    image_quality: int = 85          # JPEG/WEBP quality (1-95)
    skip_grayscale_masks: bool = True # skip 1-bit mask images (decorative)


# ── output types ─────────────────────────────────────────────────────────────

@dataclass
class PageImage:
    index: int          # image index on the page (0-based)
    width: int          # pixels
    height: int         # pixels
    data: bytes         # raw bytes in image_format
    base64: str         # base64-encoded string (useful for HTML src= or APIs)
    format: str         # e.g. "JPEG"


@dataclass
class PageResult:
    page_number: int    # 1-based
    text: str           # extracted text (empty string if none)
    images: list[PageImage] = field(default_factory=list)


# ── helpers ───────────────────────────────────────────────────────────────────

def _optimise_image(pix: fitz.Pixmap, cfg: ReaderConfig) -> bytes | None:
    """
    Convert a PyMuPDF Pixmap → optimised bytes.
    Returns None if the image should be skipped.
    """
    # Convert CMYK / unusual colour spaces → RGB
    if pix.colorspace and pix.colorspace.name not in ("DeviceRGB", "DeviceGray"):
        pix = fitz.Pixmap(fitz.csRGB, pix)

    # Skip 1-bit masks (tiny, decorative)
    if cfg.skip_grayscale_masks and pix.n == 1 and (pix.width < cfg.min_image_px or pix.height < cfg.min_image_px):
        return None

    # Skip images that are too small
    if pix.width < cfg.min_image_px or pix.height < cfg.min_image_px:
        return None

    # Convert pixmap → PIL Image
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)

    # Drop alpha channel for JPEG
    if cfg.image_format == "JPEG" and img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Downscale if too large
    if img.width > cfg.max_image_px or img.height > cfg.max_image_px:
        img.thumbnail((cfg.max_image_px, cfg.max_image_px), Image.LANCZOS)

    buf = io.BytesIO()
    save_kwargs: dict = {"format": cfg.image_format}
    if cfg.image_format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = cfg.image_quality
        save_kwargs["optimize"] = True
    img.save(buf, **save_kwargs)
    return buf.getvalue()


# ── main function ─────────────────────────────────────────────────────────────

def read_pdf(
    path: str | Path,
    pages: list[int] | None = None,   # 1-based page numbers; None = all pages
    config: ReaderConfig | None = None,
) -> Iterator[PageResult]:
    """
    Iterate over PDF pages, yielding a PageResult for each.

    Parameters
    ----------
    path   : path to the PDF file
    pages  : optional list of 1-based page numbers to read (None = all)
    config : ReaderConfig instance to customise behaviour

    Yields
    ------
    PageResult with .page_number, .text, .images
    """
    cfg = config or ReaderConfig()
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")

    # Open with both libraries
    fitz_doc = fitz.open(str(path))
    total = len(fitz_doc)

    with pdfplumber.open(str(path)) as plumber_doc:

        target_pages = pages if pages else list(range(1, total + 1))

        for page_num in target_pages:
            if page_num < 1 or page_num > total:
                continue

            idx = page_num - 1   # 0-based index

            # ── TEXT ──────────────────────────────────────────────────────────
            plumber_page = plumber_doc.pages[idx]
            text: str = plumber_page.extract_text(layout=cfg.text_layout) or ""

            # ── IMAGES ────────────────────────────────────────────────────────
            page_images: list[PageImage] = []

            if cfg.extract_images:
                fitz_page = fitz_doc[idx]
                img_list = fitz_page.get_images(full=True)

                img_index = 0
                seen_xrefs: set[int] = set()

                for img_info in img_list:
                    xref = img_info[0]
                    if xref in seen_xrefs:      # deduplicate shared images
                        continue
                    seen_xrefs.add(xref)

                    try:
                        pix = fitz.Pixmap(fitz_doc, xref)
                    except Exception:
                        continue

                    data = _optimise_image(pix, cfg)
                    if data is None:
                        continue

                    # Re-read dimensions after possible resize
                    final_img = Image.open(io.BytesIO(data))
                    w, h = final_img.size

                    page_images.append(PageImage(
                        index=img_index,
                        width=w,
                        height=h,
                        data=data,
                        base64=base64.b64encode(data).decode(),
                        format=cfg.image_format,
                    ))
                    img_index += 1

            yield PageResult(
                page_number=page_num,
                text=text,
                images=page_images,
            )

    fitz_doc.close()


# ── convenience: save all extracted images to disk ───────────────────────────

def save_images(pages: list[PageResult], output_dir: str | Path = ".") -> list[Path]:
    """Save all images from extracted pages to disk. Returns list of saved paths."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []

    for page in pages:
        for img in page.images:
            ext = img.format.lower().replace("jpeg", "jpg")
            fname = output_dir / f"page{page.page_number:03d}_img{img.index:02d}.{ext}"
            fname.write_bytes(img.data)
            saved.append(fname)

    return saved


# ── quick demo ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_reader.py <path_to_pdf> [page_numbers...]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    page_filter = [int(p) for p in sys.argv[2:]] if len(sys.argv) > 2 else None

    cfg = ReaderConfig(
        extract_images=True,
        image_format="JPEG",
        image_quality=85,
        max_image_px=1800,
        min_image_px=50,
    )

    all_pages: list[PageResult] = []

    for result in read_pdf(pdf_path, pages=page_filter, config=cfg):
        print(f"\n{'='*60}")
        print(f"PAGE {result.page_number}  |  {len(result.images)} image(s)")
        print(f"{'='*60}")
        print(result.text[:800] + ("..." if len(result.text) > 800 else ""))
        for img in result.images:
            print(f"  [Image {img.index}] {img.width}x{img.height} px  "
                  f"{len(img.data)/1024:.1f} KB  base64 len={len(img.base64)}")
        all_pages.append(result)

    # Save images next to the PDF
    out_dir = Path(pdf_path).parent / "extracted_images"
    paths = save_images(all_pages, out_dir)
    if paths:
        print(f"\nSaved {len(paths)} image(s) → {out_dir}")