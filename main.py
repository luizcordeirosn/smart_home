from smart_home.core.hub import Hub
from smart_home.core.observers import EventHandler
from smart_home.devices.bulb import Bulb
from smart_home.devices.camera import Camera
from smart_home.devices.door import Door
from smart_home.devices.outlet import Outlet
from smart_home.devices.sprinkler import Sprinkler
from smart_home.devices.thermostat import Thermostat


def setup_devices_hub(smart_home):
    for _ in range(5):
        smart_home.add_devices("door", Door())

    for _ in range(20):
        smart_home.add_devices("bulb", Bulb())

    for _ in range(10):
        smart_home.add_devices("outlet", Outlet())

    for _ in range(3):
        smart_home.add_devices("sprinkler", Sprinkler())

    for _ in range(2):
        smart_home.add_devices("thermostat", Thermostat())

    for _ in range(3):
        smart_home.add_devices("camera", Camera(memory_mb=2000))


if __name__ == "__main__":
    print("__HUB__")

    smart_home = Hub()
    event_handler = EventHandler()

    smart_home.add_observer(event_handler)

    setup_devices_hub(smart_home)

    for device_type, devices in smart_home.devices.items():
        print(f"__{device_type}__")
        for device in devices:
            print(device.state)

    smart_home.exec_routine("good_night")

    print("___")

    for device_type, devices in smart_home.devices.items():
        print(f"__{device_type}__")
        for device in devices:
            print(device.state, device.device_name)
