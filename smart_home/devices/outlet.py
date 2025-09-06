from datetime import datetime

from transitions import Machine

from smart_home.utils.descriptors import PositiveValue
from smart_home.utils.enums import SwitchEnum


class Outlet:
    __power_w = PositiveValue()

    def __init__(self, power_w: int = 600):
        self.power_w = power_w
        self.__usage_wh = 0
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
        ]

        self.machine = Machine(
            self,
            states=SwitchEnum,
            transitions=transitions,
            initial=SwitchEnum.OFF,
        )

    @property
    def power_w(self):
        return self.__power_w

    @power_w.setter
    def power_w(self, value):
        self.__power_w = value

    @property
    def usage_wh(self):
        return self.__usage_wh

    @usage_wh.setter
    def usage_wh(self, value):
        self.__usage_wh = value

    @property
    def start_usage_time(self):
        return self.__start_usage_time

    @start_usage_time.setter
    def start_usage_time(self, value):
        self.__start_usage_time = value

    def on_enter_ON(self):
        self.start_usage_time = datetime.now()

    def on_enter_OFF(self):
        usage_time = datetime.now() - self.start_usage_time

        session_consumption = (usage_time.total_seconds() / 3600) * self.power_w

        self.usage_wh += session_consumption

        print("INFO: Outlet turned off. Usage session logged.")
        print(f"    - Session duration: {usage_time}")
        print(f"    - Session consumption: {session_consumption:.4f} Wh")
        print(f"    - Total accumulated consumption: {self.usage_wh:.4f} Wh")
