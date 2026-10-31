# Feature Specification: Calorie and Nutrition Tracker

**Feature Branch**: `001-calorie-nutrition-tracker`

**Created**: 2026-10-31

**Status**: Draft

**Input**: User-provided business objective and agreed decisions for a simple, responsive
Calorie and Nutrition Tracker.

## Overview

The product is a browser-accessible web application for individuals to manually record
food intake, track daily calories and protein, optionally configure daily nutrition
targets, and view progress. Nutrition values are user-entered; the application does
not verify them against an external source.

The application is intended for individuals who want a straightforward record of
their food intake and a clear view of calorie and protein totals. It is not a
clinical, diagnostic, or nutrition-advice product.

## Clarifications

### Session 2026-10-31

- Q: How should the tracker handle user identity and access to saved records? → A:
  No accounts; one user's records are available in that browser/profile.
- Q: Which dates should users be able to view and manage? → A: Current date only.
- Q: How should users enter meal quantity or serving size, and which units should
  the tracker support? → A: A positive numeric amount with up to 2 decimal places,
  using serving(s), g, or ml.
- Q: Should the tracker suggest daily calorie or protein targets, or only use
  targets that users enter themselves? → A: Show optional, generic target
  suggestions that users may accept or change.
- Q: How long should meal records and configured targets be kept? → A: Remove meal
  records at the end of each day; keep targets until the user changes or removes
  them.
- Q: With FastAPI and SQLite but no accounts, how should meal data be separated if
  multiple browser profiles access the same deployed application? → A: Run a local,
  single-user instance; do not expose one shared database to multiple users.
- Q: Given the local single-user deployment, how should the mobile-browser
  requirement work? → A: Support responsive mobile layouts, but access the local app
  only on the device running it.
- Q: Which timezone should define “today” and the end-of-day deletion boundary for
  this local tracker? → A: The local machine's timezone.

### Open Clarification Log

- **Q-001a — Historical meal retention**: Whether meal records from prior dates must
  remain visible, editable, and queryable is still unresolved. Planning must not
  assume automatic deletion of older meal records or that only today's meals may be
  stored. Daily summaries remain scoped to the selected date without deleting other
  stored records.
- **Q-001b — Meal date editing**: Whether a saved meal's date may be changed after
  creation is unresolved. The planning baseline must not impose a hard lock on date
  edits until the business owner approves the behavior.

### Business Objective

Enable users to record their meals and understand daily calorie and protein intake
and, when configured, compare intake with daily targets.

### Scope

- Manually create meal records containing the agreed meal fields.
- Display the predefined meal categories.
- View today's meal records and daily calorie and protein totals.
- Edit and delete existing meal records.
- Configure and modify optional daily calorie and protein targets.
- Compare daily intake with configured targets.
- Support responsive use in desktop and mobile browsers.
- Allow mobile browser use only on the device running the local instance; access
  from other devices is not included.

### Out of Scope

- Food database lookup, barcode scanning, or automatic nutrition estimation.
- Social sharing, meal plans, personalized nutrition recommendations, or medical
  advice.
- Tracking nutrients other than calories and protein unless scope is approved later.
- User registration and authentication; the first version has no accounts and is
  intended for one user's records in a local, single-user instance.
- Any particular technology stack, storage architecture, or deployment platform.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Record Meals and Review Daily Intake (Priority: P1)

As an individual tracking nutrition, I want to record a meal and see its calories
and protein included in daily totals so that I can understand what I have consumed.

**Why this priority**: Manual meal recording and accurate daily totals are the
application's core value.

**Independent Test**: Enter one valid meal, then verify its details and the matching
calorie and protein totals in the daily view.

**Acceptance Scenarios**:

1. **Given** a user has entered all required meal information,
   **When** they save the meal,
   **Then** the meal is recorded with its entered values and included in the applicable
   day's totals (AC-001, AC-003, AC-007).
2. **Given** today has no recorded meals,
   **When** the user views today's nutrition progress,
   **Then** the meal list is empty and calorie and protein totals are zero (AC-008).
3. **Given** a meal record contains manually entered nutrition values,
   **When** the user views the record,
   **Then** the application presents those values as user-provided rather than
   independently verified facts (AC-003).

