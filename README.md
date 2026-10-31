# Calorie and Nutrition Tracker

## Overview

The Calorie and Nutrition Tracker is a local, single-user web application for manually tracking meals, calories, protein, and optional daily targets. It supports selected-date meal review, historical meal retention, edit/delete workflows, and responsive browser usage on the same device.

This repository contains both the governing SDD artifacts and the implementation for the approved V1 baseline. The app is intentionally local-only and does not include authentication, multi-user support, external nutrition lookups, or meal auto-deletion.

## Objectives

The approved V1 objectives are to:

- allow users to manually record meals with valid required information
- support selected-date meal review and daily calorie/protein totals
- retain historical meal records and allow access to previous dates
- support meal editing, including date changes, and deletion with confirmation
- allow optional calorie and protein target configuration
- keep the application responsive for desktop and mobile browsers on the same device
- maintain a simple local single-user architecture with no authentication or multi-user access

## Included V1 features

- Manual meal entry
- Meal categories: Breakfast, Lunch, Dinner, Snack
- Calorie and protein tracking for manually entered meal values
- Daily nutrition summaries by selected date
- Optional daily calorie and protein targets configured by the user
- Historical retention and previous-date meal access
- Meal viewing, editing, and deletion with confirmation
- Responsive browser interface for desktop and mobile browsers
- Data stored locally in SQLite on the same device

## Explicitly excluded from V1

- Food database lookup
- External nutrition API usage
- Barcode scanning
- Default numeric target suggestions
- Login, registration, roles, and multi-user support
- Automatic cleanup or expiration of old meal records
- Personalized or medical nutrition recommendations

## Technology stack

The approved implementation stack is:

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

## Project structure

```text
assignment-1/
├── .specify/
│   ├── memory/
│   ├── scripts/
│   ├── templates/
│   ├── workflows/
│   └── ...
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── docs/
│   ├── clarification-log.md
│   ├── prompt-log.md
│   ├── review-record.md
│   └── validation-plan.md
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── specs/
│   └── 001-calorie-nutrition-tracker/
│       ├── contracts/
│       ├── data-model.md
│       ├── plan.md
│       ├── quickstart.md
│       ├── research.md
│       ├── spec.md
│       └── tasks.md
├── README.md
├── .venv/
└── .gitignore
```

## Prerequisites

Required to run the application locally:

- Python 3.13 or compatible version
- Node.js and npm
- Git
- A local Python virtual environment

## Setup and installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
npm --prefix frontend install
```

## Running the application

Start the backend:

```powershell
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

Start the frontend:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1
```

The app is intended to run locally on the same device and is not intended for shared multi-user deployment.

## Running tests

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q

cd ..
npm --prefix frontend test -- --run
npm --prefix frontend run build
```

## Spec-Driven Development workflow

This project follows the Spec Kit workflow:

- Constitution establishes the governing principles.
- Specification captures business requirements and acceptance criteria.
- Clarification records approved decisions and preserves the historical record.
- Technical planning maps the approved scope to the architecture.
- Task breakdown converts the plan to executable work.
- Validation planning defines the expected scenarios and edge cases.
- Implementation proceeds under the approved baseline only.

## Documentation

Relevant project files:

- [.specify/memory/constitution.md](.specify/memory/constitution.md)
- [specs/001-calorie-nutrition-tracker/spec.md](specs/001-calorie-nutrition-tracker/spec.md)
- [specs/001-calorie-nutrition-tracker/plan.md](specs/001-calorie-nutrition-tracker/plan.md)
- [specs/001-calorie-nutrition-tracker/tasks.md](specs/001-calorie-nutrition-tracker/tasks.md)
- [docs/clarification-log.md](docs/clarification-log.md)
- [docs/review-record.md](docs/review-record.md)
- [docs/validation-plan.md](docs/validation-plan.md)
- [docs/prompt-log.md](docs/prompt-log.md)

## Current project status

The repository contains the approved SDD baseline and a working local implementation of the V1 application. The implemented features match the approved scope and business decisions, and the current automated checks pass.

## Future enhancements

These enhancements remain outside the approved V1 scope and should only be introduced after explicit approval:

- food database integration or external nutrition lookup
- barcode scanning
- personalized or medical nutrition recommendations
- multi-user or authenticated access
- advanced analytics beyond date-scoped totals
- backup and recovery beyond the local single-user scope

## Final status

The project is implemented according to the approved local-only V1 scope and is ready for local validation and further refinement under the documented baseline.
