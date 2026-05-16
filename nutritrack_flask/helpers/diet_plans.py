# helpers/diet_plans.py
# ================================================================
#  Disease + Deficiency based Diet Plan Engine
#
#  get_diet_plan(age, diseases, deficiencies)
#    → Returns a complete personalised diet plan with:
#       - Foods to eat
#       - Foods to avoid
#       - Full day meal plan (Breakfast, Lunch, Dinner, Snacks)
#       - Health tips
# ================================================================


# ── Master disease diet database ─────────────────────────────
DISEASE_PLANS = {

    "Low BP": {
        "description": "Low Blood Pressure (Hypotension) — Blood pressure below 90/60 mmHg.",
        "foods_to_eat": [
            "Salt (in moderation)", "Olives", "Beetroot juice",
            "Pomegranate juice", "Dates", "Raisins",
            "Eggs", "Chicken", "Fish",
            "Whole grains", "Nuts", "Coffee (in moderation)",
        ],
        "foods_to_avoid": [
            "Alcohol", "High-carb foods in large portions",
            "Processed foods", "Large meals (eat smaller frequent meals)",
            "Bananas in excess",
        ],
        "meal_plan": {
            "Breakfast": "2 boiled eggs + 2 whole wheat toast + 1 glass beetroot juice",
            "Mid Morning": "A handful of dates and raisins + 1 cup salted buttermilk",
            "Lunch": "2 rotis + dal + sabzi + 1 cup curd with a pinch of salt",
            "Evening Snack": "Roasted peanuts + 1 cup masala chai",
            "Dinner": "Brown rice + rajma curry + salad with olive oil dressing",
        },
        "tips": [
            "Eat small frequent meals — avoid large gaps between meals",
            "Increase salt and fluid intake",
            "Avoid sitting or standing for long periods",
            "Stay well hydrated — drink 8–10 glasses of water daily",
        ],
    },

    "High BP": {
        "description": "High Blood Pressure (Hypertension) — Blood pressure above 140/90 mmHg.",
        "foods_to_eat": [
            "Banana", "Spinach", "Beetroot", "Oats",
            "Garlic", "Pomegranate", "Watermelon",
            "Low-fat dairy (curd, buttermilk)", "Fish (salmon, mackerel)",
            "Flaxseeds", "Walnuts", "Green tea",
        ],
        "foods_to_avoid": [
            "Salt and salty foods (pickles, papad, namkeen)",
            "Processed and packaged foods", "Red meat",
            "Full-fat dairy", "Alcohol", "Caffeine in excess",
            "Fried foods", "Sugar-sweetened beverages",
        ],
        "meal_plan": {
            "Breakfast": "Oatmeal with banana and flaxseeds + 1 cup green tea",
            "Mid Morning": "1 pomegranate or watermelon slices",
            "Lunch": "2 rotis + palak dal + cucumber raita (no salt) + salad",
            "Evening Snack": "Handful of walnuts + 1 cup low-fat buttermilk",
            "Dinner": "Brown rice + fish curry (less salt) + steamed vegetables",
        },
        "tips": [
            "Reduce sodium intake to less than 2300mg per day",
            "Follow the DASH diet — rich in fruits, vegetables, whole grains",
            "Exercise regularly — 30 minutes of walking daily",
            "Avoid stress and practice meditation",
        ],
    },

    "Diabetes": {
        "description": "Diabetes — High blood sugar levels due to insufficient insulin.",
        "foods_to_eat": [
            "Bitter gourd (karela)", "Fenugreek (methi)",
            "Leafy greens (spinach, methi)", "Whole grains",
            "Legumes (dal, rajma, chana)", "Nuts and seeds",
            "Fish", "Eggs", "Low-fat dairy",
            "Berries", "Guava", "Amla (Indian gooseberry)",
        ],
        "foods_to_avoid": [
            "Sugar and sugary drinks", "White rice in large portions",
            "Maida (refined flour) products", "Potatoes in excess",
            "Fruit juices", "Sweets and desserts",
            "Processed foods", "Alcohol", "Full-fat dairy",
        ],
        "meal_plan": {
            "Breakfast": "Methi paratha (1) + curd + 1 cup green tea (no sugar)",
            "Mid Morning": "1 guava or handful of berries + 5 almonds",
            "Lunch": "2 multigrain rotis + karela sabzi + dal + salad",
            "Evening Snack": "Roasted chana + 1 cup buttermilk (no sugar)",
            "Dinner": "Small portion brown rice + palak paneer + cucumber salad",
        },
        "tips": [
            "Eat at regular intervals — never skip meals",
            "Choose low glycemic index (GI) foods",
            "Monitor blood sugar levels regularly",
            "Exercise daily — even a 30-minute walk helps",
            "Drink karela or methi water on an empty stomach",
        ],
    },

    "Anaemia": {
        "description": "Anaemia — Low haemoglobin / iron deficiency in the blood.",
        "foods_to_eat": [
            "Spinach", "Beetroot", "Pomegranate",
            "Dates", "Raisins", "Jaggery (gud)",
            "Sesame seeds (til)", "Rajma", "Soya beans",
            "Chicken liver", "Red meat", "Eggs",
            "Vitamin C foods (amla, lemon) to help iron absorption",
        ],
        "foods_to_avoid": [
            "Tea and coffee (inhibit iron absorption)",
            "Calcium-rich foods close to iron-rich meals",
            "Alcohol", "Processed foods",
            "Excessive fibre supplements",
        ],
        "meal_plan": {
            "Breakfast": "Poha with peas and lemon juice + 1 glass pomegranate juice",
            "Mid Morning": "Handful of dates and raisins + 1 amla",
            "Lunch": "2 rotis + rajma curry + spinach sabzi + salad with lemon",
            "Evening Snack": "Til (sesame) ladoo or chikki + 1 cup buttermilk",
            "Dinner": "Brown rice + dal + beetroot sabzi + salad",
        },
        "tips": [
            "Have vitamin C with iron-rich foods to improve absorption",
            "Avoid tea/coffee for 1 hour before and after meals",
            "Cook in iron utensils when possible",
            "Include jaggery instead of sugar",
        ],
    },

    "Obesity": {
        "description": "Obesity — Excess body weight with BMI above 30.",
        "foods_to_eat": [
            "Leafy greens (spinach, lettuce, cabbage)",
            "Cucumber", "Tomato", "Lemon water",
            "Oats", "Brown rice", "Whole wheat",
            "Lentils and legumes", "Eggs (boiled)",
            "Low-fat curd", "Green tea", "Chia seeds",
        ],
        "foods_to_avoid": [
            "Fried foods (samosa, pakora, puri)",
            "Sugary foods and drinks", "White bread and maida products",
            "Full-fat dairy", "Alcohol", "Fast food",
            "Processed snacks (chips, namkeen)",
            "Large portions of rice and roti",
        ],
        "meal_plan": {
            "Breakfast": "Oats with skimmed milk + 1 boiled egg + 1 cup green tea",
            "Mid Morning": "1 fruit (apple or guava) + 5 almonds",
            "Lunch": "1–2 rotis + dal + salad (large portion) + curd (low fat)",
            "Evening Snack": "Roasted makhana or cucumber slices + green tea",
            "Dinner": "Vegetable soup + 1 roti + grilled chicken or paneer",
        },
        "tips": [
            "Eat slowly and mindfully — chew food well",
            "Drink 1 glass of water before each meal",
            "Avoid eating after 8 PM",
            "Exercise at least 45 minutes daily",
            "Avoid skipping meals — it leads to overeating later",
        ],
    },

    "Thyroid": {
        "description": "Thyroid disorders — Hypothyroidism (underactive) or Hyperthyroidism (overactive).",
        "foods_to_eat": [
            "Iodine-rich foods (iodised salt, fish, dairy)",
            "Selenium-rich foods (Brazil nuts, sunflower seeds, eggs)",
            "Zinc-rich foods (pumpkin seeds, legumes)",
            "Fruits and vegetables", "Whole grains",
            "Lean proteins (chicken, fish, eggs)",
            "Coconut oil (in moderation)",
        ],
        "foods_to_avoid": [
            "Raw cruciferous vegetables in excess (cabbage, broccoli, cauliflower)",
            "Soy products in excess (tofu, soy milk)",
            "Gluten (for some thyroid patients)", "Alcohol",
            "Processed foods", "Refined sugar",
            "Excessive caffeine",
        ],
        "meal_plan": {
            "Breakfast": "Eggs (2 boiled) + whole wheat toast + 1 glass warm water with lemon",
            "Mid Morning": "1 Brazil nut + handful of pumpkin seeds + 1 fruit",
            "Lunch": "2 rotis + fish curry or dal + cooked vegetables + curd",
            "Evening Snack": "Sunflower seeds + 1 cup herbal tea",
            "Dinner": "Brown rice + lentil soup + steamed vegetables with iodised salt",
        },
        "tips": [
            "Take thyroid medication on an empty stomach",
            "Avoid raw goitrogens (cabbage, broccoli) — cook them instead",
            "Get adequate sleep (7–8 hours)",
            "Exercise regularly to boost metabolism",
            "Get iodine levels checked regularly",
        ],
    },

    "Cholesterol": {
        "description": "High Cholesterol — Elevated LDL cholesterol levels in the blood.",
        "foods_to_eat": [
            "Oats and oat bran", "Flaxseeds", "Walnuts",
            "Almonds", "Olive oil", "Avocado",
            "Fatty fish (salmon, mackerel)", "Garlic",
            "Legumes (rajma, chana, dal)", "Fruits (apple, berries, citrus)",
            "Green vegetables", "Green tea",
        ],
        "foods_to_avoid": [
            "Saturated fats (butter, ghee in excess, red meat)",
            "Trans fats (vanaspati, margarine, fried foods)",
            "Full-fat dairy", "Egg yolks in excess",
            "Processed meats (sausage, bacon)",
            "Refined carbohydrates", "Alcohol",
        ],
        "meal_plan": {
            "Breakfast": "Oatmeal with walnuts and flaxseeds + 1 cup green tea",
            "Mid Morning": "1 apple + 5 almonds",
            "Lunch": "2 rotis + rajma or chana sabzi + salad with olive oil",
            "Evening Snack": "Roasted chana + 1 cup green tea",
            "Dinner": "Grilled fish + brown rice + steamed broccoli and carrots",
        },
        "tips": [
            "Replace saturated fats with healthy fats (olive oil, nuts)",
            "Eat soluble fibre — oats, barley, fruits daily",
            "Exercise 30–45 minutes every day",
            "Quit smoking — it lowers HDL (good) cholesterol",
            "Get cholesterol levels checked every 6 months",
        ],
    },

    "PCOD": {
        "description": "PCOD/PCOS — Polycystic Ovarian Disease affecting hormonal balance.",
        "foods_to_eat": [
            "High-fibre foods (vegetables, whole grains, legumes)",
            "Lean proteins (chicken, fish, eggs, tofu)",
            "Anti-inflammatory foods (turmeric, ginger, berries)",
            "Nuts and seeds (flaxseeds, pumpkin seeds)",
            "Low-GI foods (brown rice, oats, sweet potato)",
            "Spearmint tea", "Cinnamon",
            "Leafy greens (spinach, methi)",
        ],
        "foods_to_avoid": [
            "Refined carbohydrates (maida, white rice, white bread)",
            "Sugar and sugary drinks", "Processed foods",
            "Red and processed meats", "Alcohol",
            "Full-fat dairy in excess", "Soy products in excess",
        ],
        "meal_plan": {
            "Breakfast": "Vegetable oats with flaxseeds + 1 cup spearmint tea",
            "Mid Morning": "1 fruit (berries or guava) + pumpkin seeds",
            "Lunch": "2 multigrain rotis + dal + sabzi + salad with lemon-turmeric dressing",
            "Evening Snack": "Roasted makhana + 1 cup cinnamon tea",
            "Dinner": "Grilled paneer or tofu + brown rice + steamed vegetables",
        },
        "tips": [
            "Maintain a healthy weight — even 5–10% weight loss helps",
            "Exercise regularly — yoga and strength training help most",
            "Manage stress — cortisol worsens PCOD symptoms",
            "Sleep 7–8 hours consistently",
            "Add cinnamon and turmeric to daily diet",
        ],
    },
}


