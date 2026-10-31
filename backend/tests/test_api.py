import os
import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

os.environ["NUTRITION_DB_PATH"] = str(Path(__file__).resolve().parent / "test_tracker.db")

from app.database import DATABASE_PATH, init_db
from app.main import app


@pytest.fixture(autouse=True)
def reset_db():
    init_db()
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("DELETE FROM meals")
        connection.execute("DELETE FROM target_config")
        connection.execute("INSERT INTO target_config (id, calories_kcal, protein_g) VALUES (1, NULL, NULL)")
        connection.commit()
    yield


client = TestClient(app)


def test_create_meal_and_summary():
    response = client.post(
        "/api/meals",
        json={
            "food_name": "Oatmeal",
            "meal_category": "Breakfast",
            "quantity_value": 1.5,
            "quantity_unit": "Serving",
            "calories_kcal": 320,
            "protein_g": 12,
            "meal_date": "2026-10-31",
            "meal_time": "08:00",
            "notes": "quick breakfast",
        },
    )
    assert response.status_code == 201

    summary = client.get("/api/summary", params={"selected_date": "2026-10-31"})
    assert summary.status_code == 200
    payload = summary.json()
    assert payload["total_calories"] == 320
    assert payload["total_protein"] == 12


def test_optional_time_and_notes_can_be_omitted_or_blank():
    meal_without_optional_fields = {
        "food_name": "Apple",
        "meal_category": "Snack",
        "quantity_value": 1,
        "quantity_unit": "Piece",
        "calories_kcal": 95,
        "protein_g": 0.5,
        "meal_date": "2026-10-31",
    }

    omitted_response = client.post("/api/meals", json=meal_without_optional_fields)
    assert omitted_response.status_code == 201
    assert omitted_response.json()["meal_time"] is None

    blank_response = client.post(
        "/api/meals",
        json={**meal_without_optional_fields, "meal_time": "", "notes": ""},
    )
    assert blank_response.status_code == 201
    assert blank_response.json()["meal_time"] is None
    assert blank_response.json()["notes"] is None


def test_reject_invalid_values_and_categories():
    bad_category = client.post(
        "/api/meals",
        json={
            "food_name": "Toast",
            "meal_category": "Dessert",
            "quantity_value": 1,
            "quantity_unit": "Serving",
            "calories_kcal": 150,
            "protein_g": 5,
            "meal_date": "2026-10-31",
        },
    )
    assert bad_category.status_code == 422

    bad_quantity = client.post(
        "/api/meals",
        json={
            "food_name": "Toast",
            "meal_category": "Breakfast",
            "quantity_value": 0,
            "quantity_unit": "Serving",
            "calories_kcal": 150,
            "protein_g": 5,
            "meal_date": "2026-10-31",
        },
    )
    assert bad_quantity.status_code == 422


def test_edit_meal_date_updates_both_dates():
    create = client.post(
        "/api/meals",
        json={
            "food_name": "Rice",
            "meal_category": "Lunch",
            "quantity_value": 1,
            "quantity_unit": "Serving",
            "calories_kcal": 250,
            "protein_g": 8,
            "meal_date": "2026-10-30",
        },
    )
    meal_id = create.json()["id"]

    update = client.put(
        f"/api/meals/{meal_id}",
        json={
            "meal_date": "2026-10-31",
            "meal_category": "Lunch",
            "food_name": "Rice",
            "quantity_value": 1,
            "quantity_unit": "Serving",
            "calories_kcal": 250,
            "protein_g": 8,
        },
    )
    assert update.status_code == 200

    previous_day = client.get("/api/summary", params={"selected_date": "2026-10-30"})
    next_day = client.get("/api/summary", params={"selected_date": "2026-10-31"})
    assert previous_day.json()["total_calories"] == 0
    assert next_day.json()["total_calories"] == 250


def test_historical_records_are_retained_and_delete_requires_confirmation():
    create_response = client.post(
        "/api/meals",
        json={
            "food_name": "Soup",
            "meal_category": "Dinner",
            "quantity_value": 1,
            "quantity_unit": "Cup",
            "calories_kcal": 180,
            "protein_g": 10,
            "meal_date": "2026-10-29",
        },
    )
    meal_id = create_response.json()["id"]

    list_previous = client.get("/api/meals", params={"selected_date": "2026-10-29"})
    assert list_previous.status_code == 200
    assert len(list_previous.json()) == 1

    delete_response = client.delete(f"/api/meals/{meal_id}")
    assert delete_response.status_code == 400

    confirm_delete = client.delete(f"/api/meals/{meal_id}", params={"confirm": True})
    assert confirm_delete.status_code == 200


def test_remaining_targets_never_show_negative_values():
    client.put(
        "/api/targets",
        json={"calories_kcal": 200, "protein_g": 10},
    )
    client.post(
        "/api/meals",
        json={
            "food_name": "Meal",
            "meal_category": "Lunch",
            "quantity_value": 1,
            "quantity_unit": "Serving",
            "calories_kcal": 250,
            "protein_g": 12,
            "meal_date": "2026-10-31",
        },
    )

    summary = client.get("/api/summary", params={"selected_date": "2026-10-31"}).json()
    assert summary["remaining_calories"] == 0
    assert summary["remaining_protein"] == 0
    assert summary["calories_status"] == "at_or_above_target"
    assert summary["protein_status"] == "at_or_above_target"
