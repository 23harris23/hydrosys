from machine import Pin
from time import sleep_ms


class sr_595:
    def __init__(self, ser, srclk, rclk, bit_rng = 8):
        self.ser = Pin(ser, Pin.OUT)
        self.srclk = Pin(srclk, Pin.OUT)
        self.rclk = Pin(rclk, Pin.OUT)
        self.bit_rng = bit_rng
        #possibly add clear_all function to init
    def add_0(self):
        self.ser.value(0)
        self.srclk.value(1)
        self.srclk.value(0)
    def add_1(self):
        self.ser.value(1)
        self.srclk.value(1)
        self.srclk.value(0)
    def pass_val(self):
        self.rclk.value(1)
        self.rclk.value(0)
    def clear_all(self):
        for i in range(self.bit_rng):
            self.add_0()
        self.pass_val()
    def activate_pin(self, number):
        self.clear_all()
        self.add_1()
        for i in range(number - 1):
            self.add_0()
        self.pass_val()


if __name__ == '__main__':
    sr_1 = sr_595(27, 12, 14, bit_rng = 8)
    print('Null Output, will change in 3s')
    sleep_ms(3000)
    sr_1.add_1()
    sr_1.pass_val()
    #sr_1.activate_pin(15)
    #sleep_ms(500)
    sr_1.activate_pin(11)
    sleep_ms(500)
    sr_1.clear_all()
    for i in range(8):
        sr_1.add_1()
        sleep_ms(500)
        sr_1.pass_val()
    while True:
        for i in range(8):
            sr_1.activate_pin(i + 1)
            sleep_ms(50)

