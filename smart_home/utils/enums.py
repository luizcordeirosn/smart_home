from enum import Enum


class DoorEnum(Enum):
    LOCKED = 1
    UNLOCKED = 2
    OPENED = 3

    def __str__(self):
        return f"{self.name}"


class SwitchEnum(Enum):
    OFF = 1
    ON = 2

    def __str__(self):
        return f"{self.name}"


class ColorEnum(Enum):
    WARM = 1
    COOL = 2
    NEUTRAL = 3
    DAYLIGHT = 4

    def __str__(self):
        return f"{self.name}"
