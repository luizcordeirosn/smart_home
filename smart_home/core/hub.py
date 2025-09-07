from abc import ABC

from smart_home.core.enums import DoorEnum


class Subject(ABC):
    def __init__(self):
        self.__observers = []
        self.__routines = []

    @property
    def observers(self):
        return self.__observers

    @property
    def routines(self):
        return self.__routines

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

        super().__init__()

    @property
    def devices(self):
        return self.__devices

    def add_devices(self, name, device):
        device_list = self.devices.get(name, [])

        device_list.append(device)

        self.devices[name] = device_list

    def publish_event(self, **kwargs):
        self.notify_event(**kwargs)

    def exec_routine(self, routine_name):
        routine = self.routines.get(routine_name)

        if routine:
            pass

    def exec_door_routine(self, action):
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
            is_target_state = True
            while is_target_state:
                if device.state == target_state:
                    is_target_state = False
                try:
                    if device.state == DoorEnum.OPENED:
                        device.close()
                except Exception:
                    pass
                try:
                    if device.state == DoorEnum.UNLOCKED:
                        device.lock()
                except Exception:
                    pass
