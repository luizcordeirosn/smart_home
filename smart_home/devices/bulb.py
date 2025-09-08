from transitions import Machine

from smart_home.core.descriptors import BrightnessRange, ValidColor
from smart_home.core.enums import ColorEnum, EventType, SwitchEnum
from smart_home.devices.device import Device


class Bulb(Device):
    __brightness = BrightnessRange()
    __current_color = ValidColor()

    def __init__(
        self,
        device_id,
        device_name="Default Bulb",
        initial_state: SwitchEnum = SwitchEnum.OFF,
    ):
        self.__brightness = 75
        self.__current_color = ColorEnum.NEUTRAL

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
                "conditions": "is_brightness_in_range",
                "after": "update_brightness",
            },
            {
                "trigger": "set_color",
                "source": SwitchEnum.ON,
                "dest": SwitchEnum.ON,
                "conditions": "is_valid_color",
                "after": "update_color",
            },
        ]

        self.machine = Machine(
            self,
            states=SwitchEnum,
            transitions=transitions,
            initial=initial_state,
            send_event=True,
            prepare_event="reset_event_data",
            after_state_change="set_current_event",
            on_exception="on_enter_exception",
        )

        super().__init__(device_id, device_name)

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
        self.__current_color = value

    def is_brightness_in_range(self, event):
        brightness_value = event.kwargs.get("brightness_value")

        if brightness_value is None:
            raise ValueError("brightness_value argument is missing")

        return 0 <= brightness_value <= 100

    def is_valid_color(self, event):
        color = event.kwargs.get("color")

        if color is None:
            raise ValueError("color argument is missing")

        return isinstance(color, ColorEnum)

    def update_brightness(self, event):
        self.brightness = event.kwargs.get("brightness_value")

        self.event_data["type"] = EventType.BULB_UPDATE_BRIGHTNESS
        self.event_data["brightness"] = self.brightness

    def update_color(self, event):
        self.current_color = event.kwargs.get("color")

        self.event_data["type"] = EventType.BULB_UPDATE_COLOR
        self.event_data["current_color"] = self.current_color
