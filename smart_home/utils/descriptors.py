from smart_home.utils.enums import ColorEnum


class BrightnessRange:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise ValueError("Brightness value isn't a int type")
        if not (0 <= value <= 100):
            raise ValueError("Brightness value isn't between 0 and 100")
        setattr(obj, self.private_name, value)


class ValidColor:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, owner):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if not isinstance(value, ColorEnum):
            raise ValueError("Color value isn't a ColorEnum type")
        if value not in [color for color in ColorEnum]:
            raise ValueError("Color value isn't a valid color")
        setattr(obj, self.private_name, value)
