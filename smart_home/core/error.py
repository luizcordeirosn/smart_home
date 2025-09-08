class DeviceIndexError(Exception):
    def __init__(self, **kwargs):
        super().__init__(
            f"Device of type '{kwargs.get('device_type')}' with ID '{kwargs.get('device_id')}' already exists."
        )


class RoutineNotFoundError(Exception):
    def __init__(self, **kwargs):
        super().__init__(
            f"Routine with name '{kwargs.get('routine_name')}' doesn't exist"
        )


class DeviceMachineTriggerError(Exception):
    def __init__(self, **kwargs):
        super().__init__(f"{kwargs.get('event').error}")


class DeviceMachineAttributeError(AttributeError):
    def __init__(self, **kwargs):
        super().__init__(f"Command '{kwargs.get('command_name')}' doesn't exist")
