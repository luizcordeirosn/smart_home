from abc import ABC


class Device(ABC):
    def __init__(self):
        self.__event_data = {}

    @property
    def event_data(self):
        return self.__event_data

    @event_data.setter
    def event_data(self, value):
        self.__event_data = value

    def set_current_event(self, event):
        self.event_data["event"] = event
        self.event_data["device_instance"] = self.__class__.__name__
