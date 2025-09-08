from abc import ABC

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
