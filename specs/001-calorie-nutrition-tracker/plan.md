# Implementation Plan: Calorie and Nutrition Tracker

**Branch**: `001-calorie-nutrition-tracker` | **Date**: 2026-10-31 | **Spec**:
[`spec.md`](./spec.md)

**Input**: Approved feature specification, project constitution, and user-proposed
stack: React, Python FastAPI, SQLite, REST, pytest, and Git.

## Summary

Build a small, single-user local web application. A React UI communicates with a
FastAPI REST API backed by a local SQLite database. FastAPI serves the production
React build, binds only to loopback, and supports date-scoped meal CRUD, persistent
optional targets, and a derived daily summary. Python `Decimal` calculations over
canonical decimal strings preserve user-entered values without selecting an
unspecified nutrition precision. The application contains no accounts, hosted
services, external nutrition lookup, or multi-user data separation.

The specification's numeric values and supporting basis for generic target
suggestions (Q-004a) remain pending. The app must not invent or seed suggestions;
FR-016 remains gated until that content is approved. Historical meal retention and
whether a saved meal date can be edited remain explicitly unresolved in the Open
Clarification Log and are intentionally not implemented as hard default behavior.

## Technical Context

**Language/Version**: Python and JavaScript; choose currently supported compatible
versions and pin dependencies during implementation.

**Primary Dependencies**: React, FastAPI, Pydantic (via FastAPI), Uvicorn,
Vite, Vitest, React Testing Library, pytest, FastAPI TestClient/httpx, SQLite via
Python `sqlite3`.

**Storage**: One SQLite database in the local user's application-data directory,
outside the repository. No account/user table.

**Testing**: pytest for backend unit, API, validation, and SQLite tests; React
Testing Library with Vitest for user-visible component interactions; manual
responsive and local-only smoke checks.

**Target Platform**: Desktop or mobile browser on the same device as the local
application; FastAPI and development frontend listen on loopback only.

**Technical rationale**: Loopback-only binding is a design constraint to keep the
single-user app accessible only on the same device while preserving the approved
browser-accessibility requirement without enabling remote access. This is an
implementation control for the local-only deployment model rather than a business
requirement that changes scope.

**Project Type**: Local single-user web application with a React frontend and
FastAPI REST backend.

**Performance Goals**: No numeric latency or throughput target is specified.
Calculations cover the selected date's small meal list; acceptance requires totals
to match exact sums and the primary user flows to complete without errors.

**Constraints**: No accounts or cross-device/network access; loopback binding;
meal records are not auto-purged by default while historical retention remains
unresolved; targets persist until cleared; no external food data; do not implement
numerical suggestions before Q-004a is approved; no unsupported precision/range
limits for calorie, protein, or targets.

**Scale/Scope**: One local user and date-scoped meal records, plus two optional
persistent target values. No multi-user, distributed service, or external
integration.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Before Research

- **I. Simplicity First — PASS**: One React app, one FastAPI process, one SQLite
  file, and built-in SQLite access avoid unnecessary infrastructure and
  abstractions.
- **II. User-Centric Design — PASS**: The plan covers meal entry, editing,
  deletion, optional targets, and today's progress in responsive layouts.
- **III. Data Accuracy and Integrity — PASS**: Decimal validation and exact
  backend aggregation preserve nutrition values; edits and deletions recompute the
  summary from persisted meals.
- **IV. Requirements Traceability — PASS**: The implementation and validation
  mappings below connect each FR and acceptance group to specific components and
  tests.
- **V. Maintainability — PASS**: Frontend features and backend routes, business
  logic, and database operations have small, explicit responsibilities.
- **VI. Input Validation and Error Handling — PASS**: Pydantic validation,
  service-level date checks, HTTP errors, and UI field feedback cover the specified
  invalid-input paths.
- **VII. Privacy and Security — PASS**: No accounts or data sharing; loopback-only
  binding, restricted development CORS, parameterized SQL, and generic server
  errors protect the supported local model.
- **VIII. Scope Control — PASS WITH GATE**: No barcode, database lookup, sharing,
  extra nutrients, or accounts. Generic target suggestion content remains
  explicitly blocked pending Q-004a; do not invent values. Historical retention and
  date-edit behavior remain pending clarification and are not finalized by this plan.

