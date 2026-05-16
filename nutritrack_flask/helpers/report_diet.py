"""
helpers/report_diet.py
═══════════════════════════════════════════════════════════════
Diet recommendation engine for the medical report pipeline.

Maps classified health metrics → actionable dietary advice.

Design:
  • CONDITION_MAP is the single source of truth — no scattered
    if/else chains. Every condition has:
      - "condition"       : human-readable label
      - "trigger"         : lambda(classified_metrics) → bool
      - "recommendations" : list of food/lifestyle advice strings

  • Extension guide: add one entry to CONDITION_MAP.
═══════════════════════════════════════════════════════════════
"""

import logging

logger = logging.getLogger(__name__)


# ── Condition → recommendation map ───────────────────────────
# Trigger lambdas receive the full classified_metrics dict.
# They must be safe (no KeyError) — use .get() with defaults.

CONDITION_MAP = [

    {
        "condition": "Low Hemoglobin (Anaemia Risk)",
        "trigger":   lambda m: m.get("hemoglobin", {}).get("status") == "low",
        "recommendations": [
            "Eat iron-rich foods daily: spinach, lentils, kidney beans, tofu, pumpkin seeds",
            "Pair iron foods with Vitamin C (lemon juice, amla, bell peppers) to boost absorption",
            "Include lean red meat, liver, or chicken 3–4× a week (non-vegetarian)",
            "Try iron-fortified breakfast cereals or oatmeal",
            "Avoid tea, coffee, and calcium supplements within 1 hour of iron-rich meals",
            "Cook in a cast-iron pan — leaches small amounts of iron into food",
        ],
    },

    {
        "condition": "High Hemoglobin (Polycythaemia Risk)",
        "trigger":   lambda m: m.get("hemoglobin", {}).get("status") == "high",
        "recommendations": [
            "Drink 8–10 glasses of water daily to reduce blood viscosity",
            "Reduce red meat and iron-fortified food intake",
            "Increase fruits, green vegetables, and whole grains",
            "Avoid iron supplements unless explicitly prescribed",
            "Limit alcohol — it can further raise haematocrit",
            "Consult a haematologist — persistent high Hb needs medical evaluation",
        ],
    },

    {
        "condition": "Low Vitamin B12 (B12 Deficiency)",
        "trigger":   lambda m: m.get("vitamin_b12", {}).get("status") == "low",
        "recommendations": [
            "Include dairy daily: milk, curd, paneer, cheese (richest vegetarian B12 sources)",
            "Eat eggs regularly — the yolk contains significant B12",
            "If vegetarian or vegan: take a cyanocobalamin supplement (consult doctor for dosage)",
            "Add B12-fortified foods: nutritional yeast, plant-based milks (soy/oat), breakfast cereals",
            "Non-vegetarians: include fish (salmon, tuna, mackerel), shellfish, and lean meat",
            "Avoid excessive alcohol — it impairs B12 absorption",
        ],
    },

    {
        "condition": "High Vitamin B12",
        "trigger":   lambda m: m.get("vitamin_b12", {}).get("status") == "high",
        "recommendations": [
            "Stop or reduce B12 supplements unless advised otherwise by a doctor",
            "Very high B12 (>2000 pg/mL) warrants medical investigation (liver/kidney screening)",
            "Maintain a balanced diet without extra B12-fortified foods in the short term",
            "Re-test in 4–6 weeks after stopping supplementation",
        ],
    },

    {
        "condition": "Overweight BMI",
        "trigger":   lambda m: m.get("bmi", {}).get("status") == "overweight",
        "recommendations": [
            "Target a moderate calorie deficit of 300–400 kcal/day below TDEE",
            "Build half your plate with non-starchy vegetables at every meal",
            "Choose whole grains over refined: brown rice, oats, whole-wheat bread",
            "Increase lean protein to stay satiated: eggs, legumes, fish, low-fat paneer",
            "Limit sugar-sweetened beverages, fried foods, and processed snacks",
            "Aim for 150+ minutes of moderate aerobic activity per week",
            "Practise mindful eating — eat slowly, avoid screens during meals",
        ],
    },

    {
        "condition": "Obese BMI",
        "trigger":   lambda m: m.get("bmi", {}).get("status") == "obese",
        "recommendations": [
            "Work with a registered dietitian to build a structured calorie-deficit plan",
            "Target 500–750 kcal/day deficit (≈0.5–0.75 kg/week loss rate)",
            "Fill 50% of plate with vegetables, 25% lean protein, 25% complex carbs",
            "Eliminate sugary drinks, ultra-processed snacks, and excessive saturated fats",
            "Start with low-impact exercise (walking, swimming) and increase gradually",
            "Track meals with an app (like NutriTrack!) to build awareness",
            "Consider medical evaluation for comorbidities (diabetes, hypertension, lipids)",
        ],
    },

    {
        "condition": "Underweight BMI",
        "trigger":   lambda m: m.get("bmi", {}).get("status") == "underweight",
        "recommendations": [
            "Eat 5–6 smaller meals throughout the day rather than 3 large ones",
            "Add calorie-dense, nutrient-rich foods: nuts, seeds, avocado, full-fat dairy",
            "Include complex carbohydrates: oats, brown rice, sweet potato, whole-wheat bread",
            "Boost protein intake: eggs, legumes, lean meat, tofu, full-fat paneer",
            "Use healthy fats liberally: ghee, olive oil, peanut butter, coconut",
            "Drink nutrient-rich smoothies (banana + milk + peanut butter + oats)",
            "Avoid filling up on low-calorie beverages before meals",
        ],
    },

]


