import re
from typing import Callable


class Validator:
    def validate(self, element) -> bool:
        raise NotImplementedError


class TypeValidator(Validator):
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def validate(self, element) -> bool:
        return isinstance(element, self.expected_type)


class NullValidator(Validator):
    def __init__(self, nullable: bool):
        self.nullable = bool(nullable)

    def validate(self, element) -> bool:
        if element is None:
            return self.nullable
        return True


class RegexValidator(Validator):
    def __init__(self, pattern: str, full_match: bool = True, negate: bool = False, flags: int = 0):
        self.pattern = pattern
        self.full_match = full_match
        self.negate = negate
        self.engine = re.compile(pattern, flags)

    def validate(self, element) -> bool:
        if element is None:
            return True
        if not isinstance(element, str):
            return False
        if self.full_match:
            return bool(self.engine.fullmatch(element)) ^ self.negate
        return bool(self.engine.search(element)) ^ self.negate


class ConstraintValidator(Validator):
    def __init__(self, expr: str):
        self.expr = expr

    def validate(self, element) -> bool:
        try:
            return bool(eval(self.expr, {"element": element}))
        except Exception:
            return False


class CustomFunctionValidator(Validator):
    def __init__(self, func: Callable):
        self.func = func

    def validate(self, element) -> bool:
        return bool(self.func(element))
