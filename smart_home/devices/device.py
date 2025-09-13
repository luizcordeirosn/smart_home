from abc import ABC
from datetime import datetime
from enum import Enum

from transitions import Machine


class Device(ABC):
    def __init__(
        self,
        device_id,
        device_name,
        states,
        transitions,
        initial_state,
        prepare_event_method="reset_event_data",
        after_state_change_method="set_current_event",
        on_exception_method="on_enter_exception",
    ):
        self.__event_data = {}
        self.__device_id = device_id
        self.__device_name = device_name

        self.__machine = Machine(
            self,
            states=states,
            transitions=transitions,
            initial=initial_state,
            send_event=True,
            prepare_event=prepare_event_method,
            after_state_change=after_state_change_method,
            on_exception=on_exception_method,
        )

    @property
    def event_data(self):
        return self.__event_data

    @event_data.setter
    def event_data(self, value):
        self.__event_data = value

    @property
    def device_id(self):
        return self.__device_id

    @device_id.setter
    def device_id(self, value):
        self.__device_id = value

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, value):
        self.__device_name = value

    @property
    def machine(self):
        return self.__machine

    def on_enter_exception(self, event):
        self.set_current_event(event)

    def set_current_event(self, event):
        self.event_data["event"] = event
        self.event_data["device_instance"] = self.__class__.__name__
        self.event_data["device_id"] = self.device_id
        self.event_data["device_name"] = self.device_name

    def reset_event_data(self, event):
        self.event_data = {}

    def as_dict(self):
        last_index = self.__dir__().index("trigger")

        device_attributes = self.__dir__()[:last_index]

        device_dict = {"type": self.__class__.__name__.lower()}
        attributes = {}
        for device_attribute in device_attributes:
            device_attribute_splitted = list(
                filter(lambda a: a != "", device_attribute.split("__"))
            )
            device_class = device_attribute_splitted[0].replace("__", "").lower()
            attr = device_attribute_splitted[1]

            if "device" not in device_class:
                value = self.__getattribute__(attr)
                if isinstance(value, Enum):
                    attributes[attr] = value.name
                elif isinstance(value, datetime):
                    attributes[attr] = value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    attributes[attr] = value
            elif "device" in device_class and attr != "event_data":
                device_dict[attr] = self.__getattribute__(attr)

        device_dict["state"] = self.state.name
        device_dict["attributes"] = attributes

        return device_dict