# ── Deficiency-based additions ────────────────────────────────
DEFICIENCY_ADDITIONS = {
    "Low Calories": {
        "extra_foods": ["Banana", "Peanut butter", "Avocado", "Nuts", "Ghee (1 tsp)", "Sweet potato"],
        "tip": "Add calorie-dense healthy foods to each meal.",
        "meal_plan": {
            "Breakfast":     "Banana smoothie with peanut butter + 2 whole wheat toast with ghee",
            "Mid Morning":   "Handful of mixed nuts + 1 avocado",
            "Lunch":         "2 rotis with ghee + dal + sabzi + sweet potato curry",
            "Evening Snack": "Peanut butter on toast + 1 glass whole milk",
            "Dinner":        "Brown rice + rajma curry + salad with olive oil dressing",
        },
        "foods_to_avoid": ["Diet foods", "Low-fat products", "Skipping meals", "Excessive coffee/tea"],
    },
    "Low Protein": {
        "extra_foods": ["Eggs", "Paneer", "Dal", "Chicken", "Greek yogurt", "Soya chunks"],
        "tip": "Include a protein source in every meal.",
        "meal_plan": {
            "Breakfast":     "3 boiled eggs + whole wheat toast + 1 cup milk",
            "Mid Morning":   "Greek yogurt with nuts + 1 fruit",
            "Lunch":         "2 rotis + chana dal + paneer sabzi + curd",
            "Evening Snack": "Soya chunks stir fry + 1 cup buttermilk",
            "Dinner":        "Brown rice + dal tadka + grilled chicken or tofu",
        },
        "foods_to_avoid": ["Empty carbs (white bread, maida)", "Sugary snacks", "Alcohol", "Processed foods"],
    },
    "Iron Deficiency": {
        "extra_foods": ["Spinach", "Dates", "Beetroot", "Rajma", "Sesame seeds", "Pomegranate"],
        "tip": "Pair iron-rich foods with vitamin C (lemon/amla) for better absorption.",
        "meal_plan": {
            "Breakfast":     "Poha with peas and lemon juice + 1 glass pomegranate juice",
            "Mid Morning":   "Handful of dates and raisins + 1 amla",
            "Lunch":         "2 rotis + rajma curry + spinach sabzi + salad with lemon",
            "Evening Snack": "Sesame (til) ladoo + 1 cup buttermilk",
            "Dinner":        "Brown rice + dal + beetroot sabzi + salad",
        },
        "foods_to_avoid": ["Tea and coffee (inhibit iron absorption)", "Calcium-rich foods with iron-rich meals", "Alcohol", "Processed foods"],
    },
}