### Post-Design Recheck

- Architecture and schema contain only Meal and singleton DailyTarget data; no
  user/account entity or external service is introduced.
- REST and data-model contracts preserve unset targets as null, apply date-scoped
  summaries without deleting other stored rows, and explicitly defer historical
  retention and date-edit decisions until clarified.
- The database file remains user data outside Git; test databases are temporary.
- The numeric suggestion policy is excluded from the base implementation until
  approved. This is a declared specification gate, not a silently chosen default.
- **Result: PASS for planning the resolved scope; FR-016 remains blocked on
  Q-004a before implementation or completion.**

## Architecture

### Components and Responsibilities

1. **React frontend**
   - Meal form collects the required fields and optional time/notes.
   - Today's meal list supports view, edit, and delete.
   - Target settings show configured values or an unset state and allow each
     measure to be set, changed, or cleared.
   - Daily summary displays totals and comparisons only for configured targets.
   - Shared API client translates validation responses into field-level guidance.
   - Responsive layout supports mobile and desktop browser viewports on the same
     device running the local application.

2. **FastAPI application**
   - Defines REST routes and Pydantic request/response schemas.
   - Validates boundary data and returns documented status/error responses.
   - Serves the built React assets in the local production-style run.
   - Binds only to `127.0.0.1`; never to a network interface.

3. **Business logic**
   - Validates domain constraints that depend on the selected local date.
   - Uses `Decimal` for non-negative numeric values and exact totals.
   - Computes the relevant date summary from saved meal rows and preserves the
     distinction between null/unset targets and numeric zero.
   - Coordinates record changes and summary recalculation.
   - Does not add automatic historical-meal deletion; retention beyond the active
     date remains a pending clarification.

4. **SQLite access**
   - Uses Python's built-in `sqlite3` and parameterized SQL.
   - Creates the small schema at startup with `CREATE TABLE IF NOT EXISTS`.
   - Opens connections per operation/request and uses transactions for writes.
   - Keeps the database in a per-user local application-data directory, never in
     the source tree or Git.

There is no separately deployed frontend server, authentication service, user
management, ORM, migration framework, or generalized repository framework.

### Processing Sequence

1. The user submits a meal or target change from React.
2. The frontend calls the same-origin `/api` route in a local production-style run;
   in development the local frontend server proxies only `/api` to FastAPI.
3. FastAPI parses the request into a Pydantic schema and rejects missing,
   malformed, out-of-range, or unsupported values before storage access.
4. The route/service validates current-date and domain rules, then calls the small
   SQLite data-access module using bound parameters and a transaction.
5. For summary requests, backend logic reads today's meals and configured targets,
   sums nutrition values with `Decimal`, and constructs the response.
6. FastAPI serializes the result; React updates the affected meal list, target
   settings, and/or summary from the response or a follow-up summary request.

### Business Logic

- The active date is determined by the local machine's timezone, but historical meal
  retention remains unresolved; the architecture does not delete prior-date rows by
  default.
- Meal category is one of Breakfast, Lunch, Dinner, or Snack. Quantity is positive,
  has at most two decimal places, and uses `serving`, `g`, or `ml`.
- Calories and protein are user-entered, non-negative decimals. Do not truncate or
  round stored inputs. No maximum value or fractional precision has been approved.
- Daily calories and protein are separate exact sums over the selected date's saved
  meals. An empty list yields zero for both. Do not aggregate through SQLite
  floating-point `SUM`.
- A valid edit replaces one saved meal and the next summary reflects the changed
  row; whether a saved meal's date may be edited remains an unresolved clarification.
  A delete removes the row and summary is derived again.
- Target values are independent nullable decimals. Null means unset; zero means a
  configured zero target. Updating or deleting one target must not alter the other.
- Do not return or display numeric generic suggestions until Q-004a is approved.
  The base targets API only stores values entered or explicitly accepted by the user.

## API Design

The full contract and schemas are in [`contracts/openapi.yaml`](./contracts/openapi.yaml).

