from smart_home.core.descriptors import PositiveValue
from smart_home.core.enums import CameraStateEnum, EventType
from smart_home.devices.device import Device


class Camera(Device):
    __memory_mb = PositiveValue()

    def __init__(
        self,
        device_id: str,
        device_name: str = "Default Camera",
        initial_state: str = "OFF",
        memory_mb: str = 2000,
    ):
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
                "conditions": "has_enough_memory",
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

        super().__init__(
            device_id,
            device_name,
            CameraStateEnum,
            transitions,
            CameraStateEnum[initial_state],
        )

    @property
    def memory_mb(self):
        return self.__memory_mb

    @memory_mb.setter
    def memory_mb(self, value):
        self.__memory_mb = value

    def has_enough_memory(self, event):
        self.event_data["type"] = EventType.CAMERA_HAS_ENOUGH_MEMORY
        self.event_data["memory_mb"] = self.memory_mb

        return self.memory_mb >= 50

    def on_enter_RECORDING(self, event):
        self.event_data["type"] = EventType.CAMERA_ON_ENTER_RECORDING

    def on_exit_RECORDING(self, event):
        self.memory_mb -= 50

        self.event_data["type"] = EventType.CAMERA_ON_EXIT_RECORDING
        self.event_data["memory_mb"] = self.memory_mb
