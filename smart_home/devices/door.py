from dataclasses import dataclass

from enums.door_enum import DoorEnum
from transitions import Machine


@dataclass
class Door:
    def __post_init__(self, inital_state=DoorEnum.UNLOCK):
        self.__invalid_attemps: int = 0

        transitions = [
            {
                "trigger": "unlock",
                "source": DoorEnum.LOCK,
                "dest": DoorEnum.UNLOCK,
            },
            {
                "trigger": "lock",
                "source": DoorEnum.UNLOCK,
                "dest": DoorEnum.LOCK,
            },
            {
                "trigger": "open",
                "source": DoorEnum.UNLOCK,
                "dest": DoorEnum.OPEN,
            },
            {
                "trigger": "close",
                "source": DoorEnum.OPEN,
                "dest": DoorEnum.UNLOCK,
            },
        ]

        self.__machine = Machine(
            self,
            states=DoorEnum,
            transitions=transitions,
            initial=inital_state,
        )

    @property
    def invalid_attemps(self):
        return self.__invalid_attemps

    @invalid_attemps.setter
    def invalid_attemps(self, value):
        self.__invalid_attemps = value
