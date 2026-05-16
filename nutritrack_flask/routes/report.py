"""
routes/report.py
═══════════════════════════════════════════════════════════════
Blueprint: Medical Report Analysis

POST /api/analyze-report
────────────────────────
Accepts a multipart/form-data upload with field "file"
(PDF, PNG, JPG, TIFF, or BMP) and returns structured JSON
containing extracted health metrics, diet recommendations,
and a human-readable summary.

Pipeline:
  1. Validate + read file upload
  2. Extract text  (PyMuPDF → Tesseract OCR fallback)
  3. NLP extraction + classification  (regex-based)
  4. Diet recommendations  (condition-map driven)
  5. Return structured JSON

Error responses use standard HTTP codes with descriptive messages.
═══════════════════════════════════════════════════════════════
"""

import logging

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from helpers.report_extractor import extract_text
from helpers.medical_nlp      import extract_and_classify
from helpers.report_diet      import get_diet_recommendations, generate_summary

logger    = logging.getLogger(__name__)
report_bp = Blueprint("report", __name__)

# ── Configuration ─────────────────────────────────────────────

# Accepted MIME types (used for primary validation)
ALLOWED_MIME_TYPES = frozenset({
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/tiff",
    "image/bmp",
})

# Extension → MIME fallback for browsers that send 'application/octet-stream'
EXT_TO_MIME = {
    "pdf":  "application/pdf",
    "png":  "image/png",
    "jpg":  "image/jpeg",
    "jpeg": "image/jpeg",
    "tiff": "image/tiff",
    "tif":  "image/tiff",
    "bmp":  "image/bmp",
}

# Maximum allowed file size (10 MB)
MAX_FILE_BYTES = 10 * 1024 * 1024


# ── Endpoint ──────────────────────────────────────────────────

@report_bp.route("/analyze-report", methods=["POST"])
def analyze_report():
    """
    POST /api/analyze-report
    ─────────────────────────────────────────────────────────
    Form field : file  (PDF | PNG | JPG | TIFF | BMP)

    Success — 200:
    {
      "success":   true,
      "filename":  "blood_report.pdf",
      "metrics": {
        "hemoglobin":  { "value": 10.8, "unit": "g/dL",  "status": "low"      },
        "vitamin_b12": { "value": 190,  "unit": "pg/mL", "status": "low"      },
        "bmi":         { "value": 27.4, "unit": "kg/m²", "status": "overweight" }
      },
      "diet_plan": [
        {
          "condition": "Low Hemoglobin (Anaemia Risk)",
          "recommendations": ["Eat iron-rich foods: spinach, lentils …", …]
        },
        …
      ],
      "summary": "Hemoglobin: 10.8 g/dL (low) | … Report flagged: …"
    }

    Error responses use standard HTTP status codes:
      400 → missing / empty file field
      413 → file too large
      415 → unsupported file type
      422 → text extraction failed (unreadable / corrupted file)
      500 → internal processing error
    """

    # ── Step 1: Validate file presence ────────────────────────
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "message": (
                "No 'file' field found in request. "
                "Send as multipart/form-data with field name 'file'."
            ),
        }), 400

    uploaded = request.files["file"]

    if not uploaded or uploaded.filename == "":
        return jsonify({
            "success": False,
            "message": "File field is empty. Please attach a valid PDF or image file.",
        }), 400

    filename  = secure_filename(uploaded.filename)
    mime_type = (uploaded.mimetype or "").lower().strip()

    # ── Step 2: Resolve MIME type ──────────────────────────────
    # Some clients send 'application/octet-stream' — infer from extension.
    if mime_type not in ALLOWED_MIME_TYPES:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        resolved = EXT_TO_MIME.get(ext, mime_type)
        logger.debug(
            "MIME '%s' not in allow-list; resolved via extension '.%s' → '%s'",
            mime_type, ext, resolved,
        )
        mime_type = resolved

    if mime_type not in ALLOWED_MIME_TYPES:
        return jsonify({
            "success": False,
            "message": (
                f"Unsupported file type '{mime_type}'. "
                "Accepted: PDF, PNG, JPG, TIFF, BMP."
            ),
        }), 415

    # ── Step 3: Read bytes + enforce size limit ────────────────
    file_bytes = uploaded.read()

    if len(file_bytes) == 0:
        return jsonify({
            "success": False,
            "message": "The uploaded file is empty (0 bytes).",
        }), 400

    if len(file_bytes) > MAX_FILE_BYTES:
        size_kb = len(file_bytes) // 1024
        return jsonify({
            "success": False,
            "message": f"File too large ({size_kb:,} KB). Maximum allowed size is 10 MB.",
        }), 413

    logger.info(
        "Received report: '%s' | MIME: %s | Size: %d KB",
        filename, mime_type, len(file_bytes) // 1024,
    )

    # ── Step 4: Extract text ───────────────────────────────────
    try:
        raw_text = extract_text(file_bytes, mime_type)
    except ValueError as exc:
        # Unsupported type (already checked, but belt-and-suspenders)
        return jsonify({"success": False, "message": str(exc)}), 415
    except Exception as exc:
        logger.exception("Text extraction failed for '%s'", filename)
        return jsonify({
            "success": False,
            "message": (
                f"Could not extract text from '{filename}'. "
                "Ensure the file is not password-protected or corrupted. "
                f"Detail: {exc}"
            ),
        }), 422

    if not raw_text or not raw_text.strip():
        return jsonify({
            "success": False,
            "message": (
                "No readable text was found in the uploaded file. "
                "If this is a scanned document, ensure the scan is clear "
                "and Tesseract OCR is installed on the server."
            ),
        }), 422

    logger.debug("Text extraction OK: %d chars from '%s'", len(raw_text), filename)

    # ── Step 5: NLP extraction + classification ────────────────
    try:
        classified_metrics = extract_and_classify(raw_text)
    except Exception as exc:
        logger.exception("NLP extraction failed for '%s'", filename)
        return jsonify({
            "success": False,
            "message": f"NLP extraction error: {exc}",
        }), 500

    # ── Step 6: Diet recommendations + summary ─────────────────
    try:
        diet_plan = get_diet_recommendations(classified_metrics)
        summary   = generate_summary(classified_metrics, diet_plan)
    except Exception as exc:
        logger.exception("Diet generation failed for '%s'", filename)
        return jsonify({
            "success": False,
            "message": f"Diet plan generation error: {exc}",
        }), 500

    # ── Step 7: Compose and return response ───────────────────
    found_metrics = sum(
        1 for m in classified_metrics.values() if m.get("value") is not None
    )
    logger.info(
        "Analysis complete | file='%s' | metrics_found=%d | conditions_triggered=%d",
        filename, found_metrics, len(diet_plan),
    )

    return jsonify({
        "success":   True,
        "filename":  filename,
        "metrics":   classified_metrics,
        "diet_plan": diet_plan,
        "summary":   summary,
    }), 200
