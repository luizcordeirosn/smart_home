import json

from smart_home.utils.patterns import Singleton


class Persistence(Singleton):
    FILE_SMART_HOME_CONFIG = "smart_home/data/smart_house_config.json"

    def save_devices_to_json(self, devices):
        configs = self.load_config_from_json()

        with open(self.FILE_SMART_HOME_CONFIG, "w+") as file:
            configs["devices"] = devices

            json.dump(configs, file, indent=4)

    def load_config_from_json(self):
        with open(self.FILE_SMART_HOME_CONFIG, "r+") as file:
            return json.load(file)
