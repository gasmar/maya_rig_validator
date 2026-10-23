# Adding a New Validation Rule

## 1. Create a feature branch

Start from an updated `main` branch.

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/rule-name
```

## 2. Implement the rule

**File:** `maya_validation/rules.py`

- Create a class inheriting from `ValidationRule`.
- Implement `validate(self, context) -> ValidationResult`.
- Retrieve scene data using the context.
- Identify and collect invalid objects.
- Define success and failure messages.
- Return a `ValidationResult` containing:
    - Rule name
    - Pass/fail status
    - Failed objects (full DAG paths)
    - Message

## 3. Register the rule

**File:** `ui/launcher.py`

- Import the new rule.
- Add an instance to the `rules` list.
- No changes to the runner, model, view, or controller should be necessary.

## 4. Test in Maya

- Launch the validator.
- Test a passing scenario.
- Test a failing scenario.
- Verify that failed objects appear in the UI and can be selected.

## 5. Write unit tests

**File:** `tests/test_maya_rules.py`

- Import the new rule.
- Use `FakeMayaContext` to supply test data.
- Test a passing scenario.
- Test a failing scenario.
- Verify `result.passed` and `result.failed_objects`.

Run tests from the project root:

```bash
python -m unittest discover -s tests -v
```

## 6. Commit and merge

After all tests pass:

```bash
git add .
git commit -m "Add new validation rule"
git push -u origin feature/rule-name
```

When ready to merge:

```bash
git switch main
git pull --ff-only origin main
git merge --no-ff feature/rule-name
git push origin main
```

## Important Architecture Reminder

- **Context:** Retrieves Maya scene data.
- **Rule:** Performs validation and creates a result.
- **Runner:** Executes registered rules.
- **Report:** Summarizes validation results.
- **Model:** Stores the report for the UI.
- **View:** Displays the results.
- **Controller:** Connects UI interactions to validation logic.

**Golden rule:** Adding a new validation rule should generally require changes only to `rules.py`, `launcher.py`, and
`test_maya_rules.py`.