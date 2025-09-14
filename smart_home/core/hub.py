from smart_home.core.enums import (
    CameraStateEnum,
    ColorEnum,
    DoorEnum,
    SprinklerStateEnum,
    SwitchEnum,
    ThermostatStateEnum,
)
from smart_home.core.error import (
    DeviceIndexError,
    DeviceMachineAttributeError,
    DeviceMachineTriggerError,
    DeviceNotFoundError,
    RoutineNotFoundError,
)
from smart_home.core.persistence import Persistence
from smart_home.devices.bulb import Bulb
from smart_home.devices.camera import Camera
from smart_home.devices.door import Door
from smart_home.devices.outlet import Outlet
from smart_home.devices.sprinkler import Sprinkler
from smart_home.devices.thermostat import Thermostat
from smart_home.utils.patterns import Subject


class Hub(Subject):
    def __init__(self):
        self.__routine_handlers = {
            "door": self.change_doors_state,
            "bulb": self.change_bulbs_state,
            "outlet": self.change_outlets_state,
            "sprinkler": self.change_sprinklers_state,
            "thermostat": self.change_thermostats_state,
            "camera": self.change_cameras_state,
        }
        self.__class_map = {
            "door": Door,
            "bulb": Bulb,
            "outlet": Outlet,
            "sprinkler": Sprinkler,
            "thermostat": Thermostat,
            "camera": Camera,
        }
        self.__enum_map = {
            "door": DoorEnum,
            "bulb": SwitchEnum,
            "bulb_color": ColorEnum,
            "outlet": SwitchEnum,
            "sprinkler": SprinklerStateEnum,
            "thermostat": ThermostatStateEnum,
            "camera": CameraStateEnum,
        }

        self.__devices = {}
        self.__routines = {}

        self.initial_configs()

        super().__init__()

    @property
    def devices(self):
        return self.__devices

    @property
    def routines(self):
        return self.__routines

    @property
    def routine_handlers(self):
        return self.__routine_handlers

    @property
    def class_map(self):
        return self.__class_map

    @property
    def enum_map(self):
        return self.__enum_map

    @routines.setter
    def routines(self, value):
        self.__routines = value

    def initial_configs(self):
        persistence = Persistence()

        configs = persistence.load_config_from_json()

        self.routines = configs.get("routines", {})
        self.parse_from_dict_list_to_devices(configs.get("devices", []))

    def add_device(self, device_type, device_id, **kwargs):
        device_list = self.devices.get(device_type, [])

        if self.exist_device(device_type, device_id):
            raise DeviceIndexError(device_type=device_type, device_id=device_id)

        device_class = self.class_map.get(device_type)
        device = device_class(device_id, **kwargs)

        device_list.append(device)

        self.devices[device_type] = device_list

        return device

    def get_device_by_device_type_and_device_id(self, device_type, device_id):
        if not self.exist_device(device_type, device_id):
            raise DeviceNotFoundError(device_type=device_type, device_id=device_id)

        devices = list(
            filter(
                lambda d: d.device_id == device_id, self.devices.get(device_type, [])
            )
        )

        return devices[0]

    def get_device_commands_by_device_type_and_device_id(self, device_type, device_id):
        device = self.get_device_by_device_type_and_device_id(device_type, device_id)

        len_device_enum = len(self.enum_map.get(device_type))

        return list(device.machine.events.keys())[len_device_enum:]

    def get_routine_by_routine_name(self, routine_name):
        routine = self.routines.get(routine_name)

        if routine is None:
            raise RoutineNotFoundError(routine_name=routine_name)

        return routine

    def get_devices(self):
        print("\nID | Type | State")
        for device_type, devices in self.devices.items():
            for device in devices:
                print(f"{device.device_id} | {device_type.upper()} | {device.state} ")
        print("")

    def delete_device_by_device_type_and_device_id(self, device_type, device_id):
        device = self.get_device_by_device_type_and_device_id(device_type, device_id)

        devices_type = self.devices.get(device_type)

        devices_type.remove(device)

        return device

    def parse_from_devices_to_dict_list(self):
        persistence = Persistence()

        devices = [
            device.as_dict() for value in self.devices.values() for device in value
        ]

        persistence.save_devices_to_json(devices)

    def parse_from_dict_list_to_devices(self, devices):
        for device in devices:
            device_type = device.get("type")
            device_id = device.get("device_id")
            device_name = device.get("device_name")
            device_initial_state = device.get("state")
            device_attributes = device.get("attributes", {})

            device = self.add_device(
                device_type,
                device_id,
                device_name=device_name,
                initial_state=device_initial_state,
            )

            for key_attr, value_attr in device_attributes.items():
                device.__setattr__(key_attr, value_attr)

    def exist_device(self, device_type, device_id):
        device = list(
            filter(
                lambda d: d.device_id == device_id, self.devices.get(device_type, [])
            )
        )

        return len(device) > 0

    def exist_device_command(self, device, command_name):
        device_attributes = device.__dir__()

        return command_name in device_attributes

    def exec_device_comand(self, device_type, device_id, command_name, **kwargs):
        if not self.exist_device(device_type, device_id):
            raise DeviceNotFoundError(device_type=device_type, device_id=device_id)

        device = self.get_device_by_device_type_and_device_id(device_type, device_id)

        if not self.exist_device_command(device, command_name):
            raise DeviceMachineAttributeError(command_name=command_name)

        device.__getattribute__(command_name)(**kwargs)

        event = device.event_data.get("event")
        self.notify(**device.event_data)

        if event.error is not None:
            raise DeviceMachineTriggerError(event=event, trigger=event.event.name)

    def exec_routine(self, routine_name):
        routine = self.get_routine_by_routine_name(routine_name)

        for action in routine:
            handler = self.routine_handlers.get(action.get("type"))
            if handler:
                device_type = action.get("type")
                device_id = action.get("device_id")

                device = self.get_device_by_device_type_and_device_id(
                    device_type,
                    device_id,
                )

                if device is not None:
                    handler(action, device, device_type)

    def change_doors_state(self, action, device, device_type):
        target_state = self.get_target_state_enum(
            action.get("target_state"), device_type
        )

        door_cycle = [device.close, device.lock, device.unlock, device.open]

        for cycle in door_cycle:
            if device.state == target_state:
                break
            cycle()
            self.notify(**device.event_data)

    def change_bulbs_state(self, action, device, device_type):
        target_state = self.get_target_state_enum(
            action.get("target_state"), device_type
        )

        attributes = action.get("attributes")

        bulb_cycle = [
            device.turn_on,
            device.set_brightness,
            device.set_color,
            device.turn_off,
        ]

        for cycle in bulb_cycle:
            if device.state == target_state and attributes is None:
                break
            if attributes is not None:
                brightness = attributes.get("brightness", device.brightness)

                color = attributes.get("color", device.current_color)

                if not isinstance(color, ColorEnum):
                    color_enum = self.enum_map.get("bulb_color")
                    color = color_enum[color]

                if (
                    device.state == target_state
                    and device.brightness == brightness
                    and device.current_color == color
                ):
                    break
            else:
                brightness = device.brightness
                color = device.current_color
            if brightness != device.brightness and device.state == SwitchEnum.ON:
                cycle(brightness_value=brightness)
                self.notify(**device.event_data)
            elif color != device.current_color and device.state == SwitchEnum.ON:
                cycle(color=color)
                self.notify(**device.event_data)
            else:
                cycle()
                self.notify(**device.event_data)

    def change_outlets_state(self, action, device, device_type):
        target_state = self.get_target_state_enum(
            action.get("target_state"), device_type
        )

        outlet_cycle = [
            device.turn_off,
            device.turn_on,
        ]

        for cycle in outlet_cycle:
            if device.state == target_state:
                break
            cycle()
            self.notify(**device.event_data)

    def change_sprinklers_state(self, action, device, device_type):
        target_state = self.get_target_state_enum(
            action.get("target_state"), device_type
        )

        device

        sprinkler_cycle = [
            device.turn_on,
            device.pause_watering,
            device.resume_watering,
            device.stop_watering,
        ]

        for cycle in sprinkler_cycle:
            if device.state == target_state:
                break
            cycle()
            self.notify(**device.event_data)

    def change_thermostats_state(self, action, device, device_type):
        target_state = self.get_target_state_enum(
            action.get("target_state"), device_type
        )

        attributes = action.get("attributes")

        thermostat_cycle = [
            device.turn_on,
            device.check_temperature,
            device.turn_off,
        ]

        for cycle in thermostat_cycle:
            if device.state == target_state and attributes is None:
                break
            if attributes is not None:
                target_temperature = attributes.get(
                    "target_temperature", device.current_temperature
                )
                if (
                    device.state == target_state
                    and device.current_temperature == target_temperature
                ):
                    break
            if target_state == ThermostatStateEnum.IDLE:
                cycle(target_temperature=target_temperature)
                self.notify(**device.event_data)
            elif target_state == ThermostatStateEnum.COOLING:
                device.current_temperature += 1
                cycle(target_temperature=target_temperature)
                self.notify(**device.event_data)
            elif target_state == ThermostatStateEnum.HEATING:
                device.current_temperature -= 1
                cycle(target_temperature=target_temperature)
                self.notify(**device.event_data)
            else:
                cycle()
                self.notify(**device.event_data)

    def change_cameras_state(self, action, device, device_type):
        target_state = self.get_target_state_enum(
            action.get("target_state"), device_type
        )

        cameras_cycle = [
            device.turn_on,
            device.record,
            device.stop_recording,
            device.turn_off,
        ]

        for cycle in cameras_cycle:
            if device.state == target_state:
                break
            cycle()
            self.notify(**device.event_data)

    def get_target_state_enum(self, target_state_name, device_type):
        target_state_enum = self.enum_map.get(device_type)
        return target_state_enum[target_state_name]

    def publish_event(self, **kwargs):
        self.notify(**kwargs)