### User Story 2 - Correct or Remove a Meal (Priority: P2)

As an individual tracking nutrition, I want to edit or delete a previously recorded
meal so that my daily record and totals remain accurate.

**Why this priority**: Users need to correct mistakes and keep calculated totals in
sync with their records.

**Independent Test**: Create a meal, change its nutrition values and verify the
updated totals, then delete it and verify the totals are recalculated.

**Acceptance Scenarios**:

1. **Given** a saved meal, **When** the user saves valid edits,
   **Then** the meal reflects the edited values and every affected daily total is
   recalculated (AC-009).
2. **Given** a saved meal, **When** the user deletes it,
   **Then** it is no longer included in the meal list or daily totals (AC-010).
3. **Given** an edit contains invalid information,
   **When** the user attempts to save it,
   **Then** the edit is rejected, the problem is identified, and the saved record
   remains unchanged (AC-004, AC-011).

### User Story 3 - Set Targets and Compare Progress (Priority: P3)

As an individual tracking nutrition, I want to configure or change optional daily
calorie and protein targets so that I can compare my intake with my chosen goals.

**Why this priority**: Targets add useful context, but the application must remain
usable for people who do not set targets.

**Independent Test**: View a day without targets, configure targets, and verify that
the view compares the day's totals against the configured values.

**Acceptance Scenarios**:

1. **Given** no daily target has been configured,
   **When** the user views daily nutrition progress,
   **Then** meal recording and totals remain available and no target comparison is
   shown as though the target were zero (AC-012).
2. **Given** a user has configured a daily target,
   **When** they view that day's progress,
   **Then** intake is compared with the applicable configured target (AC-013).
3. **Given** a user changes a target,
   **When** the change is saved,
   **Then** the progress comparison uses the changed target without altering meal
   records or totals (AC-014).

### User Story 4 - Use the Tracker on Desktop or Mobile (Priority: P2)

As a user on a desktop or mobile browser, I want the core tracker tasks to remain
usable so that I can record and review meals on either device class.

**Why this priority**: Responsive browser access is an agreed platform requirement
for all core user journeys.

**Independent Test**: Complete meal entry and daily progress review in desktop and
mobile browser viewports and verify that all required fields and actions remain
available.

**Acceptance Scenarios**:

1. **Given** the application is open in a desktop or mobile browser,
   **When** the user records a meal or reviews daily progress,
   **Then** the controls and content remain readable and usable without losing
   required information (AC-015).

### Edge Cases

- A meal with zero calories or zero protein is valid; negative or non-numeric
  nutrition values are not.
- An empty day has zero totals and no meal records.
- Multiple meals on the same date are each included exactly once in that date's
  totals.
- Meal date handling remains unresolved; the date for a saved meal may be subject to
  future clarification, and the plan must not impose a hard date lock.
- Deleting the only meal recorded on a selected date leaves zero totals for that date.
- A date, category, food name, or quantity/serving is missing or invalid.
- Optional time or notes are omitted; omitting either does not prevent saving.
- A configured target is zero, invalid, or absent; zero is distinct from absent, and
  invalid values are rejected.
- A user attempts to save after a validation error; other valid form values remain
  available for correction where practical.
- Date navigation and historical retention remain unresolved and must not be
  implemented as a hard restriction to the current date until the business owner
  approves the required behavior.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow a user to manually enter a meal with a required
  food name, meal category, quantity/serving amount and unit, calories in kcal,
  protein in grams, and date. Quantity MUST be a positive numeric amount with no
  more than 2 decimal places and a unit of serving(s), g, or ml. Time and notes MUST
  be optional.
- **FR-002**: The meal category control MUST provide exactly these predefined
  categories: Breakfast, Lunch, Dinner, and Snack.
- **FR-003**: The system MUST save a meal only when all required fields are present
  and valid, and MUST retain the values entered by the user.
- **FR-004**: The system MUST allow users to view saved meal details and daily
  calorie and protein totals for the relevant date in the active selection. Meal
  entry and summary calculations remain date-scoped; the historical retention policy
  is unresolved and must not assume automatic deletion of older meal records or a
  hard restriction to today's stored meals only.
- **FR-005**: The system MUST calculate daily calorie and protein totals from the
  applicable saved meals, counting each meal once.
