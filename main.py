from smart_home.devices.bulb import Bulb
from smart_home.devices.door import Door
from smart_home.utils.enums import ColorEnum

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

    print("___BULB___")
    b = Bulb()

    print(b.state)
    b.turn_on()
    print(b.state, b.brightness, b.current_color)
    b.set_brightness(brightness_value=100)
    print(b.state, b.brightness, b.current_color)
    print(b.state, b.brightness, b.current_color)
    b.set_color(ColorEnum.WARM)
    print(b.state, b.brightness, b.current_color)
