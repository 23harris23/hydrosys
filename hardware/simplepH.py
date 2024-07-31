from machine import Pin, ADC
from time import sleep_ms

class pH:
    def __init__(self, sensor_pin = 36, calibration_value = 1):
        self.sensor = ADC(Pin(sensor_pin))
        self.sensor.atten(ADC.ATTN_11DB)
        self.sensor.width(ADC.WIDTH_12BIT)
        self.calibration_value = calibration_value
        self.sensor_connected = True
    def get_volts(self):
        voltage = (self.sensor.read()/4095) * 3.3
        return voltage
    def get_pH(self):
        output_pH = self.calibration_value * self.get_volts()
        return output_pH
    def average_pH(self, sample_size):
        output_pH = 0
        for i in range(sample_size):
            output_pH = output_pH + self.get_pH()
            sleep_ms(10)
        output_pH = output_pH / sample_size
        return output_pH
    def calibrate(self): #Probe must be submerged for 30s before calibration begins
        #Need to add 2 point calibration 1 point calibration is inadaquite
        #add temperature compensation mechanism
        avg_voltage = 0
        for i in range(100):
            avg_voltage = avg_voltage + self.get_volts()
        avg_voltage = avg_voltage / 100
        self.calibration_value = 7 / avg_voltage
        return self.calibration_value
    def get_config(self):
        return self.calibration_value
    def set_config(self, value):
        self.calibration_value = value
        

