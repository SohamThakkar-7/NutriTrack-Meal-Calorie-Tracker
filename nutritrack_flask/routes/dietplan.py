# routes/dietplan.py
# ================================================================
#  Diet Plan route
#
#  POST /api/dietplan
#  Body: { age, diseases: [], deficiencies: [] }
#  Returns: personalised diet plan
# ================================================================

from flask import Blueprint, request, jsonify
from helpers.diet_plans import get_diet_plan

dietplan_bp = Blueprint("dietplan", __name__)

VALID_DISEASES = [
    "Low BP", "High BP", "Diabetes",
    "Anaemia", "Obesity", "Thyroid",
    "Cholesterol", "PCOD"
]

VALID_DEFICIENCIES = ["Low Calories", "Low Protein", "Iron Deficiency"]


@dietplan_bp.route("/dietplan", methods=["POST"])
def diet_plan():
    """
    Generate a personalised diet plan.

    Request body:
    {
        "age":          26,
        "diseases":     ["Diabetes", "Anaemia"],
        "deficiencies": ["Low Protein"]
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    # Validate age
    try:
        age = int(data.get("age", 0))
        if age <= 0 or age > 120:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Valid age is required."}), 400

    # Validate diseases
    diseases = data.get("diseases", [])
    if not isinstance(diseases, list):
        diseases = []
    diseases = [d for d in diseases if d in VALID_DISEASES]

    # Validate deficiencies
    deficiencies = data.get("deficiencies", [])
    if not isinstance(deficiencies, list):
        deficiencies = []
    deficiencies = [d for d in deficiencies if d in VALID_DEFICIENCIES]

    # Generate plan
    plan = get_diet_plan(age, diseases, deficiencies)

    return jsonify({
        "success": True,
        "plan":    plan,
    }), 200
