from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator

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


class MealBase(BaseModel):
    food_name: str = Field(..., min_length=1)
    meal_category: Literal["Breakfast", "Lunch", "Dinner", "Snack"]
    quantity_value: float = Field(..., gt=0)
    quantity_unit: str
    calories_kcal: float = Field(..., ge=0)
    protein_g: float = Field(..., ge=0)
    meal_date: date
    meal_time: str | None = None
    notes: str | None = None

    @field_validator("meal_time", "notes")
    @classmethod
    def normalize_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if value == "":
            return None
        return value

    @field_validator("food_name")
    @classmethod
    def validate_food_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Food name is required")
        return value.strip()

    @field_validator("quantity_unit")
    @classmethod
    def validate_unit(cls, value: str) -> str:
        if value not in VALID_UNITS:
            raise ValueError(f"Quantity unit must be one of: {', '.join(VALID_UNITS)}")
        return value

    @field_validator("meal_category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        if value not in VALID_CATEGORIES:
            raise ValueError(f"Meal category must be one of: {', '.join(VALID_CATEGORIES)}")
        return value

    @field_validator("meal_time")
    @classmethod
    def validate_time(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if len(value) != 5 or value[2] != ":":
            raise ValueError("Meal time must use HH:MM format")
        hours, minutes = value.split(":")
        if not hours.isdigit() or not minutes.isdigit():
            raise ValueError("Meal time must use HH:MM format")
        if int(hours) not in range(24) or int(minutes) not in range(60):
            raise ValueError("Meal time must be a valid 24-hour clock time")
        return value

    model_config = {"populate_by_name": True}


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    food_name: str | None = None
    meal_category: Literal["Breakfast", "Lunch", "Dinner", "Snack"] | None = None
    quantity_value: float | None = Field(default=None, gt=0)
    quantity_unit: str | None = None
    calories_kcal: float | None = Field(default=None, ge=0)
    protein_g: float | None = Field(default=None, ge=0)
    meal_date: date | None = None
    meal_time: str | None = None
    notes: str | None = None

    @field_validator("meal_category")
    @classmethod
    def validate_category(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value not in VALID_CATEGORIES:
            raise ValueError(f"Meal category must be one of: {', '.join(VALID_CATEGORIES)}")
        return value

    @field_validator("quantity_unit")
    @classmethod
    def validate_unit(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if value not in VALID_UNITS:
            raise ValueError(f"Quantity unit must be one of: {', '.join(VALID_UNITS)}")
        return value

    @field_validator("meal_time")
    @classmethod
    def validate_time(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if len(value) != 5 or value[2] != ":":
            raise ValueError("Meal time must use HH:MM format")
        hours, minutes = value.split(":")
        if not hours.isdigit() or not minutes.isdigit():
            raise ValueError("Meal time must use HH:MM format")
        if int(hours) not in range(24) or int(minutes) not in range(60):
            raise ValueError("Meal time must be a valid 24-hour clock time")
        return value

    @field_validator("food_name")
    @classmethod
    def validate_food_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Food name is required")
        return cleaned

    @field_validator("meal_time", "notes")
    @classmethod
    def normalize_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        return cleaned or None


class TargetValues(BaseModel):
    calories_kcal: float | None = Field(default=None, ge=0)
    protein_g: float | None = Field(default=None, ge=0)


class DailySummary(BaseModel):
    date: str
    meal_count: int
    total_calories: float
    total_protein: float
    calories_target: float | None = None
    protein_target: float | None = None
    remaining_calories: float | None = None
    remaining_protein: float | None = None
    calories_status: str
    protein_status: str


class MealRead(BaseModel):
    id: int
    food_name: str
    meal_category: str
    quantity_value: float
    quantity_unit: str
    calories_kcal: float
    protein_g: float
    meal_date: str
    meal_time: str | None = None
    notes: str | None = None
