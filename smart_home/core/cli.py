import inspect

from smart_home.core.hub import Hub
from smart_home.core.logger import Logger
from smart_home.core.observers import EventHandler
from smart_home.core.reporter import Reporter


class Cli:
    def __init__(self):
        self.__smart_home = Hub()

        self.__smart_home.add_observer(EventHandler())

        self.__menu_options = {
            "1": self.list_device_option,
            "2": self.show_device_details_option,
            "3": self.execute_command_on_device_option,
            "4": self.change_device_attribute_option,
            "5": self.run_routine_option,
            "6": self.report_menu_option,
            "7": self.save_configuration_option,
            "8": self.add_device_option,
            "9": self.remove_device_option,
            "10": self.exit_option,
        }

        self.__report_menu_options = {
            "1": self.outlet_power_consumption_option,
            "2": self.sprinkler_water_consumption_option,
            "3": self.bulb_on_time_report,
            "4": self.most_used_thermostat_temperature_report,
            "5": self.most_used_devices_report,
        }

        self.__type_map = {
            "str": str,
            "int": int,
        }

        self.__logger = Logger()
        self.__reporter = Reporter()

    @property
    def logger(self):
        return self.__logger

    @property
    def reporter(self):
        return self.__reporter

    @property
    def smart_home(self):
        return self.__smart_home

    @property
    def menu_options(self):
        return self.__menu_options

    @property
    def report_menu_options(self):
        return self.__report_menu_options

    @property
    def type_map(self):
        return self.__type_map

    def menu(self):
        is_running = True
        while is_running:
            try:
                print(
                    f"=== {self.smart_home.program_name.upper()}",
                    f"{self.smart_home.program_version} ===",
                )
                print("""1. List Devices
2. Show Device Details
3. Execute Command on Device
4. Change Device Attribute
5. Run Routine
6. Generate Report
7. Save Configuration
8. Add Device
9. Remove Device
10. Exit""")

                option_input = input("\nChoose an option: ")
                option = self.menu_options.get(option_input)

                if option is None:
                    print("\nInvalid option, please try again\n")
                else:
                    option()
                    if option_input == "10":
                        is_running = False

            except Exception as e:
                print(f"\n{e.__class__.__name__} - {e}\n")

    def list_device_option(self):
        self.smart_home.get_devices()

    def show_device_details_option(self):
        device_type = input(
            f"\nDevice Type ({', '.join(self.smart_home.devices.keys())}): "
        )
        device_id = input("Device ID: ")

        device = self.smart_home.get_device_by_device_type_and_device_id(
            device_type, device_id
        )

        print("\nName | State | Infos")
        print(f"{device}\n")

    def execute_command_on_device_option(self):
        device_type = input(
            f"\nDevice Type ({', '.join(self.smart_home.devices.keys())}): "
        )
        device_id = input("Device ID: ")

        device = self.smart_home.get_device_by_device_type_and_device_id(
            device_type, device_id
        )

        device_commands = (
            self.smart_home.get_device_commands_by_device_type_and_device_id(
                device_type, device_id
            )
        )

        command_name = input(f"Command ({' | '.join(device_commands)}): ")

        arguments = input(
            "Arguments (key=value separated by space) or ENTER for finish: "
        )

        kwargs = {}
        if arguments != "":
            arguments_list = arguments.split(" ")

            for arg in arguments_list:
                arg_items = arg.split("=")
                key, value = arg_items

                if value.isnumeric():
                    value = int(value)
                elif "." in value:
                    value = float(value)

                kwargs[key] = value

        self.smart_home.exec_device_comand(
            device_type, device_id, command_name, **kwargs
        )

        event = device.event_data.get("event")

        if event is not None:
            transition = event.transition
            trigger = event.event.name

            print(
                f"\n[EVENT] Command Executed: {{id: {device_id}, command: {trigger}, "
                f"source: {transition.source}, dest: {transition.dest}}}\n"
            )
        else:
            print("\nCommand not executed\n")

    def change_device_attribute_option(self):
        device_type = input(
            f"\nDevice Type ({', '.join(self.smart_home.devices.keys())}): "
        )
        device_id = input("Device ID: ")

        device = self.smart_home.get_device_by_device_type_and_device_id(
            device_type, device_id
        )

        new_device_name = input(
            f"Enter new name for '{device.device_name}' (or press ENTER to keep current): "
        )

        if new_device_name.strip():
            device.device_name = new_device_name
            print(
                f"\n[Device '{device_id}' name has been updated to '{new_device_name}'\n",
            )
        else:
            print("\nDevice name was not changed\n")

    def run_routine_option(self):
        print("\nAvailable routines: ")
        print(list(self.smart_home.routines.keys()))
        routine_name = input("Routine Name: ")

        self.smart_home.get_routine_by_routine_name(routine_name)

        self.smart_home.exec_routine(routine_name)

        print(f"\nRoutine '{routine_name}' executed successfully\n")

    def report_menu_option(self):
        print("""\n=== Report Menu ===
1. Outlet Power Consumption
2. Sprinkler Water Consumption
3. Bulb On-Time Report
4. Most Used Thermostat Temperature
5. Most Used Devices""")

        option_input = input("\nChoose an option: ")
        option = self.report_menu_options.get(option_input)

        if option is None:
            print("\nInvalid option\n")
        else:
            option()

    def save_configuration_option(self):
        self.smart_home.parse_from_devices_to_dict_list()
        print("\nConfiguration has been saved successfully\n")

    def add_device_option(self):
        print(f"\nDevices Type Supported ({', '.join(self.smart_home.devices.keys())})")
        device_type = input("Device Type: ")
        device_class = self.smart_home.class_map.get(device_type)

        if device_class is not None:
            init_attributes = (
                str(inspect.signature(device_class.__init__))
                .replace(" ", "")
                .split(",")
            )

            class_attributes = []
            for element in init_attributes[1:]:
                equals_index = element.find("=")
                if equals_index != -1:
                    class_attributes.append(element[:equals_index].split(":"))
                else:
                    class_attributes.append(element.split(":"))

            args = [device_type]
            kwargs = {}
            for attr in class_attributes:
                param_key = attr[0]
                param_type = attr[1]
                str_attribute_to_print = param_key.replace("_", " ").title()

                if param_key == "initial_state":
                    device_enum_values = list(
                        self.smart_home.enum_map.get(device_type).__members__.keys()
                    )

                    input_attr = input(
                        f"{str_attribute_to_print} ({', '.join(device_enum_values)}): "
                    )
                    input_attr = input_attr.upper()
                else:
                    input_attr = input(f"{str_attribute_to_print}: ")

                if not isinstance(input_attr, self.type_map.get(param_type)):
                    raise ValueError("Invalid input. Couldn't create the device")

                if param_key == "device_id":
                    args.append(input_attr)
                else:
                    kwargs[attr[0]] = input_attr

            device = self.smart_home.add_device(*args, **kwargs)

            print(
                "\n[EVENT] Device Added: ",
                f"{{id: {device.device_id}, type: {device_type}}}",
            )

            print("New device created successfully\n")

    def remove_device_option(self):
        print(f"\nDevices Type Supported ({', '.join(self.smart_home.devices.keys())})")
        device_type = input("Device Type: ")
        device_id = input("Device ID: ")

        deleted_device = self.smart_home.delete_device_by_device_type_and_device_id(
            device_type, device_id
        )

        print(
            "\n[EVENT] Device Removed: ",
            f"{{id: {deleted_device.device_id}, type: {device_type}}}",
        )

        print("New device deleted successfully\n")

    def outlet_power_consumption_option(self):
        total_consumption_wh = self.reporter.outlet_power_consumption_report()

        print(
            f"\nTotal energy consumed by all outlets: {total_consumption_wh:.4f} Wh\n"
        )

    def sprinkler_water_consumption_option(self):
        total_consumption_lh = self.reporter.sprinkler_water_consumption_report()

        print(
            f"\nTotal water consumed by all sprinklers: {total_consumption_lh:.4f} Lh\n"
        )

    def bulb_on_time_report(self):
        time_usage = self.reporter.bulb_on_time_report()

        print(f"\nTime usage by all bulbs: {time_usage}\n")

    def most_used_thermostat_temperature_report(self):
        report_data = self.reporter.most_used_thermostat_temperature_report()

        if report_data:
            thermostat_temperature, temperature_count = report_data

            print(
                f"\nThe most frequently used temperature is {thermostat_temperature}",
                f"and it was used {temperature_count} times\n",
            )
        else:
            print("\nNo device usage data available to generate a report\n")

    def most_used_devices_report(self):
        report_data = self.logger.most_used_devices()

        if report_data:
            device_name, usage_count = report_data

            print(
                f"\nThe most frequently used device is {device_name}",
                f"and it was used {usage_count} times\n",
            )
        else:
            print("\nNo Thermostat usage data available to generate a report\n")

    def exit_option(self):
        self.save_configuration_option()
        print("Exiting Smart Home Hub. Goodbye!")


if __name__ == "__main__":
    cli = Cli()

    cli.menu()
