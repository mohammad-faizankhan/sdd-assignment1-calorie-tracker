import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'

const mealList = [
  {
    id: 1,
    food_name: 'Oatmeal',
    meal_category: 'Breakfast',
    quantity_value: 1,
    quantity_unit: 'Serving',
    calories_kcal: 320,
    protein_g: 12,
    meal_date: '2026-10-31',
    meal_time: '08:00',
    notes: 'Quick breakfast',
  },
]

const targetConfig = {
  calories_kcal: 2000,
  protein_g: 120,
}

const summaryResponse = {
  date: '2026-10-31',
  meal_count: 1,
  total_calories: 320,
  total_protein: 12,
  calories_target: 2000,
  protein_target: 120,
  remaining_calories: 1680,
  remaining_protein: 108,
  calories_status: 'below_target',
  protein_status: 'below_target',
}

describe('App', () => {
  beforeEach(() => {
    global.fetch = vi.fn((input, init = {}) => {
      const url = String(input)
      const method = (init.method || 'GET').toUpperCase()

      if (url.includes('/api/meals') && method === 'GET') {
        return Promise.resolve({
          ok: true,
          text: async () => JSON.stringify(mealList),
        })
      }

      if (url.includes('/api/summary') && method === 'GET') {
        return Promise.resolve({
          ok: true,
          text: async () => JSON.stringify(summaryResponse),
        })
      }

      if (url.includes('/api/targets') && method === 'GET') {
        return Promise.resolve({
          ok: true,
          text: async () => JSON.stringify(targetConfig),
        })
      }

      if (url.includes('/api/meals') && method === 'POST') {
        const payload = JSON.parse(init.body)
        return Promise.resolve({
          ok: true,
          text: async () => JSON.stringify({ id: 2, ...payload }),
        })
      }

      if (url.includes('/api/meals/') && method === 'DELETE') {
        return Promise.resolve({
          ok: true,
          text: async () => JSON.stringify({ status: 'deleted' }),
        })
      }

      return Promise.resolve({
        ok: true,
        text: async () => JSON.stringify({ status: 'ok' }),
      })
    })
  })

  it('renders daily summary and target status for the selected date', async () => {
    render(<App />)

    expect(await screen.findByText('Daily nutrition dashboard')).toBeInTheDocument()
    expect(await screen.findByText('Daily summary')).toBeInTheDocument()
    expect(screen.getAllByText(/calories/i).length).toBeGreaterThan(0)
    expect(screen.getAllByText(/meals/i).length).toBeGreaterThan(0)
  })

  it('allows a new meal to be saved from the form', async () => {
    const user = userEvent.setup()
    render(<App />)

    const foodNameInput = screen.getByRole('textbox', { name: /food name/i })
    const quantityInput = screen.getByLabelText('Quantity')
    const caloriesInput = screen.getByLabelText('Calories (kcal)')
    const proteinInput = screen.getByLabelText('Protein (g)')

    await user.clear(foodNameInput)
    await user.type(foodNameInput, 'Apple')
    await user.clear(quantityInput)
    await user.type(quantityInput, '2')
    await user.clear(caloriesInput)
    await user.type(caloriesInput, '95')
    await user.clear(proteinInput)
    await user.type(proteinInput, '0.5')

    await user.click(screen.getByRole('button', { name: /save meal/i }))

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/meals'),
        expect.objectContaining({ method: 'POST' }),
      )
    })
  })
})
