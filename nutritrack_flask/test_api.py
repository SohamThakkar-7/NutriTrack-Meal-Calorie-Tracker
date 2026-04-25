# test_api.py
# ================================================================
#  Quick test script — run AFTER starting the Flask server.
#
#  Usage:
#      python test_api.py
#
#  It will:
#    1. Register a test user
#    2. Add 3 food intake entries
#    3. Fetch the smart dashboard
#    4. Print all results clearly
# ================================================================

import requests
import json

BASE = "http://localhost:5001/api"

def sep(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)

def pretty(data):
    print(json.dumps(data, indent=2))


# ── 1. Health check ───────────────────────────────────────────
sep("1. Health Check")
r = requests.get(f"{BASE}/health")
pretty(r.json())


# ── 2. Register a user ────────────────────────────────────────
sep("2. Register User")
user_payload = {
    "name":      "Priya Sharma",
    "email":     "priya@nutritrack.app",
    "birthdate": "2000-04-18",      # age will be calculated automatically
    "height":    165,               # cm
    "weight":    58,                # kg
}
r = requests.post(f"{BASE}/register", json=user_payload)
data = r.json()
pretty(data)

if not data.get("success"):
    print("\n⚠️  Registration failed (email may already exist). Fetching existing user...")
    r2 = requests.get(f"{BASE}/users")
    users = r2.json().get("users", [])
    if users:
        user_id = users[0]["id"]
        print(f"Using existing user ID: {user_id}")
    else:
        print("No users found. Exiting.")
        exit()
else:
    user_id = data["user"]["id"]
    print(f"\n✅ User ID: {user_id}  |  Age: {data['user']['age']} years")


# ── 3. Add food intake entries ────────────────────────────────
sep("3. Add Food Intake")

foods = [
    {"food_name": "Oatmeal with Banana", "quantity": "1 bowl",  "calories": 320, "protein": 8,  "iron": 2.5},
    {"food_name": "Boiled Eggs",         "quantity": "2 eggs",  "calories": 156, "protein": 12, "iron": 1.8},
    {"food_name": "Dal Rice",            "quantity": "1 plate", "calories": 520, "protein": 18, "iron": 3.2},
]

for food in foods:
    payload = {**food, "user_id": user_id}
    r = requests.post(f"{BASE}/intake", json=payload)
    result = r.json()
    status = "✅" if result.get("success") else "❌"
    print(f"{status} Logged: {food['food_name']} — {food['calories']} kcal")


# ── 4. Get today's intake ─────────────────────────────────────
sep("4. Today's Intake")
r = requests.get(f"{BASE}/intake/{user_id}/today")
data = r.json()
print(f"  Entries today: {data['count']}")
print(f"  Totals: {data['totals']}")


# ── 5. Get smart dashboard ────────────────────────────────────
sep("5. Smart Dashboard")
r = requests.get(f"{BASE}/dashboard/{user_id}")
data = r.json()

if data.get("success"):
    d = data["dashboard"]
    print(f"\n👤 User       : {d['user']['name']} | Age: {d['user']['age']} years")
    print(f"📊 Age Group  : {d['recommendations']['age_group']}")
    print(f"\n📋 Recommended Daily Intake:")
    rec = d["recommendations"]
    print(f"   Calories : {rec['calories']} kcal")
    print(f"   Protein  : {rec['protein']} g")
    print(f"   Iron     : {rec['iron']} mg")

    print(f"\n🍽️  Today's Intake:")
    tot = d["today_intake"]["totals"]
    print(f"   Calories : {tot['calories']} kcal")
    print(f"   Protein  : {tot['protein']} g")
    print(f"   Iron     : {tot['iron']} mg")

    print(f"\n📈 Progress Toward Goals:")
    prog = d["progress"]
    print(f"   Calories : {prog['calories_pct']}%")
    print(f"   Protein  : {prog['protein_pct']}%")
    print(f"   Iron     : {prog['iron_pct']}%")

    print(f"\n⚠️  Deficiencies Detected: {d['deficiencies'] or 'None — great job!'}")

    if d["food_suggestions"]:
        print(f"\n🥗 Food Suggestions:")
        for deficiency, foods in d["food_suggestions"].items():
            print(f"   {deficiency}: {', '.join(foods)}")

    print(f"\n💬 Status: {d['status_message']}")
else:
    pretty(data)

print("\n" + "="*55)
print("  ✅  All tests completed!")
print("="*55 + "\n")
