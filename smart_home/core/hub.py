from abc import ABC

from smart_home.core.enums import ThermostatStateEnum


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
        self.__routines = []
        self.routine_handlers = {
            "door": self.change_doors_state,
            "bulb": self.change_bulbs_state,
            "outlet": self.change_outlets_state,
            "sprinkler": self.change_sprinklers_state,
            "thermostat": self.change_thermostats_state,
            "camera": self.change_cameras_state,
        }

        super().__init__()

    @property
    def devices(self):
        return self.__devices

    @property
    def routines(self):
        return self.__routines

    def add_devices(self, name, device):
        device_list = self.devices.get(name, [])

        device_list.append(device)

        self.devices[name] = device_list

    def publish_event(self, **kwargs):
        self.notify_event(**kwargs)

    def exec_routine(self, routine_name):
        filtered_routine = list(
            filter(lambda r: r["name"] == routine_name, self.routines)
        )

        if len(filtered_routine) > 0:
            routine = filtered_routine[0]
            actions = routine.get("actions")

            for action in actions:
                handler = self.routine_handlers.get(action.get("type"))
                if handler:
                    handler(action)

    def change_doors_state(self, action):
        device_type = action.get("type")
        indices = action.get("indices")
        target_state = action.get("target_state")
        devices = self.devices.get(device_type)

        if indices == "all":
            interval = (0, len(devices))
        elif len(indices) == 1:
            interval = (indices[0], indices[0] + 1)
        else:
            interval = (indices[0], indices[1])

        for i in range(interval[0], interval[1]):
            device = devices[i]
            door_cycle = [device.close, device.lock, device.unlock, device.open]

            for cycle in door_cycle:
                if device.state == target_state:
                    break
                try:
                    cycle()
                except Exception:
                    pass

    def change_bulbs_state(self, action):
        device_type = action.get("type")
        indices = action.get("indices")
        target_state = action.get("target_state")
        attributes = action.get("attributes")
        devices = self.devices.get(device_type)

        if indices == "all":
            interval = (0, len(devices))
        elif len(indices) == 1:
            interval = (indices[0], indices[0] + 1)
        else:
            interval = (indices[0], indices[1])

        for i in range(interval[0], interval[1]):
            device = devices[i]
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
                    if (
                        device.state == target_state
                        and device.brightness == brightness
                        and device.current_color == color
                    ):
                        break
                try:
                    if brightness != device.brightness:
                        cycle(brightness_value=brightness)
                    elif color != device.current_color:
                        cycle(color=color)
                    cycle()
                except Exception:
                    pass

    def change_outlets_state(self, action):
        device_type = action.get("type")
        indices = action.get("indices")
        target_state = action.get("target_state")
        devices = self.devices.get(device_type)

        if indices == "all":
            interval = (0, len(devices))
        elif len(indices) == 1:
            interval = (indices[0], indices[0] + 1)
        else:
            interval = (indices[0], indices[1])

        for i in range(interval[0], interval[1]):
            device = devices[i]
            outlet_cycle = [device.turn_off, device.turn_on]

            for cycle in outlet_cycle:
                if device.state == target_state:
                    break
                try:
                    cycle()
                except Exception:
                    pass

    def change_sprinklers_state(self, action):
        device_type = action.get("type")
        indices = action.get("indices")
        target_state = action.get("target_state")
        devices = self.devices.get(device_type)

        if indices == "all":
            interval = (0, len(devices))
        elif len(indices) == 1:
            interval = (indices[0], indices[0] + 1)
        else:
            interval = (indices[0], indices[1])

        for i in range(interval[0], interval[1]):
            device = devices[i]
            sprinkler_cycle = [
                device.turn_on,
                device.pause_watering,
                device.resume_watering,
                device.stop_watering,
            ]

            for cycle in sprinkler_cycle:
                if device.state == target_state:
                    break
                try:
                    cycle()
                except Exception:
                    pass

    def change_thermostats_state(self, action):
        device_type = action.get("type")
        indices = action.get("indices")
        target_state = action.get("target_state")
        attributes = action.get("attributes")
        devices = self.devices.get(device_type)

        if indices == "all":
            interval = (0, len(devices))
        elif len(indices) == 1:
            interval = (indices[0], indices[0] + 1)
        else:
            interval = (indices[0], indices[1])

        for i in range(interval[0], interval[1]):
            device = devices[i]
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
                try:
                    if target_state == ThermostatStateEnum.IDLE:
                        cycle(target_temperature=target_temperature)
                    elif target_state == ThermostatStateEnum.COOLING:
                        device.current_temperature += 1
                        cycle(target_temperature=target_temperature)
                    elif target_state == ThermostatStateEnum.HEATING:
                        device.current_temperature -= 1
                        cycle(target_temperature=target_temperature)
                    cycle()
                except Exception:
                    pass

    def change_cameras_state(self, action):
        device_type = action.get("type")
        indices = action.get("indices")
        target_state = action.get("target_state")
        devices = self.devices.get(device_type)

        if indices == "all":
            interval = (0, len(devices))
        elif len(indices) == 1:
            interval = (indices[0], indices[0] + 1)
        else:
            interval = (indices[0], indices[1])

        for i in range(interval[0], interval[1]):
            device = devices[i]
            cameras_cycle = [
                device.turn_on,
                device.record,
                device.stop_recording,
                device.turn_off,
            ]

            for cycle in cameras_cycle:
                if device.state == target_state:
                    break
                try:
                    cycle()
                except Exception:
                    pass
