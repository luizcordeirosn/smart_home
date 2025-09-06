from abc import ABC, abstractmethod

from smart_home.core.enums import ColorEnum


class ValidatorDescriptor(ABC):
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    @abstractmethod
    def __set__(self, obj, value):
        pass


class BrightnessRange(ValidatorDescriptor):
    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError("Brightness value must be an int type")
        if not (0 <= value <= 100):
            raise ValueError("Brightness value must be an integer between 0 and 100")
        setattr(obj, self.private_name, value)


class ValidColor(ValidatorDescriptor):
    def __set__(self, obj, value):
        if not isinstance(value, ColorEnum):
            raise ValueError("Color value must be a ColorEnum type")
        setattr(obj, self.private_name, value)


class PositiveValue(ValidatorDescriptor):
    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError("Value must be an int type")
        if value < 0:
            raise ValueError("Value must be positive or 0")
        setattr(obj, self.private_name, value)
