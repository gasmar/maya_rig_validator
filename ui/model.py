from validation.report import ValidationReport


class ValidationModel:

    def __init__(self) -> None:
        self.report: ValidationReport | None = None

    def set_report(self, report: ValidationReport) -> None:
        self.report = report

    def get_report(self) -> ValidationReport | None:
        return self.report