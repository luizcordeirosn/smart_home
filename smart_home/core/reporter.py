import csv
from datetime import datetime, timedelta

from smart_home.utils.csv_writer import CsvWriter
from smart_home.utils.patterns import Singleton


class Reporter(Singleton):
    FILE_REPORT_PATH = "smart_home/data/devices_report.csv"

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

        CsvWriter.save_to_csv(self.FILE_REPORT_PATH, fieldnames, data_dicts)

    def outlet_power_consumption_report(self):
        reports = self.load_report_from_csv()
        outlet_reports = list(
            filter(
                lambda row: row.get("Device Instance") == "Outlet",
                reports,
            )
        )

        outlet_messages = [
            outlet_report.get("Message") for outlet_report in outlet_reports
        ]

        total_consumption = 0.0
        for message in outlet_messages:
            session_part = message.split("Session: ")[1]
            value_str = session_part.split(" ")[0]

            total_consumption += float(value_str)

        return total_consumption

    def bulb_on_time_report(self):
        reports = self.load_report_from_csv()
        bulb_reports = list(
            filter(
                lambda row: row.get("Device Instance") == "Bulb",
                reports,
            )
        )

        bulb_messages = [bulb_report.get("Message") for bulb_report in bulb_reports]

        total_usage_time = timedelta()
        for message in bulb_messages:
            duration_part = message.split("Duration: ")[1]
            h_str, m_str, s_str = duration_part.split(":")

            session_duration = timedelta(
                hours=int(h_str), minutes=int(m_str), seconds=float(s_str)
            )

            total_usage_time += session_duration

        return total_usage_time

    def most_used_devices(self):
        reports = self.load_report_from_csv()

        devices = [row.get("Device Instance") for row in reports]

        devices_set = set(devices)

        devices_usage = {
            device_set: devices.count(device_set) for device_set in devices_set
        }

        return list(
            sorted(devices_usage.items(), key=lambda x: (x[1], x[0]), reverse=True)
        )[0]

    def load_report_from_csv(self):
        with open(self.FILE_REPORT_PATH, "r+") as file:
            return list(csv.DictReader(file))
