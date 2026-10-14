from validation.result import ValidationResult
from validation.rule import ValidationRule


class ValidationRunner:
    def __init__(self, rules: list[ValidationRule]) -> None:
        self.rules = rules

    def run(self, context) -> list[ValidationResult]:
        validation_results = []

        for rule in self.rules:
            validation_results.append(rule.validate(context))

        return validation_results
