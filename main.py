from smart_home.core.hub import Hub
from smart_home.core.observers import EventHandler

if __name__ == "__main__":
    print("__HUB__")

    smart_home = Hub()

    smart_home.add_observer(EventHandler())

    smart_home.exec_device_comand("bulb", "living_room_bulb", "turn_on")
    smart_home.exec_device_comand("bulb", "living_room_bulb", "set_brightness")

    for device_type, devices in smart_home.devices.items():
        print(f"__{device_type}__")
        for device in devices:
            print(
                device.state,
                device.device_name,
            )
