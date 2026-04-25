// routes/meals.js
// ─────────────────────────────────────────────────────────
// Express router that handles all /api/* meal endpoints.
//
// Routes:
//   POST   /api/addMeal        → create & save a new meal
//   GET    /api/meals          → fetch all meals (newest first)
//   GET    /api/meals/:id      → fetch a single meal by ID
//   DELETE /api/meal/:id       → delete a meal by ID
//
// Each handler validates input, queries MongoDB via the
// Meal model, and returns clean JSON responses.
// ─────────────────────────────────────────────────────────

const express = require('express');
const router  = express.Router();
const Meal    = require('../models/Meal');

// ──────────────────────────────────────────────────────────
// POST /api/addMeal
// Body: { foodName, quantity, mealType, calories,
//         protein?, carbs?, fat?, date? }
// Returns: 201 + the saved meal document
// ──────────────────────────────────────────────────────────
router.post('/addMeal', async (req, res) => {
  try {
    const { foodName, quantity, mealType, calories, protein, carbs, fat, date } = req.body;

    // ── Manual required-field check (Mongoose also validates,
    //    but we want a clean 400 before hitting the DB) ──
    if (!foodName || !quantity || !mealType || calories === undefined) {
      return res.status(400).json({
        success: false,
        message: 'foodName, quantity, mealType, and calories are required.',
      });
    }

    const meal = new Meal({
      foodName: foodName.trim(),
      quantity: quantity.trim(),
      mealType,
      calories: Number(calories),
      protein:  Number(protein)  || 0,
      carbs:    Number(carbs)    || 0,
      fat:      Number(fat)      || 0,
      // If the frontend supplies a pre-formatted date string, use it;
      // otherwise the schema default (today) is applied automatically.
      ...(date && { date }),
    });

    const savedMeal = await meal.save();

    return res.status(201).json({
      success: true,
      message: 'Meal saved successfully.',
      meal:    savedMeal,
    });
  } catch (error) {
    // Mongoose validation errors have a specific shape
    if (error.name === 'ValidationError') {
      const messages = Object.values(error.errors).map(e => e.message);
      return res.status(400).json({ success: false, message: messages.join(' | ') });
    }
    console.error('POST /api/addMeal error:', error);
    return res.status(500).json({ success: false, message: 'Server error. Please try again.' });
  }
});

// ──────────────────────────────────────────────────────────
// GET /api/meals
// Optional query params:
//   ?mealType=Breakfast|Lunch|Dinner|Snacks  (filter)
//   ?date=18 Mar 2026                        (filter by date string)
// Returns: 200 + array of meals sorted newest-first
// ──────────────────────────────────────────────────────────
router.get('/meals', async (req, res) => {
  try {
    const filter = {};

    // Apply optional filters coming from the Reports page dropdown
    if (req.query.mealType && req.query.mealType !== 'all') {
      filter.mealType = req.query.mealType;
    }
    if (req.query.date) {
      filter.date = req.query.date;
    }

    const meals = await Meal.find(filter).sort({ createdAt: -1 });

    return res.status(200).json({
      success: true,
      count:   meals.length,
      meals,
    });
  } catch (error) {
    console.error('GET /api/meals error:', error);
    return res.status(500).json({ success: false, message: 'Server error. Please try again.' });
  }
});

// ──────────────────────────────────────────────────────────
// GET /api/meals/:id
// Returns: 200 + a single meal document
// ──────────────────────────────────────────────────────────
router.get('/meals/:id', async (req, res) => {
  try {
    const meal = await Meal.findById(req.params.id);

    if (!meal) {
      return res.status(404).json({ success: false, message: 'Meal not found.' });
    }

    return res.status(200).json({ success: true, meal });
  } catch (error) {
    // CastError = invalid ObjectId format
    if (error.name === 'CastError') {
      return res.status(400).json({ success: false, message: 'Invalid meal ID format.' });
    }
    console.error('GET /api/meals/:id error:', error);
    return res.status(500).json({ success: false, message: 'Server error. Please try again.' });
  }
});

// ──────────────────────────────────────────────────────────
// DELETE /api/meal/:id
// Returns: 200 + confirmation message
// ──────────────────────────────────────────────────────────
router.delete('/meal/:id', async (req, res) => {
  try {
    const meal = await Meal.findByIdAndDelete(req.params.id);

    if (!meal) {
      return res.status(404).json({ success: false, message: 'Meal not found.' });
    }

    return res.status(200).json({
      success: true,
      message: `Meal "${meal.foodName}" deleted successfully.`,
      deletedId: meal._id,
    });
  } catch (error) {
    if (error.name === 'CastError') {
      return res.status(400).json({ success: false, message: 'Invalid meal ID format.' });
    }
    console.error('DELETE /api/meal/:id error:', error);
    return res.status(500).json({ success: false, message: 'Server error. Please try again.' });
  }
});

// ──────────────────────────────────────────────────────────
// PUT /api/meal/:id
// Body: any subset of { foodName, quantity, mealType,
//                       calories, protein, carbs, fat }
// Returns: 200 + the updated meal document
// ──────────────────────────────────────────────────────────
router.put('/meal/:id', async (req, res) => {
  try {
    const allowed = ['foodName', 'quantity', 'mealType', 'calories', 'protein', 'carbs', 'fat'];
    const update  = {};

    allowed.forEach(key => {
      if (req.body[key] !== undefined) {
        update[key] = (key === 'foodName' || key === 'quantity')
          ? String(req.body[key]).trim()
          : (key === 'mealType' ? req.body[key] : Number(req.body[key]));
      }
    });

    if (Object.keys(update).length === 0) {
      return res.status(400).json({ success: false, message: 'No valid fields provided to update.' });
    }

    const meal = await Meal.findByIdAndUpdate(
      req.params.id,
      { $set: update },
      { new: true, runValidators: true }
    );

    if (!meal) {
      return res.status(404).json({ success: false, message: 'Meal not found.' });
    }

    return res.status(200).json({
      success: true,
      message: `Meal "${meal.foodName}" updated successfully.`,
      meal,
    });
  } catch (error) {
    if (error.name === 'CastError') {
      return res.status(400).json({ success: false, message: 'Invalid meal ID format.' });
    }
    if (error.name === 'ValidationError') {
      const messages = Object.values(error.errors).map(e => e.message);
      return res.status(400).json({ success: false, message: messages.join(' | ') });
    }
    console.error('PUT /api/meal/:id error:', error);
    return res.status(500).json({ success: false, message: 'Server error. Please try again.' });
  }
});

module.exports = router;
