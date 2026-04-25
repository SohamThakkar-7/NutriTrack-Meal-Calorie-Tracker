# database.py
# ── MongoDB connection using PyMongo ──────────────────────────
#
# We use a simple module-level client so all route files
# can import the same `db` object without reconnecting.

from pymongo import MongoClient
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)

# Select the database
db = client.get_database()

# ── Collections ───────────────────────────────────────────────
# db.users   → user profiles (name, birthdate, height, weight)
# db.intake  → daily food intake entries

print(f"OK  MongoDB connected: '{db.name}'")
