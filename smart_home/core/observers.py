from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, **kwargs):
        pass


class LoggingObserver(Observer):
    def update(self, **kwargs):
        timestamp = datetime.now()
        device_instance = kwargs.get("device_instance")
        event = kwargs.get("event")
        transition = event.transition
        trigger = kwargs.get("event").event.name

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

        event_type = kwargs.get("type")
        if event_type == "DOOR_ON_INVALID_ATTEMPT":
            invalid_attempts = kwargs.get("invalid_attempts")
            machine_error = kwargs.get("machine_error")

            log_message = (
                f"WARNING [{device_instance}]: An invalid state transition was attempted.\n"
                f"    - Error: {machine_error}\n"
                f"    - Total Invalid Attempts: {invalid_attempts}"
            )

            print(log_message)

        elif event_type == "BULB_UPDATE_BRIGHTNESS":
            brightness = kwargs.get("brightness")

            log_message = (
                f"INFO [{device_instance}]: Brightness updated to {brightness}%."
            )

            print(log_message)

        elif event_type == "BULB_UPDATE_COLOR":
            current_color = kwargs.get("current_color")

            log_message = f"INFO [{device_instance}]: Color changed to {current_color}"

            print(log_message)

        elif event_type == "OUTLET_ON_ENTER_OFF":
            usage_time = kwargs.get("usage_time")
            session_consumption = kwargs.get("session_consumption")
            usage_wh = kwargs.get("usage_wh")

            log_message = (
                f"INFO [{device_instance}]: Outlet turned off. Usage session logged.\n"
                f"    - Session duration: {usage_time}\n"
                f"    - Session consumption: {session_consumption:.4f} Wh\n"
                f"    - Total accumulated consumption: {usage_wh:.4f} Wh"
            )

            print(log_message)

        elif event_type == "SPRINKLER_ON_EXIT_WATERING":
            usage_time = kwargs.get("usage_time")
            session_consumption = kwargs.get("session_consumption")
            usage_lh = kwargs.get("usage_lh")

            log_message = (
                f"INFO [{device_instance}]: Sprinkler watering session finished.\n"
                f"    - Session Duration: {usage_time}\n"
                f"    - Session Consumption: {session_consumption:.4f} Liters\n"
                f"    - Total Accumulated Usage: {usage_lh:.4f} Liters"
            )

            print(log_message)
