from dataclasses import dataclass

from transitions import Machine

from smart_home.utils.descriptors import BrightnessRange, ValidColor
from smart_home.utils.enums import ColorEnum, SwitchEnum


@dataclass
class Bulb:
    __brightness = BrightnessRange()
    __current_color = ValidColor()

    def __post_init__(self):
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
            },
            {
                "trigger": "set_color",
                "source": SwitchEnum.ON,
                "dest": SwitchEnum.ON,
                "conditions": "is_valid_color",
            },
        ]

        self.__machine = Machine(
            self,
            states=SwitchEnum,
            transitions=transitions,
            initial=SwitchEnum.OFF,
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
        try:
            self.brightness = brightness_value
            return True
        except ValueError as e:
            print(f"Error - {e}")
            return False

    def is_valid_color(self, color):
        try:
            self.current_color = color
            return True
        except ValueError as e:
            print(f"Error - {e}")
            return False
