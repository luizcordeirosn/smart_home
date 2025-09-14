from datetime import datetime

from smart_home.utils.csv_writer import CsvWriter
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

        CsvWriter.save_to_csv(self.FILE_LOG_PATH, fieldnames, data_dicts)