| Method and path | Purpose | Request | Success response |
|---|---|---|---|
| `GET /api/meals` | List meals for the selected date | None | `200` array of Meal |
| `POST /api/meals` | Create a meal for the selected date | Meal input | `201` Meal |
| `GET /api/meals/{mealId}` | Retrieve a saved meal | Path ID | `200` Meal |
| `PUT /api/meals/{mealId}` | Replace editable meal fields | Meal input; date-edit policy remains unresolved | `200` Meal |
| `DELETE /api/meals/{mealId}` | Delete a meal | Path ID | `204` |
| `GET /api/targets` | Read current target settings | None | `200` Targets; unset values are null |
| `PUT /api/targets` | Set/replace both target fields | Targets object; null explicitly unsets | `200` Targets |
| `DELETE /api/targets/{measure}` | Clear only `calories` or `protein` | Measure path parameter | `204` |
| `GET /api/summary` | Read derived totals and target comparisons for the selected date | None | `200` DailySummary |

### Request and Response Shapes

- **Meal input**: `food_name`, `category`, positive `quantity_amount`,
  `quantity_unit`, non-negative `calories_kcal`, non-negative `protein_g`,
  `meal_date` (must match the selected or active date), optional `meal_time`,
  optional `notes`. Date-edit policy remains unresolved.
- **Meal**: Meal input plus integer `id`.
- **Targets**: `calories_kcal` and `protein_g`; each is a non-negative number or
  `null` when unset.
- **Daily summary**: `date`, `calories_kcal`, `protein_g`, and `targets`. No
  comparison value is implied for an unset target.
- **Errors**: `422` for request/domain validation with field paths and readable
  messages; `404` for unknown meal IDs; `500` for unexpected persistence failures
  with a generic user-facing message. Detailed database exceptions remain in local
  developer logs only and must not contain meal contents.
- **Suggestion API**: None in this plan. Numeric suggestions and their basis are
  pending Q-004a.

No endpoint is designed to auto-delete prior-date meals or to assume the app stores
only today's records. Invalid measure names are rejected as request validation
errors.

## Project Structure

### Documentation (this feature)

```text
specs/001-calorie-nutrition-tracker/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md                 # Created by /speckit-tasks, not by this plan
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── meals.py
│   │   ├── targets.py
│   │   └── summary.py
│   ├── schemas/
│   │   ├── meal.py
│   │   ├── targets.py
│   │   └── summary.py
│   ├── services/
│   │   ├── nutrition.py
│   │   └── retention.py
│   └── database/
│       ├── connection.py
│       ├── schema.sql
│       ├── meals.py
│       └── targets.py
├── tests/
│   ├── unit/
│   │   ├── test_nutrition.py
│   │   └── test_validation.py
│   └── integration/
│       ├── test_meals_api.py
│       ├── test_targets_api.py
│       ├── test_summary_api.py
│       └── test_retention.py
└── requirements.txt

frontend/
├── index.html
├── package.json
├── package-lock.json
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── api/
│   │   └── client.js
│   ├── features/
│   │   ├── meals/
│   │   │   ├── MealForm.jsx
│   │   │   ├── MealList.jsx
│   │   │   └── mealsApi.js
│   │   ├── targets/
│   │   │   ├── TargetSettings.jsx
│   │   │   └── targetsApi.js
│   │   └── summary/
│   │       ├── DailySummary.jsx
│   │       └── summaryApi.js
│   ├── styles/
│   │   └── app.css
│   └── test/
│       ├── setup.js
│       └── ...
├── vite.config.js
└── vitest.config.js
```

**Structure Decision**: Use one backend and one frontend directory, which keeps
React UI concerns separate from API/data concerns without introducing packages or
services. Keep schemas, route handlers, business calculations, and SQLite access in
separate small modules. Do not add a user model or target-suggestion module until
the corresponding requirement is approved.

## Validation and Error Handling

- **Missing required fields / invalid types / malformed date or time**: Pydantic
  returns `422` with field-specific paths/messages; React retains valid form values,
  marks the offending field, and explains correction.
- **Invalid nutrition values**: Reject non-numeric and negative values. Accept zero.
  Quantity must be positive, at most two decimal places, and in the allowed unit.
- **Invalid category/unit**: Enum validation returns `422`; SQLite `CHECK`
  constraints provide a final persistence boundary.
