# Quickstart: Calorie and Nutrition Tracker

This guide describes the planned local development and acceptance workflow. It does
not create application code or dependencies.

## Prerequisites

- Python with a supported version selected and pinned during implementation.
- Node.js and npm for the React development server and build.
- Git.

## Planned Local Setup

1. Clone the repository and create/activate a Python virtual environment.
2. Install the backend dependencies from the implementation's pinned requirements
   file.
3. Install frontend dependencies from the frontend package manifest.
4. Start FastAPI bound only to `127.0.0.1`; start the React development server
   bound only to loopback and proxy `/api` requests to FastAPI.
5. Open the development URL in a browser on the same device. Do not bind the API
   to `0.0.0.0` or expose the SQLite file to a shared/multi-user service.

For the planned production-style local run, build React assets and serve the static
build from the same FastAPI process, still bound to loopback. Keep the SQLite
database outside the repository in a per-user local application-data directory.

Once the planned manifests and modules exist, the intended command shape from the
repository root is:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
npm --prefix frontend install
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

In a second terminal, start the frontend development server:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1
```

The exact script names and commands must be checked in with the implementation
manifests. The backend command without `--reload` is the planned local run after
building the frontend bundle.

## Planned Validation Commands

The intended checks are:

- Backend unit and API tests: `pytest`
- Frontend tests: `npm --prefix frontend test -- --run`
- Production frontend build: `npm --prefix frontend run build`
- End-to-end smoke: start the local app and exercise the scenarios below.

## Acceptance Smoke Scenarios

1. Open today's summary with no meals and verify both totals are zero and targets
   are unset.
2. Submit an invalid meal (missing name, unsupported category, zero/negative
   quantity, invalid amount, or a date other than today) and verify actionable
   field-level feedback with no saved record.
3. Create valid meals in each category and verify exact daily totals.
4. Edit a meal's amount and delete another; verify totals update after each action.
5. Configure and clear calorie/protein targets; verify unset values are not
   displayed as zero and configured zero is distinguishable from unset.
6. Cross the local date boundary or use a controlled clock in a test; verify
   yesterday's meal records are removed and configured targets remain.
7. Test responsive layout on desktop and mobile browsers running on the same device;
   verify another device cannot connect to the loopback-bound application.
8. Verify no generic numerical target suggestions appear until Q-004a is approved.

## Detailed References

- REST request/response definitions: [`contracts/openapi.yaml`](./contracts/openapi.yaml)
- Entity and lifecycle rules: [`data-model.md`](./data-model.md)
- Requirements and acceptance criteria: [`spec.md`](./spec.md)
