from transitions import Machine

from smart_home.core.descriptors import PositiveValue
from smart_home.core.enums import CameraStateEnum


class Camera:
    __memory_mb = PositiveValue()

    def __init__(self, initial_state=CameraStateEnum.OFF, memory_mb=2000):
        self.__memory_mb = memory_mb

        transitions = [
            {
                "trigger": "turn_on",
                "source": CameraStateEnum.OFF,
                "dest": CameraStateEnum.IDLE,
            },
            {
                "trigger": "record",
                "source": CameraStateEnum.IDLE,
                "dest": CameraStateEnum.RECORDING,
                "conditions": "has_enought_memory",
            },
            {
                "trigger": "stop_recording",
                "source": CameraStateEnum.RECORDING,
                "dest": CameraStateEnum.IDLE,
            },
            {
                "trigger": "turn_off",
                "source": CameraStateEnum.IDLE,
                "dest": CameraStateEnum.OFF,
            },
        ]

        self.machine = Machine(
            self, states=CameraStateEnum, transitions=transitions, initial=initial_state
        )

    @property
    def memory_mb(self):
        return self.__memory_mb

    @memory_mb.setter
    def memory_mb(self, value):
        self.__memory_mb = value

    def has_enought_memory(self):
        print(
            f"DEBUG: Checking memory... Available: {self.memory_mb}MB, Required: 50MB"
        )
        return self.memory_mb >= 50

    def is_low_on_memory(self):
        is_low = self.memory_mb < 50
        print(f"Checking memory ({self.memory_mb}MB)... Is memory low? {is_low}")

        return is_low

    def on_enter_RECORDING(self):
        print("INFO: Camera is now recording")

    def on_exit_RECORDING(self):
        self.memory_mb -= 50
        print("INFO: Recording stopped successfully.")
        print(f"    - Remaining space: {self.memory_mb} MB")
