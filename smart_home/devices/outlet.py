from datetime import datetime

from smart_home.core.descriptors import PositiveValue
from smart_home.core.enums import EventType, SwitchEnum
from smart_home.devices.device import Device


class Outlet(Device):
    __power_w = PositiveValue()

    def __init__(
        self,
        device_id: str,
        device_name: str = "Default Outlet",
        power_w: int = 600,
        initial_state: str = "OFF",
    ):
        self.__power_w = power_w
        self.__last_usage_wh = 0
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

        super().__init__(
            device_id,
            device_name,
            SwitchEnum,
            transitions,
            initial_state=SwitchEnum[initial_state],
        )

    @property
    def power_w(self):
        return self.__power_w

    @power_w.setter
    def power_w(self, value):
        self.__power_w = value

    @property
    def last_usage_wh(self):
        return self.__last_usage_wh

    @last_usage_wh.setter
    def last_usage_wh(self, value):
        self.__last_usage_wh = value

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

        session_consumption = (usage_time.total_seconds() / 3600) * self.power_w

        self.last_usage_wh = session_consumption

        self.event_data["type"] = EventType.OUTLET_ON_ENTER_OFF
        self.event_data["usage_time"] = usage_time
        self.event_data["session_consumption"] = session_consumption
        self.event_data["usage_wh"] = self.last_usage_wh

    def __repr__(self):
        return (
            f"{self.device_name} | "
            f"{self.state} | "
            f"Power: {self.power_w} | "
            f"Last Usage Wh: {self.last_usage_wh}"
        )
