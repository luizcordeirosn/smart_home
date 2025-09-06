from enum import Enum, auto


class DoorEnum(Enum):
    LOCKED = auto()
    UNLOCKED = auto()
    OPENED = auto()

    def __str__(self):
        return f"{self.name}"


class SwitchEnum(Enum):
    OFF = auto()
    ON = auto()

    def __str__(self):
        return f"{self.name}"


class ColorEnum(Enum):
    WARM = auto()
    COOL = auto()
    NEUTRAL = auto()
    DAYLIGHT = auto()

    def __str__(self):
        return f"{self.name}"


class SprinklerState(Enum):
    IDLE = auto()
    WATERING = auto()
    PAUSED = auto()
