"""
helpers/report_extractor.py
═══════════════════════════════════════════════════════════════
Text extraction layer for the medical report analysis pipeline.

Supported inputs:
  • PDF (digital)  → direct text via PyMuPDF
  • PDF (scanned)  → render each page → Tesseract OCR
  • PNG / JPG / TIFF / BMP → Tesseract OCR

Strategy:
  1. For PDFs, try direct embedded-text extraction first.
  2. If the result is sparse (< MIN_CHARS meaningful chars),
     the PDF is likely scanned — fall back to per-page OCR.
  3. For images, go directly to OCR.

System dependency: Tesseract must be installed on the OS.
  • Windows  : https://github.com/UB-Mannheim/tesseract/wiki
  • Linux    : apt-get install tesseract-ocr
  • macOS    : brew install tesseract
═══════════════════════════════════════════════════════════════
"""

import io
import logging

try:
    import fitz          # PyMuPDF
except ImportError as e:
    raise ImportError("PyMuPDF is required: pip install PyMuPDF") from e

try:
    import pytesseract
    from PIL import Image
except ImportError as e:
    raise ImportError(
        "pytesseract and Pillow are required: pip install pytesseract Pillow"
    ) from e

logger = logging.getLogger(__name__)

# If direct PDF text extraction yields fewer than this many non-whitespace
# characters, assume the PDF is scanned and fall back to OCR.
MIN_CHARS = 80

# Tesseract language(s) to use.  'eng' covers most medical reports.
TESS_LANG = "eng"

# Render PDF pages at this zoom factor for OCR (2× ≈ 144 dpi → good accuracy).
OCR_ZOOM = 2.0


# ── Private helpers ───────────────────────────────────────────

def _ocr_pil_image(image: "Image.Image") -> str:
    """Run Tesseract OCR on a PIL Image and return the extracted text."""
    # Ensure a mode that Tesseract handles well
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    # PSM 6 = assume a uniform block of text (works well for lab reports)
    config = "--psm 6"
    text = pytesseract.image_to_string(image, lang=TESS_LANG, config=config)
    logger.debug("OCR produced %d characters", len(text))
    return text


def _ocr_bytes(image_bytes: bytes) -> str:
    """Open raw image bytes and OCR them."""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        return _ocr_pil_image(image)
    except Exception as exc:
        logger.warning("OCR failed on image bytes: %s", exc)
        raise


def _extract_pdf_text_direct(file_bytes: bytes) -> str:
    """Extract embedded text from a digital PDF using PyMuPDF."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    try:
        pages = [page.get_text("text") for page in doc]
    finally:
        doc.close()
    return "\n".join(pages)


def _ocr_pdf_pages(file_bytes: bytes) -> str:
    """
    Rasterise each page of a PDF at OCR_ZOOM and run Tesseract on each.
    Used when the PDF contains scanned (image-only) pages.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    page_texts = []
    try:
        matrix = fitz.Matrix(OCR_ZOOM, OCR_ZOOM)
        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csRGB)
            img_bytes = pix.tobytes("png")
            logger.debug("OCR-ing PDF page %d/%d", page_num, len(doc))
            page_texts.append(_ocr_bytes(img_bytes))
    finally:
        doc.close()
    return "\n".join(page_texts)


# ── Public API ────────────────────────────────────────────────

def extract_text(file_bytes: bytes, mime_type: str) -> str:
    """
    Top-level dispatcher: extract readable text from any supported file.

    Args:
        file_bytes : Raw bytes of the uploaded file.
        mime_type  : MIME type string, e.g. 'application/pdf', 'image/png'.

    Returns:
        Extracted text as a single string (may be multi-page for PDFs).

    Raises:
        ValueError  : If mime_type is not supported.
        RuntimeError: If text extraction fails unexpectedly.
    """
    mime_type = (mime_type or "").lower().strip()

    if mime_type == "application/pdf":
        logger.info("PDF upload — attempting direct text extraction (%d bytes)", len(file_bytes))
        text = _extract_pdf_text_direct(file_bytes)

        meaningful_chars = len(text.replace(" ", "").replace("\n", ""))
        if meaningful_chars < MIN_CHARS:
            logger.info(
                "PDF text sparse (%d chars) — falling back to OCR", meaningful_chars
            )
            text = _ocr_pdf_pages(file_bytes)
        else:
            logger.info("PDF direct text OK (%d chars)", len(text))

        return text

    elif mime_type in {"image/png", "image/jpeg", "image/jpg", "image/tiff", "image/bmp"}:
        logger.info(
            "Image upload (%s) — running OCR (%d bytes)", mime_type, len(file_bytes)
        )
        return _ocr_bytes(file_bytes)

    else:
        raise ValueError(
            f"Unsupported file type: '{mime_type}'. "
            "Accepted types: application/pdf, image/png, image/jpeg, image/tiff, image/bmp."
        )
