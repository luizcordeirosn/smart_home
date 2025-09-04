from devices.door import Door

if __name__ == "__main__":
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
