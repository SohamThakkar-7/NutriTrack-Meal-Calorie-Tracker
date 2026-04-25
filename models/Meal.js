// models/Meal.js
// ─────────────────────────────────────────────────────────
// Mongoose schema for a single meal entry.
// Every document saved via POST /api/addMeal conforms
// to this shape before being stored in MongoDB.
// ─────────────────────────────────────────────────────────

const mongoose = require('mongoose');

const mealSchema = new mongoose.Schema(
  {
    // ── Core fields (required) ──────────────────────────
    foodName: {
      type:     String,
      required: [true, 'Food name is required'],
      trim:     true,
      maxlength: [200, 'Food name must be 200 characters or fewer'],
    },

    quantity: {
      type:     String,
      required: [true, 'Quantity is required'],
      trim:     true,
      maxlength: [100, 'Quantity must be 100 characters or fewer'],
    },

    mealType: {
      type:     String,
      required: [true, 'Meal type is required'],
      enum: {
        values:  ['Breakfast', 'Lunch', 'Dinner', 'Snacks'],
        message: 'Meal type must be Breakfast, Lunch, Dinner, or Snacks',
      },
    },

    calories: {
      type:    Number,
      required: [true, 'Calorie count is required'],
      min:     [0, 'Calories cannot be negative'],
    },

    // ── Optional macro-nutrient fields ─────────────────
    protein: {
      type:    Number,
      default: 0,
      min:     [0, 'Protein cannot be negative'],
    },

    carbs: {
      type:    Number,
      default: 0,
      min:     [0, 'Carbs cannot be negative'],
    },

    fat: {
      type:    Number,
      default: 0,
      min:     [0, 'Fat cannot be negative'],
    },

    // ── Date stored as a display-formatted string ───────
    // e.g. "18 Mar 2026"
    // This matches the format the frontend already uses so
    // no extra parsing is needed on the client side.
    date: {
      type:    String,
      default: () =>
        new Date().toLocaleDateString('en-IN', {
          day:   '2-digit',
          month: 'short',
          year:  'numeric',
        }),
    },
  },
  {
    // Automatically adds createdAt and updatedAt timestamps
    timestamps: true,
  }
);

// Index on mealType and date so Reports-page queries are fast
mealSchema.index({ mealType: 1 });
mealSchema.index({ date: 1 });

module.exports = mongoose.model('Meal', mealSchema);
