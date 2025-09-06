from abc import ABC, abstractmethod
from datetime import datetime

from smart_home.core.enums import EventType


class Observer(ABC):
    @abstractmethod
    def update(self, **kwargs):
        pass


class LoggingObserver(Observer):
    def __init__(self):
        self.event_handlers = {
            EventType.DOOR_ON_INVALID_ATTEMPT: self.log_door_invalid_attempt,
            EventType.BULB_UPDATE_BRIGHTNESS: self.log_bulb_update_brightness,
            EventType.BULB_UPDATE_COLOR: self.log_bulb_update_color,
            EventType.OUTLET_ON_ENTER_OFF: self.log_outlet_on_enter_off,
            EventType.SPRINKLER_ON_EXIT_WATERING: self.log_sprinkler_on_exit_watering,
            EventType.THERMOSTAT_ON_ENTER_IDLE: self.log_thermostat_on_enter_idle,
            EventType.THERMOSTAT_ON_ENTER_COOLING: self.log_thermostat_on_enter_cooling_heating,
            EventType.THERMOSTAT_ON_ENTER_HEATING: self.log_thermostat_on_enter_cooling_heating,
            EventType.THERMOSTAT_ON_ENTER_OFF: self.log_thermostat_on_enter_off,
            EventType.CAMERA_HAS_ENOUGH_MEMORY: self.log_camera_has_enough_memory,
            EventType.CAMERA_ON_ENTER_RECORDING: self.log_camera_on_enter_recording,
            EventType.CAMERA_ON_EXIT_RECORDING: self.log_camera_on_exit_recording,
        }

    def update(self, **kwargs):
        # TODO: Trocar essa parte para salvar em um .json em vez de ser somente um print
        print(self.log_state_change(**kwargs))

        handler = self.event_handlers.get((kwargs.get("type")))

        if handler:
            print(handler(**kwargs))

    def log_state_change(self, **kwargs):
        timestamp = datetime.now()
        device_instance = kwargs.get("device_instance")
        event = kwargs.get("event")
        transition = event.transition
        trigger = kwargs.get("event").event.name

        return (
            f"LOG [{timestamp}] - Device: '{device_instance}', "
            f"{
                f'Transition: {transition.source} -> {transition.dest}, '
                if transition is not None
                else f'Error: {event.error}, '
            }"
            f"Trigger: '{trigger}'"
        )

    def log_door_invalid_attempt(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        invalid_attempts = kwargs.get("invalid_attempts")
        machine_error = kwargs.get("machine_error")

        return (
            f"WARNING [{device_instance}]: An invalid state transition was attempted.\n"
            f"    - Error: {machine_error}\n"
            f"    - Total Invalid Attempts: {invalid_attempts}"
        )

    def log_bulb_update_brightness(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        brightness = kwargs.get("brightness")

        return f"INFO [{device_instance}]: Brightness updated to {brightness}%."

    def log_bulb_update_color(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        current_color = kwargs.get("current_color")

        return f"INFO [{device_instance}]: Color changed to {current_color}"

    def log_outlet_on_enter_off(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        usage_time = kwargs.get("usage_time")
        session_consumption = kwargs.get("session_consumption")
        usage_wh = kwargs.get("usage_wh")

        return (
            f"INFO [{device_instance}]: Outlet turned off. Usage session logged.\n"
            f"    - Session duration: {usage_time}\n"
            f"    - Session consumption: {session_consumption:.4f} Wh\n"
            f"    - Total accumulated consumption: {usage_wh:.4f} Wh"
        )

    def log_sprinkler_on_exit_watering(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        usage_time = kwargs.get("usage_time")
        session_consumption = kwargs.get("session_consumption")
        usage_lh = kwargs.get("usage_lh")

        return (
            f"INFO [{device_instance}]: Sprinkler watering session finished.\n"
            f"    - Session Duration: {usage_time}\n"
            f"    - Session Consumption: {session_consumption:.4f} Liters\n"
            f"    - Total Accumulated Usage: {usage_lh:.4f} Liters"
        )

    def log_thermostat_on_enter_idle(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        current_temperature = kwargs.get("current_temperature")

        return f"INFO [{device_instance}]: Current temperature is {current_temperature}"

    def log_thermostat_on_enter_cooling_heating(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        event_type = kwargs.get("type")
        target_temperature = kwargs.get("target_temperature")

        is_decreasing = (
            "Decreasing"
            if event_type == EventType.THERMOSTAT_ON_ENTER_COOLING
            else "Increasing"
        )

        return f"INFO [{device_instance}]: {is_decreasing} temperature to {target_temperature}"

    def log_thermostat_on_enter_off(self, **kwargs):
        device_instance = kwargs.get("device_instance")

        return f"INFO [{device_instance}]: Thermostat turned off"

    def log_camera_has_enough_memory(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        memory_mb = kwargs.get("memory_mb")

        return f"WARNING [{device_instance}]: Checking memory... Available: {memory_mb}MB, Required: 50MB"

    def log_camera_on_enter_recording(self, **kwargs):
        device_instance = kwargs.get("device_instance")

        return f"INFO [{device_instance}]: Camera is now recording"

    def log_camera_on_exit_recording(self, **kwargs):
        device_instance = kwargs.get("device_instance")
        memory_mb = kwargs.get("memory_mb")

        return (
            f"INFO [{device_instance}]: Recording stopped successfully.\n"
            f"    - Remaining space: {memory_mb} MB"
        )
