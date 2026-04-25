# ================================================================
#  NutriTrack — Advanced Backend (Python + Flask + MongoDB)
#  app.py — Main application entry point
#
#  Run:  python app.py
#  API Base: http://localhost:5001/api
# ================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from database import db
from routes.users     import users_bp
from routes.intake    import intake_bp
from routes.dashboard import dashboard_bp
from routes.dietplan  import dietplan_bp
from routes.report    import report_bp       # ← medical report analysis

# ── Create Flask app ──────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

# ── Enable CORS so the frontend can call this API ─────────────
# Origins are loaded from FLASK_ALLOWED_ORIGINS in .env
CORS(app, origins=app.config.get("ALLOWED_ORIGINS", [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:3000",
]))

# ── Register route blueprints ─────────────────────────────────
app.register_blueprint(users_bp,     url_prefix="/api")
app.register_blueprint(intake_bp,    url_prefix="/api")
app.register_blueprint(dashboard_bp, url_prefix="/api")
app.register_blueprint(dietplan_bp,  url_prefix="/api")
app.register_blueprint(report_bp,    url_prefix="/api")  # POST /api/analyze-report

# ── Health check ──────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "message": "NutriTrack Advanced API is running 🥗",
    }), 200

# ── 404 handler ───────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "message": "Route not found."}), 404

# ── 500 handler ───────────────────────────────────────────────
@app.errorhandler(500)
def server_error(e):
    return jsonify({"success": False, "message": "Internal server error."}), 500

# ── Start ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n-----------------------------------------------")
    print("  NutriTrack Advanced API (Flask)")
    print("  Listening on  http://localhost:5001")
    print("  Press  Ctrl+C  to stop")
    print("-----------------------------------------------\n")
    app.run(host="0.0.0.0", port=5001, debug=True)
