# routes/users.py
# ================================================================
#  User routes
#
#  POST /api/register   → Register a new user profile
#  GET  /api/user/<id>  → Get a user profile by ID
#  GET  /api/users      → List all users (dev/testing helper)
# ================================================================

from flask import Blueprint, request, jsonify
from bson  import ObjectId
from datetime import datetime
from database import db
from helpers.recommendations import calculate_age

users_bp = Blueprint("users", __name__)


# ── POST /api/register ────────────────────────────────────────
@users_bp.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user with profile details.

    Request body (JSON):
    {
        "name":      "Priya Sharma",
        "email":     "priya@example.com",
        "birthdate": "2000-04-18",       ← YYYY-MM-DD format
        "height":    165,                ← cm
        "weight":    58                  ← kg
    }

    Response 201:
    {
        "success": true,
        "message": "User registered successfully.",
        "user": { ...profile with calculated age... }
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Request body must be JSON."}), 400

    # ── Required field validation ──────────────────────────
    required = ["name", "email", "birthdate", "height", "weight"]
    missing  = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({
            "success": False,
            "message": f"Missing required fields: {', '.join(missing)}"
        }), 400

    # ── Validate birthdate and calculate age ───────────────
    try:
        age = calculate_age(data["birthdate"])
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    if age < 0 or age > 120:
        return jsonify({"success": False, "message": "Invalid birthdate — age out of range."}), 400

    # ── Check for duplicate email ──────────────────────────
    existing = db.users.find_one({"email": data["email"].strip().lower()})
    if existing:
        return jsonify({"success": False, "message": "Email already registered."}), 409

    # ── Build user document ────────────────────────────────
    user = {
        "name":       data["name"].strip(),
        "email":      data["email"].strip().lower(),
        "birthdate":  data["birthdate"],          # stored as string YYYY-MM-DD
        "height":     float(data["height"]),      # cm
        "weight":     float(data["weight"]),      # kg
        "created_at": datetime.utcnow().isoformat(),
    }

    result   = db.users.insert_one(user)
    user_id  = str(result.inserted_id)

    # Return profile with calculated age (not stored)
    response = {**user, "id": user_id, "age": age}
    response.pop("_id", None)

    return jsonify({
        "success": True,
        "message": "User registered successfully.",
        "user":    response,
    }), 201


# ── GET /api/user/<id> ────────────────────────────────────────
@users_bp.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    """
    Fetch a user profile by MongoDB ObjectId.
    Age is calculated dynamically from birthdate on every request.
    """
    try:
        oid = ObjectId(user_id)
    except Exception:
        return jsonify({"success": False, "message": "Invalid user ID format."}), 400

    user = db.users.find_one({"_id": oid})
    if not user:
        return jsonify({"success": False, "message": "User not found."}), 404

    age = calculate_age(user["birthdate"])

    profile = {
        "id":        str(user["_id"]),
        "name":      user["name"],
        "email":     user["email"],
        "birthdate": user["birthdate"],
        "age":       age,              # ← always computed fresh
        "height":    user.get("height"),
        "weight":    user.get("weight"),
        "created_at":user.get("created_at"),
    }

    return jsonify({"success": True, "user": profile}), 200


# ── GET /api/users ────────────────────────────────────────────
@users_bp.route("/users", methods=["GET"])
def list_users():
    """List all registered users (useful for testing)."""
    users = []
    for u in db.users.find():
        users.append({
            "id":        str(u["_id"]),
            "name":      u["name"],
            "email":     u["email"],
            "birthdate": u["birthdate"],
            "age":       calculate_age(u["birthdate"]),
            "height":    u.get("height"),
            "weight":    u.get("weight"),
        })
    return jsonify({"success": True, "count": len(users), "users": users}), 200
