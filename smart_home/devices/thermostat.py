from transitions import Machine

from smart_home.core.enums import ThermostatStateEnum


class Thermostat:
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
        )

    @property
    def current_temperature(self):
        return self.__current_temperature

    @current_temperature.setter
    def current_temperature(self, value):
        self.__current_temperature = value

    def is_too_cold(self, target_temperature: float):
        return self.current_temperature < target_temperature

    def is_too_hot(self, target_temperature: float):
        return self.current_temperature > target_temperature

    def is_temperature_ok(self, target_temperature: float):
        return self.current_temperature == target_temperature

    def on_enter_IDLE(self, target_temperature: float):
        self.current_temperature = target_temperature
        print(f"INFO: Current temperature is {self.current_temperature}")

    def on_enter_COOLING(self, target_temperature: float):
        self.current_temperature = target_temperature
        print(f"INFO: Decreasing temperature to {target_temperature}")

    def on_enter_HEATING(self, target_temperature: float):
        self.current_temperature = target_temperature
        print(f"INFO: Increasing temperature to {target_temperature}")

    def on_enter_OFF(self):
        self.current_temperature = 0
        print("INFO: Thermostat turned off")
