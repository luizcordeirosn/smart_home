from transitions import Machine

from smart_home.core.enums import EventType, ThermostatStateEnum
from smart_home.devices.device import Device


class Thermostat(Device):
    def __init__(self, initial_state=ThermostatStateEnum.OFF):
        self.__current_temperature = 0.0

        transitions = [
            {
                "trigger": "turn_on",
                "source": ThermostatStateEnum.OFF,
                "dest": ThermostatStateEnum.IDLE,
            },
            {
                "trigger": "turn_off",
                "source": [
                    ThermostatStateEnum.IDLE,
                    ThermostatStateEnum.HEATING,
                    ThermostatStateEnum.COOLING,
                ],
                "dest": ThermostatStateEnum.OFF,
            },
            {
                "trigger": "check_temperature",
                "source": [ThermostatStateEnum.IDLE, ThermostatStateEnum.COOLING],
                "dest": ThermostatStateEnum.HEATING,
                "conditions": "is_too_cold",
            },
            {
                "trigger": "check_temperature",
                "source": [ThermostatStateEnum.IDLE, ThermostatStateEnum.HEATING],
                "dest": ThermostatStateEnum.COOLING,
                "conditions": "is_too_hot",
            },
            {
                "trigger": "check_temperature",
                "source": [
                    ThermostatStateEnum.HEATING,
                    ThermostatStateEnum.COOLING,
                    ThermostatStateEnum.IDLE,
                ],
                "dest": ThermostatStateEnum.IDLE,
                "conditions": "is_temperature_ok",
            },
        ]

        self.machine = Machine(
            self,
            states=ThermostatStateEnum,
            transitions=transitions,
            initial=initial_state,
            send_event=True,
            after_state_change="set_current_event",
        )

        super().__init__()

    @property
    def current_temperature(self):
        return self.__current_temperature

    @current_temperature.setter
    def current_temperature(self, value):
        self.__current_temperature = value

    def is_too_cold(self, event):
        return self.current_temperature < event.kwargs.get("target_temperature")

    def is_too_hot(self, event):
        return self.current_temperature > event.kwargs.get("target_temperature")

    def is_temperature_ok(self, event):
        return self.current_temperature == event.kwargs.get("target_temperature")

    def on_enter_IDLE(self, event):
        self.current_temperature = event.kwargs.get("target_temperature")

        self.event_data["type"] = EventType.THERMOSTAT_ON_ENTER_IDLE
        self.event_data["current_temperature"] = self.current_temperature

    def on_enter_COOLING(self, event):
        target_temperature = event.kwargs.get("target_temperature")

        self.current_temperature = target_temperature

        self.event_data["type"] = EventType.THERMOSTAT_ON_ENTER_COOLING
        self.event_data["target_temperature"] = target_temperature

    def on_enter_HEATING(self, event):
        target_temperature = event.kwargs.get("target_temperature")

        self.current_temperature = target_temperature

        self.event_data["type"] = EventType.THERMOSTAT_ON_ENTER_HEATING
        self.event_data["target_temperature"] = target_temperature

    def on_enter_OFF(self, event):
        self.current_temperature = 0.0

        self.event_data["type"] = EventType.THERMOSTAT_ON_ENTER_OFF
