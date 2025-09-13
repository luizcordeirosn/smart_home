import sys

from smart_home.core.hub import Hub
from smart_home.core.observers import EventHandler


class Cli:
    def __init__(self):
        self.__smart_home = Hub()

        self.__smart_home.add_observer(EventHandler())

        self.__menu_options = {
            "1": self.list_device_option,
            "2": self.show_device_details_option,
            "3": self.execute_command_on_device_option,
        }

    def menu(self):
        try:
            args = sys.argv[1:]
            if len(args) == 0:
                print("""=== SMART HOME HUB ===
1. List Devices
2. Show Device Details
3. Execute Command on Device
4. Change Device Attribute
5. Run Routine
6. Generate Report
7. Save Configuration
8. Add Device
9. Remove Device
10. Exit
Choose an option:""")

                print("\nUsage: python -m smart_home.core.cli <option>")
                print("Example: python -m smart_home.core.cli 1")
            else:
                option = self.menu_options.get(args[0])

                if option is None:
                    print("Invalid option, please try again")
                else:
                    option()

        except Exception as e:
            print(e)

    def list_device_option(self):
        self.smart_home.get_devices()

    def show_device_details_option(self):
        device_type = input(
            "Device Type (door, bulb, outlet, sprinkler, thermostat and camera): "
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

        print("Name | State | Infos")
        print(f"{device}")
        print("Commands")
        print(f"{' | '.join(device_commands)}")

    def execute_command_on_device_option(self, *args):
        device_type = input(
            "Device Type (door, bulb, outlet, sprinkler, thermostat and camera): "
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

        self.smart_home.exec_device_comand(device_type, device_id, command_name)

        event = device.event_data.get("event")
        transition = event.transition
        trigger = event.event.name

        print(
            f"[EVENT] Command Executed: {{id: {device_id}, command: {trigger}, "
            f"source: {transition.source}, dest: {transition.dest}}}"
        )

    @property
    def smart_home(self):
        return self.__smart_home

    @property
    def menu_options(self):
        return self.__menu_options


if __name__ == "__main__":
    cli = Cli()

    cli.menu()
