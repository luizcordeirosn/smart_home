from smart_home.core.hub import Hub
from smart_home.core.observers import EventHandler

if __name__ == "__main__":
    print("__HUB__")

    smart_home = Hub()
    event_handler = EventHandler()

    smart_home.add_observer(event_handler)

    smart_home.add_device(
        device_id="entrance_door",
        device_type="door",
        initial_state="OPENED",
    )

    smart_home.add_device(
        device_id="living_room_door",
        device_name="Living Room Door",
        device_type="door",
        initial_state="OPENED",
    )

    smart_home.add_device(
        device_id="living_room_bulb",
        device_type="bulb",
        device_name="Living Room Bulb",
        initial_state="ON",
    )

    smart_home.add_device(
        device_id="living_room_outlet",
        device_type="outlet",
        power_w=750,
    )

    smart_home.add_device(
        device_id="garden_sprinkler",
        device_type="sprinkler",
        flow_rate=20,
    )

    smart_home.add_device(
        device_id="living_room_thermostat",
        device_type="thermostat",
        initial_state="OFF",
    )

    smart_home.add_device(
        device_id="security_cam",
        device_type="camera",
        memory_mb=3000,
    )

    print("__DOOR__")
    print(
        smart_home.devices.get("door")[0].state,
        smart_home.devices.get("door")[0].device_id,
        smart_home.devices.get("door")[0].device_name,
    )
    print(
        smart_home.devices.get("door")[1].state,
        smart_home.devices.get("door")[1].device_id,
        smart_home.devices.get("door")[1].device_name,
    )

    print("__BULB__")
    print(
        smart_home.devices.get("bulb")[0].state,
        smart_home.devices.get("bulb")[0].device_id,
        smart_home.devices.get("bulb")[0].device_name,
        smart_home.devices.get("bulb")[0].brightness,
        smart_home.devices.get("bulb")[0].current_color,
    )

    print("__OUTLET__")
    print(
        smart_home.devices.get("outlet")[0].state,
        smart_home.devices.get("outlet")[0].device_id,
        smart_home.devices.get("outlet")[0].device_name,
        smart_home.devices.get("outlet")[0].power_w,
    )

    print("__SPRINKLER__")
    print(
        smart_home.devices.get("sprinkler")[0].state,
        smart_home.devices.get("sprinkler")[0].device_id,
        smart_home.devices.get("sprinkler")[0].device_name,
        smart_home.devices.get("sprinkler")[0].flow_rate,
    )

    print("__THERMOSTAT__")
    print(
        smart_home.devices.get("thermostat")[0].state,
        smart_home.devices.get("thermostat")[0].device_id,
        smart_home.devices.get("thermostat")[0].device_name,
        smart_home.devices.get("thermostat")[0].current_temperature,
    )

    print("__CAMERA__")
    print(
        smart_home.devices.get("camera")[0].state,
        smart_home.devices.get("camera")[0].device_id,
        smart_home.devices.get("camera")[0].device_name,
        smart_home.devices.get("camera")[0].memory_mb,
    )

    smart_home.devices.get("thermostat")[0].check_temperature()
    smart_home.notify(**smart_home.devices.get("thermostat")[0].event_data)

    print("__EXEC_ROUTINE__")
    for device_type, devices in smart_home.devices.items():
        print(f"__{device_type}__")
        for device in devices:
            print(
                device.state,
                device.device_name,
            )

    smart_home.exec_routine("leaving_home")

    print("___")

    for device_type, devices in smart_home.devices.items():
        print(f"__{device_type}__")
        for device in devices:
            print(
                device.state,
                device.device_name,
            )

    device = smart_home.get_device_by_device_type_and_device_id(
        "bulb", "living_room_bulb"
    )
    print(device.state, device.brightness, device.current_color)
    smart_home.exec_device_comand(
        "thermostat",
        "living_room_thermostat",
        "check_temperature",
        target_temperature=30.0,
    )
    device = smart_home.get_device_by_device_type_and_device_id(
        "bulb", "living_room_bulb"
    )
    print(device.state, device.brightness, device.current_color)

    smart_home.get_device_commands_by_device_type_and_device_id(
        "door", "living_room_door"
    )

    commands = smart_home.get_device_commands_by_device_type_and_device_id(
        "door", "living_room_door"
    )
    print(commands)
    commands = smart_home.get_device_commands_by_device_type_and_device_id(
        "bulb", "living_room_bulb"
    )
    print(commands)
    commands = smart_home.get_device_commands_by_device_type_and_device_id(
        "outlet", "living_room_outlet"
    )
    print(commands)
    commands = smart_home.get_device_commands_by_device_type_and_device_id(
        "sprinkler", "garden_sprinkler"
    )
    print(commands)
    commands = smart_home.get_device_commands_by_device_type_and_device_id(
        "thermostat", "living_room_thermostat"
    )
    print(commands)
    commands = smart_home.get_device_commands_by_device_type_and_device_id(
        "camera", "security_cam"
    )
    print(commands)

    print("__")

    device = smart_home.get_device_by_device_type_and_device_id(
        "bulb", "living_room_bulb"
    )
