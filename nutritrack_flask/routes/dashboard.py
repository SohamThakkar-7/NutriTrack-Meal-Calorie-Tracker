# routes/dashboard.py
# ================================================================
#  Dashboard route — the brain of the system
#
#  GET /api/dashboard/<user_id>
#
#  Returns everything the frontend needs in one call:
#    • User profile + dynamically calculated age
#    • Age-based recommended daily intake
#    • Today's actual intake (summed from db.intake)
#    • Detected deficiencies (if any)
#    • Food suggestions based on deficiencies
#    • A short personalised message
# ================================================================

from flask import Blueprint, jsonify
from bson  import ObjectId
from database import db
from datetime import date
from helpers.recommendations import (
    calculate_age,
    get_recommendations,
    detect_deficiencies,
    get_food_suggestions,
)

dashboard_bp = Blueprint("dashboard", __name__)


def today_str():
    return date.today().strftime("%Y-%m-%d")


# ── GET /api/dashboard/<user_id> ──────────────────────────────
@dashboard_bp.route("/dashboard/<user_id>", methods=["GET"])
def get_dashboard(user_id):
    """
    Master dashboard endpoint.
    Aggregates user profile, today's intake, recommendations,
    deficiency detection and food suggestions into one response.

    Response 200:
    {
      "success": true,
      "dashboard": {
        "user": {
          "id":        "...",
          "name":      "Priya Sharma",
          "age":       26,
          "height":    165,
          "weight":    58
        },
        "recommendations": {
          "age_group": "18-40 (Young Adults)",
          "calories":  2500,
          "protein":   60,
          "iron":      18.0
        },
        "today_intake": {
          "date":     "2026-04-19",
          "calories": 1200,
          "protein":  30,
          "iron":     6.0,
          "entries": [ ... ]
        },
        "deficiencies":      ["Low Calories", "Iron Deficiency"],
        "food_suggestions":  {
          "Low Calories":     ["Banana", "Rice", ...],
          "Iron Deficiency":  ["Spinach", "Dates", ...]
        },
        "status_message": "⚠️ You have 2 deficiency/ies today. Check the suggestions below!"
      }
    }
    """

    # ── 1. Fetch user ──────────────────────────────────────
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"success": False, "message": "Invalid user ID format."}), 400

    user = db.users.find_one({"_id": oid})
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # ── 2. Calculate age dynamically ───────────────────────
    try:
        age = calculate_age(user["birthdate"])
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    # ── 3. Get age-based recommendations ──────────────────
    recommendations = get_recommendations(age)

    # ── 4. Fetch today's intake entries ───────────────────
    today_entries = list(
        db.intake.find({"user_id": user_id, "date": today_str()})
    )

    # Sum up the nutrients
    today_totals = {
        "calories": round(sum(float(e.get("calories", 0)) for e in today_entries), 2),
        "protein":  round(sum(float(e.get("protein",  0)) for e in today_entries), 2),
        "iron":     round(sum(float(e.get("iron",     0)) for e in today_entries), 2),
    }

    # Serialise entries (remove _id, convert ObjectId to str)
    serialised_entries = []
    for e in today_entries:
        serialised_entries.append({
            "id":        str(e["_id"]),
            "food_name": e["food_name"],
            "quantity":  e.get("quantity", ""),
            "calories":  e.get("calories", 0),
            "protein":   e.get("protein",  0),
            "iron":      e.get("iron",     0),
            "logged_at": e.get("logged_at",""),
        })

    # ── 5. Detect deficiencies ─────────────────────────────
    deficiencies = detect_deficiencies(today_totals, recommendations)

    # ── 6. Get food suggestions ────────────────────────────
    food_suggestions = get_food_suggestions(deficiencies)

    # ── 7. Build a personalised status message ─────────────
    if not today_entries:
        status_message = "📋 No food logged today yet. Start adding your meals!"
    elif not deficiencies:
        status_message = "✅ Great job! You have met all your nutritional goals for today."
    elif len(deficiencies) == 1:
        status_message = f"⚠️ You have 1 deficiency today: {deficiencies[0]}. Check the suggestions below!"
    else:
        status_message = (
            f"⚠️ You have {len(deficiencies)} deficiencies today: "
            f"{', '.join(deficiencies)}. Check the suggestions below!"
        )

    # ── 8. Calculate percentage of goals met ───────────────
    def pct(actual, goal):
        if goal == 0:
            return 0
        return min(round((actual / goal) * 100, 1), 100)

    progress = {
        "calories_pct": pct(today_totals["calories"], recommendations["calories"]),
        "protein_pct":  pct(today_totals["protein"],  recommendations["protein"]),
        "iron_pct":     pct(today_totals["iron"],     recommendations["iron"]),
    }

    # ── 9. Compose final dashboard response ────────────────
    dashboard = {
        "user": {
            "id":        str(user["_id"]),
            "name":      user["name"],
            "email":     user.get("email", ""),
            "birthdate": user["birthdate"],
            "age":       age,
            "height":    user.get("height"),
            "weight":    user.get("weight"),
        },
        "recommendations": recommendations,
        "today_intake": {
            "date":    today_str(),
            "totals":  today_totals,
            "entries": serialised_entries,
            "count":   len(serialised_entries),
        },
        "progress":        progress,
        "deficiencies":    deficiencies,
        "food_suggestions": food_suggestions,
        "status_message":  status_message,
    }

    return jsonify({"success": True, "dashboard": dashboard}), 200
