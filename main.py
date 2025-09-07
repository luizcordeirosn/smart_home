from smart_home.core.enums import (
    CameraStateEnum,
    ColorEnum,
    DoorEnum,
    SprinklerStateEnum,
    SwitchEnum,
    ThermostatStateEnum,
)
from smart_home.core.hub import Hub
from smart_home.core.observers import LoggingObserver
from smart_home.devices.bulb import Bulb
from smart_home.devices.camera import Camera
from smart_home.devices.door import Door
from smart_home.devices.outlet import Outlet
from smart_home.devices.sprinkler import Sprinkler
from smart_home.devices.thermostat import Thermostat


def setup_devices_hub(smart_home):
    for _ in range(5):
        smart_home.add_devices("door", Door(initial_state=DoorEnum.OPENED))

    for _ in range(20):
        smart_home.add_devices("bulb", Bulb(initial_state=SwitchEnum.ON))

    for _ in range(10):
        smart_home.add_devices("outlet", Outlet(initial_state=SwitchEnum.ON))

    for _ in range(3):
        smart_home.add_devices("sprinkler", Sprinkler())

    for _ in range(3):
        smart_home.add_devices("thermostat", Thermostat())

    for _ in range(3):
        smart_home.add_devices("camera", Camera(memory_mb=2000))


def setup_routines(smart_home):
    leaving_home_routine = {
        "name": "leaving_home",
        "actions": [
            {"type": "door", "indices": (2, 4), "target_state": DoorEnum.LOCKED},
            {"type": "bulb", "indices": "all", "target_state": SwitchEnum.OFF},
            {"type": "outlet", "indices": "all", "target_state": SwitchEnum.OFF},
            {"type": "thermostat", "indices": (0,), "target_temperature": 28.0},
            {
                "type": "sprinkler",
                "indices": "all",
                "target_state": SprinklerStateEnum.IDLE,
            },
            {
                "type": "camera",
                "indices": "all",
                "target_state": CameraStateEnum.RECORDING,
            },
        ],
    }

    good_night_routine = {
        "name": "good_night",
        "actions": [
            {"type": "door", "indices": "all", "target_state": DoorEnum.LOCKED},
            {
                "type": "bulb",
                "indices": (0, 3),
                "target_state": SwitchEnum.ON,
                "attributes": {"brightness": 30},
            },
            {"type": "bulb", "indices": (3, 10), "target_state": SwitchEnum.OFF},
            {
                "type": "thermostat",
                "indices": (0,),
                "target_state": ThermostatStateEnum.COOLING,
                "attributes": {"target_temperature": 18},
            },
            {
                "type": "camera",
                "indices": "all",
                "target_state": CameraStateEnum.RECORDING,
            },
        ],
    }

    smart_home.routines.append(leaving_home_routine)
    smart_home.routines.append(good_night_routine)


if __name__ == "__main__":
    print("__HUB__")

    smart_home = Hub()
    logging = LoggingObserver()

    smart_home.add_observer(logging)

    setup_devices_hub(smart_home)
    setup_routines(smart_home)

    action = smart_home.routines[0].get("actions")[0]

    for door in smart_home.devices.get("door"):
        print(door.state)

    print("____")

    smart_home.exec_door_routine(action)

    for door in smart_home.devices.get("door"):
        print(door.state)
