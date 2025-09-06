from abc import ABC


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

    def notify_event(self, *args, **kwargs):
        for obs in self.observers:
            obs.update(*args, **kwargs)


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

    def publish_event(self, event_data):
        self.notify_event(event_data=event_data)
