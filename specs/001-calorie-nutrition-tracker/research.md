# Research: Calorie and Nutrition Tracker

## Decisions

### Application shape

- **Decision**: Use one local React frontend and one FastAPI process backed by one
  SQLite file. Serve the production React build from FastAPI so the shipped local
  application has one origin and one process to start.
- **Rationale**: The product is single-user, local-only, and small. This avoids
  distributed services, a hosted database, accounts, and production CORS
  configuration. During development, run the React and FastAPI dev servers on
  loopback and allow only the exact development origin.
- **Alternatives considered**: A shared hosted API/database would expose one
  account-free dataset to multiple users and contradict the approved local-only
  access model. A separate static hosting service would add deployment complexity.
- **Sources**: [SQLite appropriate uses](https://www.sqlite.org/whentouse.html);
  [Uvicorn socket binding](https://github.com/encode/uvicorn/blob/master/docs/settings.md#socket-binding);
  [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/).

### Frontend structure

- **Decision**: Use React components aligned to the meal form, meal list, target
  settings, and daily summary. Keep state near its consumers and share only summary
  and target state where needed. Use Vite for the dev server and production build,
  and Vitest with React Testing Library for focused component interaction tests;
  exact dependency versions are selected and pinned during implementation.
- **Rationale**: The interface has a few clear screens and does not need a global
  state-management library. The browser remains responsive at desktop and mobile
  viewport sizes on the same device as the local app.
- **Alternatives considered**: A general state-management framework or separate
  frontend runtime service is not justified by this scope.
- **Sources**: [React: Thinking in React](https://react.dev/learn/thinking-in-react);
  [React: Sharing State](https://react.dev/learn/sharing-state-between-components);
  [React: Choosing State Structure](https://react.dev/learn/choosing-the-state-structure);
  [Vite Guide](https://vite.dev/guide/);
  [Vitest Guide](https://vitest.dev/guide/).

### Backend and SQLite access

- **Decision**: Use FastAPI request/response models for API validation and Python's
  built-in `sqlite3` for parameterized, transactional database operations. Keep
  routes, validation/business calculations, and database access in small, separate
  backend modules. Scope connections to an operation/request rather than sharing a
  global connection.
- **Rationale**: SQLite is a single-file, no-administration store appropriate for
  this local single-user application. The built-in driver avoids an ORM and extra
  dependencies. Daily totals use Python `Decimal` arithmetic over the day's stored
  decimal strings rather than SQLite floating-point aggregation.
- **Alternatives considered**: A client/server database, ORM, and generalized
  repository framework introduce infrastructure or indirection not needed by the
  current data model.
- **Sources**: [SQLite appropriate uses](https://www.sqlite.org/whentouse.html);
  [Python sqlite3 parameter binding](https://docs.python.org/3/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries).

### REST validation and errors

- **Decision**: Define explicit Pydantic request/response models, rely on FastAPI
  field-level validation for invalid requests (HTTP 422), return 404 for absent
  meal IDs, 201 for meal creation, 204 for successful deletion, and a generic 500
  message for unexpected database failures. Do not expose SQL or exception details.
- **Rationale**: These status codes directly represent the specified operations and
  give the React UI actionable validation information without custom error
  abstractions.
- **Alternatives considered**: A custom error envelope is unnecessary unless the
  frontend later demonstrates a concrete need for one.
- **Sources**: [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/);
  [FastAPI error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/).

### Local access and privacy

- **Decision**: Bind FastAPI and the production static app to `127.0.0.1`; never use
  `0.0.0.0`. In development, bind the frontend dev server to loopback and permit
  only that exact origin. Store SQLite data outside the repository in a
  per-user application-data directory.
- **Rationale**: This enforces the approved no-accounts, single-user, same-device
  boundary. Loopback binding limits network reachability; it is not authentication
  against other processes or users on the same machine. Development CORS is
  restricted to the known local frontend origin.
- **Alternatives considered**: Network binding would allow other devices/users to
  reach personal meal data without authentication and is out of scope.
- **Sources**: [Uvicorn socket binding](https://github.com/encode/uvicorn/blob/master/docs/settings.md#socket-binding);
  [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/).

### Testing and local development

- **Decision**: Use pytest for backend unit, SQLite integration, and FastAPI
  `TestClient` tests. Use pytest temporary directories for isolated database files.
  Add focused React interaction tests with Vitest and Testing Library; versions
  are pinned with the implementation dependencies.
  Exclude the virtual environment and SQLite data file from Git.
- **Rationale**: This covers decimal calculations, API validation/status codes,
  database changes, and user-visible interactions without introducing end-to-end
  infrastructure. Run the frontend and backend locally during development, with
  Uvicorn reload limited to development.
- **Alternatives considered**: Distributed browser test infrastructure is
  unnecessary for the current single-device feature; manual responsive smoke tests
  complement component tests.
- **Sources**: [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/);
  [pytest tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html);
  [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/);
  [Python venv](https://docs.python.org/3/library/venv.html);
  [Uvicorn settings](https://www.uvicorn.org/settings/);
  [Git ignore](https://git-scm.com/docs/gitignore).

## Open Decision — Target Suggestion Content

The specification requires optional generic target suggestions, but numeric values
and their approved basis remain pending under Q-004a. This plan does not choose
values, source nutrition advice, or calculate recommendations. The main meal and
user-configured target features can proceed, but FR-016 remains blocked until the
suggestion content and basis are approved. No suggestion endpoint, seeded default,
or personalized calculation is included in the base design.

## Version Selection

The proposed technologies are retained. The specification does not mandate exact
runtime/library versions. Implementation must select supported, mutually compatible
versions and record them in the Python dependency manifest/lock approach and
JavaScript package lockfile before coding.
