from abc import ABC, abstractmethod

from validation.result import ValidationResult


class ValidationRule(ABC):
    @abstractmethod
    def validate(self) -> ValidationResult:
        pass