# ── Main function ─────────────────────────────────────────────
def get_diet_plan(age, diseases, deficiencies):
    """
    Generate a complete personalised diet plan.

    Parameters:
        age          (int)       → user's age
        diseases     (list[str]) → e.g. ["Diabetes", "High BP"]
        deficiencies (list[str]) → e.g. ["Low Protein", "Iron Deficiency"]

    Returns:
        dict with keys:
            age_note, diseases_addressed, deficiencies_addressed,
            combined_foods_to_eat, combined_foods_to_avoid,
            meal_plan, tips, deficiency_additions
    """
    if not diseases and not deficiencies:
        return {
            "message": "No diseases or deficiencies reported. Maintain a balanced diet!",
            "general_tips": [
                "Eat a variety of fruits and vegetables daily",
                "Drink 8–10 glasses of water",
                "Exercise 30 minutes every day",
                "Avoid processed and junk foods",
                "Sleep 7–8 hours per night",
            ]
        }

    # Collect data from all selected diseases
    all_eat   = []
    all_avoid = []
    all_tips  = []
    meal_plan = {}
    diseases_info = []
    deficiency_additions = {}

    for disease in diseases:
        if disease in DISEASE_PLANS:
            plan = DISEASE_PLANS[disease]
            all_eat.extend(plan["foods_to_eat"])
            all_avoid.extend(plan["foods_to_avoid"])
            all_tips.extend(plan["tips"])
            diseases_info.append({
                "name":        disease,
                "description": plan["description"],
            })
            # Use meal plan from first disease as base
            if not meal_plan:
                meal_plan = plan["meal_plan"].copy()

    # Deficiency additions
    for deficiency in deficiencies:
        if deficiency in DEFICIENCY_ADDITIONS:
            d = DEFICIENCY_ADDITIONS[deficiency]
            deficiency_additions[deficiency] = d
            all_eat.extend(d["extra_foods"])
            all_tips.append(d["tip"])
            all_avoid.extend(d.get("foods_to_avoid", []))
            # Use deficiency meal plan if no disease meal plan exists
            if not meal_plan and "meal_plan" in d:
                meal_plan = d["meal_plan"].copy()

    # Age-specific note
    if age < 18:
        age_note = "⚠️ You are under 18. Growing bodies need extra calcium, iron and protein. Consult a doctor before any dietary restrictions."
    elif age > 40:
        age_note = "⚠️ Above 40: Focus on bone health (calcium, vitamin D), heart health, and maintaining muscle mass."
    else:
        age_note = "✅ Age 18–40: Prime time to build healthy habits that last a lifetime."

    # Remove duplicates and conflicts
    # If a food appears in both eat and avoid, keep it in avoid (safety first)
    avoid_set = set(all_avoid)
    eat_clean = list(dict.fromkeys([f for f in all_eat if f not in avoid_set]))
    avoid_clean = list(dict.fromkeys(all_avoid))

    return {
        "age":                   age,
        "age_note":              age_note,
        "diseases_addressed":    diseases_info,
        "deficiencies_addressed": deficiencies,
        "combined_foods_to_eat":  eat_clean[:15],   # top 15
        "combined_foods_to_avoid": avoid_clean[:12], # top 12
        "meal_plan":             meal_plan,
        "tips":                  list(dict.fromkeys(all_tips))[:8],
        "deficiency_additions":  deficiency_additions,
    }
