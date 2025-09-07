from datetime import datetime

from transitions import Machine

from smart_home.core.descriptors import PositiveValue
from smart_home.core.enums import EventType, SwitchEnum
from smart_home.devices.device import Device


class Outlet(Device):
    __power_w = PositiveValue()

    def __init__(self, power_w: int = 600, initial_state=SwitchEnum.OFF):
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
            initial=initial_state,
            send_event=True,
            after_state_change="set_current_event",
        )

        super().__init__()

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

    def on_enter_ON(self, event):
        self.start_usage_time = datetime.now()

    def on_enter_OFF(self, event):
        usage_time = datetime.now() - self.start_usage_time

        session_consumption = (usage_time.total_seconds() / 3600) * self.power_w

        self.usage_wh += session_consumption

        self.event_data["type"] = EventType.OUTLET_ON_ENTER_OFF
        self.event_data["usage_time"] = usage_time
        self.event_data["session_consumption"] = session_consumption
        self.event_data["usage_wh"] = self.usage_wh
