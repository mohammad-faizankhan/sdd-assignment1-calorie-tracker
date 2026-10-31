from __future__ import annotations

from datetime import date

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    clear_target,
    delete_meal,
    fetch_meal_by_id,
    fetch_meals_for_date,
    fetch_summary_for_date,
    fetch_target_config,
    get_connection,
    init_db,
    insert_meal,
    set_targets,
    update_meal,
)
from app.models import DailySummary, MealCreate, MealRead, MealUpdate, TargetValues

app = FastAPI(title="Calorie and Nutrition Tracker", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/meals", response_model=list[MealRead])
def list_meals(selected_date: date | None = Query(default=None)) -> list[MealRead]:
    target_date = (selected_date or date.today()).isoformat()
    rows = fetch_meals_for_date(target_date)
    return [MealRead.model_validate(row) for row in rows]


@app.post("/api/meals", response_model=MealRead, status_code=status.HTTP_201_CREATED)
def create_meal(payload: MealCreate) -> MealRead:
    meal = insert_meal(payload.model_dump())
    if meal is None:
        raise HTTPException(status_code=500, detail="Meal could not be created")
    return MealRead.model_validate(meal)


@app.get("/api/meals/{meal_id}", response_model=MealRead)
def get_meal(meal_id: int) -> MealRead:
    meal = fetch_meal_by_id(meal_id)
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return MealRead.model_validate(meal)


@app.put("/api/meals/{meal_id}", response_model=MealRead)
def update_existing_meal(meal_id: int, payload: MealUpdate) -> MealRead:
    existing = fetch_meal_by_id(meal_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    update_payload = payload.model_dump(exclude_unset=True)
    if not update_payload:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    updated = update_meal(meal_id, update_payload)
    if updated is None:
        raise HTTPException(status_code=500, detail="Meal update failed")
    return MealRead.model_validate(updated)


@app.delete("/api/meals/{meal_id}")
def delete_existing_meal(meal_id: int, confirm: bool = Query(default=False)) -> dict[str, str]:
    if not confirm:
        raise HTTPException(status_code=400, detail="Deletion requires confirmation")
    if fetch_meal_by_id(meal_id) is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    delete_meal(meal_id)
    return {"status": "deleted"}


@app.get("/api/summary", response_model=DailySummary)
def get_summary(selected_date: date | None = Query(default=None)) -> DailySummary:
    target_date = (selected_date or date.today()).isoformat()
    summary = fetch_summary_for_date(target_date)
    return DailySummary.model_validate(summary)


@app.get("/api/targets")
def read_targets() -> dict[str, float | None]:
    return fetch_target_config()


@app.put("/api/targets")
def save_targets(payload: TargetValues) -> dict[str, float | None]:
    values = payload.model_dump(exclude_none=True)
    if not values:
        raise HTTPException(status_code=400, detail="Provide at least one target value")
    return set_targets(values)


@app.delete("/api/targets")
def clear_target_value(field: str = Query(..., alias="field")) -> dict[str, float | None]:
    if field not in {"calories_kcal", "protein_g"}:
        raise HTTPException(status_code=400, detail="Target field must be calories_kcal or protein_g")
    try:
        return clear_target(field)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Calorie and Nutrition Tracker API"}


with get_connection() as connection:
    connection.execute("PRAGMA journal_mode=WAL")
