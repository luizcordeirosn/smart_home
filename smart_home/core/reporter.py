from datetime import datetime, timedelta

from smart_home.utils.csv_manager import CsvManager
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

        CsvManager.save_to_csv(self.FILE_REPORT_PATH, fieldnames, data_dicts)

    def outlet_power_consumption_report(self):
        reports = CsvManager.load_report_from_csv(self.FILE_REPORT_PATH)
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

    def sprinkler_water_consumption_report(self):
        reports = CsvManager.load_report_from_csv(self.FILE_REPORT_PATH)
        sprinkler_reports = list(
            filter(
                lambda row: row.get("Device Instance") == "Sprinkler",
                reports,
            )
        )

        sprinkler_messages = [
            sprinkler_report.get("Message") for sprinkler_report in sprinkler_reports
        ]

        total_consumption = 0.0
        for message in sprinkler_messages:
            session_part = message.split("Consumption: ")[1]
            value_str = session_part.split(" ")[0]

            total_consumption += float(value_str)

        return total_consumption

    def bulb_on_time_report(self):
        reports = CsvManager.load_report_from_csv(self.FILE_REPORT_PATH)
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

    def most_used_thermostat_temperature_report(self):
        reports = CsvManager.load_report_from_csv(self.FILE_REPORT_PATH)

        thermostat_reports = list(
            filter(
                lambda row: row.get("Device Instance") == "Thermostat",
                reports,
            )
        )

        if not thermostat_reports:
            return None

        thermostat_messages = [
            thermostat_report.get("Message") for thermostat_report in thermostat_reports
        ]

        thermostat_temperatures = [
            thermostat_message.split(" ")[-1]
            for thermostat_message in thermostat_messages
            if thermostat_message.split(" ")[-1] != "off"
        ]

        thermostat_temperatures_set = set(thermostat_temperatures)

        thermostat_temperatures_counts = {
            float(thermostat_temperature_set): thermostat_temperatures.count(
                thermostat_temperature_set
            )
            for thermostat_temperature_set in thermostat_temperatures_set
        }

        return list(
            sorted(
                thermostat_temperatures_counts.items(),
                key=lambda x: (x[1], x[0]),
                reverse=True,
            )
        )[0]
