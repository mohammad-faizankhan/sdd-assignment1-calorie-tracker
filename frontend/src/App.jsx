import { useEffect, useState } from 'react'
import './App.css'

const API_BASE = 'http://127.0.0.1:8000'
const MEAL_CATEGORIES = ['Breakfast', 'Lunch', 'Dinner', 'Snack']
const VALID_UNITS = ['Serving', 'Piece', 'Gram', 'Millilitre', 'Cup', 'Tablespoon', 'Teaspoon']

function createDefaultMealForm(dateValue) {
  return {
    food_name: '',
    meal_category: 'Breakfast',
    quantity_value: '',
    quantity_unit: 'Serving',
    calories_kcal: '',
    protein_g: '',
    meal_date: dateValue,
    meal_time: '',
    notes: '',
  }
}

async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  const text = await response.text()
  const data = text ? JSON.parse(text) : null

  if (!response.ok) {
    const detail = data?.detail || 'Request failed'
    throw new Error(Array.isArray(detail) ? detail.map((item) => item.msg).join(', ') : detail)
  }

  return data
}

function App() {
  const todayString = new Date().toISOString().split('T')[0]
  const [selectedDate, setSelectedDate] = useState(todayString)
  const [meals, setMeals] = useState([])
  const [summary, setSummary] = useState({
    meal_count: 0,
    total_calories: 0,
    total_protein: 0,
    calories_target: null,
    protein_target: null,
    remaining_calories: null,
    remaining_protein: null,
    calories_status: 'not_configured',
    protein_status: 'not_configured',
  })
  const [targets, setTargets] = useState({ calories_kcal: '', protein_g: '' })
  const [form, setForm] = useState(createDefaultMealForm(todayString))
  const [editingId, setEditingId] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const loadData = async (dateValue = selectedDate) => {
    try {
      const [mealData, summaryData, targetData] = await Promise.all([
        apiFetch(`/api/meals?selected_date=${dateValue}`),
        apiFetch(`/api/summary?selected_date=${dateValue}`),
        apiFetch('/api/targets'),
      ])

      setMeals(mealData)
      setSummary(summaryData)
      setTargets({
        calories_kcal: targetData.calories_kcal ?? '',
        protein_g: targetData.protein_g ?? '',
      })
    } catch (loadError) {
      setError(loadError.message)
    }
  }

  useEffect(() => {
    setForm((previousForm) => ({ ...previousForm, meal_date: selectedDate }))
    loadData(selectedDate)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedDate])

  const handleFieldChange = (event) => {
    const { name, value } = event.target
    setForm((previousForm) => ({
      ...previousForm,
      [name]: value,
    }))
  }

  const resetForm = () => {
    setEditingId(null)
    setForm(createDefaultMealForm(selectedDate))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')

    const payload = {
      ...form,
      quantity_value: Number(form.quantity_value),
      calories_kcal: Number(form.calories_kcal),
      protein_g: Number(form.protein_g),
      meal_date: selectedDate,
    }

    try {
      if (editingId) {
        await apiFetch(`/api/meals/${editingId}`, {
          method: 'PUT',
          body: JSON.stringify(payload),
        })
        setSuccess('Meal updated successfully.')
      } else {
        await apiFetch('/api/meals', {
          method: 'POST',
          body: JSON.stringify(payload),
        })
        setSuccess('Meal saved successfully.')
      }
      resetForm()
      await loadData(selectedDate)
    } catch (submitError) {
      setError(submitError.message)
    }
  }

  const handleEdit = (meal) => {
    setEditingId(meal.id)
    setSelectedDate(meal.meal_date)
    setForm({
      food_name: meal.food_name,
      meal_category: meal.meal_category,
      quantity_value: String(meal.quantity_value),
      quantity_unit: meal.quantity_unit,
      calories_kcal: String(meal.calories_kcal),
      protein_g: String(meal.protein_g),
      meal_date: meal.meal_date,
      meal_time: meal.meal_time || '',
      notes: meal.notes || '',
    })
  }

  const handleDelete = async (mealId) => {
    const confirmed = window.confirm('Delete this meal?')
    if (!confirmed) return

    try {
      await apiFetch(`/api/meals/${mealId}?confirm=true`, {
        method: 'DELETE',
      })
      setSuccess('Meal deleted.')
      await loadData(selectedDate)
    } catch (deleteError) {
      setError(deleteError.message)
    }
  }

  const handleTargetSave = async (event) => {
    event.preventDefault()
    setError('')
    setSuccess('')

    try {
      const payload = {
        calories_kcal: targets.calories_kcal === '' ? null : Number(targets.calories_kcal),
        protein_g: targets.protein_g === '' ? null : Number(targets.protein_g),
      }

      await apiFetch('/api/targets', {
        method: 'PUT',
        body: JSON.stringify(payload),
      })
      setSuccess('Targets updated.')
      await loadData(selectedDate)
    } catch (targetError) {
      setError(targetError.message)
    }
  }

  const summaryLabel = summary.calories_target === null && summary.protein_target === null ? 'No target configured' : 'Target status'

  return (
    <div className="app-shell">
      <header className="page-header">
        <div>
          <p className="eyebrow">Calorie and Nutrition Tracker</p>
          <h1>Daily nutrition dashboard</h1>
        </div>
        <label className="date-picker">
          <span>Selected date</span>
          <input
            type="date"
            value={selectedDate}
            onChange={(event) => setSelectedDate(event.target.value)}
            aria-label="Selected date"
          />
        </label>
      </header>

      {error && <div className="alert error">{error}</div>}
      {success && <div className="alert success">{success}</div>}

      <section className="summary-grid">
        <article className="summary-card">
          <h2>Daily summary</h2>
          <div className="stat-row">
            <span>Meals</span>
            <strong>{summary.meal_count}</strong>
          </div>
          <div className="stat-row">
            <span>Calories</span>
            <strong>{summary.total_calories} kcal</strong>
          </div>
          <div className="stat-row">
            <span>Protein</span>
            <strong>{summary.total_protein} g</strong>
          </div>
        </article>

        <article className="summary-card">
          <h2>{summaryLabel}</h2>
          <div className="stat-row">
            <span>Calories target</span>
            <strong>{summary.calories_target ?? '—'} kcal</strong>
          </div>
          <div className="stat-row">
            <span>Protein target</span>
            <strong>{summary.protein_target ?? '—'} g</strong>
          </div>
          <div className="stat-row">
            <span>Remaining calories</span>
            <strong>{summary.remaining_calories ?? '—'} kcal</strong>
          </div>
          <div className="stat-row">
            <span>Remaining protein</span>
            <strong>{summary.remaining_protein ?? '—'} g</strong>
          </div>
        </article>
      </section>

      <main className="panel-grid">
        <section className="card form-card">
          <h2>{editingId ? 'Edit meal' : 'Add meal'}</h2>
          <form onSubmit={handleSubmit} className="meal-form" aria-label="Meal form">
            <label>
              Food name
              <input name="food_name" value={form.food_name} onChange={handleFieldChange} aria-label="Food name" required />
            </label>

            <label>
              Meal category
              <select name="meal_category" value={form.meal_category} onChange={handleFieldChange} aria-label="Meal category">
                {MEAL_CATEGORIES.map((category) => (
                  <option key={category} value={category}>{category}</option>
                ))}
              </select>
            </label>

            <div className="two-column">
              <label>
                Quantity
                <input type="number" min="0.01" step="0.01" name="quantity_value" value={form.quantity_value} onChange={handleFieldChange} aria-label="Quantity" required />
              </label>

              <label>
                Unit
                <select name="quantity_unit" value={form.quantity_unit} onChange={handleFieldChange} aria-label="Quantity unit">
                  {VALID_UNITS.map((unit) => (
                    <option key={unit} value={unit}>{unit}</option>
                  ))}
                </select>
              </label>
            </div>

            <div className="two-column">
              <label>
                Calories (kcal)
                <input type="number" min="0" step="0.01" name="calories_kcal" value={form.calories_kcal} onChange={handleFieldChange} aria-label="Calories" required />
              </label>

              <label>
                Protein (g)
                <input type="number" min="0" step="0.01" name="protein_g" value={form.protein_g} onChange={handleFieldChange} aria-label="Protein" required />
              </label>
            </div>

            <div className="two-column">
              <label>
                Date
                <input type="date" name="meal_date" value={form.meal_date} onChange={handleFieldChange} aria-label="Meal date" required />
              </label>

              <label>
                Time (optional)
                <input type="time" name="meal_time" value={form.meal_time} onChange={handleFieldChange} aria-label="Meal time" />
              </label>
            </div>

            <label>
              Notes
              <textarea name="notes" value={form.notes} onChange={handleFieldChange} aria-label="Notes" rows="3" />
            </label>

            <div className="button-row">
              <button type="submit" className="primary-button">{editingId ? 'Update meal' : 'Save meal'}</button>
              {editingId && (
                <button type="button" className="secondary-button" onClick={resetForm}>Cancel</button>
              )}
            </div>
          </form>
        </section>

        <section className="card target-card">
          <h2>Optional targets</h2>
          <form onSubmit={handleTargetSave} className="target-form">
            <label>
              Calories target
              <input
                type="number"
                min="0"
                step="0.01"
                value={targets.calories_kcal}
                onChange={(event) => setTargets((previous) => ({ ...previous, calories_kcal: event.target.value }))}
                aria-label="Calories target"
              />
            </label>
            <label>
              Protein target
              <input
                type="number"
                min="0"
                step="0.01"
                value={targets.protein_g}
                onChange={(event) => setTargets((previous) => ({ ...previous, protein_g: event.target.value }))}
                aria-label="Protein target"
              />
            </label>
            <button type="submit" className="primary-button">Save targets</button>
          </form>
        </section>
      </main>

      <section className="card meal-list-card">
        <div className="list-header">
          <h2>Meals for {selectedDate}</h2>
        </div>
        {meals.length === 0 ? (
          <p className="empty-state">No meals recorded for this date.</p>
        ) : (
          <ul className="meal-list">
            {meals.map((meal) => (
              <li key={meal.id} className="meal-item">
                <div className="meal-details">
                  <div className="meal-topline">
                    <strong>{meal.food_name}</strong>
                    <span>{meal.meal_category}</span>
                  </div>
                  <p>
                    {meal.quantity_value} {meal.quantity_unit} · {meal.calories_kcal} kcal · {meal.protein_g} g
                  </p>
                  {meal.meal_time && <p>Time: {meal.meal_time}</p>}
                  {meal.notes && <p>Notes: {meal.notes}</p>}
                </div>
                <div className="meal-actions">
                  <button type="button" className="secondary-button" onClick={() => handleEdit(meal)}>Edit</button>
                  <button type="button" className="danger-button" onClick={() => handleDelete(meal.id)}>Delete</button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}

export default App
