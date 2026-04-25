/* ================================================================
   NUTRITRACK — new_script.js
   Rename this file to script.js and replace the old one.
   ================================================================ */

/* ── API base URL ──
   In production, set window.__NUTRITRACK_API__ in your HTML
   before this script loads, e.g.:
     <script>window.__NUTRITRACK_API__ = 'https://nutritrack-api.onrender.com/api';</script>
   Locally, it falls back to the Express dev server.
*/
const isProduction = window.location.hostname !== '127.0.0.1' && window.location.hostname !== 'localhost';

const API_BASE = (typeof window !== 'undefined' && window.__NUTRITRACK_API__)
  ? window.__NUTRITRACK_API__
  : isProduction
    ? `${window.location.origin}/api`
    : 'http://127.0.0.1:5000/api';

const FLASK_API_BASE = (typeof window !== 'undefined' && window.__NUTRITRACK_FLASK_API__)
  ? window.__NUTRITRACK_FLASK_API__
  : isProduction
    ? 'https://sohamthakkar-07-nutritrack-ai.hf.space/api'
    : 'http://127.0.0.1:5001/api';

/* ── API layer — all meal data goes to MongoDB via Express ── */
const API = {
  async getMeals(filter) {
    const url = (!filter || filter === 'all')
      ? `${API_BASE}/meals`
      : `${API_BASE}/meals?mealType=${encodeURIComponent(filter)}`;
    const res  = await fetch(url);
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to fetch meals');
    return data.meals;
  },
  async addMeal(meal) {
    const res  = await fetch(`${API_BASE}/addMeal`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(meal),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to save meal');
    return data.meal;
  },
  async deleteMeal(id) {
    const res  = await fetch(`${API_BASE}/meal/${id}`, { method: 'DELETE' });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to delete meal');
    return data;
  },
  async updateMeal(id, updates) {
    const res  = await fetch(`${API_BASE}/meal/${id}`, {
      method:  'PUT',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(updates),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Failed to update meal');
    return data.meal;
  },
  async searchFood(query) {
    const res  = await fetch(`${API_BASE}/searchfood?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Search failed');
    return data.foods || [];
  },
  async analyzeReport(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const res = await fetch(`${FLASK_API_BASE}/analyze-report`, {
      method: 'POST',
      body: formData, // fetch will automatically set Content-Type to multipart/form-data with the correct boundary
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message || 'Report analysis failed');
    return data;
  }
};


/* ── Auth layer — localStorage only (no backend auth yet) ── */
const Auth = {
  getUser()       { return JSON.parse(localStorage.getItem('nct_user')       || 'null'); },
  setUser(u)      { localStorage.setItem('nct_user', JSON.stringify(u)); },
  getRegistered() { return JSON.parse(localStorage.getItem('nct_registered') || '[]'); },
  registerUser(u) {
    const all = this.getRegistered();
    all.push(u);
    localStorage.setItem('nct_registered', JSON.stringify(all));
  },
};

/* Ensure demo account exists */
(function () {
  if (Auth.getRegistered().length === 0) {
    Auth.registerUser({ name: 'Demo User', email: 'demo@nutri.app', password: 'demo123' });
  }
})();

/* ================================================================
   UTILITIES
   ================================================================ */
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function showToast(msg, type = 'success') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.style.cssText =
      'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  const bg = type === 'success' ? 'var(--green-main)' : 'var(--danger)';
  toast.style.cssText =
    `background:${bg};color:#fff;padding:.75rem 1.25rem;border-radius:10px;` +
    `font-family:var(--font-body);font-size:.9rem;font-weight:500;` +
    `box-shadow:0 8px 24px rgba(0,0,0,.2);transform:translateX(120%);` +
    `transition:transform .35s cubic-bezier(.4,0,.2,1);max-width:300px;`;
  toast.textContent = msg;
  container.appendChild(toast);
  requestAnimationFrame(() => { toast.style.transform = 'translateX(0)'; });
  setTimeout(() => {
    toast.style.transform = 'translateX(120%)';
    setTimeout(() => toast.remove(), 400);
  }, 3000);
}

const Validate = {
  required(v) { return v.trim().length > 0; },
  email(v)    { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()); },
  minLen(v,n) { return v.trim().length >= n; },
  match(a,b)  { return a === b; },
  positive(v) { return parseFloat(v) > 0; },
};

function showError(el, msg) {
  el.classList.add('is-invalid');
  let fb = el.nextElementSibling;
  if (!fb || !fb.classList.contains('invalid-feedback')) {
    fb = document.createElement('div');
    fb.className = 'invalid-feedback';
    el.parentNode.insertBefore(fb, el.nextSibling);
  }
  fb.textContent = msg;
}
function clearError(el) {
  el.classList.remove('is-invalid');
  const fb = el.nextElementSibling;
  if (fb && fb.classList.contains('invalid-feedback')) fb.textContent = '';
}
function clearAllErrors(form) {
  form.querySelectorAll('.is-invalid').forEach(el => clearError(el));
}
document.querySelectorAll('.form-control, .form-select').forEach(el => {
  el.addEventListener('input', () => clearError(el));
});

/* ── Navbar scroll shadow ── */
window.addEventListener('scroll', () => {
  document.querySelector('.navbar')?.classList.toggle('scrolled', window.scrollY > 20);
});

/* ── Active nav link ── */
(function () {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === page ||
       (page === '' && link.getAttribute('href') === 'index.html')) {
      link.classList.add('active');
    }
  });
})();

/* ================================================================
   REGISTER PAGE
   ================================================================ */
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', function (e) {
    e.preventDefault();
    clearAllErrors(this);
    const name    = document.getElementById('regName');
    const email   = document.getElementById('regEmail');
    const pass    = document.getElementById('regPassword');
    const confirm = document.getElementById('regConfirm');
    let valid = true;

    if (!Validate.required(name.value))             { showError(name,    'Full name is required.');                  valid = false; }
    if (!Validate.email(email.value))                { showError(email,   'Please enter a valid email address.');     valid = false; }
    if (!Validate.minLen(pass.value, 6))             { showError(pass,    'Password must be at least 6 characters.'); valid = false; }
    if (!Validate.match(pass.value, confirm.value))  { showError(confirm, 'Passwords do not match.');                 valid = false; }

    const existing = Auth.getRegistered().find(u => u.email === email.value.trim().toLowerCase());
    if (existing) { showError(email, 'This email is already registered.'); valid = false; }
    if (!valid) return;

    const user = { name: name.value.trim(), email: email.value.trim().toLowerCase(), password: pass.value };
    Auth.registerUser(user);
    Auth.setUser(user);
    showToast('Account created! Redirecting…', 'success');
    setTimeout(() => { window.location.href = 'dashboard.html'; }, 1400);
  });
}

