from dataclasses import dataclass

from transitions import Machine
from transitions.core import MachineError

from smart_home.utils.enums import DoorEnum


@dataclass
class Door:
    def __post_init__(self):
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

        self.__machine = Machine(
            self,
            states=DoorEnum,
            transitions=transitions,
            initial=DoorEnum.UNLOCKED,
            on_exception="raise_error",
            send_event=True,
        )

    @property
    def invalid_attemps(self):
        return self.__invalid_attemps

    @property
    def machine(self):
        return self.__machine

    @invalid_attemps.setter
    def invalid_attemps(self, value):
        self.__invalid_attemps = value

    def raise_error(self, event):
        self.invalid_attemps += 1
        raise MachineError(event.error)
