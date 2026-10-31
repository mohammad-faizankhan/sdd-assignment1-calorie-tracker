# Clarification Log

This log records the business clarifications, decisions, and unresolved items for the Calorie and Nutrition Tracker. It preserves the approved decisions already reflected in the feature specification and retains unresolved questions explicitly without inventing answers.

## Agreed decisions

| ID | Decision | Status | Notes |
| --- | --- | --- | --- |
| CL-001 | Responsive browser-accessible web application for desktop and mobile browsers. | Agreed | The product must remain usable in supported desktop and mobile browser viewports. |
| CL-002 | Meal fields include required food name, meal category, quantity/serving, calories, protein, and date. Time and notes are optional. | Agreed | Required meal data is user-entered manually; values must be retained as entered. |
| CL-003 | Predefined categories: Breakfast, Lunch, Dinner, Snack. No custom categories in V1. | Agreed | Category choices are fixed and limited to the four approved values. |
| CL-004 | Daily targets are optional initially and can be configured or modified later. | Agreed | A target may be unset, configured, or changed later without altering saved meal records. |
| CL-005 | Nutrition values are manually entered. No food database, nutrition API, or barcode scanning in V1. | Agreed | The application does not verify values against an external source. |
| CL-006 | Users can view, edit, and delete meals. Deletion requires confirmation, and totals recalculate after edits or deletions. | Agreed | The specification records the requirement, but the confirmation UX is not expanded beyond the business rule. |

## Unresolved questions and pending decisions

| ID | Question | Status |
| --- | --- | --- |
| Q-001a | Can users view historical meal records, or only today's meals? | Unresolved; must remain open until the business owner approves the behavior. |
| Q-002a | Which units should quantity/serving support? | Unresolved in the current artifacts; the approved set is limited to the business clarification record, but the final implementation should not assume a broader set without approval. |
| Q-004a | Should the application suggest default nutrition targets? | Unresolved; the specification explicitly prohibits inventing numerical suggestion values until approved. |
| Q-005a | Is authentication or user registration required? | Unresolved; the current baseline is a local single-user instance with no accounts. |
| Q-006a | What is the data-retention policy? | Unresolved; meal retention beyond the active date is not approved as a default rule and must not be implemented as automatic deletion without approval. |

## Clarification notes

- The specification baseline is a local, single-user app with no requirement for authentication or multi-user account management.
- The daily summary is date-scoped and must not delete other stored records while historical retention remains unresolved.
- Meal totals are recalculated for relevant dates after create, edit, and delete operations.
- Daily targets remain optional and are not automatically seeded or suggested unless explicitly approved.
- No business-owner answer has been invented for unresolved items; these questions remain visible in the planning and review records.
