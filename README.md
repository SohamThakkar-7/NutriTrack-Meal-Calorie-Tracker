# 🥗 NutriTrack — Full-Stack Setup Guide

A college Software Engineering project: Nutrition & Calorie Tracker.  
**Frontend:** HTML · CSS · Bootstrap 5 · Chart.js  
**Backend:** Node.js · Express · MongoDB (Mongoose)

---

## 📁 Project Folder Structure

```
nutritrack/
│
├── backend/                     ← Node.js + Express server
│   ├── config/
│   │   └── db.js                ← Mongoose connection
│   ├── models/
│   │   └── Meal.js              ← Meal schema & model
│   ├── routes/
│   │   └── meals.js             ← API route handlers
│   ├── .env                     ← Environment variables (you create this)
│   ├── .env.example             ← Template — copy to .env
│   ├── .gitignore
│   ├── package.json
│   └── server.js                ← Express app entry point
│
└── frontend/                    ← Static HTML/CSS/JS files
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── add_meal.html
    ├── reports.html
    ├── about.html
    ├── style.css
    └── script.js                ← Updated: uses fetch() instead of localStorage
```

---

## ⚙️ Prerequisites

| Tool | Version | Install |
|---|---|---|
| Node.js | v18 or later | https://nodejs.org |
| npm | comes with Node | — |
| MongoDB | v6 or later | https://www.mongodb.com/try/download/community |

> **MongoDB Atlas alternative:** You can use a free cloud cluster at  
> https://cloud.mongodb.com instead of installing MongoDB locally.

---

## 🚀 Backend Setup (Step-by-Step)

### Step 1 — Install dependencies

```bash
# Navigate into the backend folder
cd nutritrack/backend

# Install all packages listed in package.json
npm install
```

This installs: `express`, `mongoose`, `cors`, `dotenv`, and `nodemon`.

---

### Step 2 — Create your .env file

```bash
# Copy the example template
cp .env.example .env
```

Open `.env` and confirm these values:

```env
# Local MongoDB (default — works if MongoDB is installed on your machine)
MONGO_URI=mongodb://127.0.0.1:27017/nutritrack

# Port the server listens on
PORT=5000
```

> **Using MongoDB Atlas?**  
> Replace `MONGO_URI` with your Atlas connection string:
> ```
> MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/nutritrack
> ```

---

### Step 3 — Start MongoDB (local only)

If you installed MongoDB locally, make sure it is running:

```bash
# macOS / Linux
mongod

# Windows (run in a separate terminal as Administrator)
"C:\Program Files\MongoDB\Server\6.0\bin\mongod.exe"
```

> If you see `waiting for connections on port 27017`, MongoDB is ready.  
> **Atlas users skip this step** — your cluster is always running.

---

### Step 4 — Start the Express server

```bash
# From the backend/ folder:

# Production start
node server.js

# Development start (auto-restarts on file save — recommended)
npx nodemon server.js
```

You should see:

```
┌─────────────────────────────────────────┐
│   🥗  NutriTrack API Server              │
│   Listening on http://localhost:5000    │
│   Press Ctrl+C to stop                 │
└─────────────────────────────────────────┘

✅  MongoDB connected: 127.0.0.1
📦  Database name   : nutritrack
```

---

### Step 5 — Open the frontend

Open the `frontend/` HTML files in your browser.  
The easiest way is **VS Code Live Server** (right-click `index.html` → *Open with Live Server*),
which serves the files at `http://127.0.0.1:5500`.

> The CORS configuration in `server.js` already allows `http://127.0.0.1:5500`  
> and `http://localhost:5500` out of the box.

---

## 🌐 API Reference

All endpoints are prefixed with `/api`.  
Base URL: `http://localhost:5000/api`

---

### `POST /api/addMeal`

Save a new meal to MongoDB.

**Request body (JSON):**

