# Tasks: Calorie and Nutrition Tracker

**Input**: Design documents from `/specs/001-calorie-nutrition-tracker/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/openapi.yaml, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each story.

**Planning note**: Historical meal retention and meal date editing remain unresolved. Tasks intentionally avoid hard automatic deletion of older meal records and avoid locking a meal's date until the business owner approves the behavior. Summaries remain date-scoped without deleting other stored rows.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the project skeleton and install required local dependencies.

- [ ] T001 [P] Create the backend and frontend project structure in `backend/app`, `backend/tests`, `frontend/src`, and `frontend/public` (Refs: AC-019, AC-026)
- [ ] T002 Initialize the FastAPI backend with pinned Python dependencies in `backend/requirements.txt` (Refs: AC-019)
- [ ] T003 [P] Initialize the React + Vite frontend with the required npm dependencies in `frontend/package.json` (Refs: AC-019)
- [ ] T004 [P] Configure local development and build scripts for loopback-only FastAPI and React servers in `backend/` and `frontend/` (Refs: AC-010, AC-026)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the core app infrastructure before any user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T005 Define the SQLite database lifecycle and startup configuration in `backend/app/config.py` and `backend/app/db.py` (Refs: AC-020, AC-026, AC-027)
- [ ] T006 Implement database schema creation, parameterized queries, and date-scoped data access in `backend/app/db.py` and `backend/app/services/cleanup_service.py` without assuming automatic historical deletion (Refs: AC-016, AC-024, AC-027)
- [ ] T007 Define API request/response models and decimal validation rules in `backend/app/schemas.py` and `backend/app/models/meal.py` (Refs: AC-001, AC-003, AC-005, AC-022)
- [ ] T008 Set up FastAPI app bootstrap, router registration, dependency wiring, and local-only server configuration in `backend/app/main.py` and `backend/app/api/router.py` (Refs: AC-020, AC-026, AC-027)
- [ ] T009 [P] Implement the shared API client and error handling layer for frontend requests in `frontend/src/api/client.ts` and `frontend/src/api/errors.ts` (Refs: AC-015, AC-017, AC-019)
- [ ] T010 [P] Create the base React app shell and state container in `frontend/src/App.tsx` and `frontend/src/app/store.ts` (Refs: AC-015, AC-019)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Record Meals and Review Daily Intake (Priority: P1) 🎯 MVP

**Goal**: Allow users to add meals and see accurate calories and protein totals for the active date.

**Independent Test**: Create a valid meal, confirm it is stored for the selected date, and verify the daily totals update correctly.

### Implementation for User Story 1

- [ ] T011 [US1] Implement meal persistence, validation, and date-scoped summary aggregation in `backend/app/services/meal_service.py` (Refs: AC-001, AC-003, AC-005, AC-007, AC-008, AC-022)
- [ ] T012 [US1] Add REST endpoints for listing, creating, updating, and deleting meals in `backend/app/api/routes/meals.py` (Refs: AC-001, AC-004, AC-010, AC-011, AC-022)
- [ ] T013 [US1] Add the daily summary endpoint and response shaping in `backend/app/api/routes/summary.py` (Refs: AC-007, AC-008, AC-012, AC-013, AC-025)
- [ ] T014 [US1] Create the meal form and list UI in `frontend/src/components/MealForm.tsx` and `frontend/src/components/MealList.tsx` (Refs: AC-001, AC-002, AC-006, AC-015)
- [ ] T015 [US1] Wire the frontend meal API calls and update totals in `frontend/src/api/meals.ts` and `frontend/src/App.tsx` (Refs: AC-007, AC-008, AC-012, AC-013, AC-015)
- [ ] T016 [US1] Handle invalid meal input and field-level validation feedback in `backend/app/api/routes/meals.py` and `frontend/src/components/MealForm.tsx` (Refs: AC-004, AC-005, AC-011, AC-017, AC-022)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Correct or Remove a Meal (Priority: P2)

**Goal**: Let users edit or delete existing meals while keeping totals and stored data consistent.

**Independent Test**: Modify a saved meal, verify the totals change, then delete it and confirm the totals return to zero when appropriate.

### Implementation for User Story 2

- [ ] T017 [US2] Implement meal update and delete service logic with validation, date-aware totals, and no hard date lock in `backend/app/services/meal_service.py` (Refs: AC-009, AC-010, AC-011, AC-024)
- [ ] T018 [US2] Expose update and delete semantics through the meal routes in `backend/app/api/routes/meals.py` (Refs: AC-009, AC-010, AC-011, AC-024)
- [ ] T019 [US2] Add optional meal edit actions in the UI and keep list state synchronized in `frontend/src/components/MealList.tsx` and `frontend/src/components/MealEditor.tsx` (Refs: AC-009, AC-010, AC-015)
- [ ] T020 [US2] Ensure the app recalculates totals after each edit and delete action in `frontend/src/App.tsx` and `frontend/src/api/meals.ts` (Refs: AC-009, AC-010, AC-012, AC-013)
- [ ] T021 [US2] Handle save failures without mutating the original meal record in `backend/app/services/meal_service.py` and `frontend/src/components/MealEditor.tsx` (Refs: AC-009, AC-011)

**Checkpoint**: At this point, User Stories 1 and 2 should both work independently.

---

## Phase 5: User Story 3 - Set Targets and Compare Progress (Priority: P3)

**Goal**: Support optional calorie and protein daily targets and compare totals against them without showing zero for unset values.

**Independent Test**: View a date without targets, set one or both values, and verify the comparison reflects the configured target while unset targets remain absent.

### Implementation for User Story 3

- [ ] T022 [US3] Implement singleton target persistence and null-vs-zero semantics in `backend/app/models/targets.py` and `backend/app/services/target_service.py` (Refs: AC-012, AC-013, AC-014, AC-025)
- [ ] T023 [US3] Add target GET/PUT/DELETE API routes and validation in `backend/app/api/routes/targets.py` (Refs: AC-012, AC-013, AC-014, AC-025)
- [ ] T024 [US3] Extend the summary response with optional target comparisons in `backend/app/api/routes/summary.py` (Refs: AC-012, AC-013, AC-014, AC-025)
- [ ] T025 [US3] Build the target settings UI and clear/set actions in `frontend/src/components/TargetSettings.tsx` (Refs: AC-012, AC-013, AC-014, AC-015, AC-023)
- [ ] T026 [US3] Connect target API calls and summary rendering to the main dashboard in `frontend/src/api/targets.ts` and `frontend/src/App.tsx` (Refs: AC-012, AC-013, AC-014, AC-015, AC-023)
- [ ] T027 [US3] Block generic target suggestions and ensure no numerical suggestion values are introduced until Q-004a is approved in `backend/app/services/target_service.py` and `frontend/src/components/TargetSettings.tsx` (Refs: AC-023)

**Checkpoint**: At this point, User Stories 1-3 should be independently functional.

---

## Phase 6: User Story 4 - Use the Tracker on Desktop or Mobile (Priority: P2)

**Goal**: Ensure the tracker remains usable across desktop and mobile browser viewports while being loopback-only.

**Independent Test**: Open the app in a mobile viewport and a desktop viewport, then confirm the same core flows remain readable and usable.

### Implementation for User Story 4

- [ ] T028 [US4] Add responsive layout styling for the dashboard, meal form, list, and target controls in `frontend/src/styles/` and `frontend/src/App.tsx` (Refs: AC-015, AC-026)
- [ ] T029 [US4] Confirm all required controls remain available in mobile and desktop layouts in `frontend/src/components/` (Refs: AC-015, AC-026)
- [ ] T030 [US4] Ensure FastAPI and the dev frontend are loopback-bound only in `backend/app/main.py`, `frontend/vite.config.*`, and the runtime documentation in `quickstart.md` (Refs: AC-020, AC-026)

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final cleanup, validation of the planned local workflow, and edge-case verification.

- [ ] T031 [P] Review all CRUD and summary flows against the acceptance smoke scenarios in `quickstart.md` (Refs: AC-001, AC-007, AC-008, AC-009, AC-010, AC-012, AC-013, AC-015, AC-023)
- [ ] T032 [P] Verify date-scoped summary behavior and retention policy expectations in `backend/app/services/cleanup_service.py` without automatic historical deletion (Refs: AC-016, AC-024, AC-027)
- [ ] T033 [P] Confirm Decimal arithmetic and exact totals match the spec for zero, positive, and edited values in `backend/app/services/meal_service.py` (Refs: AC-007, AC-008, AC-009, AC-010, AC-012, AC-013)
- [ ] T034 Update implementation docs and the run guide for the final app structure in `quickstart.md`, `README.md`, and any backend/frontend setup docs (Refs: AC-019, AC-020, AC-026)
- [ ] T035 Run the planned validation commands for the backend, frontend, and local smoke flow: `pytest`, `npm --prefix frontend test -- --run`, and `npm --prefix frontend run build` (Refs: AC-001, AC-003, AC-007, AC-008, AC-009, AC-010, AC-012, AC-013, AC-015, AC-023)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies; can start immediately.
- **Phase 2 (Foundational)**: Depends on setup completion and blocks all user stories.
- **User Stories (Phases 3-6)**: All depend on Phase 2 completion.
- **Phase 7 (Polish)**: Depends on all story phases being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational; delivers the MVP.
- **User Story 2 (P2)**: Can start after Foundational; depends on the meal model/service contracts built in US1 but should remain independently testable.
- **User Story 3 (P3)**: Can start after Foundational; depends on the summary contract from US1 and target persistence model.
- **User Story 4 (P2)**: Can start after Foundational; validates responsive and local-only constraints but is independent of the nutrition logic.

### Parallel Opportunities

- Setup tasks T001-T004 can run in parallel.
- Foundational tasks T005-T010 can run in parallel where their file scopes do not overlap.
- User Story 1 tasks T011-T016 can be implemented in parallel after the foundation is ready.
- User Story 2 tasks T017-T021 can proceed in parallel with US3/US4 work once the shared meal contracts are in place.
- Final validation tasks T031-T035 may run after all story work is complete.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Stop and validate the flow before continuing to US2-US4

### Incremental Delivery

1. Finish the meal recording and summary flow.
2. Add the edit/delete correction workflows.
3. Add target configuration and comparison behavior.
4. Finalize responsive rendering and local-only protections.
5. Run the quickstart smoke validation and polish the final experience.

**Note**: This implementation intentionally does not add generic numeric target suggestions or stored suggestion values until Q-004a is approved, per the feature gate in the specification and plan. Historical retention and meal date editing remain unresolved and are not implemented as hard default behavior.
