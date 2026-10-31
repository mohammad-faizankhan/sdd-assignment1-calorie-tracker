# Tasks: Calorie and Nutrition Tracker

**Input**: Approved feature specification, plan, and clarification log for v1.0.0
**Baseline**: `v1.0.0`

## Phase 1: Setup and foundation

### Purpose
Create the project structure and the local-only development environment for the approved scope.

- [ ] T001 Create the backend and frontend project structure in `backend/app`, `backend/tests`, `frontend/src`, and `frontend/public` (Refs: AC-019, AC-015)
- [ ] T002 Initialize Python dependencies for FastAPI, Pydantic, SQLite access, and pytest (Refs: AC-019)
- [ ] T003 Initialize the React + Vite frontend and required test tooling (Refs: AC-015, AC-019)
- [ ] T004 Configure local-only development scripts so the API and frontend run on loopback only (Refs: AC-015, AC-019)

## Phase 2: Core persistence and validation

### Purpose
Set up the database, schemas, and validation rules required by the approved V1 behavior.

- [ ] T005 Define the SQLite schema for meals and optional targets in `backend/app/db.py` and related configuration files (Refs: AC-019, AC-020, AC-024)
- [ ] T006 Implement meal and target persistence logic using parameterized SQLite queries and explicit local retention rules (Refs: AC-019, AC-020, AC-024, AC-025)
- [ ] T007 Define request and response schemas, including required meal fields, unit selection, target values, and optional notes/time (Refs: AC-001, AC-003, AC-004, AC-005, AC-016, AC-017)
- [ ] T008 Implement FastAPI app bootstrap, router registration, and local-only configuration (Refs: AC-015, AC-019)
- [ ] T009 Implement a frontend API client and shared error handling pattern for standard validation feedback (Refs: AC-003, AC-011, AC-015)

## Phase 3: Meal entry, listing, and daily summary

### Purpose
Support meal creation, listing, and selected-date summaries.

- [ ] T010 Implement meal creation and retrieval service logic and SQLite queries for selected-date meal listing (Refs: AC-001, AC-003, AC-006, AC-007, AC-008, AC-014)
- [ ] T011 Add meal create/read endpoints in the API and validate required fields, categories, units, and numeric values (Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006)
- [ ] T012 Add the daily summary API to aggregate meals for the selected date and include optional target comparisons (Refs: AC-007, AC-014, AC-016, AC-017, AC-018)
- [ ] T013 Build the meal form and selected-date meal list UI for desktop and mobile layouts (Refs: AC-001, AC-007, AC-015)
- [ ] T014 Connect the frontend to the meal API and refresh totals after saving meals (Refs: AC-001, AC-007, AC-014, AC-015)

## Phase 4: Meal editing, deletion, and date changes

### Purpose
Support date edits, meal updates, deletion confirmation, and recalculation.

- [ ] T015 Implement meal update logic and date-change handling so the meal moves to the selected date and totals recalc for both dates (Refs: AC-009, AC-010, AC-011, AC-024)
- [ ] T016 Implement meal delete logic with confirmation and totals recalculation (Refs: AC-012, AC-013, AC-026)
- [ ] T017 Expose update and delete routes in the API and ensure failed edits do not mutate the stored record (Refs: AC-009, AC-010, AC-011, AC-012, AC-013)
- [ ] T018 Add the meal edit UI, date-change handling, and delete confirmation workflow (Refs: AC-009, AC-010, AC-012, AC-015)
- [ ] T019 Sync frontend totals after edit and delete actions (Refs: AC-009, AC-010, AC-013, AC-024)

## Phase 5: Optional daily targets

### Purpose
Implement optional user-defined targets without introducing suggestions or authentication.

- [ ] T020 Implement target persistence and null-vs-zero logic in the backend (Refs: AC-016, AC-017, AC-018, AC-023, AC-025)
- [ ] T021 Add target read/write/delete API endpoints and validation rules (Refs: AC-016, AC-017, AC-018, AC-023)
- [ ] T022 Extend the summary response to include optional target comparisons without showing default values (Refs: AC-016, AC-017, AC-018, AC-023)
- [ ] T023 Build the target settings UI and support clearing targets as an explicit action (Refs: AC-016, AC-017, AC-018, AC-023, AC-015)
- [ ] T024 Connect target API calls to the dashboard and keep comparison output in sync with user changes (Refs: AC-016, AC-017, AC-018, AC-023)

## Phase 6: Validation, responsiveness, and baseline checks

### Purpose
Validate the approved V1 requirements and keep the project aligned to the SDD baseline.

- [ ] T025 Add backend and API tests covering valid creation, invalid fields, category validation, units, date changes, historical retention, and summary logic (Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-013, AC-014, AC-020, AC-024)
- [ ] T026 Add frontend tests covering responsive layout, meal entry flow, delete confirmation, and target comparisons (Refs: AC-015, AC-016, AC-017, AC-018, AC-019, AC-023)
- [ ] T027 Verify no default target suggestions are emitted and no authentication is introduced in V1 (Refs: AC-019, AC-022)
- [ ] T028 Run the validation checklist against the SDD baseline and confirm all acceptance criteria are covered without implementation drift (Refs: AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, AC-009, AC-010, AC-011, AC-012, AC-013, AC-014, AC-015, AC-016, AC-017, AC-018, AC-019, AC-020, AC-021, AC-022, AC-023, AC-024, AC-025, AC-026)

## Dependency summary

- T001-T004 are prerequisites for all implementation work.
- T005-T009 establish the persistence and validation foundation.
- T010-T014 deliver meal creation and daily summary functionality.
- T015-T019 deliver editing, deletion, and date-change support.
- T020-T024 deliver optional target configuration and comparisons.
- T025-T028 provide final validation and baseline confirmation.

## Exclusions and scope boundaries

- No automatic expiration or deletion of historical meal records.
- No target suggestion generation or default target values in V1.
- No authentication, registration, or multi-user behavior.
- No source-code implementation is generated by this planning task.
