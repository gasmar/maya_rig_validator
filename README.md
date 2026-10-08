# Maya Rig Validator

A Python validation framework proof of concept designed to explore reusable validation architecture across DCC
applications.

The project separates DCC-agnostic validation infrastructure from Maya-specific validation rules, allowing different
applications to implement their own rules while sharing consistent a execution and reporting interface.

**Current scope:** Five Maya joint validation rules, a generic validation runner, and standardized validation results.

**Purpose:** Evaluate the architecture, identify potential limitations, and gather feedback before expanding the
framework.

## Architecture

The framework is split into two parts:

* `validation/` — Shared validation logic that doesn't depend on Maya.
* `maya_validation/` — Maya-specific rules that use the shared framework.

### Core Components

* **ValidationRule (`rule.py`):** Abstract base class defining the `validate()` method that every rule must implement.
* **ValidationRunner (`runner.py`):** Executes a list of rules and collects their results.
* **ValidationResult (`result.py`):** Stores the validation name, pass/fail status, failed objects, and message.

### Maya Rules

The current implementation includes five joint validations:

* Scene contains joints
* Unique joint names
* Joint naming convention
* Joint rotations
* Joint scales

Each rule inherits from `ValidationRule` and returns a `ValidationResult`.

## Usage

The example runs inside Maya's Python environment.

1. Add the repository root to Python's `sys.path`.
2. Run `example.py` to execute all five validation rules.

```python
import sys

sys.path.append(r"PATH_TO_REPOSITORY")

import example

example.main()
```

The results are printed to Maya's Script Editor, including the validation name, pass/fail status, failed objects, and
message.

NOTE:
For this example, the validator expects joints' suffix to be `_jnt`.

## Future Considerations

* Supporting additional DCCs using the same validation framework.
* Handling validation errors and skipped rules.
* Introducing configurable validation settings.
* Improving how scene data is passed to validation rules.
* Adding unit tests for the shared framework.

The goal is to get feedback on the current architecture before implementing these features.


