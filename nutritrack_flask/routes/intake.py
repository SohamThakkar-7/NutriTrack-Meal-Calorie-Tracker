# routes/intake.py
# ================================================================
#  Food Intake routes
#
#  POST /api/intake              → Add a food intake entry
#  GET  /api/intake/<user_id>    → Get all intake for a user
#  GET  /api/intake/<user_id>/today → Get today's intake only
#  DELETE /api/intake/<entry_id> → Delete an intake entry
# ================================================================

from flask import Blueprint, request, jsonify
from bson  import ObjectId
from datetime import datetime, date
from database import db

intake_bp = Blueprint("intake", __name__)


# ── Helper: today's date string ────────────────────────────────
def today_str():
    return date.today().strftime("%Y-%m-%d")


# ── POST /api/intake ──────────────────────────────────────────
@intake_bp.route("/intake", methods=["POST"])
def add_intake():
    """
    Add a food intake entry for a user.

    Request body (JSON):
    {
        "user_id":   "661f2a3b4c5d6e7f8a9b0c1d",
        "food_name": "Boiled Egg",
        "quantity":  "2 eggs",
        "calories":  156,
        "protein":   12.4,
        "iron":      1.8
    }

    Response 201:
    {
        "success": true,
        "message": "Food intake recorded.",
        "entry":   { ...saved document... }
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    # ── Required field validation ──────────────────────────
    required = ["user_id", "food_name", "calories"]
    missing  = [f for f in required if data.get(f) is None]
    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing required fields: {', '.join(missing)}"
        }), 400

    # ── Validate user exists ───────────────────────────────
    try:
        user_oid = ObjectId(data["user_id"])
    except Exception:
        return jsonify({"success": False, "message": "Invalid user_id format."}), 400

    user = db.users.find_one({"_id": user_oid})
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    # ── Build intake document ──────────────────────────────
    entry = {
        "user_id":   data["user_id"],
        "food_name": data["food_name"].strip(),
        "quantity":  data.get("quantity", "").strip(),
        "calories":  float(data.get("calories", 0)),
        "protein":   float(data.get("protein",  0)),   # grams
        "iron":      float(data.get("iron",     0)),   # mg
        "date":      today_str(),                      # YYYY-MM-DD
        "logged_at": datetime.utcnow().isoformat(),
    }

    result   = db.intake.insert_one(entry)
    entry_id = str(result.inserted_id)

    response = {**entry, "id": entry_id}
    response.pop("_id", None)

    return jsonify({
        "success": True,
        "message": "Food intake recorded.",
        "entry":   response,
    }), 201


# ── GET /api/intake/<user_id> ─────────────────────────────────
@intake_bp.route("/intake/<user_id>", methods=["GET"])
def get_all_intake(user_id):
    """
    Fetch all food intake entries for a user.
    Optional query param: ?date=YYYY-MM-DD to filter by date.
    """
    filter_date = request.args.get("date")
    query = {"user_id": user_id}
    if filter_date:
        query["date"] = filter_date

    entries = []
    for e in db.intake.find(query).sort("logged_at", -1):
        entries.append({
            "id":        str(e["_id"]),
            "food_name": e["food_name"],
            "quantity":  e.get("quantity", ""),
            "calories":  e.get("calories", 0),
            "protein":   e.get("protein",  0),
            "iron":      e.get("iron",     0),
            "date":      e.get("date",     ""),
            "logged_at": e.get("logged_at",""),
        })

    return jsonify({"success": True, "count": len(entries), "entries": entries}), 200


# ── GET /api/intake/<user_id>/today ──────────────────────────
@intake_bp.route("/intake/<user_id>/today", methods=["GET"])
def get_today_intake(user_id):
    """Fetch only today's food intake entries for a user."""
    entries = []
    for e in db.intake.find({"user_id": user_id, "date": today_str()}):
        entries.append({
            "id":        str(e["_id"]),
            "food_name": e["food_name"],
            "quantity":  e.get("quantity", ""),
            "calories":  e.get("calories", 0),
            "protein":   e.get("protein",  0),
            "iron":      e.get("iron",     0),
            "logged_at": e.get("logged_at",""),
        })

    # Compute totals
    totals = {
        "calories": round(sum(e["calories"] for e in entries), 2),
        "protein":  round(sum(e["protein"]  for e in entries), 2),
        "iron":     round(sum(e["iron"]     for e in entries), 2),
    }

    return jsonify({
        "success":  True,
        "date":     today_str(),
        "count":    len(entries),
        "entries":  entries,
        "totals":   totals,
    }), 200


# ── DELETE /api/intake/<entry_id> ─────────────────────────────
@intake_bp.route("/intake/entry/<entry_id>", methods=["DELETE"])
def delete_intake(entry_id):
    """Delete a specific food intake entry by its ID."""
    try:
        oid = ObjectId(entry_id)
    except Exception:
        return jsonify({"success": False, "message": "Invalid entry ID."}), 400

    entry = db.intake.find_one({"_id": oid})
    if not entry:
        return jsonify({"success": False, "message": "Entry not found."}), 404

    db.intake.delete_one({"_id": oid})
    return jsonify({
        "success": True,
        "message": f"Entry '{entry['food_name']}' deleted successfully.",
    }), 200
