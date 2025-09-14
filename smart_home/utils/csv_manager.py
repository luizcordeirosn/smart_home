import csv
import os


class CsvManager:
    @staticmethod
    def save_to_csv(file_path, fieldnames, data_dicts):
        file_exists = os.path.exists(file_path)

        with open(file_path, "a+", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerows(data_dicts)

    @staticmethod
    def load_report_from_csv(file_path):
        with open(file_path, "r+") as file:
            return list(csv.DictReader(file))