```json
{
  "foodName": "Oatmeal with Banana",
  "quantity": "1 bowl",
  "mealType": "Breakfast",
  "calories": 320,
  "protein": 8,
  "carbs": 58,
  "fat": 5,
  "date": "18 Mar 2026"
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `foodName` | String | ✅ | Max 200 chars |
| `quantity` | String | ✅ | e.g. "1 bowl", "200g" |
| `mealType` | String | ✅ | Must be: `Breakfast` `Lunch` `Dinner` `Snacks` |
| `calories` | Number | ✅ | Must be ≥ 0 |
| `protein` | Number | ❌ | Defaults to 0 |
| `carbs` | Number | ❌ | Defaults to 0 |
| `fat` | Number | ❌ | Defaults to 0 |
| `date` | String | ❌ | Defaults to today (`"18 Mar 2026"` format) |

**Success response `201`:**
```json
{
  "success": true,
  "message": "Meal saved successfully.",
  "meal": {
    "_id": "661f2a3b4c5d6e7f8a9b0c1d",
    "foodName": "Oatmeal with Banana",
    "quantity": "1 bowl",
    "mealType": "Breakfast",
    "calories": 320,
    "protein": 8,
    "carbs": 58,
    "fat": 5,
    "date": "18 Mar 2026",
    "createdAt": "2026-03-18T07:30:00.000Z",
    "updatedAt": "2026-03-18T07:30:00.000Z"
  }
}
```

**Error response `400`:**
```json
{
  "success": false,
  "message": "foodName, quantity, mealType, and calories are required."
}
```

---

### `GET /api/meals`

Fetch all meals, sorted newest-first.

**Optional query params:**

| Param | Example | Effect |
|---|---|---|
| `mealType` | `?mealType=Breakfast` | Filter by meal type |
| `date` | `?date=18 Mar 2026` | Filter by date string |

**Success response `200`:**
```json
{
  "success": true,
  "count": 2,
  "meals": [
    {
      "_id": "661f2a3b4c5d6e7f8a9b0c1d",
      "foodName": "Dal Rice",
      "quantity": "1 plate",
      "mealType": "Dinner",
      "calories": 520,
      "protein": 18,
      "carbs": 80,
      "fat": 10,
      "date": "18 Mar 2026",
      "createdAt": "2026-03-18T19:00:00.000Z"
    }
  ]
}
```

---

### `GET /api/meals/:id`

Fetch a single meal by its MongoDB `_id`.

**Success response `200`:**
```json
{
  "success": true,
  "meal": { ... }
}
```

**Not found `404`:**
```json
{ "success": false, "message": "Meal not found." }
```

---

### `DELETE /api/meal/:id`

Delete a meal by its MongoDB `_id`.

**Success response `200`:**
```json
{
  "success": true,
  "message": "Meal \"Dal Rice\" deleted successfully.",
  "deletedId": "661f2a3b4c5d6e7f8a9b0c1d"
}
```

---

### `GET /api/health`

Quick ping to confirm the server is up.

```json
{
  "success": true,
  "message": "NutriTrack API is running 🥗",
  "timestamp": "2026-03-18T10:00:00.000Z"
}
```

---

## 🔌 Frontend → API Integration

The updated `script.js` replaces all `localStorage` meal operations with `fetch()` calls.  
The `API_BASE` constant at the top of the file points to the backend:

```js
const API_BASE = 'http://localhost:5000/api';
```

### How each page calls the API

| Page | Operation | API Call |
|---|---|---|
| `add_meal.html` | Save a new meal | `POST /api/addMeal` |
| `dashboard.html` | Load today's meals | `GET /api/meals` |
| `reports.html` | Load all meals, filter, delete | `GET /api/meals`, `DELETE /api/meal/:id` |

### Example fetch snippets

#### Add a meal
```js
const response = await fetch('http://localhost:5000/api/addMeal', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    foodName: 'Grilled Chicken',
    quantity: '200g',
    mealType: 'Lunch',
    calories: 330,
    protein: 48,
    carbs: 0,
    fat: 14,
    date: '18 Mar 2026'
  })
});
const data = await response.json();
console.log(data.meal._id); // MongoDB ObjectId
```

#### Get all meals
```js
const response = await fetch('http://localhost:5000/api/meals');
const data = await response.json();
console.log(data.meals); // array of meal objects
```

#### Delete a meal
```js
const id = '661f2a3b4c5d6e7f8a9b0c1d'; // MongoDB _id
const response = await fetch(`http://localhost:5000/api/meal/${id}`, {
  method: 'DELETE'
});
const data = await response.json();
console.log(data.message); // "Meal "Grilled Chicken" deleted successfully."
```

---

## 🧪 Test the API with curl

```bash
# Health check
curl http://localhost:5000/api/health

# Add a meal
curl -X POST http://localhost:5000/api/addMeal \
  -H "Content-Type: application/json" \
  -d '{"foodName":"Idli","quantity":"3 pieces","mealType":"Breakfast","calories":150}'

# Get all meals
curl http://localhost:5000/api/meals

# Get only Lunch entries
curl "http://localhost:5000/api/meals?mealType=Lunch"

# Delete a meal (replace <ID> with a real _id from GET /meals)
curl -X DELETE http://localhost:5000/api/meal/<ID>
```

---

## 🔧 Common Issues & Fixes

| Problem | Fix |
|---|---|
| `ECONNREFUSED` on port 5000 | The Express server is not running. Run `node server.js`. |
| `MongoServerError: connect ECONNREFUSED 127.0.0.1:27017` | MongoDB is not running. Start it with `mongod`. |
| CORS error in browser console | Ensure `API_BASE` in `script.js` matches the server URL exactly (`http://localhost:5000`). |
| `Cannot find module 'express'` | You forgot `npm install`. Run it from the `backend/` folder. |
| `MONGO_URI is undefined` | `.env` file is missing. Copy `.env.example` → `.env`. |
| Port 5000 already in use | Change `PORT=5001` in `.env` and update `API_BASE` in `script.js`. |

---

## 📝 Notes

- **Auth is still localStorage-based** in this phase. Adding a backend auth layer (JWT + bcrypt) is a natural next step.
- MongoDB automatically creates the `nutritrack` database and `meals` collection the first time a meal is saved — no manual setup needed.
- The `_id` field from MongoDB (a 24-character hex string) replaces the old `Date.now()` numeric IDs used in the localStorage version.
