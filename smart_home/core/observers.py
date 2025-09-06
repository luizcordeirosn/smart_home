from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, *args, **kwargs):
        pass


class LoggingObserver(Observer):
    def update(self, *args, **kwargs):
        event_data = kwargs.get("event_data")

        timestamp = datetime.now()
        device_instance = event_data.get("device_instance")
        transition = event_data.get("event").transition
        trigger = event_data.get("event").event.name

        log_message = (
            f"LOG [{timestamp}] - Device: '{device_instance}', "
            f"Transition: {transition.source} -> {transition.dest}, "
            f"Trigger: '{trigger}'"
        )

        print(log_message)

        event_type = event_data.get("type")
        if event_type == "SPRINKLER_ON_EXIT_WATERING":
            device_class = event_data.get("device_class")
            usage_time = event_data.get("usage_time")
            session_consumption = event_data.get("session_consumption")
            usage_lh = event_data.get("usage_lh")

            log_message = (
                f"INFO [{device_class}]: Sprinkler watering session finished.\n"
                f"    - Session Duration: {usage_time}\n"
                f"    - Session Consumption: {session_consumption:.4f} Liters\n"
                f"    - Total Accumulated Usage: {usage_lh:.4f} Liters"
            )

            print(log_message)
