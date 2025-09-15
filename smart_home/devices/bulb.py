from datetime import datetime

from smart_home.core.descriptors import BrightnessRange, ValidColor
from smart_home.core.enums import ColorEnum, EventType, SwitchEnum
from smart_home.devices.device import Device


class Bulb(Device):
    __brightness = BrightnessRange()
    __current_color = ValidColor()

    def __init__(
        self,
        device_id: str,
        device_name: str = "Default Bulb",
        initial_state: str = "OFF",
    ):
        self.__brightness: int = 75
        self.__current_color: ColorEnum = ColorEnum.NEUTRAL
        self.__start_usage_time = None

        transitions = [
            {
                "trigger": "turn_on",
                "source": SwitchEnum.OFF,
                "dest": SwitchEnum.ON,
            },
            {
                "trigger": "turn_off",
                "source": SwitchEnum.ON,
                "dest": SwitchEnum.OFF,
            },
            {
                "trigger": "set_brightness",
                "source": SwitchEnum.ON,
                "dest": SwitchEnum.ON,
                "after": "update_brightness",
            },
            {
                "trigger": "set_color",
                "source": SwitchEnum.ON,
                "dest": SwitchEnum.ON,
                "after": "update_color",
            },
        ]

        super().__init__(
            device_id,
            device_name,
            SwitchEnum,
            transitions,
            initial_state,
        )

    @property
    def brightness(self):
        return self.__brightness

    @brightness.setter
    def brightness(self, value):
        self.__brightness = value

    @property
    def current_color(self):
        return self.__current_color

    @current_color.setter
    def current_color(self, value):
        if isinstance(value, str):
            value = ColorEnum[value]
        self.__current_color = value

    @property
    def start_usage_time(self):
        return self.__start_usage_time

    @start_usage_time.setter
    def start_usage_time(self, value):
        if isinstance(value, str):
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        self.__start_usage_time = value

    def on_enter_ON(self, event):
        self.start_usage_time = datetime.now()

    def on_enter_OFF(self, event):
        usage_time = datetime.now() - self.start_usage_time

        self.event_data["type"] = EventType.BULB_ON_ENTER_OFF
        self.event_data["usage_time"] = usage_time

    def update_brightness(self, event):
        brightness_value = event.kwargs.get("brightness_value")

        if brightness_value is None:
            raise ValueError("brightness_value is missing")

        self.brightness = brightness_value
        self.event_data["type"] = EventType.BULB_UPDATE_BRIGHTNESS
        self.event_data["brightness"] = self.brightness

    def update_color(self, event):
        color = event.kwargs.get("color").upper()

        if color is None:
            raise ValueError("color argument is missing")

        self.current_color = color
        self.event_data["type"] = EventType.BULB_UPDATE_COLOR
        self.event_data["current_color"] = self.current_color

    def __repr__(self):
        return (
            f"{self.device_name} | "
            f"{self.state} | "
            f"Brightness: {self.brightness} | "
            f"Current Color: {self.current_color.name}"
        )
