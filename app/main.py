from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_value = min_amount
        self.max_value = max_amount

    def __get__(self, instance: Any, owner: type) -> int:
        return getattr(instance, self.name)

    def __set__(self, instance: Any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError
        if value < self.min_value or value > self.max_value:
            raise ValueError
        setattr(instance, self.name, value)

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name


class Visitor:
    def __init__(self, name: str, age: int, height: int, weight: int) -> None:
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight


class SlideLimitationValidator(ABC):
    def __init__(self, age: int, height: int, weight: int) -> None:
        self.age = age
        self.height = height
        self.weight = weight


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        limitation = self.limitation_class(
            visitor.age,
            visitor.height,
            visitor.weight)
        try:
            limitation.age = visitor.age
            limitation.height = visitor.height
            limitation.weight = visitor.weight
            return True
        except (TypeError, ValueError):
            return False
