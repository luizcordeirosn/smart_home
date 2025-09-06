from smart_home.core.enums import ColorEnum
from smart_home.core.hub import Hub
from smart_home.core.observers import LoggingObserver
from smart_home.devices.bulb import Bulb
from smart_home.devices.camera import Camera
from smart_home.devices.door import Door
from smart_home.devices.outlet import Outlet
from smart_home.devices.sprinkler import Sprinkler
from smart_home.devices.thermostat import Thermostat

if __name__ == "__main__":
    print("__HUB__")

    smart_home = Hub()
    logging = LoggingObserver()

    sprinkler = Sprinkler()
    door = Door()

    smart_home.add_observer(logging)
    smart_home.add_devices("sprinkler", sprinkler)
    smart_home.add_devices("door", door)

    print("___DOOR___")
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )
    smart_home.devices["door"][0].lock()
    smart_home.publish_event(smart_home.devices["door"][0].event_data)
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )
    smart_home.devices["door"][0].unlock()
    smart_home.publish_event(smart_home.devices["door"][0].event_data)
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )
    smart_home.devices["door"][0].open()
    smart_home.publish_event(smart_home.devices["door"][0].event_data)
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )
    smart_home.devices["door"][0].close()
    smart_home.publish_event(smart_home.devices["door"][0].event_data)
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )
    smart_home.devices["door"][0].lock()
    smart_home.publish_event(smart_home.devices["door"][0].event_data)
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )
    try:
        smart_home.devices["door"][0].open()
    except Exception:
        pass
    smart_home.publish_event(smart_home.devices["door"][0].event_data)
    print(
        smart_home.devices["door"][0].state,
        smart_home.devices["door"][0].invalid_attempts,
    )

    print("___BULB___")
    b = Bulb()

    print(b.state)
    b.turn_on()
    print(b.state, b.brightness, b.current_color)
    b.set_brightness(brightness_value=100)
    print(b.state, b.brightness, b.current_color)
    print(b.state, b.brightness, b.current_color)
    b.set_color(color=ColorEnum.WARM)
    print(b.state, b.brightness, b.current_color)

    print("___OUTLET___")
    outlet = Outlet()
    print(outlet.state, outlet.power_w, outlet.start_usage_time, outlet.usage_wh)
    outlet.turn_on()
    print(outlet.state, outlet.power_w, outlet.start_usage_time, outlet.usage_wh)
    outlet.turn_off()
    print(outlet.state, outlet.power_w, outlet.start_usage_time, outlet.usage_wh)
    outlet.turn_on()
    print(outlet.state, outlet.power_w, outlet.start_usage_time, outlet.usage_wh)
    outlet.turn_off()
    print(outlet.state, outlet.power_w, outlet.start_usage_time, outlet.usage_wh)

    print("__SPRINKLER__")
    print(
        smart_home.devices["sprinkler"][0].state,
        smart_home.devices["sprinkler"][0].flow_rate,
        smart_home.devices["sprinkler"][0].start_usage_time,
        smart_home.devices["sprinkler"][0].usage_lh,
    )
    smart_home.devices["sprinkler"][0].turn_on()
    smart_home.publish_event(smart_home.devices["sprinkler"][0].event_data)
    print(
        smart_home.devices["sprinkler"][0].state,
        smart_home.devices["sprinkler"][0].flow_rate,
        smart_home.devices["sprinkler"][0].start_usage_time,
        smart_home.devices["sprinkler"][0].usage_lh,
    )
    smart_home.devices["sprinkler"][0].pause_watering()
    smart_home.publish_event(smart_home.devices["sprinkler"][0].event_data)
    print(
        smart_home.devices["sprinkler"][0].state,
        smart_home.devices["sprinkler"][0].flow_rate,
        smart_home.devices["sprinkler"][0].start_usage_time,
        smart_home.devices["sprinkler"][0].usage_lh,
    )
    smart_home.devices["sprinkler"][0].resume_watering()
    smart_home.publish_event(smart_home.devices["sprinkler"][0].event_data)
    print(
        smart_home.devices["sprinkler"][0].state,
        smart_home.devices["sprinkler"][0].flow_rate,
        smart_home.devices["sprinkler"][0].start_usage_time,
        smart_home.devices["sprinkler"][0].usage_lh,
    )
    smart_home.devices["sprinkler"][0].stop_watering()
    smart_home.publish_event(smart_home.devices["sprinkler"][0].event_data)
    print(
        smart_home.devices["sprinkler"][0].state,
        smart_home.devices["sprinkler"][0].flow_rate,
        smart_home.devices["sprinkler"][0].start_usage_time,
        smart_home.devices["sprinkler"][0].usage_lh,
    )

    print("___THERMOSTAT___")
    thermostat = Thermostat()

    print(thermostat.state, thermostat.current_temperature)
    thermostat.turn_on(target_temperature=25)
    print(thermostat.state, thermostat.current_temperature)
    thermostat.check_temperature(target_temperature=25.5)
    print(thermostat.state, thermostat.current_temperature)
    thermostat.check_temperature(target_temperature=20.5)
    print(thermostat.state, thermostat.current_temperature)
    thermostat.check_temperature(target_temperature=21.5)
    print(thermostat.state, thermostat.current_temperature)

    print("__CAMERA__")
    camera = Camera(memory_mb=2000)
    print(camera.state, camera.memory_mb)
    camera.turn_on()
    print(camera.state, camera.memory_mb)
    camera.record()
    print(camera.state, camera.memory_mb)
    camera.stop_recording()
    print(camera.state, camera.memory_mb)
