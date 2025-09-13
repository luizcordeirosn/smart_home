from smart_home.core.hub import Hub
from smart_home.core.observers import EventHandler

if __name__ == "__main__":
    print("__HUB__")

    smart_home = Hub()
    event_handler = EventHandler()

    smart_home.add_observer(event_handler)

    for device_type, devices in smart_home.devices.items():
        print(f"__{device_type}__")
        for device in devices:
            print(
                device.state,
                device.device_name,
            )
            if device_type == "sprinkler":
                print(device.start_usage_time)
