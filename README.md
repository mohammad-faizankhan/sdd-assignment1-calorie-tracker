# Calorie and Nutrition Tracker

## 1. Project Overview

The Calorie and Nutrition Tracker is a planned single-user, browser-accessible web application for manually logging food intake and reviewing daily calorie and protein totals. The application is intended to help an individual record meals, monitor daily nutrition intake, and compare intake with optional daily targets without relying on external nutrition services or authentication.

This project is currently in the Spec-Driven Development planning stage. The repository contains the governing constitution, feature specification, technical plan, task breakdown, and supporting documentation, but the application source code and test suites have not yet been created.

## 2. Objectives

The documented objectives are to:

- allow a user to record meals with required nutrition information and optional notes/time
- provide a simple daily summary of calories and protein
- support optional daily target configuration and comparison
- maintain a responsive local web interface for desktop and mobile browser viewports on the same device
- keep the solution local, simple, and scoped to a single user without introducing accounts or a shared backend

## 3. Features

### Planned V1 features

- Manual meal entry
- Meal categories: Breakfast, Lunch, Dinner, and Snack
- Calorie and protein tracking for manually entered meals
- Daily nutrition summaries by date
- Optional daily nutrition targets
- Meal viewing, editing, and deletion
- Responsive browser interface for desktop and mobile browsers on the same device

### Not yet implemented

The following items are planned but not implemented in the current repository state:

- backend application code
- frontend application code
- database schema and API implementation
- automated tests and build configuration

The repository currently documents the planned work rather than delivering the application itself.

## 4. Technology Stack

The technical plan identifies the following technologies:

- React: frontend UI library for the browser interface
- Vite: frontend development/build tooling
- FastAPI: Python REST API framework
- Pydantic: request and response validation in the backend
- SQLite: local single-user data storage
- Python sqlite3: database access layer
- Uvicorn: ASGI server for the FastAPI app
- pytest: backend test framework
- Vitest and React Testing Library: frontend interaction testing
- Git: version control

These technologies are documented as the selected implementation approach for the planned local app. No code has been generated yet.

## 5. Project Structure

The current repository contains the Spec Kit and documentation artifacts, and does not yet include an implemented frontend or backend application structure.

```text
assignment-1/
├── .github/
│   └── skills/
├── .specify/
│   ├── .gitignore
│   ├── feature.json
│   ├── init-options.json
│   ├── integration.json
│   ├── integrations/
│   ├── memory/
│   ├── scripts/
│   ├── templates/
│   └── workflows/
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
└── (no implemented source-code or test directories are present yet)
```

## 6. Prerequisites

The planned prerequisites documented in the project artifacts are:

- Python with a supported version selected and pinned during implementation
- Node.js and npm
- Git

The technical plan also indicates the project will use a local Python virtual environment and a frontend package installation flow using npm.

## 7. Setup and Installation

The project documentation includes the planned setup flow. Based on the technical plan and quickstart, the intended installation sequence is:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
npm --prefix frontend install
```

These are planned commands for the implementation phase and are not validated in the current repository state because the backend and frontend project directories are not present yet.

## 8. Running the Application

The project quickstart describes the intended local run workflow:

1. Start the backend API with FastAPI bound to `127.0.0.1`.
2. Start the frontend development server on loopback.
3. Open the local app in a browser on the same device.

Planned backend command:

```powershell
uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

Planned frontend command:

```powershell
npm --prefix frontend run dev -- --host 127.0.0.1
```

These commands are documented as the planned local development workflow and have not been executed in this repository as part of the current planning artifacts.

## 9. Running Tests

The technical plan and quickstart document the following validation commands:

- Backend tests: `pytest`
- Frontend tests: `npm --prefix frontend test -- --run`
- Frontend production build: `npm --prefix frontend run build`

No test results are recorded in the repository for these commands. The project currently serves as a planning and specification artifact set rather than a running implementation.

## 10. Spec-Driven Development Process

This project follows the Spec Kit workflow and is organized around a structured development process:

- Constitution: defines the governing principles for simplicity, data integrity, traceability, privacy, security, and scope control
- Specification: captures user-visible requirements, behaviors, and acceptance criteria
- Clarification: records business questions, accepted decisions, and unresolved items
- Technical planning: translates approved requirements into a simple local architecture and implementation strategy
- Task breakdown: organizes the implementation work into structured phases and task references
- Analysis: reviews specification and planning artifacts for gaps, ambiguities, and inconsistencies
- Implementation: intended to follow the approved plan and acceptance criteria, once the final decisions are approved
- Validation: tests the acceptance scenarios and confirms requirements are satisfied

## 11. Documentation

Relevant documents in this repository include:

- [docs/clarification-log.md](docs/clarification-log.md)
- [docs/review-record.md](docs/review-record.md)
- [docs/validation-plan.md](docs/validation-plan.md)
- [docs/prompt-log.md](docs/prompt-log.md)
- [specs/001-calorie-nutrition-tracker/spec.md](specs/001-calorie-nutrition-tracker/spec.md)
- [specs/001-calorie-nutrition-tracker/plan.md](specs/001-calorie-nutrition-tracker/plan.md)
- [specs/001-calorie-nutrition-tracker/tasks.md](specs/001-calorie-nutrition-tracker/tasks.md)
- [specs/001-calorie-nutrition-tracker/quickstart.md](specs/001-calorie-nutrition-tracker/quickstart.md)
- [specs/001-calorie-nutrition-tracker/data-model.md](specs/001-calorie-nutrition-tracker/data-model.md)
- [specs/001-calorie-nutrition-tracker/research.md](specs/001-calorie-nutrition-tracker/research.md)
- [.specify/memory/constitution.md](.specify/memory/constitution.md)

## 12. Current Project Status

The project is currently in the planning and review stage of the Spec-Driven Development lifecycle.

Current status:

- feature specification is in draft form
- technical plan and task breakdown are documented
- clarification log preserves unresolved business decisions
- README and supporting documentation were created for project traceability
- source code, dependency manifests, and application runtime directories are not yet present

This means the project is not yet built, validated, or ready for implementation approval unless the remaining unresolved business decisions are confirmed.

## 13. Future Enhancements

The following are reasonable future enhancements, but they are outside the current V1 scope as stated in the project specification:

- food database lookup or external nutrition API integration
- barcode scanning or automatic nutrition estimation
- social sharing or meal-plan features
- personalization or medical/nutrition-advice features
- additional tracked nutrients beyond calories and protein
- multi-user or authenticated access

## Summary

This repository currently functions as a specification and planning workspace for the Calorie and Nutrition Tracker. It documents the intended local, single-user, responsive nutrition tracking product, but it does not yet include an implemented application or successful validation results.

This README is therefore an accurate project overview for the current planning stage, not a claim of completed implementation.
