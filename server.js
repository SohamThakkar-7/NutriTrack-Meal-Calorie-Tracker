// server.js
// ─────────────────────────────────────────────────────────
// NutriTrack – Express + MongoDB backend
// Entry point: starts the HTTP server and connects to MongoDB
//
// Run:  node server.js
// Dev:  npx nodemon server.js   (auto-restarts on file changes)
// ─────────────────────────────────────────────────────────

// ── Load environment variables from .env ──────────────────
require('dotenv').config();

const express    = require('express');
const cors       = require('cors');
const connectDB  = require('./config/db');
const mealRoutes = require('./routes/meals');

const app  = express();
const PORT = process.env.PORT || 5000;

// ── Connect to MongoDB ────────────────────────────────────
connectDB();

// ── Global Middleware ─────────────────────────────────────

// CORS – allowed origins are read from ALLOWED_ORIGINS env var
// (comma-separated list) so we can configure production origins
// without touching code.  Falls back to common local dev origins.
const allowedOrigins = process.env.ALLOWED_ORIGINS
  ? process.env.ALLOWED_ORIGINS.split(',').map(o => o.trim())
  : [
      'http://127.0.0.1:5500',
      'http://localhost:5500',
      'http://localhost:3000',
      'http://127.0.0.1:3000',
      'http://localhost:5173',
    ];

app.use(cors({
  origin: allowedOrigins,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  credentials: true,
}));

// Parse incoming JSON request bodies
app.use(express.json());

// Parse URL-encoded form data (useful if HTML forms post directly)
app.use(express.urlencoded({ extended: true }));

// ── Request logger (development helper) ───────────────────
app.use((req, _res, next) => {
  const ts = new Date().toISOString().slice(11, 19); // HH:MM:SS
  console.log(`[${ts}] ${req.method} ${req.originalUrl}`);
  next();
});

// ── API Routes ────────────────────────────────────────────
// All meal endpoints are prefixed with /api
app.use('/api', mealRoutes);

// ── Health-check endpoint ─────────────────────────────────
// GET /api/health  →  quick ping to confirm the server is up
app.get('/api/health', (_req, res) => {
  res.status(200).json({
    success: true,
    message: 'NutriTrack API is running 🥗',
    timestamp: new Date().toISOString(),
  });
});

// ── Food Search Proxy ─────────────────────────────────────
// GET /api/searchfood?q=banana
// Proxies the request to Open Food Facts so the browser
// never hits the external API directly (avoids CORS errors).
app.get('/api/searchfood', async (req, res) => {
  const query = req.query.q;
  if (!query || query.trim().length < 2) {
    return res.status(400).json({ success: false, message: 'Query parameter "q" is required (min 2 chars).' });
  }

  try {
    // Use dynamic import for node-fetch (ESM) or the built-in fetch (Node 18+)
    const fetchFn = globalThis.fetch
      ? globalThis.fetch.bind(globalThis)
      : (await import('node-fetch')).default;

    const url =
      `https://world.openfoodfacts.org/cgi/search.pl` +
      `?search_terms=${encodeURIComponent(query.trim())}` +
      `&search_simple=1&action=process&json=1&page_size=10` +
      `&fields=product_name,serving_size,nutriments`;

    const response = await fetchFn(url, {
      headers: { 'User-Agent': 'NutriTrack-App/1.0 (college project)' },
      signal: AbortSignal.timeout(8000),   // 8-second timeout
    });

    if (!response.ok) throw new Error(`Open Food Facts responded with ${response.status}`);

    const data = await response.json();

    // Normalise the results into the same shape as the local DB
    const foods = (data.products || [])
      .filter(p => p.product_name && p.nutriments)
      .map(p => {
        const n = p.nutriments;
        return {
          name:     p.product_name,
          serving:  p.serving_size || '100g',
          calories: Math.round(n['energy-kcal_serving'] || n['energy-kcal_100g'] || 0),
          protein:  Math.round(n['proteins_serving']     || n['proteins_100g']    || 0),
          carbs:    Math.round(n['carbohydrates_serving']|| n['carbohydrates_100g']|| 0),
          fat:      Math.round(n['fat_serving']          || n['fat_100g']          || 0),
        };
      })
      .filter(f => f.calories > 0)
      .slice(0, 8);

    return res.status(200).json({ success: true, count: foods.length, foods });

  } catch (err) {
    console.error('Food search proxy error:', err.message);
    return res.status(502).json({
      success: false,
      message: 'Could not reach Open Food Facts: ' + err.message,
    });
  }
});

// ── 404 handler – catches any unmatched route ─────────────
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Route ${req.method} ${req.originalUrl} not found.`,
  });
});

// ── Global error handler ──────────────────────────────────
// Catches any error passed via next(err) from route handlers
app.use((err, _req, res, _next) => {
  console.error('Unhandled error:', err.stack || err.message);
  res.status(err.status || 500).json({
    success: false,
    message: err.message || 'An unexpected server error occurred.',
  });
});

// ── Start server ──────────────────────────────────────────
app.listen(PORT, () => {
  console.log('');
  console.log('┌─────────────────────────────────────────┐');
  console.log('│   🥗  NutriTrack API Server              │');
  console.log(`│   Listening on http://localhost:${PORT}    │`);
  console.log('│   Press Ctrl+C to stop                  │');
  console.log('└─────────────────────────────────────────┘');
  console.log('');
});