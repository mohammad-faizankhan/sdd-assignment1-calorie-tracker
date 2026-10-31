# Calorie and Nutrition Tracker

## Overview

The Calorie and Nutrition Tracker is a planned local, single-user web application for manually tracking food intake, daily calories, and protein. It is intended to help a person record meals, review selected-date summaries, and compare intake against optional personal targets without using external nutrition services or creating user accounts.

This repository is in the Spec-Driven Development planning and review stage and contains the governing constitution, feature specification, technical plan, task breakdown, validation matrix, and project documentation. No implementation source code has been generated in this repository.

## Objectives

The approved V1 objectives are to:

- allow users to manually record meals with valid required information
- support selected-date meal review and daily calorie/protein totals
- preserve historical records and allow access to previous dates
- support meal editing, including date changes, and deletion with confirmation
- allow optional calorie and protein target configuration
- keep the application responsive for desktop and mobile browsers on the same device
- maintain a simple local single-user architecture with no authentication or multi-user access

## Planned V1 features

- Manual meal entry
- Meal categories: Breakfast, Lunch, Dinner, Snack
- Calorie and protein tracking for manually entered meal values
- Daily nutrition summaries by selected date
- Optional daily calorie and protein targets configured by the user
- Historical retention and previous-date meal access
- Meal viewing, editing, and deletion
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

These technologies support the planned local single-user architecture and validation workflow.

## Project structure

```text
assignment-1/
├── .specify/
│   ├── memory/
│   ├── scripts/
│   ├── templates/
│   ├── workflows/
│   └── ...
├── docs/
│   ├── clarification-log.md
│   ├── prompt-log.md
│   ├── review-record.md
│   └── validation-plan.md
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
└── (no source-code implementation directories are present yet)
```

## Prerequisites

Planned implementation prerequisites include:

- Python with a supported version selected during setup
- Node.js and npm
- Git
- A local virtual environment for Python-based development work

No runtime directories or dependency manifests are present yet because the project is still in the planning and baseline stage.

## Setup and installation

The project artifacts describe the planned setup flow as follows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
npm --prefix frontend install
```

These are planned commands only and are not claimed to have been executed in this repository.

## Running the application

Planned local execution:

```powershell
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
npm --prefix frontend run dev -- --host 127.0.0.1
```

The app is intended to run locally on the same device and is not planned for deployment as a shared multi-user service.

## Running tests

Planned test commands for implementation:

- Backend tests: `pytest`
- Frontend tests: `npm --prefix frontend test -- --run`
- Frontend build: `npm --prefix frontend run build`

No implementation code or recorded test results are present yet.

## Spec-Driven Development process

This project follows the Spec Kit workflow:

- Constitution establishes the governing principles.
- Specification captures business requirements and acceptance criteria.
- Clarification records the approved decisions and preserves the historical record.
- Technical planning maps the approved scope to implementation architecture.
- Task breakdown converts the approved plan into structured work.
- Validation planning defines the tests for required scenarios.
- Implementation is intentionally deferred until the approved baseline is established and the project is ready for execution.

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

The project has reached the approved SDD Baseline v1.0.0 at the planning layer. The repository contains the approved specification, plan, tasks, validation matrix, and documentation. The project is not yet an implementation codebase and no application source code has been generated.

## Future enhancements

These enhancements remain outside the approved V1 scope and should only be introduced after explicit approval:

- food database integration or external nutrition lookup
- barcode scanning
- personalized or medical nutrition recommendations
- multi-user or authenticated access
- advanced analytics beyond date-scoped totals
- backup and recovery beyond the local single-user scope

## Final status

The repository is ready as a planning baseline for implementation, but it remains a documentation-first project until execution begins under the approved V1 scope.
