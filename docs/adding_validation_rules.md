# Adding Validation Rules

This guide explains how to add new validation rules to the Maya Rig Validator.

## Architecture Overview

The validator separates reusable validation logic, Maya-specific functionality, and the Qt interface.

```text
maya_rig_validator/
├── validation/
│   └── validation.py
├── maya_validation/
│   ├── context.py
│   ├── rules.py
│   └── launcher.py
├── ui/
│   └── view.py
└── tests/
    ├── test_maya_rules.py
    └── test_runner.py
```

**Core components:**

- `ValidationRule`: Abstract base class for validation rules.
- `ValidationResult`: Stores a rule's name, state, affected objects, and message.
- `ValidationState`: Defines `PASS`, `WARNING`, and `FAIL`.
- `ValidationRunner`: Executes validation rules against a supplied context.
- `ValidationReport`: Groups results and provides `has_any_failures()`.

The validation framework has no dependencies on Maya or Qt.

## 1. Create a Validation Rule

Add a new class to `maya_validation/rules.py`.

Every rule must inherit from `ValidationRule` and implement `validate(context)`.

Example: A rule that checks whether joints are visible.

```python
from validation.validation import (
    ValidationRule,
    ValidationResult,
    ValidationState,
)


class JointVisibilityRule(ValidationRule):
    def validate(self, context) -> ValidationResult:
        joints = context.get_joints()

        hidden_joints = [
            joint
            for joint in joints
            if not context.get_attribute(joint, "visibility")
        ]

        state = (
            ValidationState.FAIL
            if hidden_joints
            else ValidationState.PASS
        )

        return ValidationResult(
            name="Joint Visibility",
            state=state,
            failed_objects=hidden_joints,
            message="Some joints are hidden." if hidden_joints
            else "All joints are visible.",
        )
```

Rules access scene information through the supplied context rather than importing `maya.cmds` directly.

## 2. Return a ValidationResult

Each rule returns a `ValidationResult` with the following information:

| Field            | Description                                  |
|------------------|----------------------------------------------|
| `name`           | Human-readable name of the validation rule   |
| `state`          | `ValidationState.PASS`, `WARNING`, or `FAIL` |
| `failed_objects` | List of objects associated with the result   |
| `message`        | Description of the validation outcome        |

**Validation states:**

- `PASS`: Validation succeeded.
- `WARNING`: A non-blocking issue was detected.
- `FAIL`: Validation failed.

`ValidationReport.has_any_failures()` returns `True` only when at least one result has the `FAIL` state.

## 3. Register the Rule

Open `maya_validation/launcher.py`.

Import your new rule and add it to the list inside `launch()`:

```python
rules = [
    SceneHasJointsRule(),
    UniqueJointNamesRule(),
    JointNamingConventionRule("_jnt"),
    JointRotationRule(),
    JointScaleRule(),
    JointVisibilityRule(),
    # YourNewRule(),
]
```

The launcher creates the runner and supplies the UI with callable functions for running validation and selecting
objects.

This keeps `ui/view.py` independent of Maya.

## 4. Write Unit Tests

Add tests to `tests/test_maya_rules.py`.

Use a fake context to supply test data without requiring Maya.

Example:

```python
import unittest

from maya_validation.rules import JointVisibilityRule
from validation.validation import ValidationState


class FakeContext:
    def get_joints(self):
        return ["root_jnt"]

    def get_attribute(self, joint, attribute):
        return False


class TestJointVisibilityRule(unittest.TestCase):
    def test_hidden_joint_fails(self):
        result = JointVisibilityRule().validate(FakeContext())

        self.assertEqual(result.state, ValidationState.FAIL)
        self.assertEqual(result.failed_objects, ["root_jnt"])
```

Test both valid and invalid scenarios for each new rule. Add warning-state tests if the rule can produce warnings.

## 5. Run the Tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

Tests should run without Maya when using fake contexts.

## 6. Test in Maya

Launch the validator through `maya_validation.launcher.launch()`.

Verify that:

- The new rule appears in the results list.
- Its state and message are correct.
- Selecting a result displays its details.
- Clicking an affected object selects it in Maya.

## Design Guidelines

- Keep the core validation framework independent of Maya and Qt.
- Put Maya-specific rules and scene access in `maya_validation/`.
- Keep `ui/view.py` independent of Maya.
- Return structured `ValidationResult` objects rather than printing validation outcomes.
- Add unit tests for new rules.
- Register new rules in the Maya launcher.

## POC Limitations

The current UI supports basic PASS/FAIL display. Although the validation framework supports `WARNING`, warning-specific
presentation is not yet implemented.

A custom `QListWidgetItem` for formatting validation results is planned as a separate UI improvement.