# ── Public API ────────────────────────────────────────────────

def get_diet_recommendations(classified_metrics: dict) -> list:
    """
    Evaluate each condition trigger against the classified metrics.

    Args:
        classified_metrics: Output of medical_nlp.extract_and_classify().

    Returns:
        List of triggered conditions with their recommendations:
        [
          {
            "condition":       "Low Hemoglobin (Anaemia Risk)",
            "recommendations": ["...", "..."],
          },
          ...
        ]
    """
    triggered = []
    for entry in CONDITION_MAP:
        try:
            if entry["trigger"](classified_metrics):
                triggered.append({
                    "condition":       entry["condition"],
                    "recommendations": entry["recommendations"],
                })
                logger.debug("Condition triggered: '%s'", entry["condition"])
        except Exception as exc:
            logger.warning(
                "Error evaluating condition '%s': %s", entry.get("condition", "?"), exc
            )
    logger.info("%d condition(s) triggered out of %d", len(triggered), len(CONDITION_MAP))
    return triggered


def generate_summary(classified_metrics: dict, diet_plan: list) -> str:
    """
    Generate a concise, human-readable summary of the analysis.

    Args:
        classified_metrics: Output of medical_nlp.extract_and_classify().
        diet_plan:          Output of get_diet_recommendations().

    Returns:
        A single-paragraph summary string.
    """
    # Build metric lines
    metric_parts = []
    for metric_name, data in classified_metrics.items():
        label  = metric_name.replace("_", " ").title()
        value  = data.get("value")
        unit   = data.get("unit", "")
        status = data.get("status", "not_found").replace("_", " ")

        if value is None:
            metric_parts.append(f"{label}: not detected")
        else:
            metric_parts.append(f"{label}: {value} {unit} ({status})")

    metric_line = " | ".join(metric_parts) if metric_parts else "No metrics detected"

    # Build advice sentence
    if not diet_plan:
        detected_any = any(
            d.get("value") is not None for d in classified_metrics.values()
        )
        if detected_any:
            advice = (
                "All detected values appear within normal ranges. "
                "Maintain a balanced, varied diet and stay physically active."
            )
        else:
            advice = (
                "No health metrics could be extracted from this report. "
                "Please ensure the report is clearly legible or try re-uploading a higher-quality scan."
            )
    else:
        conditions = [d["condition"] for d in diet_plan]
        advice = (
            f"Report flagged: {', '.join(conditions)}. "
            "Personalised dietary guidance has been generated below. "
            "⚠️ Always consult a registered dietitian or doctor before making significant dietary changes."
        )

    return f"{metric_line}. {advice}"
