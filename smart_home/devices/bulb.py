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

    def update_brightness(self, event):
        self.brightness = event.kwargs.get("brightness_value")

        self.event_data["type"] = EventType.BULB_UPDATE_BRIGHTNESS
        self.event_data["brightness"] = self.brightness

    def update_color(self, event):
        self.current_color = event.kwargs.get("color").upper()

        self.event_data["type"] = EventType.BULB_UPDATE_COLOR
        self.event_data["current_color"] = self.current_color

    def __repr__(self):
        return f"{self.device_id} | {self.device_name} | {self.brightness} | {self.current_color.name}"