- **FR-006**: The system MUST allow a user to edit a saved meal and MUST recalculate
  totals for any affected dates after a valid edit.
- **FR-007**: The system MUST allow a user to delete a saved meal and MUST recalculate
  its date's totals after deletion.
- **FR-008**: The system MUST allow a user to configure and modify daily calorie and
  protein targets; targets MUST remain optional.
- **FR-009**: When a relevant target is configured, the system MUST compare the
  applicable daily intake with that target. An unset target MUST NOT be represented
  as zero.
- **FR-010**: The system MUST support the core meal entry and daily progress journeys
  in desktop and mobile browsers using a responsive presentation. Browser access
  MUST be limited to the device running the local instance.
- **FR-011**: The system MUST identify invalid fields and explain how the user can
  correct them. A rejected create or edit MUST NOT corrupt or partially replace
  existing saved data.
- **FR-012**: The system MUST preserve saved meal records for subsequent access,
  until the end of the current date, then remove those meal records. Configured
  targets MUST persist until the user changes or removes them.
- **FR-013**: The system MUST NOT use an external food database, barcode scanning, or
  automatic nutrition lookup to populate meal values.
- **FR-014**: The system MUST NOT require a user to configure targets before recording
  meals or viewing totals.
- **FR-015**: The system MUST NOT require registration or authentication; saved
  records are for one user within a local, single-user instance and MUST NOT be
  exposed as a shared dataset to multiple users.
- **FR-016**: The system MUST offer generic daily calorie and protein target
  suggestions for users to accept or change. Suggestions MUST be optional,
  non-personalized, clearly identified as general information, and MUST NOT be
  applied without user acceptance. Their numeric values and supporting basis require
  explicit approval (Q-004a).
- **FR-017**: The system MUST allow users to remove a configured daily calorie or
  protein target so that it becomes unset.

### Business Rules

- **BR-001**: A meal belongs to the current date in the local machine's timezone
  when recorded; daily aggregation includes only meals recorded for that date.
- **BR-002**: Meal categories are limited to Breakfast, Lunch, Dinner, and Snack.
- **BR-003**: Calories and protein are user-entered values and are not independently
  verified by the system.
- **BR-004**: A daily calorie total is the sum of calorie values of meals recorded
  for that date; a daily protein total is the sum of protein values for those meals.
- **BR-005**: A date with no meals has calorie and protein totals of zero.
- **BR-006**: Targets are optional; an unset target is different from a configured
  target of zero.
- **BR-007**: Adding, editing, or deleting a meal MUST update all affected daily
  totals consistently.
- **BR-008**: Meal date handling remains unresolved until the business owner approves
  whether a saved meal's date may be changed after creation; the planning baseline
  MUST NOT impose a hard date-lock or automatic date migration.
- **BR-009**: Meal nutrition amounts MUST be non-negative; quantity/serving MUST be
  greater than zero, have no more than 2 decimal places, and use serving(s), g, or
  ml.
- **BR-010**: The application MUST NOT describe tracked values as medical advice or
  authoritative nutrition facts.
- **BR-011**: Generic target suggestions MUST NOT be represented as personalized,
  medically appropriate, or authoritative advice; they MUST NOT become configured
  targets unless the user accepts them.
- **BR-012**: Meal retention beyond the active date remains unresolved; the system
  MUST apply date-scoped summaries without deleting other stored records, and
  configured targets MUST remain until the user changes or removes them. The date
  boundary is determined using the local machine's timezone when a date is selected.

### Non-Functional Requirements

- **NFR-001**: The application MUST remain usable in desktop and mobile browsers for
  meal entry, target configuration, and daily progress review.
- **NFR-002**: Nutrition totals shown for a date MUST equal the sum of the saved
  applicable meal values for that date, using a consistent display precision.
- **NFR-003**: Validation errors MUST be associated with the relevant input and
  understandable without requiring technical knowledge.
- **NFR-004**: The system MUST collect and expose no more personal data than is
  necessary for the agreed tracker functionality; it MUST NOT share meal records
  without an approved requirement.
- **NFR-005**: The specification and eventual implementation MUST avoid prescribing
  an unnecessary framework, service, or infrastructure for this small application.
