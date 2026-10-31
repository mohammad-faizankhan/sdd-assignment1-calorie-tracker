# Clarification Log

This log records the business clarifications, decisions, and approvals for the Calorie and Nutrition Tracker. It preserves the approved historical record and clearly distinguishes approved business decisions from earlier superseded guidance.

## Approved decisions

| ID | Decision | Status | Decision owner | Rationale | Impacted artifacts |
| --- | --- | --- | --- | --- | --- |
| CL-001 | Responsive browser-accessible web application for desktop and mobile browsers. | Approved | Project owner | A browser-focused local tracker must work in desktop and mobile browser layouts. | spec.md, plan.md, README.md |
| CL-002 | Meal information includes the required food name, meal category, quantity/serving, calories, protein, and date. Time and notes are optional. | Approved | Project owner | These are the required V1 meal fields. | spec.md, plan.md |
| CL-003 | Meal categories are limited to Breakfast, Lunch, Dinner, and Snack. Custom categories are excluded from V1. | Approved | Project owner | This keeps validation, UI, and domain logic simple and consistent. | spec.md, plan.md |
| CL-004 | Daily targets are optional initially and can be configured or modified later. | Approved | Project owner | Optional targets are part of V1, but not required for daily tracking. | spec.md, plan.md, tasks.md |
| CL-005 | Nutrition values are manually entered. V1 excludes food databases, external nutrition APIs, and barcode scanning. | Approved | Project owner | The product is a local tracker, not a nutrition intelligence service. | spec.md, plan.md, README.md |
| CL-006 | Users can view, edit, and delete meals. Deletion requires confirmation, and totals recalculate after edits or deletions. | Approved | Project owner | This preserves the core CRUD behavior without added complexity. | spec.md, plan.md, tasks.md, validation-plan.md |
| CL-007 | Historical meal retention is approved: retain all historical meal records and allow users to view meals and nutrition summaries for previous dates. | Approved | Project owner | This supersedes earlier end-of-day deletion assumptions and keeps daily summaries date-scoped without deleting other records. | spec.md, plan.md, tasks.md, validation-plan.md |
| D-001 | Meal date editing is approved: users may change the date of an existing meal, and both the previous and new dates' totals recalculated. | Approved | Project owner | This is a necessary and testable user workflow for date-based meal tracking. | spec.md, plan.md, tasks.md, validation-plan.md |
| D-002 | Quantity and serving units are approved: quantity must be a positive numeric value with a required predefined unit selected from Serving, Piece, Gram, Millilitre, Cup, Tablespoon, and Teaspoon. No automatic nutrition calculations or conversions are introduced. | Approved | Project owner | This resolves the V1 unit model without expanding the feature scope. | spec.md, plan.md, tasks.md, validation-plan.md |
| D-003 | Nutrition target suggestions are approved as out of scope for V1: no default numeric target suggestions. Users enter their own optional calorie and protein targets. | Approved | Project owner | This keeps the tracker simple and avoids unapproved recommendation behavior. | spec.md, plan.md, tasks.md, validation-plan.md |
| D-004 | Authentication is approved as out of scope for V1: local single-user application with no login, registration, roles, or multi-user support. | Approved | Project owner | This aligns with the local-only architecture and avoids unsupported user-management requirements. | spec.md, plan.md, tasks.md, README.md |
| D-005 | Data retention is approved: all meal records are persistently retained in local SQLite until explicitly deleted by the user. No automatic cleanup or expiration. | Approved | Project owner | This formalizes the approved retention policy and replaces any previous end-of-day cleanup assumption. | spec.md, plan.md, tasks.md, validation-plan.md |

## Clarification history and superseded decisions

| ID | Historical record | Status |
| --- | --- | --- |
| Q-001a | Prior question: Can users view historical meal records, or only today's meals? | Superseded by CL-007. |
| Q-006a | Prior question: What is the data-retention policy? | Superseded by D-005 and CL-007. |
| Session 2026-10-31 | Earlier guidance: delete meal records at the end of each day and keep only the current day. | Superseded. This behavior is explicitly not approved and must not be implemented. |

## Important approval note

The earlier end-of-day deletion decision is superseded by the approved historical-retention decision and the explicit project-owner approval for persistent local retention. Daily summaries remain date-scoped and calculate only for the selected date; they do not delete or purge other preserved meal records.

## Clarification notes

- The application remains a local, single-user tracker with no authentication or multi-user behavior.
- Historical meal records are retained and may be reviewed by selected date.
- The business owner explicitly approved date editing and unit selection for V1.
- Default target suggestions remain excluded from V1 and are not treated as a requirement.
- All implementation planning and future coding work should reflect these approved decisions and suppress any earlier end-of-day cleanup assumptions.
