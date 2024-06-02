from machine import Pin
from time import sleep_ms

class water_inlet_valve:
    def __init__(self, valve_pin, float_sensor_callback = None):
        if float_sensor_callback is None:
            self.float_sensor_callback = self.default_float_sensor_callback
        else:
            self.float_sensor_callback = float_sensor_callback
        self.valve = Pin(valve_pin, Pin.IN, Pin.PULL_DOWN)
        self.valve.irq(trigger = Pin.IRQ_FALLING, handler = self.float_sensor_action)
    def on(self):
        self.valve.irq(handler = None)
        self.valve.init(pull = Pin.PULL_UP)
        sleep_ms(10)
        self.valve.irq(handler = self.float_sensor_action)
    def off(self):
        self.valve.init(pull = Pin.PULL_DOWN)
    def float_sensor_action(self, irq):
        self.off()
        self.default_float_sensor_callback()
    def default_float_sensor_callback(self):
        print('Float sensor triggered')


if __name__ == '__main__':
    valve1 = water_inlet_valve(27)
    valve1.on()
    while True:
        #print(test_input.value())
        sleep_ms(10)
    