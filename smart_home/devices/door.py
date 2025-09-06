from transitions import Machine
from transitions.core import MachineError

from smart_home.core.enums import DoorEnum


class Door:
    def __init__(self, initial_state: DoorEnum = DoorEnum.UNLOCKED):
        self.__invalid_attemps: int = 0

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
        )

    @property
    def invalid_attemps(self):
        return self.__invalid_attemps

    @invalid_attemps.setter
    def invalid_attemps(self, value):
        self.__invalid_attemps = value

    def on_invalid_attempt(self, event):
        self.invalid_attemps += 1
        print(f"Invalid transition attempted. Attempts: {self.invalid_attemps}")
        raise MachineError(event.error)
