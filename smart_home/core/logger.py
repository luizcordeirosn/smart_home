import csv
import json
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
        device_id = kwargs.get("device_id")
        event = kwargs.get("event")
        transition = [value for value in event.event.transitions.values()][0][0]
        source = transition.source
        dest = transition.dest
        trigger = kwargs.get("event").event.name
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
                "Source": source.lower(),
                "Destination": dest.lower(),
                "Error": error if error is not None else "N/A",
                "Trigger": trigger,
            }
        ]

        self.save_to_csv(self.FILE_LOG_PATH, fieldnames, data_dicts)

    def save_report_to_csv(self, **kwargs):
        timestamp = datetime.now()
        message = kwargs.get("handler_message").split(" - ")
        level = message[0]
        device_instance = kwargs.get("device_instance")
        device_id = kwargs.get("device_id")
        device_name = kwargs.get("device_name")
        message = message[1]

        fieldnames = [
            "Time",
            "Level",
            "Device Instance",
            "Device ID",
            "Device Name",
            "Message",
        ]

        data_dicts = [
            {
                "Time": timestamp,
                "Level": level,
                "Device Instance": device_instance,
                "Device ID": device_id,
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

    def load_config_from_json(self):
        with open("smart_home/data/smart_house_config.json", "r+") as file:
            return json.load(file)