- **NFR-006**: Core form fields and actions MUST remain identifiable and operable in
  supported desktop and mobile browser layouts.

### Data Requirements

- **Meal record**: Food name; one predefined meal category; positive numeric
  quantity/serving amount with up to 2 decimal places and unit of serving(s), g, or
  ml; calories in kcal; protein in grams; date; optional time; optional notes.
- **Daily target**: Optional calorie target and optional protein target, each
  distinguishable from an unset value. The system MUST retain and display configured
  values for comparison until the user changes or removes them. Targets apply to
  the single user's local instance. Generic suggested values
  may be accepted or changed; their values and basis require approval (Q-004a).
- **Daily totals**: Derived sums of meal calories and protein grouped by the meal's
  recorded date. Totals MUST be recalculated after meal create, edit, or deletion.
- **Access and retention**: The first version has no application accounts and runs
  as a local, single-user instance, not a shared database for multiple users.
  Historical meal retention is not yet approved; date-scoped totals must not delete
  other stored records, while configured targets remain until the user changes or
  removes them.

### Input Validation and Error Scenarios

- Food name MUST be present and MUST contain a non-whitespace value.
- Meal category MUST match one of the four predefined options.
- Quantity/serving MUST be a positive numeric amount with no more than 2 decimal
  places. The unit MUST be selected from serving(s), g, or ml.
- Calories and protein MUST be numeric and non-negative. Zero is allowed.
- Date MUST be present and valid. Time, when supplied, MUST be a valid time value.
- Notes are optional and MUST NOT be required to save a meal.
- Configured targets MUST be numeric and non-negative; unset targets MUST remain
  unset and MUST NOT be converted to zero. Generic suggestions MUST NOT be applied
  automatically; their content requires approval (Q-004a).
- When the current date ends, the system MUST remove that day's meal records and
  MUST retain configured targets unless the user changes or removes them.
- When validation fails, the system MUST explain which field is invalid and how to
  correct it. It MUST NOT save an invalid new meal or apply a partial edit.
- If a save operation fails, the system MUST communicate that failure and preserve
  the last successfully saved record.

### Key Entities *(include if data involved)*

- **Meal**: A user-entered food item with category, quantity/serving, calories,
  protein, date, and optional time and notes.
- **Daily target**: Optional user-configured calorie and protein goal values used
  for comparison with daily intake.
- **Daily nutrition summary**: The derived calorie and protein totals for a date,
  optionally compared with configured targets.

### Acceptance Criteria

- **AC-001** *(FR-001, FR-003, BR-002, BR-009)*: **Given** all required fields contain valid
  values and the category is selected from the predefined options, **When** the user
  saves the meal, **Then** the system accepts the meal and retains each entered
  required value.
- **AC-002** *(FR-002, BR-002)*: **Given** the user opens the meal category control,
  **When** the available choices are displayed, **Then** the choices are exactly
  Breakfast, Lunch, Dinner, and Snack.
- **AC-003** *(FR-003, FR-013, BR-003, BR-010)*: **Given** a valid meal has been saved,
  **When** the user views its details, **Then** the entered nutrition values are
  displayed without implying external verification.
- **AC-004** *(FR-003, FR-011)*: **Given** any required field is missing or invalid,
  **When** the user attempts to save a new meal, **Then** the system identifies the
  invalid field, explains the correction, and does not create the meal.
- **AC-005** *(FR-003, BR-009)*: **Given** calories or protein is negative or
  non-numeric, **When** the user attempts to save the meal, **Then** the system
  rejects that value; **And given** either value is zero with all other required
  fields valid, **When** the user saves, **Then** the system accepts the value.
- **AC-006** *(FR-001, FR-003)*: **Given** time and notes are both omitted and all
  required fields are valid, **When** the user saves the meal, **Then** the meal is
  accepted without requiring either optional field.
- **AC-007** *(FR-004, FR-005, BR-001, BR-004, NFR-002)*: **Given** today has
  multiple saved meals, **When** the user views today's nutrition summary,
  **Then** each meal is listed and the displayed calorie and protein totals equal
  the sums of their respective meal values.
- **AC-008** *(FR-004, FR-005, BR-005)*: **Given** no meals have been recorded for
  today, **When** the user views today's nutrition summary, **Then** the meal list is
  empty and both totals are zero.
