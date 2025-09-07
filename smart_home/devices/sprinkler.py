from datetime import datetime

from transitions import Machine

from smart_home.core.descriptors import PositiveValue
from smart_home.core.enums import EventType, SprinklerStateEnum
from smart_home.devices.device import Device


class Sprinkler(Device):
    __flow_rate = PositiveValue()

    def __init__(
        self,
        device_name="Default Sprinkler",
        initial_state: SprinklerStateEnum = SprinklerStateEnum.IDLE,
        flow_rate: int = 15,
    ):
        self.flow_rate = flow_rate
        self.__usage_lh = 0
        self.__start_usage_time = None

        transitions = [
            {
                "trigger": "turn_on",
                "source": SprinklerStateEnum.IDLE,
                "dest": SprinklerStateEnum.WATERING,
            },
            {
                "trigger": "pause_watering",
                "source": SprinklerStateEnum.WATERING,
                "dest": SprinklerStateEnum.PAUSED,
            },
            {
                "trigger": "resume_watering",
                "source": SprinklerStateEnum.PAUSED,
                "dest": SprinklerStateEnum.WATERING,
            },
            {
                "trigger": "stop_watering",
                "source": [SprinklerStateEnum.WATERING, SprinklerStateEnum.PAUSED],
                "dest": SprinklerStateEnum.IDLE,
            },
        ]

        self.machine = Machine(
            model=self,
            states=SprinklerStateEnum,
            transitions=transitions,
            initial=initial_state,
            send_event=True,
            after_state_change="set_current_event",
        )

        super().__init__(device_name)

    @property
    def flow_rate(self):
        return self.__flow_rate

    @flow_rate.setter
    def flow_rate(self, value):
        self.__flow_rate = value

    @property
    def usage_lh(self):
        return self.__usage_lh

    @usage_lh.setter
    def usage_lh(self, value):
        self.__usage_lh = value

    @property
    def start_usage_time(self):
        return self.__start_usage_time

    @start_usage_time.setter
    def start_usage_time(self, value):
        self.__start_usage_time = value

    def on_enter_WATERING(self, event):
        self.start_usage_time = datetime.now()

    def on_exit_WATERING(self, event):
        usage_time = datetime.now() - self.start_usage_time

        session_consumption = (usage_time.total_seconds() / 3600) * self.flow_rate

        self.usage_lh += session_consumption

        self.event_data["type"] = EventType.SPRINKLER_ON_EXIT_WATERING
        self.event_data["usage_time"] = usage_time
        self.event_data["session_consumption"] = session_consumption
        self.event_data["usage_lh"] = self.usage_lh
