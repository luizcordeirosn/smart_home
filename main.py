from smart_home.core.enums import ColorEnum
from smart_home.devices.bulb import Bulb
from smart_home.devices.camera import Camera
from smart_home.devices.door import Door
from smart_home.devices.outlet import Outlet
from smart_home.devices.sprinkler import Sprinkler
from smart_home.devices.thermostat import Thermostat

if __name__ == "__main__":
    print("___DOOR___")
    d = Door()

    print(d.state)
    d.lock()
    print(d.state)
    d.unlock()
    print(d.state)
    d.open()
    print(d.state)
    d.close()
    print(d.state)
    d.lock()
    print(d.state)

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

    print("___SPRINKLER___")
    sprinkler = Sprinkler()
    print(
        sprinkler.state,
        sprinkler.flow_rate,
        sprinkler.start_usage_time,
        sprinkler.usage_lh,
    )
    sprinkler.turn_on()
    print(
        sprinkler.state,
        sprinkler.flow_rate,
        sprinkler.start_usage_time,
        sprinkler.usage_lh,
    )
    sprinkler.pause_watering()
    print(
        sprinkler.state,
        sprinkler.flow_rate,
        sprinkler.start_usage_time,
        sprinkler.usage_lh,
    )
    sprinkler.resume_watering()
    print(
        sprinkler.state,
        sprinkler.flow_rate,
        sprinkler.start_usage_time,
        sprinkler.usage_lh,
    )
    sprinkler.stop_watering()
    print(
        sprinkler.state,
        sprinkler.flow_rate,
        sprinkler.start_usage_time,
        sprinkler.usage_lh,
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