- **AC-009** *(FR-006, FR-011, BR-007, BR-008)*: **Given** a saved meal is edited
  with valid values, **When** the edit is saved, **Then** the record shows the new
  values and the relevant date totals reflect the change exactly once; the date
  handling for saved meals remains subject to the unresolved clarification of whether
  date changes are permitted.
- **AC-010** *(FR-007, BR-005, BR-007)*: **Given** a saved meal is deleted,
  **When** deletion succeeds, **Then** the meal is absent from the applicable list
  and totals are recalculated, including to zero if it was the last meal.
- **AC-011** *(FR-006, FR-011)*: **Given** a saved meal is edited with invalid
  values, **When** the user attempts to save, **Then** the system explains the error
  and the previously saved meal and totals remain unchanged.
- **AC-012** *(FR-008, FR-009, FR-014, BR-006)*: **Given** no target is configured,
  **When** the user records a meal and views daily progress, **Then** meal recording
  and totals work normally and the system does not show a target of zero or a
  misleading target comparison.
- **AC-013** *(FR-008, FR-009)*: **Given** a target is configured for a nutrition
  measure, **When** the user views daily progress, **Then** that measure's intake is
  compared with its configured target and the displayed values identify intake and
  target distinctly.
- **AC-014** *(FR-008, FR-009)*: **Given** a user changes a configured target,
  **When** the new target is saved, **Then** subsequent progress comparison uses the
  changed value and meal records and calculated totals remain unchanged.
- **AC-015** *(FR-010, NFR-001, NFR-006)*: **Given** a supported desktop or mobile
  browser viewport, **When** a user completes meal entry and reviews progress,
  **Then** required fields, validation feedback, totals, and relevant actions remain
  readable and usable without losing information.
- **AC-016** *(FR-012)*: **Given** a meal has been saved successfully,
  **When** the user returns in the same browser/profile, **Then** the saved record
  remains available until a retention policy is approved; the historical retention
  decision remains unresolved and must not introduce automatic deletion of older
  meal records.
- **AC-017** *(FR-011, NFR-003)*: **Given** an input is invalid, **When** validation
  is presented, **Then** the message identifies the affected field and a correction
  without requiring technical knowledge.
- **AC-018** *(NFR-004)*: **Given** no approved requirement permits additional data
  collection or sharing, **When** the system's data handling is reviewed, **Then**
  it collects only data required for the agreed tracker functionality and does not
  share meal records.
- **AC-019** *(NFR-005)*: **Given** an implementation approach is proposed, **When**
  it is reviewed against the requirements, **Then** each added framework, service,
  or infrastructure component has a documented requirement-based justification.
- **AC-020** *(FR-015)*: **Given** a user opens the tracker, **When** they access
  meal records, **Then** the tracker does not require registration or authentication,
  runs as a local single-user instance, and does not expose a shared dataset to
  multiple users.
- **AC-021** *(FR-004, BR-001)*: **Given** a user opens meal entry or daily progress,
  **When** a date is selected, **Then** the tracker displays the meal list and totals
  for that relevant date without deleting other stored records; the historical
  retention and date-navigation policy remains pending clarification.
- **AC-022** *(FR-001, BR-009)*: **Given** a quantity is positive, has no more than
  2 decimal places, and uses serving(s), g, or ml, **When** the meal is saved,
  **Then** the amount and unit are retained; **And given** the amount is missing,
  zero, negative, has more than 2 decimal places, or uses another unit, **When** the
  user attempts to save, **Then** the system rejects it with field-level guidance.
- **AC-023** *(FR-016, BR-011)*: **Given** approved generic target suggestions are
  available, **When** the user views target settings, **Then** each suggestion is
  clearly labeled as general, is not presented as personalized or medical advice,
  and does not become an active target unless the user accepts it; **And given** no
  values have been approved, **Then** the system does not invent or display
  numerical suggestions.
- **AC-024** *(FR-012, BR-012)*: **Given** a meal is saved for a relevant date,
  **When** a date-scoped summary is computed, **Then** the calculation includes only
  the records for that date and does not delete other stored meal records; the
  historical retention policy remains unresolved.
