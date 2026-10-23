from abc import ABC, abstractmethod
from enum import auto, Enum


class ValidationState(Enum):
    PASS = auto()
    WARNING = auto()
    FAIL = auto()


class ValidationResult:
    def __init__(
            self,
            name: str,
            state: ValidationState,
            failed_objects: list[str],
            message: str
    ) -> None:

        self.name = name
        self.state = state
        self.failed_objects = failed_objects
        self.message = message


class ValidationRule(ABC):
    @abstractmethod
    def validate(self, context) -> ValidationResult:
        pass


class ValidationRunner:
    def __init__(self, rules: list[ValidationRule]) -> None:
        self.rules = rules

    def run(self, context) -> list[ValidationResult]:
        validation_results = []

        for rule in self.rules:
            validation_results.append(rule.validate(context))

        return validation_results


class ValidationReport:

    def __init__(self, results: list[ValidationResult]) -> None:
        self.results = results

    def has_any_failures(self) -> bool:
        for result in self.results:
            if result.state == ValidationState.FAIL:
                return True
        return False

    def get_total_rules(self) -> int:
        return len(self.results)

    def get_passed_rules(self) -> int:
        passed_rules = 0
        for result in self.results:
            if result.passed:
                passed_rules += 1
        return passed_rules

    def get_failed_rules(self) -> int:
        failed_rules = 0
        for result in self.results:
            if not result.passed:
                failed_rules += 1
        return failed_rules

    def is_valid(self) -> bool:
        if self.get_total_rules() == 0 or self.get_failed_rules() > 0:
            return False
        return True

    def get_failed_results(self) -> list[ValidationResult]:
        failed_results = []
        for result in self.results:
            if not result.passed:
                failed_results.append(result)
        return failed_results