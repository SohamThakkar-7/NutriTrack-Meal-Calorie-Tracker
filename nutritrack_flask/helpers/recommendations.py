# helpers/recommendations.py
# ================================================================
#  All the "intelligence" of the system lives here:
#
#  1. calculate_age(birthdate_str)     → int
#  2. get_recommendations(age)         → dict
#  3. detect_deficiencies(intake, rec) → list of str
#  4. get_food_suggestions(deficiencies) → dict
# ================================================================

from datetime import date, datetime


# ── 1. Calculate age dynamically from birthdate ───────────────
def calculate_age(birthdate_str):
    """
    Calculate age in years from a birthdate string.

    Accepts formats: "YYYY-MM-DD"
    Returns: int (age in years)

    Example:
        calculate_age("2000-04-18") → 26  (if today is 2026-04-19)
    """
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            f"Invalid birthdate format '{birthdate_str}'. Expected YYYY-MM-DD."
        )

    today = date.today()

    # Count full years — subtract 1 if birthday hasn't occurred yet this year
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    return age


# ── 2. Age-based recommended daily intake ────────────────────
def get_recommendations(age):
    """
    Return recommended daily intake based on age group.

    Age groups:
        Below 18  → children / teenagers
        18 to 40  → young adults
        Above 40  → older adults

    Returns a dict:
        {
            "age_group":  str,
            "calories":   int,   # kcal per day
            "protein":    int,   # grams per day
            "iron":       float, # mg per day
        }
    """
    if age < 18:
        return {
            "age_group": "Below 18 (Children / Teenagers)",
            "calories":  2200,
            "protein":   52,     # g/day
            "iron":      15.0,   # mg/day (higher for growing bodies)
        }
    elif 18 <= age <= 40:
        return {
            "age_group": "18–40 (Young Adults)",
            "calories":  2500,
            "protein":   60,     # g/day
            "iron":      18.0,   # mg/day (higher for women of reproductive age)
        }
    else:  # age > 40
        return {
            "age_group": "Above 40 (Older Adults)",
            "calories":  2000,
            "protein":   65,     # g/day (higher to prevent muscle loss)
            "iron":      8.0,    # mg/day (lower requirement post-menopause)
        }


# ── 3. Deficiency detection ───────────────────────────────────
def detect_deficiencies(intake, recommendations):
    """
    Compare today's intake against recommendations.
    Uses simple if-else thresholds (80 % of recommended = deficient).

    Parameters:
        intake          (dict) → { "calories": int, "protein": float, "iron": float }
        recommendations (dict) → from get_recommendations()

    Returns:
        list of str — e.g. ["Low Calories", "Iron Deficiency"]
    """
    deficiencies = []

    # Threshold: if intake < 80% of recommended → flag as deficient
    THRESHOLD = 0.80

    # ── Calories check ──────────────────────────────────────
    if intake.get("calories", 0) < recommendations["calories"] * THRESHOLD:
        deficiencies.append("Low Calories")

    # ── Protein check ───────────────────────────────────────
    if intake.get("protein", 0) < recommendations["protein"] * THRESHOLD:
        deficiencies.append("Low Protein")

    # ── Iron check ──────────────────────────────────────────
    if intake.get("iron", 0) < recommendations["iron"] * THRESHOLD:
        deficiencies.append("Iron Deficiency")

    return deficiencies


# ── 4. Food suggestions based on deficiencies ────────────────
def get_food_suggestions(deficiencies):
    """
    Map each detected deficiency to a list of suggested foods.

    Parameters:
        deficiencies (list of str)

    Returns:
        dict → { "Low Protein": [...], "Iron Deficiency": [...], ... }
                Returns empty dict {} if no deficiencies.
    """
    # Master suggestion map
    SUGGESTIONS = {
        "Low Calories": [
            "Banana",
            "Rice",
            "Peanut Butter",
            "Whole Wheat Bread",
            "Avocado",
            "Sweet Potato",
            "Nuts & Dry Fruits",
        ],
        "Low Protein": [
            "Eggs",
            "Paneer",
            "Dal (Lentils)",
            "Chicken Breast",
            "Greek Yogurt",
            "Tofu",
            "Soya Chunks",
        ],
        "Iron Deficiency": [
            "Spinach",
            "Dates",
            "Beetroot",
            "Pomegranate",
            "Rajma (Kidney Beans)",
            "Sesame Seeds (Til)",
            "Dark Chocolate",
        ],
    }

    result = {}
    for deficiency in deficiencies:
        if deficiency in SUGGESTIONS:
            result[deficiency] = SUGGESTIONS[deficiency]

    return result
