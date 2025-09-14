from datetime import datetime

from smart_home.utils.csv_manager import CsvManager
from smart_home.utils.patterns import Singleton


class Logger(Singleton):
    FILE_LOG_PATH = "smart_home/data/events_log.csv"

    def save_log_to_csv(self, **kwargs):
        timestamp = datetime.now()
        device_instance = kwargs.get("device_instance")
        device_id = kwargs.get("device_id")
        event = kwargs.get("event")
        transition = event.transition
        trigger = event.event.name
        error = event.error

        fieldnames = [
            "Time",
            "Device Instance",
            "Device ID",
            "Source",
            "Destination",
            "Error",
            "Trigger",
        ]

        data_dicts = [
            {
                "Time": timestamp,
                "Device Instance": device_instance,
                "Device ID": device_id,
                "Source": transition.source
                if transition is not None
                else event.state.name,
                "Destination": transition.dest if transition is not None else "N/A",
                "Error": error if error is not None else "N/A",
                "Trigger": trigger,
            }
        ]

        CsvManager.save_to_csv(self.FILE_LOG_PATH, fieldnames, data_dicts)

    def most_used_devices(self):
        reports = CsvManager.load_report_from_csv(self.FILE_LOG_PATH)

        devices = [row.get("Device Instance") for row in reports]

        if not devices:
            return None

        devices_set = set(devices)

        devices_usage_count = {
            device_set: devices.count(device_set) for device_set in devices_set
        }

        return list(
            sorted(
                devices_usage_count.items(), key=lambda x: (x[1], x[0]), reverse=True
            )
        )[0]
