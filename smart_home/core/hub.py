from abc import ABC

from smart_home.core.enums import (
    CameraStateEnum,
    ColorEnum,
    DoorEnum,
    SprinklerStateEnum,
    SwitchEnum,
    ThermostatStateEnum,
)
from smart_home.core.logger import Logger
from smart_home.devices.bulb import Bulb
from smart_home.devices.camera import Camera
from smart_home.devices.door import Door
from smart_home.devices.outlet import Outlet
from smart_home.devices.sprinkler import Sprinkler
from smart_home.devices.thermostat import Thermostat


class Subject(ABC):
    def __init__(self):
        self.__observers = []

    @property
    def observers(self):
        return self.__observers

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_event(self, **kwargs):
        for obs in self.observers:
            obs.update(**kwargs)


class Hub(Subject):
    def __init__(self):
        self.__devices = {}
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

        logger = Logger()

        self.__routines = logger.load_config_from_json().get("routines")

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

    def add_devices(self, device_id, device_type, **kwargs):
        device_list = self.devices.get(device_type, [])

        exist_device = self.exist_device(device_type, device_id)

        if exist_device:
            raise ValueError(
                f"Device of type '{device_type}' with ID '{device_id}' already exists."
            )

        device_class = self.class_map.get(device_type)
        device = device_class(device_id, **kwargs)

        device_list.append(device)

        self.devices[device_type] = device_list

    def get_routine_by_device_type_and_device_id(self, device_type, device_id):
        devices = list(
            filter(
                lambda d: d.device_id == device_id, self.devices.get(device_type, [])
            )
        )

        if len(devices) == 1:
            return devices[0]

    def exist_device(self, device_type, device_id):
        device = list(
            filter(
                lambda d: d.device_id == device_id, self.devices.get(device_type, [])
            )
        )

        return len(device) > 0

    def exec_routine(self, routine_name):
        routine = self.routines.get(routine_name)

        if routine is None:
            return

        for action in routine:
            handler = self.routine_handlers.get(action.get("type"))
            if handler:
                handler(action)

    def change_doors_state(self, action):
        device_type = action.get("type")
        device_id = action.get("device_id")

        target_state_name = action.get("target_state")
        target_state_enum = self.enum_map.get(device_type)
        target_state = target_state_enum[target_state_name]

        device = self.get_routine_by_device_type_and_device_id(
            device_type,
            device_id,
        )

        if device is None:
            return

        door_cycle = [device.close, device.lock, device.unlock, device.open]

        for cycle in door_cycle:
            if device.state == target_state:
                break
            cycle()
            self.notify_event(**device.event_data)

    def change_bulbs_state(self, action):
        device_type = action.get("type")
        device_id = action.get("device_id")

        target_state_name = action.get("target_state")
        target_state_enum = self.enum_map.get(device_type)
        target_state = target_state_enum[target_state_name]

        attributes = action.get("attributes")

        device = self.get_routine_by_device_type_and_device_id(
            device_type,
            device_id,
        )

        if device is None:
            return

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
            # TODO Verificar lógica com relação a mudança de estados durante a rotina
            if brightness != device.brightness and device.state == SwitchEnum.ON:
                cycle(brightness_value=brightness)
                self.notify_event(**device.event_data)
            elif color != device.current_color and device.state == SwitchEnum.ON:
                cycle(color=color)
                self.notify_event(**device.event_data)
            else:
                cycle()
                self.notify_event(**device.event_data)

    def change_outlets_state(self, action):
        device_type = action.get("type")
        device_id = action.get("device_id")

        target_state_name = action.get("target_state")
        target_state_enum = self.enum_map.get(device_type)
        target_state = target_state_enum[target_state_name]

        device = self.get_routine_by_device_type_and_device_id(
            device_type,
            device_id,
        )

        if device is None:
            return

        outlet_cycle = [
            device.turn_off,
            device.turn_on,
        ]

        for cycle in outlet_cycle:
            if device.state == target_state:
                break
            cycle()
            self.notify_event(**device.event_data)

    def change_sprinklers_state(self, action):
        device_type = action.get("type")
        device_id = action.get("device_id")

        target_state_name = action.get("target_state")
        target_state_enum = self.enum_map.get(device_type)
        target_state = target_state_enum[target_state_name]

        device = device = self.get_routine_by_device_type_and_device_id(
            device_type,
            device_id,
        )

        if device is None:
            return

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
            self.notify_event(**device.event_data)

    def change_thermostats_state(self, action):
        device_type = action.get("type")
        device_id = action.get("device_id")

        target_state_name = action.get("target_state")
        target_state_enum = self.enum_map.get(device_type)
        target_state = target_state_enum[target_state_name]

        attributes = action.get("attributes")

        device = device = device = self.get_routine_by_device_type_and_device_id(
            device_type,
            device_id,
        )

        if device is None:
            return

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
                self.notify_event(**device.event_data)
            elif target_state == ThermostatStateEnum.COOLING:
                device.current_temperature += 1
                cycle(target_temperature=target_temperature)
                self.notify_event(**device.event_data)
            elif target_state == ThermostatStateEnum.HEATING:
                device.current_temperature -= 1
                cycle(target_temperature=target_temperature)
                self.notify_event(**device.event_data)
            else:
                cycle()
                self.notify_event(**device.event_data)

    def change_cameras_state(self, action):
        device_type = action.get("type")
        device_id = action.get("device_id")

        target_state_name = action.get("target_state")
        target_state_enum = self.enum_map.get(device_type)
        target_state = target_state_enum[target_state_name]

        device = device = device = self.get_routine_by_device_type_and_device_id(
            device_type,
            device_id,
        )

        if device is None:
            return

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
            self.notify_event(**device.event_data)

    def publish_event(self, **kwargs):
        self.notify_event(**kwargs)
