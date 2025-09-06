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


class SprinklerStateEnum(Enum):
    IDLE = auto()
    WATERING = auto()
    PAUSED = auto()


class ThermostatStateEnum(Enum):
    OFF = auto()
    IDLE = auto()
    HEATING = auto()
    COOLING = auto()


class CameraStateEnum(Enum):
    OFF = auto()
    IDLE = auto()
    RECORDING = auto()
