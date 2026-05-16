// config/db.js
// ─────────────────────────────────────────────────────────
// Establishes and exports the Mongoose connection.
// Called once at server startup; all models share this
// connection automatically.
// ─────────────────────────────────────────────────────────

const mongoose = require('mongoose');

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.MONGO_URI, {
      // These options silence deprecation warnings in Mongoose 7/8
      // (they are the defaults in Mongoose 8 but kept here for clarity)
    });

    console.log(`✅  MongoDB connected: ${conn.connection.host}`);
    console.log(`📦  Database name   : ${conn.connection.name}`);
  } catch (error) {
    console.error('❌  MongoDB connection failed:', error.message);
    // Exit the process so the server doesn't start in a broken state
    process.exit(1);
  }
};

module.exports = connectDB;
