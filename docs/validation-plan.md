# Validation Plan

This validation plan is based on the approved V1 feature specification and the approved business decisions recorded in the clarification log. It is a planned test matrix only and does not claim that any implementation has passed.

## Validation rules

- Use only acceptance criteria IDs that exist in the current specification.
- Mark any scenario requiring authorization by an unapproved decision as out of scope; these decisions have all been explicitly approved for V1.
- No test is reported as passed in this document.

## Approved decisions included in validation

- D-001: Meal dates may be edited and totals recalculated for both affected dates.
- D-002: Quantity requires a positive numeric value and an approved unit.
- D-003: No default target suggestions in V1.
- D-004: Local single-user app with no login or registration.
- D-005: Historical meal records persist until explicit user deletion.
- CL-007: Historical retention and previous-date summaries remain approved.

## Test matrix

| Test ID | Related AC ID | Scenario | Preconditions | Input | Expected outcome | Test category |
| --- | --- | --- | --- | --- | --- | --- |
| V-001 | AC-001 | Valid meal creation | User is on the meal form. | Enter valid food name, category, quantity, unit, calories, protein, and date. | Meal is saved and appears in the selected date list. | Normal |
| V-002 | AC-003 | Missing required fields | Meal form is incomplete. | Leave required fields blank or whitespace-only. | Validation rejects the save and highlights the invalid fields. | Invalid |
| V-003 | AC-002 | Invalid meal category | Meal form is open. | Enter a category outside Breakfast, Lunch, Dinner, or Snack. | Save attempt is rejected. | Invalid |
| V-004 | AC-004 | Quantity and unit validation | Meal form is open. | Enter zero or negative quantity, or omit the unit. | Validation rejects the input. | Invalid |
| V-005 | AC-004 | Approved quantity units | Meal form is open. | Select a valid unit such as Serving, Piece, Gram, Millilitre, Cup, Tablespoon, or Teaspoon. | Save succeeds when all other fields are valid. | Normal |
| V-006 | AC-005 | Invalid calorie and protein values | Meal form is open. | Enter negative calories or protein, or a non-numeric value. | Validation rejects the save. | Invalid |
| V-007 | AC-005 | Zero nutrition boundary values | Meal form is open. | Set calories or protein to zero while other required values are valid. | Zero values are accepted as valid user data. | Boundary |
| V-008 | AC-006 | Meal date required | Meal form is open. | Leave the date blank or invalid. | Save is rejected. | Invalid |
| V-009 | AC-007, AC-014 | Selected date summary | At least one meal exists for a chosen date. | Select the date and view the summary. | Only that date's meals contribute to the running total. | Normal |
| V-010 | AC-014 | Empty date summary | No meals exist on the selected date. | Open an empty date. | Summary shows zero totals and no meal entries. | Edge case |
| V-011 | AC-008, AC-020, AC-024 | Historical meal access | Meals exist on multiple dates. | Select a previous date. | The previous-date meal list and summary are shown without deleting records from other dates. | Normal |
| V-012 | AC-009, AC-011 | Valid meal edit | Meal exists in the database. | Update a valid calorie or protein value. | The record updates and totals recalculate. | Normal |
| V-013 | AC-010 | Edit meal date | Meal exists in the database. | Change the meal date to another day and save. | The meal moves to the new date; totals recalculate for both the old and new dates. | Normal |
| V-014 | AC-011 | Invalid edit | Meal exists in the database. | Attempt invalid values while editing. | Validation blocks the update and original data remains unchanged. | Invalid |
| V-015 | AC-012, AC-026 | Delete meal with confirmation | A valid meal exists. | Trigger delete and confirm the action. | The meal is removed only after confirmation. | Normal |
| V-016 | AC-013 | Total recalculation after deletion | Meal list includes at least one item. | Delete one meal and view the summary. | Totals are recalculated based on remaining records. | Normal |
| V-017 | AC-016 | Targets not configured | No target values are set. | Add a meal and view the summary. | The app continues to function without a target comparison. | Edge case |
| V-018 | AC-017, AC-023 | Targets configured and modified | User has an optional target configuration. | Set or change calorie and/or protein targets. | The summary reflects the configured values and then the updated values after modification. | Normal |
| V-019 | AC-018, AC-025 | Intake below, equal to, and above target | At least one meal is recorded and targets exist. | Create values below, equal to, and above the configured target. | The summary shows the correct comparison state for each measure. | Normal |
| V-020 | AC-015 | Responsive behavior on desktop and mobile | App is running on the device. | Open app in desktop and mobile-sized viewports. | Required controls and summaries remain accessible in both layouts. | Normal |
| V-021 | AC-019 | Local single-user operation | App runs locally on a single device. | Open the app in the local browser. | No login, registration, or multi-user flow is presented. | Normal |
| V-022 | AC-020 | Persistence across restarts | Meal records already exist and app is closed. | Restart the app and view a previous date. | Historical records remain available and are not auto-deleted. | Edge case |
| V-023 | AC-021 | No external nutrition lookup | App is configured for local use. | Check data source behavior. | Meal values are not populated from external food or nutrition services. | Normal |
| V-024 | AC-022 | No default target suggestions in V1 | Target configuration view is open. | Inspect the target UI. | No default numeric suggestions are displayed or auto-applied. | Edge case |
| V-025 | AC-024 | Date-scoped summary does not alter retention | Existing old records are present. | View a summary for a selected date. | The selected date summary updates without deleting or purging any other stored records. | Edge case |

## Notes

- The test plan is intentionally planning-level and does not claim pass or fail results.
- All approved decisions noted above are included in the validation scope.
- No unresolved business decisions remain for V1 implementation.