- **AC-025** *(FR-008, FR-017, BR-012)*: **Given** a calorie or protein target is
  configured, **When** the user removes it, **Then** that target becomes unset and
  its comparison is no longer shown; **And given** the date changes, **Then** any
  configured target remains set.
- **AC-026** *(FR-010, FR-015)*: **Given** the application is running locally on one
  device, **When** the user opens it in a desktop or mobile browser on that device,
  **Then** the responsive tracker is usable; **And given** another device attempts
  to connect, **Then** the local instance is not exposed for remote access.
- **AC-027** *(FR-004, FR-012, BR-001, BR-012)*: **Given** the local machine's date
  changes at midnight, **When** the tracker next performs date-sensitive work,
  **Then** it treats the new local date as the active date for summary calculations
  and retains configured targets; historical meal retention remains unresolved and
  must not be implemented as automatic deletion of prior-date records.

### Success Criteria

#### Measurable Outcomes

- **SC-001**: Every required meal field and each of the four allowed categories can
  be entered and saved in acceptance testing with valid values.
- **SC-002**: For every daily-total test case, displayed calorie and protein totals
  match the sum of applicable saved meal values, including empty days and
  post-edit/delete states.
- **SC-003**: Every invalid-input case in the validation test set is rejected with
  actionable field-level feedback and without corrupting saved data.
- **SC-004**: Users can complete the meal recording and daily progress journeys in
  both desktop and mobile browser tests.
- **SC-005**: When targets are unset, meal entry and totals remain usable; when
  targets are configured or changed, comparisons use those values without changing
  meal records.
- **SC-006**: No unresolved business decision is implemented as a confirmed behavior
  without approval before planning and implementation.

### Assumptions

- The intended user is an individual manually tracking their own food intake.
- Calorie and protein values are entered per meal record, in kcal and grams
  respectively, as specified by the business decisions.
- Nutrition amounts and targets may be zero but may not be negative. Quantity/serving
  must be positive, have no more than 2 decimal places, and use serving(s), g, or ml.
- A user can record meals and review totals without configuring targets.
- The application displays user-entered nutrition information and does not claim
  medical authority or independent verification.
- No technology stack or architecture is assumed by the original business
  requirements. The first version does not use application accounts and is intended
  to run as a local single-user instance. Generic target suggestions are
  non-personalized and require approval for their actual values and basis.

### Dependencies and Constraints

- The solution MUST follow the project constitution: keep the architecture small,
  validate user input, preserve data integrity, protect privacy, and remain within
  the approved scope.

### Unresolved Business Decisions

- **Q-001 — Date scope and retention (pending):** Whether the app may retain and
  view meals beyond the current date remains unresolved. The planning baseline MUST
  avoid automatic deletion of earlier meal records and MUST NOT assume that only
  today’s meals may be stored. Daily summaries remain date-scoped without deleting
  other records.
- **Q-001b — Meal date editing (pending):** Whether a saved meal's date may be
  changed after creation remains unresolved. The plan must not impose a hard date
  lock until the business owner approves the behavior.
- **Q-002 — Identity and access (resolved):** The first version requires no
  registration or authentication; run as a local single-user instance and do not
  expose one shared dataset to multiple users.
- **Q-002a — Mobile access (resolved):** Mobile responsive layouts are supported on
  the device running the local instance; cross-device access is out of scope.
- **Q-002b — Date boundary (resolved):** Use the local machine's timezone to define
  the active date for daily calculations.
- **Q-003 — Quantity units (resolved):** Quantity is a positive numeric amount with
  up to 2 decimal places and a unit selected from serving(s), g, or ml.
- **Q-004 — Target suggestions (resolved):** Show optional, generic daily calorie
  and protein suggestions that users may accept or change; do not apply them
  automatically or present them as personalized or medical advice.
- **Q-004a — Suggestion values and basis (pending):** Which numeric calorie and
  protein values should be suggested, and what approved source or rationale supports
  them? Do not invent numerical suggestions before this is decided.
- **Q-005 — Retention (pending):** Whether meal records beyond the active date
  remain accessible and how long they are kept remains unresolved; configured
  targets remain until the user changes or removes them.

The numerical values and supporting basis for generic target suggestions MUST be
approved before those suggestions are implemented. Until then, the tracker MUST NOT
invent or display numerical recommendations.