/* ================================================================
   LOGIN PAGE
   ================================================================ */
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    clearAllErrors(this);
    const email = document.getElementById('loginEmail');
    const pass  = document.getElementById('loginPassword');
    let valid = true;

    if (!Validate.email(email.value))    { showError(email, 'Enter a valid email.'); valid = false; }
    if (!Validate.required(pass.value))  { showError(pass,  'Password is required.'); valid = false; }
    if (!valid) return;

    const found     = Auth.getRegistered().find(
      u => u.email === email.value.trim().toLowerCase() && u.password === pass.value
    );
    const defaultOk = email.value.trim().toLowerCase() === 'demo@nutri.app' && pass.value === 'demo123';

    if (!found && !defaultOk) {
      showError(pass,  'Invalid email or password.');
      showError(email, ' ');
      return;
    }
    const user = found || { name: 'Demo User', email: 'demo@nutri.app' };
    Auth.setUser(user);
    showToast('Welcome back, ' + user.name.split(' ')[0] + '!', 'success');
    setTimeout(() => { window.location.href = 'dashboard.html'; }, 1200);
  });
}

/* ================================================================
   DASHBOARD PAGE
   ================================================================ */
(function initDashboard() {
  if (!document.getElementById('dashboardPage')) return;

  const user     = Auth.getUser();
  const userName = user ? user.name.split(' ')[0] : 'there';
  const wlcEl    = document.getElementById('welcomeName');
  if (wlcEl) wlcEl.textContent = userName;

  const today = new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
  const safe  = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };

  safe('totalCalories', '…');
  safe('totalProtein',  '…');
  safe('totalCarbs',    '…');
  safe('totalFat',      '…');

  API.getMeals('all')
    .then(allMeals => {
      const todayMeals = allMeals.filter(m => m.date === today);

      const totals = { calories: 0, protein: 0, carbs: 0, fat: 0 };
      todayMeals.forEach(m => {
        totals.calories += Number(m.calories) || 0;
        totals.protein  += Number(m.protein)  || 0;
        totals.carbs    += Number(m.carbs)    || 0;
        totals.fat      += Number(m.fat)      || 0;
      });

      safe('totalCalories', totals.calories);
      safe('totalProtein',  totals.protein + 'g');
      safe('totalCarbs',    totals.carbs   + 'g');
      safe('totalFat',      totals.fat     + 'g');

      /* Calorie progress bar */
      const goal = 2000;
      const pct  = Math.min(Math.round((totals.calories / goal) * 100), 100);
      const pb   = document.getElementById('calorieProgress');
      if (pb) { pb.style.width = pct + '%'; pb.setAttribute('aria-valuenow', pct); }
      const pbl  = document.getElementById('calorieProgressLabel');
      if (pbl) pbl.textContent = `${totals.calories} / ${goal} kcal (${pct}%)`;

      /* Macro bars */
      [
        { id: 'proteinBar', val: totals.protein, max: 150 },
        { id: 'carbsBar',   val: totals.carbs,   max: 250 },
        { id: 'fatBar',     val: totals.fat,      max: 70  },
      ].forEach(({ id, val, max }) => {
        const el = document.getElementById(id);
        if (el) el.style.width = Math.min(Math.round((val / max) * 100), 100) + '%';
      });

      /* Weekly Chart.js bar chart */
      const ctx = document.getElementById('weeklyChart');
      if (ctx && window.Chart) {
        const dayLabels  = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const dayIdx     = (new Date().getDay() + 6) % 7;
        const weekTotals = Array(7).fill(0);
        allMeals.forEach(m => {
          if (!m.createdAt) return;
          const diff = Math.floor((Date.now() - new Date(m.createdAt).getTime()) / 86400000);
          if (diff >= 0 && diff < 7) weekTotals[(dayIdx - diff + 7) % 7] += Number(m.calories) || 0;
        });
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: dayLabels,
            datasets: [{
              label: 'Calories (kcal)',
              data:  weekTotals,
              backgroundColor: dayLabels.map((_, i) => i === dayIdx ? '#40916c' : 'rgba(64,145,108,0.2)'),
              borderRadius: 8,
              borderSkipped: false,
            }],
          },
          options: {
            responsive: true,
            plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => c.parsed.y + ' kcal' } } },
            scales: {
              y: { beginAtZero: true, grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { family: 'DM Sans' } } },
              x: { grid: { display: false },                               ticks: { font: { family: 'DM Sans' } } },
            },
          },
        });
      }

      /* Recent meals list */
      const listEl = document.getElementById('recentMealsList');
      if (listEl) {
        if (todayMeals.length === 0) {
          listEl.innerHTML =
            `<p class="text-center py-3" style="color:var(--text-light);font-size:.9rem;">
               No meals logged today. <a href="add_meal.html">Add your first meal →</a>
             </p>`;
        } else {
          listEl.innerHTML = todayMeals.slice(0, 5).map(m => `
            <div class="recent-meal-item">
              <div>
                <strong style="font-size:.9rem;">${escHtml(m.foodName)}</strong>
                <div style="font-size:.78rem;color:var(--text-light);">
                  ${escHtml(m.quantity)} · <span class="meal-badge">${escHtml(m.mealType)}</span>
                </div>
              </div>
              <span class="meal-kcal">${m.calories} kcal</span>
            </div>
          `).join('');
        }
      }
    })
    .catch(err => {
      console.error('Dashboard load error:', err.message);
      showToast('Could not load data. Is the server running?', 'error');
      safe('totalCalories', 0); safe('totalProtein', '0g');
      safe('totalCarbs', '0g'); safe('totalFat', '0g');
    });
})();

