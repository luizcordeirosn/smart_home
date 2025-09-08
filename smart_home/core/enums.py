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


class EventType(Enum):
    DOOR_ON_INVALID_ATTEMPT = auto()
    BULB_UPDATE_BRIGHTNESS = auto()
    BULB_UPDATE_COLOR = auto()
    BULB_ON_ENTER_OFF = auto()
    OUTLET_ON_ENTER_OFF = auto()
    SPRINKLER_ON_EXIT_WATERING = auto()
    THERMOSTAT_ON_ENTER_IDLE = auto()
    THERMOSTAT_ON_ENTER_COOLING = auto()
    THERMOSTAT_ON_ENTER_HEATING = auto()
    THERMOSTAT_ON_ENTER_OFF = auto()
    CAMERA_HAS_ENOUGH_MEMORY = auto()
    CAMERA_ON_ENTER_RECORDING = auto()
    CAMERA_ON_EXIT_RECORDING = auto()
