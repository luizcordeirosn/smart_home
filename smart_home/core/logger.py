import csv
import os
from datetime import datetime


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Logger(Singleton):
    FILE_LOG_PATH = "smart_home/data/events_log.csv"
    FILE_REPORT_PATH = "smart_home/data/devices_report.csv"

    def save_log_to_csv(self, **kwargs):
        timestamp = datetime.now()
        device_instance = kwargs.get("device_instance")
        event = kwargs.get("event")
        transition = event.transition
        trigger = kwargs.get("event").event.name

        fieldnames = [
            "Time",
            "Device Instance",
            "Source",
            "Destination",
            "Error",
            "Trigger",
        ]

        data_dicts = [
            {
                "Time": timestamp,
                "Device Instance": device_instance,
                "Source": transition.source if transition is not None else "N/A",
                "Destination": transition.dest if transition is not None else "N/A",
                "Error": event.error if transition is None else "N/A",
                "Trigger": trigger,
            }
        ]

        self.save_to_csv(self.FILE_LOG_PATH, fieldnames, data_dicts)

    def save_report_to_csv(self, **kwargs):
        timestamp = datetime.now()
        message = kwargs.get("handler_message").split(" - ")
        level = message[0]
        device_instance = kwargs.get("device_instance")
        device_name = kwargs.get("device_name")
        message = message[1]

        fieldnames = [
            "Time",
            "Level",
            "Device Instance",
            "Device Name",
            "Message",
        ]

        data_dicts = [
            {
                "Time": timestamp,
                "Level": level,
                "Device Instance": device_instance,
                "Device Name": device_name,
                "Message": message,
            }
        ]

        self.save_to_csv(self.FILE_REPORT_PATH, fieldnames, data_dicts)

    def save_to_csv(self, file_path, fieldnames, data_dicts):
        file_exists = os.path.exists(file_path)

        with open(file_path, "a+", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerows(data_dicts)