- **Date not today**: Reject with `422`; do not store user-selected past/future
  dates.
- **Missing meal ID**: Return `404`; do not alter the list or totals.
- **Database failure**: Roll back the write transaction, log the exception without
  meal data, return a generic `500`, and do not claim success.
- **Targets unset**: Serialize as `null`; omit target comparison in the UI. A
  numeric zero remains a valid configured target.
- **Numeric precision**: Preserve decimal input and sum with `Decimal`; do not
  invent maximums or fractional precision for calorie/protein/targets. Any range
  constraint needed for abuse prevention requires explicit review rather than
  silent behavioral limits.

## Security

- This is a local-only, single-user app with no account authentication. Do not
  claim account-level isolation or protection from other processes/users on the
  same machine.
- Bind Uvicorn to `127.0.0.1` only in development and local runs. Do not provide a
  configurable network bind address in the beginner-facing run path.
- In development, allow CORS only from the exact loopback frontend origin. In the
  built local app, serve the UI and API on the same origin.
- Restrict accepted Host/Origin values to the local app endpoints; do not enable
  wildcard CORS. Require JSON for writes and use standard browser protections;
  document that these controls do not equal authentication.
- Use bound SQL parameters, validate path IDs, keep the SQLite file outside Git
  with user-only filesystem permissions where supported, and exclude it from logs.
- Return generic server errors; never return SQL, file paths, stack traces, or
  stored meal details in error messages.
- Do not collect telemetry or share records. Do not expose the database through a
  static file route or network share.

## Testing Strategy

### Backend unit tests (pytest)

- Category, quantity, unit, date, and decimal validation, including missing,
  malformed, negative, zero, boundary and invalid precision cases.
- Daily totals for empty, one-meal, multi-meal, zero-value, edit, and delete cases.
- Null target versus configured zero, independent target updates/removal, and
  target persistence across date changes.
- Retention using an injected/fake local clock around midnight and a date change.

### SQLite and API integration tests (pytest + FastAPI TestClient)

- Use a fresh temporary SQLite file per test; never touch a developer's real DB.
- Verify meal create/list/get/update/delete status codes, stored values, and
  not-found behavior.
- Verify target GET/PUT/DELETE, null semantics, and summary comparisons.
- Verify request validation errors for absent fields, unsupported category/unit,
  invalid amounts, negative nutrition values, and non-today dates.
- Verify transaction rollback and generic error responses when storage operations
  fail.
- Verify startup/request cleanup of expired rows while preserving targets.
- Verify the application config binds to loopback and rejects non-local origins in
  its supported setup.

### Frontend tests and smoke validation

- Test meal form success, category/quantity constraints, field-level error display,
  retained input after rejection, and accessible labels.
- Test target unset/configured/zero/removed states and summary refresh after CRUD.
- Test responsive layouts at representative desktop and mobile viewport sizes on
  the same device.
- Run the end-to-end quickstart flow from [`quickstart.md`](./quickstart.md).
- Keep numerical target-suggestion tests out until Q-004a is approved; before that,
  verify the UI does not invent or display suggestion values.

## Development and Deployment

### Local Development

- Use Git for source history; commit dependency manifests and lockfiles, not local
  databases, virtual environments, build output, or secrets.
- The current workspace has no initialized Git repository; repository
  initialization is required before source changes can be versioned.
- Create a Python virtual environment and install FastAPI, Uvicorn, pytest, and
  test-client dependencies from the pinned backend requirements.
- Install React and the frontend dev/build/test dependencies with npm from the
  checked-in package manifest and lockfile.
- Run FastAPI on loopback with reload enabled only for development. Run the
  frontend dev server on loopback with an `/api` proxy to FastAPI.
- Store the SQLite file in the user's platform application-data directory; permit
  an explicit development-only override for isolated tests, not a network path.

### Local Run

- Build the React assets and serve them from FastAPI for a one-process local run.
- Start the app bound to `127.0.0.1`; open it in a browser on the same device.
- No internet service, hosted database, accounts, CORS wildcard, or remote-device
  access is part of deployment.
- The repository currently contains planning files only. Dependency manifests,
  run scripts, ignore rules, and application code are implementation deliverables,
  not created by this planning command.

## Requirements Traceability

