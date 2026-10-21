import unittest

from validation.result import ValidationResult
from validation.rule import ValidationRule
from validation.runner import ValidationRunner


class FakeRule(ValidationRule):

    def validate(self, context):
        return ValidationResult(
            name="Fake Rule",
            passed=True,
            failed_objects=[],
            message="Fake validation passed."
        )


class FailingRule(ValidationRule):

    def validate(self, context) -> ValidationResult:
        return ValidationResult(
            name="Failing Rule",
            passed=False,
            failed_objects=["joint1"],
            message="Validation failed."
        )


class ContextCheckRule(ValidationRule):

    def __init__(self) -> None:
        self.received_context = None

    def validate(self, context) -> ValidationResult:
        self.received_context = context

        return ValidationResult(
            name="Context Check",
            passed=True,
            failed_objects=[],
            message="Context received."
        )


class ErrorRule(ValidationRule):
    def validate(self, context) -> ValidationResult:
        raise RuntimeError("Validation crashed.")


class TestValidationRunner(unittest.TestCase):

    def test_runner_with_no_rules(self):
        rules = []
        runner = ValidationRunner(rules)
        results = runner.run(None)

        self.assertEqual(results, rules)

    def test_runner_with_one_rule(self):
        rule = FakeRule()
        rules = [rule]
        runner = ValidationRunner(rules)
        results = runner.run(None)

        self.assertEqual(len(results), len(rules))
        self.assertTrue(results[0].passed)

    def test_runner_passes_context(self):
        rule = ContextCheckRule()
        context = object()
        runner = ValidationRunner([rule])
        runner.run(context)

        self.assertIs(rule.received_context, context)

    def test_runner_with_multiple_rules(self):
        rule1 = FakeRule()
        rule2 = FakeRule()
        rule3 = FakeRule()
        rules = [rule1, rule2, rule3]
        runner = ValidationRunner(rules)
        results = runner.run(None)

        self.assertEqual(len(results), 3)
        self.assertTrue(all(result.passed for result in results))

    def test_runner_with_failing_rule(self):
        rule = FailingRule()
        rules = [rule]
        runner = ValidationRunner(rules)
        results = runner.run(None)

        self.assertFalse(results[0].passed)
        self.assertEqual(results[0].failed_objects, ["joint1"])

    def test_runner_with_mixed_results(self):
        fake_rule1 = FakeRule()
        failed_rule1 = FailingRule()
        fake_rule2 = FakeRule()
        rules = [fake_rule1, failed_rule1, fake_rule2]
        runner = ValidationRunner(rules)
        results = runner.run(None)
        passed_values = [result.passed for result in results]

        self.assertEqual(len(results), 3)
        self.assertEqual(passed_values, [True, False, True])

    def test_runner_with_error_rule(self):
        error_rule = ErrorRule()
        runner = ValidationRunner([error_rule])

        with self.assertRaises(RuntimeError):
            runner.run(None)
