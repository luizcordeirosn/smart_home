import csv
import os
from datetime import datetime

from transitions import Machine

from smart_home.utils.descriptors import PositivePower
from smart_home.utils.enums import SwitchEnum


class Outlet:
    __power_w = PositivePower()

    def __init__(self, initial_power_w: float = 600):
        self.power_w = initial_power_w
        self.__usage_wh = 0
        self.__usage_start_time = None

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
    def usage_start_time(self):
        return self.__usage_start_time

    @usage_start_time.setter
    def usage_start_time(self, value):
        self.__usage_start_time = value

    def on_enter_ON(self):
        self.usage_start_time = datetime.now()

    def on_enter_OFF(self):
        usage_time = datetime.now() - self.usage_start_time

        self.usage_wh += (usage_time.total_seconds() / 3600) * self.power_w
