
class ValidationResult:
    def __init__(
            self,
            name: str,
            passed: bool,
            failed_objects: list[str],
            message: str
    ) -> None:
        
        self.name = name
        self.passed = passed
        self.failed_objects = failed_objects
        self.message = message
