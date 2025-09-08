from abc import ABC, abstractmethod

from smart_home.core.enums import EventType
from smart_home.core.logger import Logger


class Observer(ABC):
    @abstractmethod
    def update(self, **kwargs):
        pass


class EventHandler(Observer):
    def __init__(self):
        self.event_handlers = {
            EventType.DOOR_ON_INVALID_ATTEMPT: self.door_invalid_attempt,
            EventType.BULB_UPDATE_BRIGHTNESS: self.bulb_update_brightness,
            EventType.BULB_UPDATE_COLOR: self.bulb_update_color,
            EventType.OUTLET_ON_ENTER_OFF: self.outlet_on_enter_off,
            EventType.SPRINKLER_ON_EXIT_WATERING: self.sprinkler_on_exit_watering,
            EventType.THERMOSTAT_ON_ENTER_IDLE: self.thermostat_on_enter_idle,
            EventType.THERMOSTAT_ON_ENTER_COOLING: self.thermostat_on_enter_cooling_heating,
            EventType.THERMOSTAT_ON_ENTER_HEATING: self.thermostat_on_enter_cooling_heating,
            EventType.THERMOSTAT_ON_ENTER_OFF: self.thermostat_on_enter_off,
            EventType.CAMERA_HAS_ENOUGH_MEMORY: self.camera_has_enough_memory,
            EventType.CAMERA_ON_ENTER_RECORDING: self.camera_on_enter_recording,
            EventType.CAMERA_ON_EXIT_RECORDING: self.camera_on_exit_recording,
        }

    def update(self, **kwargs):
        logger = Logger()
        logger.save_log_to_csv(**kwargs)

        handler = self.event_handlers.get((kwargs.get("type")))

        if handler:
            handler_message = handler(**kwargs)
            logger.save_report_to_csv(**kwargs, handler_message=handler_message)

    def door_invalid_attempt(self, **kwargs):
        invalid_attempts = kwargs.get("invalid_attempts")
        error = kwargs.get("event").error

        return (
            f"WARNING - Invalid transition attempted. "
            f"Error: '{error}'. "
            f"Total Attempts: {invalid_attempts}"
        )

    def bulb_update_brightness(self, **kwargs):
        brightness = kwargs.get("brightness")

        return f"INFO - Brightness updated to {brightness}%."

    def bulb_update_color(self, **kwargs):
        current_color = kwargs.get("current_color")

        return f"INFO - Color changed to {current_color}"

    def outlet_on_enter_off(self, **kwargs):
        usage_time = kwargs.get("usage_time")
        session_consumption = kwargs.get("session_consumption")
        usage_wh = kwargs.get("usage_wh")

        return (
            f"INFO - Outlet turned off. "
            f"Duration: {usage_time}, "
            f"Session: {session_consumption:.4f} Wh, "
            f"Total: {usage_wh:.4f} Wh"
        )

    def sprinkler_on_exit_watering(self, **kwargs):
        usage_time = kwargs.get("usage_time")
        session_consumption = kwargs.get("session_consumption")
        usage_lh = kwargs.get("usage_lh")

        return (
            f"INFO - Sprinkler session finished. "
            f"Duration: {usage_time}, "
            f"Consumption: {session_consumption:.4f} L, "
            f"Total Usage: {usage_lh:.4f} L"
        )

    def thermostat_on_enter_idle(self, **kwargs):
        current_temperature = kwargs.get("current_temperature")

        return f"INFO - Current temperature is {current_temperature}"

    def thermostat_on_enter_cooling_heating(self, **kwargs):
        event_type = kwargs.get("type")
        target_temperature = kwargs.get("target_temperature")

        is_decreasing = (
            "Decreasing"
            if event_type == EventType.THERMOSTAT_ON_ENTER_COOLING
            else "Increasing"
        )

        return f"INFO - {is_decreasing} temperature to {target_temperature}"

    def thermostat_on_enter_off(self, **kwargs):
        return "INFO - Thermostat turned off"

    def camera_has_enough_memory(self, **kwargs):
        memory_mb = kwargs.get("memory_mb")

        return f"WARNING - Checking memory... Available: {memory_mb}MB, Required: 50MB"

    def camera_on_enter_recording(self, **kwargs):
        return "INFO - Camera is now recording"

    def camera_on_exit_recording(self, **kwargs):
        memory_mb = kwargs.get("memory_mb")

        return f"INFO - Recording stopped. Remaining space: {memory_mb} MB"
