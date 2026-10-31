# Feature Specification: Calorie and Nutrition Tracker

**Feature Branch**: `001-calorie-nutrition-tracker`
**Created**: 2026-10-31
**Status**: Approved for SDD Baseline v1.0.0

## Product overview

This product is a responsive, browser-accessible web application for individuals to manually record meals, review daily calorie and protein totals, and optionally compare intake against user-configured daily targets. The product is local and single-user by design and stores data in a local SQLite database on the same device running the application.

The application is meant to support straightforward nutrition tracking and does not provide medical advice, external nutrition lookups, or user accounts.

## Approved clarifications

- CL-001: Responsive browser-accessible web application for desktop and mobile browsers.
- CL-002: Meal fields include required food name, meal category, quantity/serving, calories, protein, and date; time and notes are optional.
- CL-003: Meal categories are Breakfast, Lunch, Dinner, and Snack only.
- CL-004: Daily targets are optional and configurable.
- CL-005: Nutrition values are manually entered; no food database, API, or barcode scanning in V1.
- CL-006: Users can view, edit, and delete meals; deletion requires confirmation; totals recalculate after edits or deletions.
- CL-007: Historical meal retention is approved; all records are retained, and users may view meals and summaries for previous dates.
- D-001: Users can edit a saved meal's date; the meal moves to the selected date, and totals recalc for both affected dates.
- D-002: Meal quantity requires a positive numeric value and a required predefined unit selected from Serving, Piece, Gram, Millilitre, Cup, Tablespoon, or Teaspoon.
- D-003: No default numeric target suggestions in V1; users enter their own optional calorie and protein targets.
- D-004: V1 is a local single-user application; no login, registration, roles, or multi-user support.
- D-005: All meal records remain persistently stored until explicitly deleted by the user; no automatic cleanup or expiration.

## User description

The primary user is a person who wants a simple local tool to track their daily food intake and compare it against personal targets. The user is not expected to be a nutrition professional, and the tool is intentionally limited to manual entry and date-based summaries.

## V1 scope

In scope:

- Manual meal entry
- Meal categories: Breakfast, Lunch, Dinner, Snack
- Manual calorie and protein entry
- Selected-date meal listing and daily totals
- Historical record retention and previous-date access
- Meal editing, including date changes
- Meal deletion with confirmation
- Optional daily target configuration and comparison
- Responsive desktop and mobile browser layouts
- Local single-user SQLite-based storage

Out of scope:

- Food database lookup
- External nutrition API integration
- Barcode scanning
- Personalized nutrition recommendations or medical guidance
- User accounts or authentication
- Shared/multi-user systems
- Default target suggestions
- Automatic retention expiry or end-of-day cleanup

## Functional requirements

- FR-001: The system MUST allow a user to manually enter a meal with a required food name, meal category, positive numeric quantity, required unit, calories in kcal, protein in grams, and date. Time and notes are optional.
- FR-002: The system MUST provide exactly the predefined meal categories: Breakfast, Lunch, Dinner, and Snack.
- FR-003: The system MUST save a meal only when all required fields are valid and MUST preserve the values entered by the user.
- FR-004: The system MUST allow a user to view saved meals and daily calorie and protein totals for the selected date, including previous dates, while retaining historical records.
- FR-005: The system MUST calculate daily calorie and protein totals from the meals saved for the selected date.
- FR-006: The system MUST allow an existing meal to be edited and MUST recalculate totals for any affected dates after a valid edit.
- FR-007: The system MUST allow a user to delete a saved meal and MUST recalculate totals after deletion.
- FR-008: The system MUST allow a user to configure and modify daily calorie and protein targets; targets remain optional.
- FR-009: When a target is configured, the system MUST compare daily intake against that target. Unset targets MUST remain unset and not be treated as zero.
- FR-010: The system MUST support the same core flows in desktop and mobile browsers with a responsive layout.
- FR-011: The system MUST validate inputs and describe the invalid fields clearly without modifying valid data.
- FR-012: The system MUST retain all meal records and must not automatically delete older meal records. Daily summaries are computed for the selected date without purging other stored records.
- FR-013: The system MUST not use external food databases, external nutrition APIs, or barcode scanning to populate meal values.
- FR-014: The system MUST allow meal entry and daily summary review without requiring users to configure targets.
- FR-015: The system MUST operate as a local single-user application with no login, registration, roles, or multi-user support.
- FR-016: The system MUST not provide default numeric nutrition target suggestions in V1; users enter their own optional targets.
- FR-017: The system MUST allow users to clear or remove a configured target so that it becomes unset.

