from machine import Pin, Timer
from time import sleep_ms, ticks_ms, ticks_diff

class water_inlet_valve:
    def __init__(self,
                 valve_pin,
                 float_sensor_callback = None,
                 tank_capacity = 30,
                 ms_per_unit = 300):
        if float_sensor_callback is None:
            self.float_sensor_callback = self.default_float_sensor_callback
        else:
            self.float_sensor_callback = float_sensor_callback
        self.tank_capacity = tank_capacity
        self.ms_per_unit = ms_per_unit
        self.valve = Pin(valve_pin, Pin.IN, Pin.PULL_DOWN)
        self.float_sensor_state = False
        self.valve.irq(trigger = Pin.IRQ_FALLING, handler = self.float_sensor_action)
    def on(self):
        self.float_sensor_state = True
        self.valve.irq(handler = None)
        self.valve.init(pull = Pin.PULL_UP)
        sleep_ms(10)
        self.valve.irq(handler = self.float_sensor_action)
    def off(self):
        self.float_sensor_state = False
        self.valve.init(pull = Pin.PULL_DOWN)
    def float_sensor_action(self, irq):
        self.off()
        self.default_float_sensor_callback()
    def timer_wrapper(self, timer):
        self.off()
    def default_float_sensor_callback(self):
        #float sensor gets false positives from software shutoffs find method to correct error
        print('Float sensor triggered')
    def get_fill_time(self):
        start_time = ticks_ms()
        self.on()
        while self.float_sensor_state == True:
            pass
        total_time = ticks_diff(ticks_ms(), start_time)
        return total_time
    def get_fill_rate(self):
        fill_time = self.get_fill_time()
        self.ms_per_unit = round(fill_time / self.tank_capacity)
        return self.ms_per_unit
    def fill_quantity(self, ammount):
        if ammount < self.tank_capacity:
            ammount = self.tank_capacity
            #Add error functionality
        fill_time = round(ammount * self.ms_per_unit)
        fill_timer = Timer(0)
        self.on()
        fill_timer.init(period = fill_time, mode = Timer.ONE_SHOT, callback = self.timer_wrapper)
        print('done')

if __name__ == '__main__':
    valve1 = water_inlet_valve(23)
    #valve1.on()
    #fill_time = valve1.get_fill_time()
    #print(fill_time)
    fill_rate = valve1.get_fill_rate()
    print(fill_rate)
    sleep_ms(1000)
    valve1.fill_quantity(10)

