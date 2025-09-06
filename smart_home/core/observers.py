from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, **kwargs):
        pass


class LoggingObserver(Observer):
    def update(self, **kwargs):
        event_data = kwargs.get("event_data")

        timestamp = datetime.now()
        device_instance = event_data.get("device_instance")
        event = event_data.get("event")
        transition = event.transition
        trigger = event_data.get("event").event.name

        log_message = (
            f"LOG [{timestamp}] - Device: '{device_instance}', "
            f"{
                f'Transition: {transition.source} -> {transition.dest}, '
                if transition is not None
                else f'Error: {event.error}, '
            }"
            f"Trigger: '{trigger}'"
        )

        # TODO: Trocar essa parte para salvar em um .json em vez de ser somente um print
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

        elif event_type == "DOOR_ON_INVALID_ATTEMPT":
            invalid_attempts = event_data.get("invalid_attempts")
            machine_error = event_data.get("machine_error")
            device_class = event_data.get("device_class", "Door")

            log_message = (
                f"WARNING [{device_class}]: An invalid state transition was attempted.\n"
                f"    - Error: {machine_error}\n"
                f"    - Total Invalid Attempts: {invalid_attempts}"
            )

            print(log_message)
