"""
helpers/medical_nlp.py
═══════════════════════════════════════════════════════════════
NLP extraction and classification layer.

Extracts health metrics from free-form text (OCR or direct PDF)
and classifies each value as low / normal / high / etc.

Currently supports:
  • Hemoglobin  (g/dL)
  • Vitamin B12 (pg/mL)
  • BMI         (kg/m²)

Extension guide:
  Adding a new metric requires only one new entry in METRIC_REGISTRY:
  {
    "patterns":   [list of regex strings],
    "unit":       "unit string",
    "thresholds": [(upper_bound, label), ..., (inf, label)],
  }
═══════════════════════════════════════════════════════════════
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


# ── Regex helpers ─────────────────────────────────────────────

def _first_match(patterns: list, text: str) -> Optional[float]:
    """
    Try each regex pattern in order against `text`.
    Returns the first successfully parsed float, or None.

    Patterns must capture the numeric value in group 1.
    """
    for pattern in patterns:
        try:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                raw = match.group(1).replace(",", ".")
                return float(raw)
        except (ValueError, IndexError, AttributeError):
            continue
    return None


# ── Classification helper ─────────────────────────────────────

def _classify(value: float, thresholds: list) -> str:
    """
    Classify `value` using an ascending list of (upper_bound, label) pairs.
    The last entry's upper_bound should be float('inf').

    Example:
      thresholds = [(12, "low"), (16, "normal"), (float("inf"), "high")]
      _classify(11.2, thresholds)  →  "low"
      _classify(14.0, thresholds)  →  "normal"
      _classify(17.5, thresholds)  →  "high"
    """
    for upper_bound, label in thresholds:
        if value < upper_bound:
            return label
    # Fallback to the last label (should never be reached with float("inf"))
    return thresholds[-1][1]


# ── Metric registry ───────────────────────────────────────────
# Each metric is fully self-contained: patterns + unit + thresholds.
# This is the ONLY place to touch when adding new health parameters.

METRIC_REGISTRY = {

    "hemoglobin": {
        "description": "Hemoglobin level in blood",
        "unit": "g/dL",
        "patterns": [
            # Strict: requires the unit (g/dL) immediately after the number
            r"(?:ha?e?moglobin|hb|hgb).*?((?:[2-9]|\d{2,})\.?\d*)\s*g\s*/?\s*d\s*l?",
            # Loose: captures the first realistic number (skipping '1') found after the keyword
            r"(?:ha?e?moglobin).{0,50}?((?:[2-9]|\d{2,})\.?\d*)",
            r"\b(?:hb|hgb)\b.{0,25}?((?:[2-9]|\d{2,})\.?\d*)",
        ],
        "thresholds": [
            (12.0,         "low"),
            (16.0,         "normal"),
            (float("inf"), "high"),
        ],
    },

    "height": {
        "description": "Patient's height",
        "unit": "cm",
        "patterns": [
            r"\b(?:height|ht)\b[^\d]{0,20}?(\d+\.?\d*)\s*(?:cm|m|in)?",
        ],
        "thresholds": [
            (float("inf"), "normal"),
        ],
    },

    "weight": {
        "description": "Patient's body weight",
        "unit": "kg",
        "patterns": [
            r"\b(?:weight|wt)\b.*?(\d+\.?\d*)\s*(?:kg|lbs)",
            r"\b(?:weight|wt)\b[^\d]{0,20}?(\d+\.?\d*)",
        ],
        "thresholds": [
            (float("inf"), "normal"),
        ],
    },

    "vitamin_b12": {
        "description": "Vitamin B12 (cobalamin) serum level",
        "unit": "pg/mL",
        "patterns": [
            r"(?:vit(?:amin)?\s*)?b[\s\-]?12.*?(\d+\.?\d*)\s*(?:pg\s*/?\s*m\s*l?|pmol)",
            r"(?:cyano)?cobalamin.*?(\d+\.?\d*)\s*(?:pg\s*/?\s*m\s*l?|pmol)",
            r"(?:vit(?:amin)?\s*)?b[\s\-]?12[^\d]{0,30}?(\d+\.?\d*)",
            r"(?:cyano)?cobalamin[^\d]{0,30}?(\d+\.?\d*)",
        ],
        "thresholds": [
            (200.0,        "low"),
            (900.0,        "normal"),
            (float("inf"), "high"),
        ],
    },

    "bmi": {
        "description": "Body Mass Index",
        "unit": "kg/m²",
        "patterns": [
            r"\bb\.?m\.?i\.?\b.*?(\d+\.?\d*)\s*kg\s*/?\s*m\s*2?",
            r"body\s+mass\s+index.*?(\d+\.?\d*)\s*kg\s*/?\s*m\s*2?",
            r"\bb\.?m\.?i\.?\b[^\d]{0,40}?(\d+\.?\d*)",
            r"body\s+mass\s+index[^\d]{0,30}?(\d+\.?\d*)",
        ],
        "thresholds": [
            (18.5,         "underweight"),
            (25.0,         "normal"),
            (30.0,         "overweight"),
            (float("inf"), "obese"),
        ],
    },
}


# ── Public API ────────────────────────────────────────────────

def extract_and_classify(text: str) -> dict:
    """
    Run every registered metric extractor against `text`.

    Returns a dict keyed by metric name:
    {
      "hemoglobin":  { "value": 11.2, "unit": "g/dL",  "status": "low"     },
      "vitamin_b12": { "value": None,  "unit": "pg/mL", "status": "not_found" },
      "bmi":         { "value": 27.3,  "unit": "kg/m²", "status": "overweight" },
    }

    "not_found" status means the metric was not detected in the text
    (not necessarily missing from the patient's record).
    """
    results = {}

    for metric_name, meta in METRIC_REGISTRY.items():
        value = _first_match(meta["patterns"], text)

        if value is None:
            logger.debug("Metric '%s' — not found in text", metric_name)
            results[metric_name] = {
                "value":  None,
                "unit":   meta["unit"],
                "status": "not_found",
            }
        else:
            status = _classify(value, meta["thresholds"])
            logger.debug(
                "Metric '%s' = %s %s → status: '%s'",
                metric_name, value, meta["unit"], status,
            )
            results[metric_name] = {
                "value":  value,
                "unit":   meta["unit"],
                "status": status,
            }

    found_count = sum(1 for r in results.values() if r["value"] is not None)
    logger.info(
        "NLP extraction complete: %d/%d metrics detected",
        found_count, len(METRIC_REGISTRY),
    )
    return results
