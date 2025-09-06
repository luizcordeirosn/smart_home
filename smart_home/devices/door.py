from transitions import Machine
from transitions.core import MachineError

from smart_home.core.enums import DoorEnum
from smart_home.devices.device import Device


class Door(Device):
    def __init__(self, initial_state: DoorEnum = DoorEnum.UNLOCKED):
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

        self.machine = Machine(
            self,
            states=DoorEnum,
            transitions=transitions,
            initial=initial_state,
            on_exception="on_invalid_attempt",
            send_event=True,
            after_state_change="set_current_event",
        )

        super().__init__()

    @property
    def invalid_attempts(self):
        return self.__invalid_attempts

    @invalid_attempts.setter
    def invalid_attempts(self, value):
        self.__invalid_attempts = value

    def on_invalid_attempt(self, event):
        self.invalid_attempts += 1

        self.event_data["type"] = "DOOR_ON_INVALID_ATTEMPT"
        self.event_data["invalid_attempts"] = self.invalid_attempts
        self.event_data["machine_error"] = event.error

        self.set_current_event(event)

        raise MachineError(event.error)
