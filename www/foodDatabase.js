/* ================================================================
   NUTRITRACK — LOCAL FOOD DATABASE
   100+ Indian & common foods with nutrition per standard serving.
   Fields: name, serving, calories, protein(g), carbs(g), fat(g)
   Used by the food search auto-fill on the Add Meal page.
   ================================================================ */

const FOOD_DATABASE = [

  // ── Indian Staples ───────────────────────────────────────────
  { name: "Dal Rice",            serving: "1 plate (300g)",  calories: 520, protein: 18, carbs: 80, fat: 10 },
  { name: "Roti / Chapati",      serving: "1 piece (40g)",   calories: 70,  protein: 3,  carbs: 13, fat: 1  },
  { name: "Paratha",             serving: "1 piece (80g)",   calories: 200, protein: 4,  carbs: 28, fat: 8  },
  { name: "Aloo Paratha",        serving: "1 piece (120g)",  calories: 260, protein: 5,  carbs: 38, fat: 10 },
  { name: "Naan",                serving: "1 piece (90g)",   calories: 260, protein: 8,  carbs: 45, fat: 5  },
  { name: "Puri",                serving: "2 pieces (60g)",  calories: 200, protein: 4,  carbs: 26, fat: 9  },
  { name: "Steamed Rice",        serving: "1 cup (200g)",    calories: 260, protein: 5,  carbs: 57, fat: 1  },
  { name: "Jeera Rice",          serving: "1 plate (250g)",  calories: 340, protein: 6,  carbs: 60, fat: 8  },
  { name: "Biryani (Veg)",       serving: "1 plate (300g)",  calories: 450, protein: 10, carbs: 72, fat: 14 },
  { name: "Biryani (Chicken)",   serving: "1 plate (350g)",  calories: 550, protein: 30, carbs: 65, fat: 18 },
  { name: "Pulao",               serving: "1 plate (250g)",  calories: 380, protein: 8,  carbs: 65, fat: 10 },

  // ── Indian Dals & Curries ────────────────────────────────────
  { name: "Toor Dal",            serving: "1 bowl (150g)",   calories: 150, protein: 9,  carbs: 22, fat: 3  },
  { name: "Moong Dal",           serving: "1 bowl (150g)",   calories: 130, protein: 8,  carbs: 20, fat: 2  },
  { name: "Chana Dal",           serving: "1 bowl (150g)",   calories: 160, protein: 10, carbs: 24, fat: 3  },
  { name: "Rajma",               serving: "1 bowl (200g)",   calories: 220, protein: 13, carbs: 35, fat: 3  },
  { name: "Chole / Chana Masala",serving: "1 bowl (200g)",   calories: 270, protein: 14, carbs: 40, fat: 7  },
  { name: "Palak Paneer",        serving: "1 bowl (200g)",   calories: 280, protein: 14, carbs: 12, fat: 20 },
  { name: "Paneer Butter Masala",serving: "1 bowl (200g)",   calories: 380, protein: 16, carbs: 18, fat: 28 },
  { name: "Butter Chicken",      serving: "1 bowl (250g)",   calories: 400, protein: 30, carbs: 15, fat: 25 },
  { name: "Chicken Curry",       serving: "1 bowl (250g)",   calories: 350, protein: 32, carbs: 10, fat: 20 },
  { name: "Fish Curry",          serving: "1 bowl (250g)",   calories: 280, protein: 28, carbs: 8,  fat: 15 },
  { name: "Egg Curry",           serving: "2 eggs + gravy",  calories: 220, protein: 16, carbs: 8,  fat: 14 },
  { name: "Aloo Gobi",           serving: "1 bowl (200g)",   calories: 180, protein: 5,  carbs: 28, fat: 7  },
  { name: "Mixed Veg Sabzi",     serving: "1 bowl (200g)",   calories: 160, protein: 5,  carbs: 22, fat: 6  },
  { name: "Baingan Bharta",      serving: "1 bowl (180g)",   calories: 140, protein: 4,  carbs: 18, fat: 6  },
  { name: "Sambar",              serving: "1 bowl (200g)",   calories: 120, protein: 6,  carbs: 18, fat: 3  },

  // ── South Indian ─────────────────────────────────────────────
  { name: "Idli",                serving: "2 pieces (100g)", calories: 150, protein: 5,  carbs: 30, fat: 1  },
  { name: "Dosa (Plain)",        serving: "1 large (100g)",  calories: 170, protein: 4,  carbs: 32, fat: 3  },
  { name: "Masala Dosa",         serving: "1 piece (200g)",  calories: 300, protein: 7,  carbs: 50, fat: 8  },
  { name: "Uttapam",             serving: "1 piece (120g)",  calories: 200, protein: 5,  carbs: 36, fat: 4  },
  { name: "Upma",                serving: "1 bowl (200g)",   calories: 250, protein: 6,  carbs: 42, fat: 7  },
  { name: "Pongal",              serving: "1 bowl (200g)",   calories: 280, protein: 8,  carbs: 46, fat: 8  },
  { name: "Coconut Chutney",     serving: "2 tbsp (30g)",    calories: 60,  protein: 1,  carbs: 3,  fat: 5  },
  { name: "Rasam",               serving: "1 bowl (200ml)",  calories: 60,  protein: 2,  carbs: 10, fat: 1  },

  // ── North Indian Snacks & Street Food ────────────────────────
  { name: "Samosa",              serving: "1 piece (100g)",  calories: 260, protein: 5,  carbs: 32, fat: 13 },
  { name: "Kachori",             serving: "1 piece (80g)",   calories: 230, protein: 5,  carbs: 28, fat: 12 },
  { name: "Poha",                serving: "1 bowl (200g)",   calories: 250, protein: 5,  carbs: 42, fat: 7  },
  { name: "Aloo Tikki",          serving: "2 pieces (100g)", calories: 200, protein: 4,  carbs: 30, fat: 8  },
  { name: "Pav Bhaji",           serving: "1 plate (300g)",  calories: 450, protein: 10, carbs: 68, fat: 15 },
  { name: "Vada Pav",            serving: "1 piece (150g)",  calories: 300, protein: 7,  carbs: 44, fat: 10 },
  { name: "Bhel Puri",           serving: "1 plate (150g)",  calories: 200, protein: 5,  carbs: 38, fat: 4  },
  { name: "Pani Puri",           serving: "6 pieces (120g)", calories: 180, protein: 4,  carbs: 34, fat: 4  },
  { name: "Dhokla",              serving: "4 pieces (120g)", calories: 200, protein: 8,  carbs: 32, fat: 4  },
  { name: "Medu Vada",           serving: "2 pieces (100g)", calories: 220, protein: 7,  carbs: 26, fat: 10 },
  { name: "Pakora (Veg)",        serving: "5 pieces (100g)", calories: 250, protein: 6,  carbs: 28, fat: 13 },

  // ── Breakfast Items ───────────────────────────────────────────
  { name: "Oatmeal",             serving: "1 bowl (250ml)",  calories: 160, protein: 6,  carbs: 28, fat: 3  },
  { name: "Oatmeal with Banana", serving: "1 bowl (300g)",   calories: 250, protein: 7,  carbs: 46, fat: 4  },
  { name: "Cornflakes with Milk",serving: "1 bowl (250ml)",  calories: 200, protein: 7,  carbs: 38, fat: 3  },
  { name: "Muesli with Milk",    serving: "1 bowl (250ml)",  calories: 300, protein: 10, carbs: 50, fat: 7  },
  { name: "Bread Toast",         serving: "2 slices (60g)",  calories: 160, protein: 5,  carbs: 28, fat: 3  },
  { name: "Bread Butter Toast",  serving: "2 slices (70g)",  calories: 220, protein: 5,  carbs: 28, fat: 10 },
  { name: "Scrambled Eggs",      serving: "2 eggs (120g)",   calories: 200, protein: 14, carbs: 2,  fat: 15 },
  { name: "Boiled Egg",          serving: "1 egg (50g)",     calories: 78,  protein: 6,  carbs: 1,  fat: 5  },
  { name: "Omelette (2 egg)",    serving: "1 serving (120g)",calories: 190, protein: 14, carbs: 2,  fat: 14 },
  { name: "Poached Egg",         serving: "1 egg (50g)",     calories: 72,  protein: 6,  carbs: 0,  fat: 5  },

  // ── Dairy & Beverages ─────────────────────────────────────────
  { name: "Whole Milk",          serving: "1 glass (250ml)", calories: 150, protein: 8,  carbs: 12, fat: 8  },
  { name: "Toned Milk",          serving: "1 glass (250ml)", calories: 120, protein: 8,  carbs: 12, fat: 4  },
  { name: "Curd / Dahi",         serving: "1 bowl (200g)",   calories: 120, protein: 8,  carbs: 10, fat: 4  },
  { name: "Greek Yogurt",        serving: "200g",            calories: 130, protein: 15, carbs: 8,  fat: 3  },
  { name: "Lassi (Sweet)",       serving: "1 glass (300ml)", calories: 230, protein: 8,  carbs: 38, fat: 5  },
  { name: "Lassi (Salted)",      serving: "1 glass (300ml)", calories: 150, protein: 8,  carbs: 18, fat: 5  },
  { name: "Chai with Milk",      serving: "1 cup (200ml)",   calories: 80,  protein: 3,  carbs: 10, fat: 3  },
  { name: "Masala Chai",         serving: "1 cup (200ml)",   calories: 90,  protein: 3,  carbs: 12, fat: 3  },
  { name: "Black Coffee",        serving: "1 cup (240ml)",   calories: 5,   protein: 0,  carbs: 0,  fat: 0  },
  { name: "Coffee with Milk",    serving: "1 cup (240ml)",   calories: 60,  protein: 3,  carbs: 8,  fat: 2  },
  { name: "Paneer",              serving: "100g",            calories: 260, protein: 18, carbs: 4,  fat: 20 },
  { name: "Butter",              serving: "1 tbsp (14g)",    calories: 100, protein: 0,  carbs: 0,  fat: 11 },
  { name: "Ghee",                serving: "1 tsp (5g)",      calories: 45,  protein: 0,  carbs: 0,  fat: 5  },

  // ── Fruits ────────────────────────────────────────────────────
  { name: "Banana",              serving: "1 medium (120g)", calories: 105, protein: 1,  carbs: 27, fat: 0  },
  { name: "Apple",               serving: "1 medium (182g)", calories: 95,  protein: 0,  carbs: 25, fat: 0  },
  { name: "Mango",               serving: "1 cup (165g)",    calories: 100, protein: 1,  carbs: 25, fat: 1  },
  { name: "Orange",              serving: "1 medium (130g)", calories: 62,  protein: 1,  carbs: 15, fat: 0  },
  { name: "Grapes",              serving: "1 cup (150g)",    calories: 104, protein: 1,  carbs: 27, fat: 0  },
  { name: "Watermelon",          serving: "2 cups (280g)",   calories: 85,  protein: 2,  carbs: 21, fat: 0  },
  { name: "Papaya",              serving: "1 cup (140g)",    calories: 55,  protein: 1,  carbs: 14, fat: 0  },
  { name: "Guava",               serving: "1 medium (100g)", calories: 68,  protein: 3,  carbs: 14, fat: 1  },

  // ── Vegetables (cooked) ───────────────────────────────────────
  { name: "Boiled Potato",       serving: "1 medium (150g)", calories: 130, protein: 3,  carbs: 30, fat: 0  },
  { name: "Sweet Potato",        serving: "1 medium (130g)", calories: 112, protein: 2,  carbs: 26, fat: 0  },
  { name: "Boiled Corn",         serving: "1 cob (90g)",     calories: 90,  protein: 3,  carbs: 19, fat: 1  },

  // ── Proteins & Non-Veg ────────────────────────────────────────
  { name: "Grilled Chicken",     serving: "100g",            calories: 165, protein: 31, carbs: 0,  fat: 4  },
  { name: "Chicken Breast",      serving: "100g",            calories: 165, protein: 31, carbs: 0,  fat: 4  },
  { name: "Chicken Leg",         serving: "1 piece (100g)",  calories: 200, protein: 26, carbs: 0,  fat: 10 },
  { name: "Tandoori Chicken",    serving: "2 pieces (200g)", calories: 300, protein: 38, carbs: 6,  fat: 14 },
  { name: "Mutton Curry",        serving: "1 bowl (250g)",   calories: 380, protein: 28, carbs: 8,  fat: 26 },
  { name: "Fish (Rohu, grilled)",serving: "100g",            calories: 120, protein: 20, carbs: 0,  fat: 4  },
  { name: "Prawns (cooked)",     serving: "100g",            calories: 99,  protein: 24, carbs: 0,  fat: 1  },
  { name: "Tuna (canned)",       serving: "100g",            calories: 116, protein: 26, carbs: 0,  fat: 1  },

  // ── Nuts & Seeds ──────────────────────────────────────────────
  { name: "Almonds",             serving: "10 pieces (14g)", calories: 82,  protein: 3,  carbs: 3,  fat: 7  },
  { name: "Cashews",             serving: "10 pieces (16g)", calories: 90,  protein: 3,  carbs: 5,  fat: 7  },
  { name: "Peanuts",             serving: "1 handful (28g)", calories: 161, protein: 7,  carbs: 5,  fat: 14 },
  { name: "Walnuts",             serving: "5 halves (15g)",  calories: 98,  protein: 2,  carbs: 2,  fat: 10 },
  { name: "Peanut Butter",       serving: "2 tbsp (32g)",    calories: 190, protein: 8,  carbs: 6,  fat: 16 },

  // ── Sweets & Desserts ─────────────────────────────────────────
  { name: "Gulab Jamun",         serving: "2 pieces (80g)",  calories: 260, protein: 4,  carbs: 44, fat: 8  },
  { name: "Rasgulla",            serving: "2 pieces (100g)", calories: 186, protein: 5,  carbs: 36, fat: 2  },
  { name: "Kheer",               serving: "1 bowl (150g)",   calories: 220, protein: 6,  carbs: 36, fat: 6  },
  { name: "Halwa",               serving: "1 bowl (150g)",   calories: 350, protein: 4,  carbs: 52, fat: 14 },
  { name: "Ladoo (Besan)",       serving: "1 piece (50g)",   calories: 220, protein: 4,  carbs: 28, fat: 10 },
  { name: "Jalebi",              serving: "2 pieces (60g)",  calories: 200, protein: 2,  carbs: 44, fat: 3  },
  { name: "Ice Cream (Vanilla)", serving: "1 scoop (100g)",  calories: 207, protein: 3,  carbs: 24, fat: 11 },

  // ── Fast Food & Western ───────────────────────────────────────
  { name: "Burger (Veg)",        serving: "1 piece (180g)",  calories: 380, protein: 10, carbs: 52, fat: 15 },
  { name: "Burger (Chicken)",    serving: "1 piece (200g)",  calories: 450, protein: 24, carbs: 48, fat: 20 },
  { name: "Pizza (1 slice)",     serving: "1 slice (107g)",  calories: 285, protein: 12, carbs: 36, fat: 10 },
  { name: "French Fries",        serving: "1 medium (117g)", calories: 365, protein: 4,  carbs: 48, fat: 17 },
  { name: "Sandwich (Veg)",      serving: "1 piece (150g)",  calories: 280, protein: 9,  carbs: 40, fat: 9  },
  { name: "Grilled Cheese Sandwich", serving: "1 piece (140g)", calories: 380, protein: 14, carbs: 38, fat: 20 },
  { name: "Pasta (cooked)",      serving: "1 cup (200g)",    calories: 220, protein: 8,  carbs: 43, fat: 2  },
  { name: "Maggi Noodles",       serving: "1 pack (80g dry)",calories: 350, protein: 7,  carbs: 50, fat: 14 },

  // ── Salads & Light Meals ──────────────────────────────────────
  { name: "Green Salad",         serving: "1 bowl (150g)",   calories: 50,  protein: 3,  carbs: 8,  fat: 1  },
  { name: "Grilled Chicken Salad", serving: "1 plate (300g)",calories: 280, protein: 36, carbs: 12, fat: 10 },
  { name: "Fruit Salad",         serving: "1 bowl (200g)",   calories: 120, protein: 2,  carbs: 30, fat: 1  },
  { name: "Sprouts Salad",       serving: "1 bowl (150g)",   calories: 120, protein: 9,  carbs: 18, fat: 1  },
  { name: "Raita",               serving: "1 bowl (150g)",   calories: 80,  protein: 4,  carbs: 8,  fat: 3  },
];
