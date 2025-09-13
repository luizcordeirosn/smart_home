from smart_home.core.enums import DoorEnum, EventType
from smart_home.devices.device import Device


class Door(Device):
    def __init__(
        self,
        device_id: str,
        device_name: str = "Default Door",
        initial_state: str = "UNLOCKED",
    ):
        self.__invalid_attempts: int = 0

        transitions = [
            {
                "trigger": "unlock",
                "source": DoorEnum.LOCKED,
                "dest": DoorEnum.UNLOCKED,
            },
            {
                "trigger": "lock",
                "source": DoorEnum.UNLOCKED,
                "dest": DoorEnum.LOCKED,
            },
            {
                "trigger": "open",
                "source": DoorEnum.UNLOCKED,
                "dest": DoorEnum.OPENED,
            },
            {
                "trigger": "close",
                "source": DoorEnum.OPENED,
                "dest": DoorEnum.UNLOCKED,
            },
        ]

        super().__init__(
            device_id,
            device_name,
            DoorEnum,
            transitions,
            DoorEnum[initial_state],
            on_exception_method="on_invalid_attempt",
        )

    @property
    def invalid_attempts(self):
        return self.__invalid_attempts

    @invalid_attempts.setter
    def invalid_attempts(self, value):
        self.__invalid_attempts = value

    def on_invalid_attempt(self, event):
        self.invalid_attempts += 1

        self.event_data["type"] = EventType.DOOR_ON_INVALID_ATTEMPT
        self.event_data["invalid_attempts"] = self.invalid_attempts

        self.set_current_event(event)

    def __repr__(self):
        return f"{self.device_name} | {self.state} | {self.invalid_attempts} invalid attempts"
