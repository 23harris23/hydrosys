from machine import Pin, ADC
from time import sleep_ms

class pH:
    def __init__(self, sensor_pin = 36, calibration_value = {}):
        self.sensor = ADC(Pin(sensor_pin))
        self.sensor.atten(ADC.ATTN_11DB)
        self.sensor.width(ADC.WIDTH_12BIT)
        self.calibration_value = calibration_value
        self.sensor_connected = True
    def get_volts(self):
        voltage = (self.sensor.read()/4095) * 3.3
        return voltage
    def get_pH(self):
        output_pH = self.calibration_value['slope'] * self.get_volts() + self.calibration_value['zero']
        return output_pH
    def average_pH(self, sample_size):
        output_pH = 0
        for i in range(sample_size):
            output_pH = output_pH + self.get_pH()
            sleep_ms(10)
        output_pH = output_pH / sample_size
        return output_pH
    def calibrate(self, low_pH_value, low_pH_reading, high_pH_value, high_pH_reading):
        #Probe must be submerged for 30s before calibration begins
        #add temperature compensation mechanism
        m = (high_pH_value - low_pH_value) / (high_pH_reading - low_pH_reading)
        b = low_pH_value - (low_pH_reading * m)
        self.calibration_value = {'slope': m, 'zero': b}
        return self.calibration_value
    def get_config(self):
        return self.calibration_value
    def set_config(self, value):
        self.calibration_value = value
