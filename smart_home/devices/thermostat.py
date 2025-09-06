from transitions import Machine

from smart_home.core.enums import ThermostatEnum


class Thermostat:
    def __init__(self, initial_state=ThermostatEnum.OFF):
        self.__current_temperature = 0.0

        transitions = [
            {
                "trigger": "turn_on",
                "source": ThermostatEnum.OFF,
                "dest": ThermostatEnum.IDLE,
            },
            {
                "trigger": "turn_off",
                "source": [
                    ThermostatEnum.IDLE,
                    ThermostatEnum.HEATING,
                    ThermostatEnum.COOLING,
                ],
                "dest": ThermostatEnum.OFF,
            },
            {
                "trigger": "check_temperature",
                "source": [ThermostatEnum.IDLE, ThermostatEnum.COOLING],
                "dest": ThermostatEnum.HEATING,
                "conditions": "is_too_cold",
            },
            {
                "trigger": "check_temperature",
                "source": [ThermostatEnum.IDLE, ThermostatEnum.HEATING],
                "dest": ThermostatEnum.COOLING,
                "conditions": "is_too_hot",
            },
            {
                "trigger": "check_temperature",
                "source": [
                    ThermostatEnum.HEATING,
                    ThermostatEnum.COOLING,
                    ThermostatEnum.IDLE,
                ],
                "dest": ThermostatEnum.IDLE,
                "conditions": "is_temperature_ok",
            },
        ]

        self.machine = Machine(
            self,
            states=ThermostatEnum,
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
