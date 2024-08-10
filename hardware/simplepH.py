from machine import Pin, ADC
from time import sleep_ms
from math import log

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
    def get_avg_volts(self, sample_size):
        avg_volts = 0
        for i in range(sample_size):
            avg_volts += self.get_volts()
        avg_volts = avg_volts / sample_size
        return avg_volts
    def get_pH(self):
        average_voltage = self.get_avg_volts(100)
        output_pH = self.calibration_value['slope'] * average_voltage + self.calibration_value['zero']
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

def pH_to_H(pH): #converts pH to mol [H+] per L
    charge_per_liter: float = (10 ** (-pH))
    return charge_per_liter

def H_to_pH(H): #converts mol [H+] per L to pH
    pH: float = -log(H, 10)
    return pH

def solve_pH_addition(target_pH, additive_pH, current_pH, solution_volume):
    #Finds the amount of pH down in mL to add to reduce the nutrient solution to a given pH
    current_ion_concentration = pH_to_H(current_pH)
    target_H = pH_to_H(target_pH)
    additive_H = pH_to_H(additive_pH)
    H_ion_difference = target_H - current_ion_concentration
    additive_proportion = H_ion_difference / additive_H
    additive_quantity = (additive_proportion * solution_volume) * 1000
    return additive_quantity