/* ================================================================
   ADD MEAL PAGE — FOOD SEARCH + AUTO-FILL
   ================================================================ */
(function initAddMealPage() {
  if (!document.getElementById('addMealForm')) return;

  const searchInput   = document.getElementById('foodSearch');
  const dropdown      = document.getElementById('foodDropdown');
  const searchBtn     = document.getElementById('searchBtn');
  const searchStatus  = document.getElementById('searchStatus');
  const preview       = document.getElementById('nutritionPreview');
  const fieldFoodName = document.getElementById('foodName');
  const fieldQuantity = document.getElementById('quantity');
  const fieldCalories = document.getElementById('calories');
  const fieldProtein  = document.getElementById('protein');
  const fieldCarbs    = document.getElementById('carbs');
  const fieldFat      = document.getElementById('fat');

  function flashField(el) {
    el.classList.add('autofilled');
    setTimeout(() => el.classList.remove('autofilled'), 1800);
  }

  function fillFields(food) {
    fieldFoodName.value = food.name     || '';
    fieldQuantity.value = food.serving  || '';
    fieldCalories.value = food.calories || 0;
    fieldProtein.value  = food.protein  || 0;
    fieldCarbs.value    = food.carbs    || 0;
    fieldFat.value      = food.fat      || 0;
    [fieldFoodName, fieldCalories, fieldProtein, fieldCarbs, fieldFat].forEach(flashField);
    if (preview) {
      document.getElementById('previewFoodName').textContent =
        food.name + (food.serving ? ' · ' + food.serving : '');
      document.getElementById('previewCalories').textContent = food.calories || 0;
      document.getElementById('previewProtein').textContent  = (food.protein || 0) + 'g';
      document.getElementById('previewCarbs').textContent    = (food.carbs   || 0) + 'g';
      document.getElementById('previewFat').textContent      = (food.fat     || 0) + 'g';
      preview.style.display = 'block';
    }
  }

  function setStatus(msg, color) {
    if (searchStatus) {
      searchStatus.textContent = msg;
      searchStatus.style.color = color || 'var(--text-light)';
    }
  }

  function closeDropdown() {
    if (dropdown) { dropdown.innerHTML = ''; dropdown.classList.remove('open'); }
  }

  function makeRow(food, badgeType) {
    const item = document.createElement('div');
    item.className = 'dropdown-item-food';
    item.innerHTML = `
      <div style="min-width:0;">
        <div class="food-item-name">${escHtml(food.name)}</div>
        <div class="food-item-meta">${escHtml(food.serving || '')}
          <span class="source-badge ${badgeType}" style="margin-left:.3rem;">
            ${badgeType === 'local' ? '🇮🇳 Local' : '🌐 Online'}
          </span>
        </div>
      </div>
      <div class="food-item-kcal">${food.calories} kcal</div>`;
    item.addEventListener('mousedown', e => {
      e.preventDefault();
      fillFields(food);
      closeDropdown();
      if (searchInput) searchInput.value = food.name;
      setStatus('✅ Nutrition auto-filled! Adjust quantity if needed.', 'var(--green-main)');
    });
    return item;
  }

  /* Local search — uses FOOD_DATABASE from foodDatabase.js */
  function searchLocal(query) {
    if (typeof FOOD_DATABASE === 'undefined' || !query) return [];
    const q = query.toLowerCase().trim();
    return FOOD_DATABASE.filter(f => f.name.toLowerCase().includes(q)).slice(0, 8);
  }

  /* Live local search on every keystroke */
  let debounce = null;
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      clearTimeout(debounce);
      const q = searchInput.value.trim();
      if (q.length < 2) { closeDropdown(); setStatus(''); return; }

      debounce = setTimeout(() => {
        const results = searchLocal(q);
        dropdown.innerHTML = '';
        if (results.length > 0) {
          results.forEach(f => dropdown.appendChild(makeRow(f, 'local')));
          dropdown.classList.add('open');
          setStatus(`${results.length} local result${results.length > 1 ? 's' : ''} found`);
        } else {
          dropdown.innerHTML =
            `<div class="dropdown-status">No local match for "<strong>${escHtml(q)}</strong>". Try Search Online.</div>`;
          dropdown.classList.add('open');
          setStatus('No local match — try Search Online');
        }
      }, 200);
    });

    searchInput.addEventListener('blur', () => setTimeout(closeDropdown, 200));

    searchInput.addEventListener('keydown', e => {
      const items   = [...dropdown.querySelectorAll('.dropdown-item-food')];
      if (!items.length) return;
      const current = dropdown.querySelector('.highlighted');
      const idx     = items.indexOf(current);
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (current) current.classList.remove('highlighted');
        items[Math.min(idx + 1, items.length - 1)].classList.add('highlighted');
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (current) current.classList.remove('highlighted');
        items[Math.max(idx - 1, 0)].classList.add('highlighted');
      } else if (e.key === 'Enter') {
        e.preventDefault();
        dropdown.querySelector('.highlighted')?.dispatchEvent(new MouseEvent('mousedown'));
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    });
  }

  /* Search Online button — calls backend proxy */
  if (searchBtn) {
    searchBtn.addEventListener('click', async () => {
      const q = searchInput ? searchInput.value.trim() : '';
      if (!q) { setStatus('⚠️ Type a food name first.', 'var(--warning)'); return; }

      searchBtn.disabled    = true;
      searchBtn.textContent = '⏳ Searching…';
      setStatus('Searching online…');
      closeDropdown();

      try {
        const results = await API.searchFood(q);
        dropdown.innerHTML = '';
        if (results.length > 0) {
          results.forEach(f => dropdown.appendChild(makeRow(f, 'api')));
          dropdown.classList.add('open');
          setStatus(`${results.length} online result${results.length > 1 ? 's' : ''} found`, 'var(--info)');
        } else {
          dropdown.innerHTML =
            `<div class="dropdown-status">No online results for "<strong>${escHtml(q)}</strong>". Enter values manually.</div>`;
          dropdown.classList.add('open');
          setStatus('No online results — enter values manually', 'var(--warning)');
        }
      } catch (err) {
        setStatus('⚠️ Online search failed: ' + err.message, 'var(--danger)');
      } finally {
        searchBtn.disabled    = false;
        searchBtn.textContent = '🌐 Search Online';
      }
    });
  }

  /* Form submit */
  document.getElementById('addMealForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    clearAllErrors(this);

    const foodNameEl = document.getElementById('foodName');
    const quantityEl = document.getElementById('quantity');
    const caloriesEl = document.getElementById('calories');
    const mealTypeEl = document.querySelector('input[name="mealType"]:checked');
    let valid = true;

    if (!Validate.required(foodNameEl.value)) { showError(foodNameEl, 'Food name is required.');        valid = false; }
    if (!Validate.required(quantityEl.value)) { showError(quantityEl, 'Quantity is required.');         valid = false; }
    if (!Validate.positive(caloriesEl.value)) { showError(caloriesEl, 'Enter a valid calorie amount.'); valid = false; }
    if (!mealTypeEl) {
      const err = document.getElementById('mealTypeError');
      if (err) err.style.display = 'block';
      valid = false;
    }
    if (!valid) return;

    const submitBtn = this.querySelector('[type="submit"]');
    if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Saving…'; }

    const meal = {
      foodName: foodNameEl.value.trim(),
      quantity: quantityEl.value.trim(),
      mealType: mealTypeEl.value,
      calories: parseInt(caloriesEl.value),
      protein:  parseInt(document.getElementById('protein')?.value || 0),
      carbs:    parseInt(document.getElementById('carbs')?.value   || 0),
      fat:      parseInt(document.getElementById('fat')?.value     || 0),
      date: new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }),
    };

    try {
      const saved = await API.addMeal(meal);
      const successMsg = document.getElementById('mealSuccessMsg');
      if (successMsg) {
        successMsg.style.display = 'flex';
        successMsg.innerHTML =
          `✅ &nbsp;<strong>${escHtml(saved.foodName)}</strong> (${saved.calories} kcal) logged as ${saved.mealType}!`;
        setTimeout(() => { successMsg.style.display = 'none'; }, 4000);
      }
      this.reset();
      if (searchInput) searchInput.value = '';
      if (preview) preview.style.display = 'none';
      setStatus('');
      showToast('Meal saved to database! 🎉', 'success');
    } catch (err) {
      console.error('Save meal error:', err.message);
      showToast('Failed to save: ' + err.message, 'error');
    } finally {
      if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = '💾 Save Meal Entry'; }
    }
  });

  document.querySelectorAll('input[name="mealType"]').forEach(rb => {
    rb.addEventListener('change', () => {
      const err = document.getElementById('mealTypeError');
      if (err) err.style.display = 'none';
    });
  });
})();

