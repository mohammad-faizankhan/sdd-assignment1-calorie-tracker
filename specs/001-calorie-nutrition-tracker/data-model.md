# Data Model: Calorie and Nutrition Tracker

This model supports the approved single-user, local-only application. It contains
no user or account entity. Numeric suggestion values are intentionally excluded
until Q-004a is approved.

## Entities

### Meal

One manually entered food item recorded for the selected active date. Historical meal
retention and whether a saved meal's date may be edited remain pending clarification;
this model intentionally does not assume that earlier records are auto-deleted or that
meal dates are locked after creation.

| Field | SQLite type | Required | Constraints and meaning |
|---|---|---:|---|
| `id` | `INTEGER` | Yes | Primary key, generated locally. |
| `food_name` | `TEXT` | Yes | Trimmed, non-empty name. |
| `category` | `TEXT` | Yes | `Breakfast`, `Lunch`, `Dinner`, or `Snack`. |
| `quantity_amount` | `TEXT` | Yes | Canonical non-negative decimal representation; must be greater than zero and have at most 2 decimal places. Stored as text to avoid selecting an unstated precision or relying on binary floating-point aggregation. |
| `quantity_unit` | `TEXT` | Yes | `serving`, `g`, or `ml`; UI may label `serving` as “serving(s)”. |
| `calories_kcal` | `TEXT` | Yes | Canonical non-negative decimal supplied by the user. No decimal precision or maximum is established in the spec. |
| `protein_g` | `TEXT` | Yes | Canonical non-negative decimal supplied by the user. No decimal precision or maximum is established in the spec. |
| `meal_date` | `TEXT` | Yes | ISO `YYYY-MM-DD`; must match the active date in the local machine timezone unless a later clarification approves date editing. |
| `meal_time` | `TEXT` | No | Optional local time in `HH:MM`; no timezone conversion. |
| `notes` | `TEXT` | No | Optional free text. |

`quantity_amount`, `calories_kcal`, and `protein_g` are parsed and validated as
decimal values in the API/business layer, then stored as canonical decimal strings.
All sums use decimal arithmetic in the backend. The API returns JSON numbers;
formatting precision for display remains an implementation detail to agree before
coding if it would round user-entered values.

The database SHOULD enforce the category and unit enumerations with `CHECK`
constraints. Required fields are `NOT NULL`; the primary key is unique. The
application layer validates decimal syntax and range before writes.

### DailyTarget

The optional pair of user-configured daily nutrition targets for this single-user
local instance. A single fixed row represents the configuration.

| Field | SQLite type | Required | Constraints and meaning |
|---|---|---:|---|
| `singleton_id` | `INTEGER` | Yes | Primary key constrained to `1`; prevents multiple target rows. |
| `calories_kcal` | `TEXT` | No | Optional non-negative decimal; `NULL` means unset, while `"0"` is a configured zero target. |
| `protein_g` | `TEXT` | No | Optional non-negative decimal; `NULL` means unset, while `"0"` is a configured zero target. |

The row is initialized with both target values unset. Updating one measure MUST NOT
silently unset the other. The user can explicitly clear a measure. Generic suggestion
values and their source are not stored or returned until Q-004a is approved.

## Relationships and Derived Values

- There are no user/account relationships. The database is local to one user and
  MUST NOT be shared by a multi-user deployment.
- Daily summary is derived from all `Meal` rows whose `meal_date` matches the
  selected local date; this does not imply that older rows are deleted or that only
  one date may be stored.
- Daily calorie and protein totals are exact decimal sums of their respective
  fields; an empty set yields zero.
- Configured target values are read separately and are never included in meal
  totals.

## Lifecycle and Retention

- Create, edit, and delete operate on the active date selected by the user or the
  application; historical retention remains unresolved.
- A saved meal's date may or may not be editable; the model does not impose a hard
  lock until the business owner approves the behavior.
- Do not add automatic deletion of older meal rows. Summary queries use the
  selected date and must not delete other stored records.
- Targets persist across date changes until the user changes or removes them.
- No historical meal archive, export, or recovery mechanism is included unless a
  future approval adds one.

## Open Constraint

Q-004a leaves the numerical suggestions and supporting basis unapproved. The model
does not store suggestion content; the target settings UI/API can be implemented
without suggestions, but FR-016 cannot be considered complete until that decision
is approved.

Additional unresolved decisions: whether older meal records remain visible and
queryable beyond the active date, and whether a saved meal's date may be changed
after creation. These decisions remain in the clarification log and are not
implicitly resolved by this data model.