## Non-functional requirements

- NFR-001: The application MUST remain usable in desktop and mobile browser viewports for meal entry, daily review, and target configuration.
- NFR-002: Totals shown for a date MUST match the sum of the saved meal values for that date using consistent precision and exact calculation rules.
- NFR-003: Validation errors MUST be associated with the relevant input and written in plain language.
- NFR-004: The application MUST store only the approved fields necessary for V1 tracking and MUST not expose data outside the local single-user context.
- NFR-005: Technical implementation MUST remain simple, local-only, and compatible with the approved architecture and business constraints.

## Assumptions and constraints

- The application runs on the local device and uses the local machine's timezone for date boundaries.
- A SQLite database is used for local persistence.
- Meal records are retained until the user explicitly deletes them.
- Quantity units are chosen from the approved predefined list and are not automatically converted.
- Nutrition values are manually entered and not validated against an external source.
- No implementation code is generated as part of this specification baseline.

## User stories

### User story 1: Record meals and review daily intake

As a user, I want to record meals and see the totals for the selected date so that I can understand my daily intake.

### User story 2: Correct or remove meals

As a user, I want to edit or delete meals and keep daily totals accurate so that my record remains trusted.

### User story 3: Set optional targets

As a user, I want to configure optional daily calorie and protein targets so that I can compare my daily intake against my personal goals.

### User story 4: Review previous dates and historical records

As a user, I want to view meals and summaries for previous dates so that I can review my historical data without losing older records.

### User story 5: Use the app on desktop and mobile

As a user, I want the interface to remain usable on desktop and mobile browsers so that I can track meals on either device class.

## Acceptance criteria

- AC-001: A valid meal can be created when the user enters a required food name, meal category, quantity, required unit, calories, protein, and date.
- AC-002: The system rejects a meal category that is not one of Breakfast, Lunch, Dinner, or Snack.
- AC-003: The system rejects a meal if required fields are missing or blank.
- AC-004: A positive quantity value is required, and the unit is required from the approved predefined list.
- AC-005: Calories and protein values must be numeric and non-negative; invalid negative or non-numeric values are rejected.
- AC-006: The meal date is required; the system stores the selected date and uses the local device timezone for date boundaries.
- AC-007: The system lists meals for the selected date and includes those meals in the daily totals for that date.
- AC-008: Users can view meals and totals for a previous date without deleting other stored records.
- AC-009: A valid edit replaces the meal data and recalculates totals for the affected date or dates.
- AC-010: A user can change the date of an existing meal; the meal moves to the selected date and totals for both the prior and new dates are recalculated.
- AC-011: Invalid edits are rejected and the original saved record remains unchanged.
- AC-012: A user can delete a meal only after confirmation; deletion removes the meal from the list and totals.
- AC-013: Totals recalculate after a meal is deleted.
- AC-014: The daily summary shows the totals for the selected date and zero totals when no meals are recorded.
- AC-015: The app remains usable in responsive desktop and mobile browser layouts.
- AC-016: Targets are optional and do not block meal entry or daily summary review when unset.
- AC-017: Users can configure and modify optional calorie and protein targets.
- AC-018: When configured, the summary shows whether intake is below, equal to, or above the configured target for that measure.
- AC-019: The application stores records locally in SQLite and is a single-user system without login or registration.
- AC-020: Historical meal records persist across application restarts and are not auto-deleted.
- AC-021: No external food database or nutrition API is used to populate meal values.
- AC-022: Numeric target suggestions are not displayed or applied in V1.
- AC-023: Clearing a configured target returns that target to an unset state without altering other configured values.
- AC-024: Daily summaries are calculated for the selected date and do not delete or purge other stored records.
- AC-025: The system distinguishes an unset target from a configured zero target.
- AC-026: Deletion requires confirmation before a record is removed permanently.

## Explicit business decisions

- Approved business decision: Users may edit a saved meal's date and move it to another day. Both date totals recalculate.
- Approved business decision: Quantity must be a positive number with a required predefined unit.
- Approved business decision: No default numeric nutrition target suggestions are provided in V1.
- Approved business decision: V1 is a local single-user app without login, registration, or multi-user access.
- Approved business decision: All meal records remain in the local SQLite database until explicitly deleted by the user.
- Approved business decision: Historical meal records remain available for previous dates, and summaries are selected-date based.

## Final status

All required business decisions for V1 implementation have been explicitly approved by the project owner. No unresolved business questions remain for the approved baseline.
