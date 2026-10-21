from validation.result import ValidationResult


class ValidationReport:

    def __init__(self, results: list[ValidationResult]) -> None:
        self.results = results

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