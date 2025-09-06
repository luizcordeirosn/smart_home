from transitions import Machine

from smart_home.utils.descriptors import BrightnessRange, ValidColor
from smart_home.utils.enums import ColorEnum, SwitchEnum


class Bulb:
    __brightness = BrightnessRange()
    __current_color = ValidColor()

    def __init__(self, initial_state: SwitchEnum = SwitchEnum.OFF):
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
                "after": "_update_brightness",
            },
            {
                "trigger": "set_color",
                "source": SwitchEnum.ON,
                "dest": SwitchEnum.ON,
                "conditions": "is_valid_color",
                "after": "_update_color",
            },
        ]

        self.machine = Machine(
            self,
            states=SwitchEnum,
            transitions=transitions,
            initial=initial_state,
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
        self.__current_color = value

    def is_brightness_in_range(self, brightness_value):
        return 0 <= brightness_value <= 100

    def is_valid_color(self, color):
        return isinstance(color, ColorEnum)

    def _update_brightness(self, brightness_value):
        self.brightness = brightness_value

    def _update_color(self, color):
        self.current_color = color
