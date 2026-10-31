# Validation Plan

This validation plan is based on the current Calorie and Nutrition Tracker specification and acceptance criteria only. It preserves unresolved decisions as pending clarification and does not assume that unapproved business rules have been accepted.

## Scope and traceability rules

- Use only acceptance criterion IDs that exist in the current specification.
- If a scenario cannot be mapped to a current acceptance criterion, mark the mapping as `Pending` instead of inventing a new ID.
- Keep unresolved business decisions visible in the validation set rather than treating them as approved behaviors.

## Test scenarios

| Test ID | Related AC ID | Scenario | Input or precondition | Expected result | Test type |
| --- | --- | --- | --- | --- | --- |
| VAL-001 | AC-001, AC-003 | Valid meal creation | Enter a valid food name, category, quantity, calories, protein, and date using allowed values. | The meal is accepted and retained with the entered values. | Normal |
| VAL-002 | AC-004, AC-017 | Missing required fields | Leave one or more required fields empty or spaces-only. | Validation identifies the invalid field and the meal is not saved. | Invalid |
| VAL-003 | AC-005, AC-017 | Invalid or negative calorie/protein values | Enter a negative calorie value, a negative protein value, or a non-numeric value. | The meal is rejected with field-level feedback and the record is not created. | Invalid |
| VAL-004 | AC-005, AC-022 | Zero values and boundary values | Save a meal with `0` calories, `0` protein, or a valid positive quantity at the boundary allowed by the rule. | Zero values are accepted when valid; invalid zero quantity or unsupported units are rejected. | Boundary |
| VAL-005 | AC-002, AC-004 | Invalid meal categories | Attempt to save a meal using a category outside Breakfast, Lunch, Dinner, or Snack. | The value is rejected and the wrong category is not retained. | Invalid |
| VAL-006 | AC-009 | Editing meals with valid values | Open a saved meal and change the calorie or protein values to valid numbers. | The edited values are saved and the relevant date totals reflect the new arithmetic. | Normal |
| VAL-007 | AC-011 | Editing meals with invalid values | Attempt to save invalid nutrition data to an existing meal. | The system presents the error and keeps the previously saved values and totals unchanged. | Invalid |
| VAL-008 | Pending | Deleting meals with confirmation | Select a saved meal and attempt delete flow with confirmation required by CL-006. | The meal is removed only after confirmation and the list/totals update accordingly. | Edge case |
| VAL-009 | AC-009, AC-010 | Daily total recalculation after edits and deletions | Edit an existing meal, then delete a meal or leave the last meal removed. | Totals update exactly and return to zero when appropriate. | Normal |
| VAL-010 | AC-007, AC-021, AC-024 | Daily summary for a date with meals | Save multiple meals on the currently selected date and open the daily summary. | The meal list and totals reflect only the selected date and match the sum of that date's meal values. | Normal |
| VAL-011 | AC-008 | Daily summary when no meals exist | Use a date with no saved meals. | The meal list is empty and the totals are zero. | Edge case |
| VAL-012 | AC-012 | Targets not configured | View the daily progress without setting a target. | The tracker continues to work and does not show a misleading zero target or target comparison. | Edge case |
| VAL-013 | AC-013, AC-014, AC-025 | Targets configured and modified | Set or change a calorie and/or protein target and then save the change. | The comparison uses the configured target and subsequent totals remain accurate; clearing a target removes the comparison. | Normal |
| VAL-014 | AC-013, AC-014 | Intake below, equal to, and above targets | Record meals that produce intake less than, equal to, and greater than the configured target. | The display shows each comparison state without altering the underlying meal records. | Normal |
| VAL-015 | AC-015, AC-026 | Responsive behavior on desktop and mobile | Open the app in a desktop viewport and a mobile viewport. | Core meal entry, target controls, and progress review remain readable and operable without loss of required information. | Normal |
| VAL-016 | Pending | Historical meal visibility beyond the active date | Attempt to view or edit meals recorded on previous dates. | This remains pending business clarification; the spec does not currently approve a definitive behavior. | Edge case |
| VAL-017 | Pending | Meal date editing after save | Change the recorded date of an existing meal. | This remains pending clarification because the spec explicitly does not approve a hard date lock or a default date-change rule. | Edge case |
| VAL-018 | Pending | Generic target suggestion values | Review target settings and any suggestion logic. | The system should not invent or display numerical suggestions until Q-004a is approved. | Edge case |

## Validation notes

- The following scenarios are intentionally marked as pending clarification because the current specification explicitly leaves them unresolved: historical meal retention, meal date editing, exact quantity/serving units, and target suggestion content.
- The validation plan contains no invented acceptance criteria IDs. All mapping references are limited to the IDs present in the current specification or explicitly labelled as pending.
- This validation baseline is intended to be used as a working test plan for the current draft and should be updated once the remaining clarification decisions are approved.