/* ================================================================
   REPORTS PAGE
   ================================================================ */
(function initReports() {
  if (!document.getElementById('reportsPage')) return;

  const tableBody  = document.getElementById('mealsTableBody');
  const noDataMsg  = document.getElementById('noDataMessage');
  const totalCalEl = document.getElementById('reportTotalCal');
  const avgCalEl   = document.getElementById('reportAvgCal');
  const totalMeals = document.getElementById('reportTotalMeals');
  const filterEl   = document.getElementById('filterMealType');

  window.renderTablePublic = () => loadAndRender(filterEl ? filterEl.value : 'all');

  async function loadAndRender(filter) {
    filter = filter || 'all';
    if (tableBody) {
      tableBody.innerHTML =
        `<tr><td colspan="9" style="text-align:center;padding:2rem;color:var(--text-light);">Loading…</td></tr>`;
    }
    if (noDataMsg) noDataMsg.style.display = 'none';

    try {
      const allMeals = await API.getMeals('all');

      /* Stat cards — always from full unfiltered list */
      const totalC = allMeals.reduce((s, m) => s + (Number(m.calories) || 0), 0);
      const dates  = [...new Set(allMeals.map(m => m.date))];
      const avgC   = dates.length ? Math.round(totalC / dates.length) : 0;
      if (totalCalEl) totalCalEl.textContent = totalC > 0 ? totalC + ' kcal'       : '0 kcal';
      if (avgCalEl)   avgCalEl.textContent   = avgC   > 0 ? avgC   + ' kcal / day' : '0 kcal / day';
      if (totalMeals) totalMeals.textContent = allMeals.length;

      /* Filter for table rows */
      const filtered = filter === 'all'
        ? allMeals
        : allMeals.filter(m => m.mealType === filter);

      if (!tableBody) return;

      if (filtered.length === 0) {
        tableBody.innerHTML = '';
        if (noDataMsg) {
          noDataMsg.style.display = 'block';
          noDataMsg.innerHTML = filter !== 'all'
            ? `<div style="font-size:3rem;margin-bottom:1rem;">🔍</div>
               <p style="color:var(--text-light);margin-bottom:1rem;">No <strong>${escHtml(filter)}</strong> entries found.</p>
               <button class="btn btn-outline-green"
                 onclick="document.getElementById('filterMealType').value='all';renderTablePublic()">
                 Clear Filter
               </button>`
            : `<div style="font-size:3rem;margin-bottom:1rem;">🍽️</div>
               <p style="color:var(--text-light);margin-bottom:1rem;">No meals recorded yet. Start by adding your first meal.</p>
               <a href="add_meal.html" class="btn btn-primary-green">+ Add Your First Meal</a>`;
        }
        return;
      }

      tableBody.innerHTML = filtered.map(m => `
        <tr>
          <td><span style="font-family:var(--font-mono);font-size:.82rem;">${escHtml(m.date)}</span></td>
          <td><strong>${escHtml(m.foodName)}</strong></td>
          <td>${escHtml(m.quantity)}</td>
          <td><span class="meal-badge">${escHtml(m.mealType)}</span></td>
          <td><strong style="color:var(--green-main);font-family:var(--font-mono);">${m.calories}</strong></td>
          <td>${m.protein || 0}g</td>
          <td>${m.carbs   || 0}g</td>
          <td>${m.fat     || 0}g</td>
          <td>
            <button class="btn btn-danger-soft btn-sm"
                    data-id="${m._id}"
                    onclick="handleDeleteMeal(this)">✕</button>
          </td>
        </tr>
      `).join('');

    } catch (err) {
      console.error('Reports load error:', err.message);
      if (tableBody) {
        tableBody.innerHTML =
          `<tr><td colspan="9" style="text-align:center;padding:2rem;color:var(--danger);">
             ⚠️ Could not load data. Is the server running?
           </td></tr>`;
      }
      showToast('Could not load report data. Check your server.', 'error');
    }
  }

  window.handleDeleteMeal = async function (btn) {
    const id = btn.getAttribute('data-id');
    if (!id || !confirm('Remove this meal entry?')) return;
    btn.closest('tr').style.opacity = '0.4';
    btn.disabled = true;
    try {
      await API.deleteMeal(id);
      showToast('Meal deleted.', 'success');
      loadAndRender(filterEl ? filterEl.value : 'all');
    } catch (err) {
      showToast('Failed to delete: ' + err.message, 'error');
      btn.closest('tr').style.opacity = '1';
      btn.disabled = false;
    }
  };

  loadAndRender('all');
  if (filterEl) filterEl.addEventListener('change', () => loadAndRender(filterEl.value));
})();
