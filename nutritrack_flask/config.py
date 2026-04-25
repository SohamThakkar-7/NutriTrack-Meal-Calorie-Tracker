# config.py
# ── Application configuration ─────────────────────────────────
# Reads values from the .env file (via python-dotenv) so that
# secrets are never hardcoded and deployment is just an env swap.

import os
from dotenv import load_dotenv

# Load the .env file located in the same directory as this file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    # MongoDB connection string (Atlas for prod, localhost for dev)
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/nutritrack_advanced")

    # Flask secret key – use a strong random string in production!
    SECRET_KEY = os.getenv("SECRET_KEY", "nutritrack-secret-key-2026")

    # Debug mode – never True in production
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

    # Allowed CORS origins (comma-separated string → list)
    ALLOWED_ORIGINS = [
        o.strip() for o in
        os.getenv("FLASK_ALLOWED_ORIGINS",
                  "http://127.0.0.1:5500,http://localhost:5500,http://localhost:3000,https://nutri-track-meal-calorie-tracker.vercel.app").split(",")
    ]
