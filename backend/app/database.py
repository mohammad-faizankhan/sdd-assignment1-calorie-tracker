import sqlite3
from typing import Any

from app.config import DATABASE_PATH


VALID_UNITS = [
    "Serving",
    "Piece",
    "Gram",
    "Millilitre",
    "Cup",
    "Tablespoon",
    "Teaspoon",
]
VALID_CATEGORIES = ["Breakfast", "Lunch", "Dinner", "Snack"]


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_name TEXT NOT NULL,
                meal_category TEXT NOT NULL CHECK(meal_category IN ('Breakfast', 'Lunch', 'Dinner', 'Snack')),
                quantity_value REAL NOT NULL CHECK(quantity_value > 0),
                quantity_unit TEXT NOT NULL CHECK(quantity_unit IN ('Serving', 'Piece', 'Gram', 'Millilitre', 'Cup', 'Tablespoon', 'Teaspoon')),
                calories_kcal REAL NOT NULL CHECK(calories_kcal >= 0),
                protein_g REAL NOT NULL CHECK(protein_g >= 0),
                meal_date TEXT NOT NULL,
                meal_time TEXT,
                notes TEXT
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS target_config (
                id INTEGER PRIMARY KEY CHECK(id = 1),
                calories_kcal REAL,
                protein_g REAL
            )
            """
        )
        connection.execute(
            "INSERT OR IGNORE INTO target_config (id, calories_kcal, protein_g) VALUES (1, NULL, NULL)"
        )
        connection.commit()


def fetch_meals_for_date(date_value: str) -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM meals
            WHERE meal_date = ?
            ORDER BY datetime(meal_time) DESC, id DESC
            """,
            (date_value,),
        ).fetchall()
    return [dict(row) for row in rows]


def fetch_meal_by_id(meal_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone()
    return dict(row) if row else None


def insert_meal(payload: dict[str, Any]) -> dict[str, Any]:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO meals (
                food_name,
                meal_category,
                quantity_value,
                quantity_unit,
                calories_kcal,
                protein_g,
                meal_date,
                meal_time,
                notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload["food_name"],
                payload["meal_category"],
                float(payload["quantity_value"]),
                payload["quantity_unit"],
                float(payload["calories_kcal"]),
                float(payload["protein_g"]),
                payload["meal_date"],
                payload.get("meal_time"),
                payload.get("notes"),
            ),
        )
        connection.commit()
        new_id = cursor.lastrowid
    return fetch_meal_by_id(new_id)


def update_meal(meal_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    with get_connection() as connection:
        fields = []
        values = []
        for key, value in payload.items():
            if key == "food_name":
                fields.append("food_name = ?")
            elif key == "meal_category":
                fields.append("meal_category = ?")
            elif key == "quantity_value":
                fields.append("quantity_value = ?")
            elif key == "quantity_unit":
                fields.append("quantity_unit = ?")
            elif key == "calories_kcal":
                fields.append("calories_kcal = ?")
            elif key == "protein_g":
                fields.append("protein_g = ?")
            elif key == "meal_date":
                fields.append("meal_date = ?")
            elif key == "meal_time":
                fields.append("meal_time = ?")
            elif key == "notes":
                fields.append("notes = ?")
            else:
                continue
            values.append(value)
        if not fields:
            return fetch_meal_by_id(meal_id)
        values.append(meal_id)
        connection.execute(f"UPDATE meals SET {', '.join(fields)} WHERE id = ?", tuple(values))
        connection.commit()
    return fetch_meal_by_id(meal_id)


def delete_meal(meal_id: int) -> None:
    with get_connection() as connection:
        connection.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        connection.commit()


def fetch_target_config() -> dict[str, float | None]:
    with get_connection() as connection:
        row = connection.execute("SELECT calories_kcal, protein_g FROM target_config WHERE id = 1").fetchone()
    if row is None:
        return {"calories_kcal": None, "protein_g": None}
    return {
        "calories_kcal": row["calories_kcal"],
        "protein_g": row["protein_g"],
    }


def set_targets(payload: dict[str, float | None]) -> dict[str, float | None]:
    with get_connection() as connection:
        connection.execute(
            "UPDATE target_config SET calories_kcal = ?, protein_g = ? WHERE id = 1",
            (
                payload.get("calories_kcal"),
                payload.get("protein_g"),
            ),
        )
        connection.commit()
    return fetch_target_config()


def clear_target(field_name: str) -> dict[str, float | None]:
    with get_connection() as connection:
        if field_name == "calories_kcal":
            connection.execute("UPDATE target_config SET calories_kcal = NULL WHERE id = 1")
        elif field_name == "protein_g":
            connection.execute("UPDATE target_config SET protein_g = NULL WHERE id = 1")
        else:
            raise ValueError("Unsupported target field")
        connection.commit()
    return fetch_target_config()


def fetch_summary_for_date(date_value: str) -> dict[str, Any]:
    meals = fetch_meals_for_date(date_value)
    total_calories = round(sum(float(meal["calories_kcal"]) for meal in meals), 2)
    total_protein = round(sum(float(meal["protein_g"]) for meal in meals), 2)
    targets = fetch_target_config()
    summary = {
        "date": date_value,
        "meal_count": len(meals),
        "total_calories": total_calories,
        "total_protein": total_protein,
        "calories_target": targets["calories_kcal"],
        "protein_target": targets["protein_g"],
        "remaining_calories": None,
        "remaining_protein": None,
        "calories_status": "not_configured",
        "protein_status": "not_configured",
    }
    if targets["calories_kcal"] is not None:
        summary["remaining_calories"] = max(0, round(float(targets["calories_kcal"]) - total_calories, 2))
        summary["calories_status"] = "below_target" if total_calories < float(targets["calories_kcal"]) else "at_or_above_target"
    if targets["protein_g"] is not None:
        summary["remaining_protein"] = max(0, round(float(targets["protein_g"]) - total_protein, 2))
        summary["protein_status"] = "below_target" if total_protein < float(targets["protein_g"]) else "at_or_above_target"
    return summary
