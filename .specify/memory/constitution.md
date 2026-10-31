<!-- Sync Impact Report
- Version change: 1.0.0 -> 2.0.0
- List of modified principles:
  I. User Value and Correctness -> I. Simplicity First
  II. Simplicity and Explicit Design -> II. User-Centric Design
  III. Test-First and Evidence -> III. Data Accuracy and Integrity
  IV. Secure and Responsible Delivery -> IV. Requirements Traceability
  V. Review, Ownership, and Continuous Improvement -> V. Maintainability
  Added: VI. Input Validation and Error Handling, VII. Privacy and Security,
  VIII. Scope Control
- Added sections: None
- Removed sections: None
- Follow-up TODOs: None
-->

# Calorie and Nutrition Tracker Constitution

## Core Principles

### I. Simplicity First
**Principle:** Choose the smallest solution that completely meets the stated requirements.

**Why it matters:** This is a fundamentals-level application; unnecessary architecture
and technology make it harder to understand, verify, and maintain.

**Development rules:**
- Specifications and plans MUST prefer direct, understandable designs over speculative
  abstractions, services, or frameworks.
- Implementation MUST use existing project conventions and add a dependency only when
  a stated requirement cannot be met reasonably without it.
- Validation MUST use the narrowest relevant checks; complexity MUST have a documented
  requirement-based justification.

### II. User-Centric Design
**Principle:** Make meal entry, target configuration, and daily progress clear and usable.

**Why it matters:** Users need to record food manually and quickly understand their
calorie and protein totals without navigating unnecessary complexity.

**Development rules:**
- Specifications MUST cover manual meal recording, calorie and protein values,
  optional daily targets, and daily nutrition progress.
- Plans and implementations MUST keep the primary tasks discoverable and present
  progress and target status using clear labels and units.
- Validation MUST verify that recorded meals and configured targets are reflected
  consistently in the user's daily view.

### III. Data Accuracy and Integrity
**Principle:** Preserve user-entered nutrition data and calculate daily totals
consistently.

**Why it matters:** Incorrect or inconsistent calorie and protein totals undermine
the application's core purpose and user trust.

**Development rules:**
- Meal entries MUST retain the calorie and protein values entered by the user; the
  application MUST NOT imply that manual values are independently verified.
- The specification MUST define the units and aggregation behavior used for each
  nutrition value, and implementation MUST apply them consistently.
- Daily totals MUST include each applicable meal entry once and MUST agree with the
  displayed entries for that day.
- Tests MUST cover total calculations, empty days, and any supported edit or removal
  behavior.

### IV. Requirements Traceability
**Principle:** Connect every implemented behavior and validation check to an explicit
requirement.

**Why it matters:** Traceability prevents features from being missed while keeping
work focused on what users asked for.

**Development rules:**
- Specifications MUST express functional requirements as observable behaviors with
  acceptance criteria.
- Plans MUST identify the components and checks needed to satisfy those criteria,
  without introducing unrelated capabilities.
- Implementation and tests MUST be traceable to requirements; validation MUST report
  any requirement that is incomplete or unverified.

### V. Maintainability
**Principle:** Keep the application easy to understand, change, and test.

**Why it matters:** A small application benefits from simple ownership and clear
responsibilities rather than infrastructure that obscures its behavior.

**Development rules:**
- Code MUST follow established project structure and naming conventions, and keep
  responsibilities cohesive.
- Shared logic MUST have one clear source of truth; duplication that risks inconsistent
  calculations MUST be avoided.
- Changes MUST include focused tests for meaningful behavior and update directly
  affected documentation.
- Plans MUST account for maintainability without prescribing architecture beyond
  project needs.

### VI. Input Validation and Error Handling
**Principle:** Validate user input at entry points and explain recoverable errors clearly.

**Why it matters:** Invalid or misunderstood values can corrupt nutrition records or
make the application frustrating to use.

**Development rules:**
- Meal names and nutrition values MUST be validated according to documented
  requirements; numeric nutrition values MUST NOT accept invalid negative or
  non-numeric inputs.
- Optional targets MUST be distinguishable from unset targets; an unset target MUST
  NOT be treated as zero.
- Validation errors MUST identify the affected input and how to correct it, while
  preserving other valid user input where practical.
- Tests MUST cover invalid, boundary, and missing values as well as successful entry.

### VII. Privacy and Security
**Principle:** Collect and expose only the data and access required by the agreed
application behavior.

**Why it matters:** Meal and nutrition records are personal information, and
unnecessary collection or exposure creates avoidable risk.

**Development rules:**
- Specifications MUST identify what user data is handled and MUST NOT add data
  collection or sharing that is not required.
- Plans MUST use the simplest appropriate safeguards for the chosen storage and
  access model; secrets MUST NOT be committed or exposed to client code.
- Implementation MUST avoid logging sensitive meal details unnecessarily and MUST
  protect records from unintended access within the supported application model.
- Validation MUST check relevant access and data-handling behavior; security claims
  MUST not exceed what the implementation demonstrates.

### VIII. Scope Control
**Principle:** Deliver only the defined nutrition-tracking capabilities unless scope
is explicitly amended.

**Why it matters:** Restricting scope keeps this fundamentals-level application
focused, testable, and appropriately small.

**Development rules:**
- The baseline scope is manual meal entry, calorie and protein tracking, optional
  daily targets, and daily progress display.
- Features such as barcode scanning, food databases, social sharing, meal plans,
  recommendations, or additional nutrients MUST NOT be added without an approved
  requirement.
- Specifications and plans MUST call out assumptions and out-of-scope requests;
  implementation MUST defer them rather than silently expanding scope.
- Validation MUST confirm the requested scope is complete and identify unrelated
  behavior introduced by the change.

## Additional Constraints
The application MUST remain appropriate for a small web project. No particular
framework, database, deployment platform, or external nutrition service is mandated
by this constitution; select technology only when project requirements justify it.
The tracker records user-provided nutrition information and MUST NOT present itself as
medical advice or as an authoritative source of nutrition facts.

## Development Workflow
1. **Specification:** Define user-visible behavior, acceptance criteria, data meaning,
   validation, and out-of-scope features.
2. **Planning:** Map requirements to a simple implementation approach and focused
   validation checks; explain any necessary complexity.
3. **Implementation:** Deliver only the approved scope, preserve data integrity, and
   handle invalid input and errors explicitly.
4. **Validation:** Test each acceptance criterion, including relevant boundaries and
   empty or unset states; report checks that could not be run.
5. **Review:** Check traceability, privacy, maintainability, and scope before
   considering the work complete.

Any exception MUST identify the unmet rule, reason, and impact, and receive
maintainer review before merge.

## Governance
This constitution governs specification, planning, implementation, and validation.
Amendments MUST document their rationale, affected principles, and impact, and MUST
be reviewed by the responsible maintainer. Version changes follow semantic
versioning: MAJOR for incompatible principle or governance changes, MINOR for new
principles or materially expanded requirements, and PATCH for clarifications that do
not change obligations.

Every specification, plan, implementation, and validation MUST be reviewed for
compliance with this constitution. Conflicts MUST be resolved before proceeding or
recorded as a reviewed exception; requirements and risks MUST NOT be silently waived.

**Version**: 2.0.0 | **Ratified**: 2026-10-31 | **Last Amended**: 2026-10-31