| Requirements | Planned components | Verification |
|---|---|---|
| FR-001–003, FR-013; BR-002, BR-003, BR-009–010; AC-001–006, AC-022 | Meal form; meal schemas and service; `Meal` table | UI form tests; Pydantic validation; create API and DB tests; user-provided data labeling |
| FR-004–005; BR-001, BR-004–005; AC-007–008, AC-021, AC-027 | Today-only meal/summary routes; date service; summary calculation | FR-004 date rejection and FR-005 total tests; local date rollover test |
| FR-006; BR-007–008; AC-009, AC-011 | Meal edit control; update route and DB transaction | FR-006 update test; totals after edit; invalid edit leaves row unchanged |
| FR-007; BR-005, BR-007; AC-010 | Meal delete control; delete route and DB transaction | FR-007 deletion test; totals after deletion and empty-day case |
| FR-008, FR-014; BR-006; AC-012–014 | Target settings; target route/schema; singleton `DailyTarget` | FR-008 configuration tests; null/zero distinction and progress UI/API tests |
| FR-009; BR-006; AC-012–014 | Daily summary target comparison | FR-009 unset/configured/zero target comparisons |
| FR-017; BR-006; AC-025 | Target clear action; target delete route | FR-017 removes only selected measure; other target remains unchanged |
| FR-010, FR-015; AC-015, AC-020, AC-026 | Responsive React UI; loopback app configuration | Desktop/mobile viewport checks; non-local reachability/config tests |
| FR-011; NFR-003; AC-004–005, AC-011, AC-017, AC-022 | Pydantic schemas; frontend error mapping | Invalid input matrix and field feedback tests |
| FR-012; BR-012; AC-016, AC-024, AC-027 | Retention service and local date rollover | Controlled-clock tests; prior-date deletion and target retention |
| FR-016; BR-011; AC-023 | Deferred until suggestion values and basis are approved | Q-004a gate; no invented suggestions before approval |
| NFR-001, NFR-006; AC-015, AC-026 | Responsive React layout | Manual/component tests at representative viewport sizes |
| NFR-002; AC-007 | `Decimal` aggregation service | Exact comparison of totals with persisted meal values |
| NFR-004; AC-018, AC-020, AC-026 | Local-only deployment, no accounts or telemetry | Configuration review; no network binding or data-sharing feature |
| NFR-005; AC-019 | One frontend, one backend, one local DB | Review all dependencies/components against a stated requirement |

### Constitution Principles

| Principle | Design and validation enforcement |
|---|---|
| I. Simplicity First | One local process for packaged use; built-in `sqlite3`; no ORM or distributed service. |
| II. User-Centric Design | Meal, target, and daily summary components; responsive same-device browser tests. |
| III. Data Accuracy and Integrity | Decimal string persistence and `Decimal` sums; CRUD and empty-state tests. |
| IV. Requirements Traceability | Traceability matrix above maps each requirement family to components and tests. |
| V. Maintainability | Small modules by responsibility and focused unit/API/frontend tests. |
| VI. Input Validation and Error Handling | Pydantic boundary schemas, service rules, explicit 404/422/500 behavior, field feedback. |
| VII. Privacy and Security | Loopback binding, restricted CORS, parameterized SQL, local DB outside Git, no telemetry. |
| VIII. Scope Control | No accounts, external food lookup, extra nutrients, or suggestions before Q-004a approval. |

## Open Decisions and Gates

- **Q-004a — Generic target suggestion values and basis**: The specification
  requires suggestions, but no values or approved basis are defined. Do not
  implement or seed suggestions until approved. Meal CRUD, user-configured targets,
  and summaries do not depend on this decision.
- **Nutrition/target numeric bounds and display precision**: The specification
  defines non-negative values but not upper bounds or fractional precision. Store
  and calculate exact decimals; do not silently cap or round. Agree any display
  formatting that changes visible values before implementation.
- **Operational performance/availability targets**: None are specified. The plan
  does not add numeric service-level objectives for a local single-user app.

## Complexity Tracking

No constitution violations are proposed. The separate React frontend and FastAPI
backend are the user-approved stack; SQLite and the local loopback deployment keep
the architecture within a single-user application's scope. No exception table is
required.
