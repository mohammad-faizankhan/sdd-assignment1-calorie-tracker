# Implementation Plan: Calorie and Nutrition Tracker

**Branch**: `001-calorie-nutrition-tracker`  
**Date**: 2026-10-31  
**Baseline**: `v1.0.0`  
**Spec**: [`spec.md`](./spec.md)

## Summary

Build a small, local, single-user web application. A React frontend displays the tracker interface, and a FastAPI backend exposes a REST API backed by SQLite. The application stores meals and optional daily targets in a local SQLite database, supports historical record retention, and calculates daily totals for the selected date without deleting older rows. The app is constrained to the same-device local deployment model and does not include login, registration, or multi-user behavior.

The approved V1 scope includes date editing, unit-aware quantity validation, optional user-defined targets, and persistent retention of all meal records until explicit deletion.

## Technical context

**Language/Version**: Selected during implementation with supported Python and Node.js versions pinned in the project setup.

**Primary dependencies**:
- React
- Vite
- Python
- FastAPI
- Pydantic
- SQLite
- Python sqlite3
- Uvicorn
- pytest
- Vitest
- React Testing Library
- Git

**Storage**: SQLite database stored locally outside the repository in an application-data directory. No separate database per user, no auth-backed user tables, and no remote persistence.

**Target platform**: Desktop or mobile browser on the same device running the local app.

**Technical rationale**: Bind the API and frontend to loopback only so the app remains local and same-device while preserving the browser-accessibility requirement without introducing network exposure. This is a technical constraint for the approved local-only scope.

**Project type**: Local single-user web application with React frontend and FastAPI backend.

**Constraints**:
- No accounts, login, registration, roles, or shared multi-user data.
- No external food database or nutrition API.
- No target suggestions in V1.
- Persist meal history until the user explicitly deletes a record.
- Daily summaries filter by selected date without deleting or expiring other records.
- Quantity units use the approved predefined list and are not automatically converted.

## Constitution checks

- Simplicity: PASS. One frontend, one backend, one SQLite database, no extra infrastructure.
- User-centric design: PASS. The app supports meal entry, date-based review, editing, deletion, view of historical dates, and optional targets.
- Data accuracy and integrity: PASS. Meal values are stored as entered, totals are recalculated from persisted rows, and validation rejects invalid data.
- Requirements traceability: PASS. Requirements and acceptance criteria are directly mapped to the implementation and validation tasks.
- Maintainability: PASS. Frontend, API, business logic, and database layers remain separated and small.
- Input validation and error handling: PASS. Numeric, category, unit, and required-field validation are explicit and user-friendly.
- Privacy and security: PASS. Local-only storage, no accounts, and loopback binding keep the solution within the approved single-user model.
- Scope control: PASS. The implementation remains within the approved V1 scope and does not include unapproved suggestion logic or multi-user features.

## Architecture

### Components and responsibilities

1. React frontend
   - Provides the meal form and list view.
   - Supports responsive layout for desktop and mobile browsers.
   - Allows meal creation, edit, delete, and date-change operations.
   - Shows daily summaries and optional target comparisons.

2. FastAPI backend
   - Exposes REST endpoints for meals, targets, and summaries.
   - Validates request payloads with Pydantic.
   - Enforces date, category, numeric, unit, and target rules.
   - Binds to localhost or loopback only.

3. Business logic
   - Validates required fields and approved units.
   - Recalculates totals after create, edit, and delete operations.
   - Computes selected-date summaries from persisted meal records.
   - Treats unset targets differently from configured zero values.

4. SQLite access layer
   - Creates and maintains the local schema.
   - Uses parameterized SQL to protect data integrity.
   - Persists all records without automatic deletion.
   - Supports selected-date queries and historical date access.

### Processing sequence

1. User enters or edits a meal in the React interface.
2. The frontend submits the request to the local FastAPI API using the approved local-only route pattern.
3. FastAPI validates field presence, category, unit, numeric values, and date data.
4. The service layer writes the meal to SQLite or updates/deletes the existing record.
5. The service recalculates totals for the affected date or dates.
6. The summary endpoint reads the meals for the selected date and returns updated totals and optional target comparisons.
7. The UI reflects the updated records and totals without deleting older preserved rows.

## Data model

### Meal table

Required fields:
- id
- food_name
- meal_category
- quantity_value
- quantity_unit
- calories_kcal
- protein_g
- meal_date
- meal_time (optional)
- notes (optional)

Constraints:
- category is restricted to Breakfast, Lunch, Dinner, Snack
- quantity_value must be greater than zero
- quantity_unit must be one of Serving, Piece, Gram, Millilitre, Cup, Tablespoon, Teaspoon
- calories_kcal and protein_g must be numeric and non-negative
- meal_date is required and is determined by the selected date

### Target table

A simple optional local target store that tracks a single per-user target configuration:
- calories_kcal: nullable decimal
- protein_g: nullable decimal

Rules:
- null means unset
- zero is a valid configured target value
- target values must be numeric and non-negative
- a cleared target becomes unset and does not alter other values

### Historical retention

- All meal records remain in SQLite until explicitly deleted by the user.
- Date-scoped summaries pull from the relevant date and do not remove older rows.
- Previous-date summaries are supported.

## API design

| Method | Path | Purpose |
| --- | --- | --- |
| GET | /api/meals | List meals for the selected date |
| POST | /api/meals | Create a meal |
| GET | /api/meals/{id} | Retrieve one meal |
| PUT | /api/meals/{id} | Update a meal, including date changes |
| DELETE | /api/meals/{id} | Delete a meal after confirmation |
| GET | /api/summary | Return totals and comparisons for the selected date |
| GET | /api/targets | Read target values |
| PUT | /api/targets | Set or update targets |
| DELETE | /api/targets/{field} | Clear one target |

### Validation rules

- Required fields must be present.
- Category must be one of the approved four values.
- Quantity must be positive numeric with an approved unit.
- Calories and protein must be numeric and non-negative.
- A deleted meal must require confirmation before removal.
- Unset target values remain null, not zero.
- No default target suggestion values are created or returned.

## Validation and error handling

- Reject incomplete forms with 422-style validation responses or equivalent UI feedback.
- Reject invalid units, categories, negative values, and invalid dates.
- Preserve original data on failed edits.
- Recalculate totals on create, edit, and delete actions.
- Use generic server error responses without exposing database internals.

## Security and privacy

- Local-only application, same-device access only.
- No authentication, no registration, no user tables.
- No telemetry or external data sharing.
- SQLite file remains local to the device and outside the Git repository.

## Deployment and execution constraints

- Local frontend and API run on loopback or localhost only.
- Same-device browser access is supported for both desktop and mobile screen sizes.
- No production remote deployment is included in V1 scope.

## Validation matrix alignment

The final validation plan must cover:
- valid meal entry
- required-field validation
- invalid category and units
- date editing and date-based recalculation
- historical retention and previous-date summaries
- delete confirmation and recalculation
- optional target configuration and comparison
- no default target suggestions
- local single-user usage
- desktop/mobile responsiveness

This plan remains a planning artifact only and does not claim that implementation has already been completed.
