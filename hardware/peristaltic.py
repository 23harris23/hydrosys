from machine import Pin
from time import sleep_ms

class Pump:
    def __init__(self, pin, corrective_factor = 800):
        self._p = Pin(pin, Pin.OUT)
        self.CF = corrective_factor
    def calibrate(self, target_mL, actual_mL):
        multiplier = target_mL / actual_mL
        self.CF = self.CF * multiplier
        return self.CF
    def dispense_mL(self, mL):
        corrected_value = int(mL * self.CF)
        self._run_pump(corrected_value)
    def prime(self):
        self._run_pump(5000)
    def _run_pump(self, duration):
        self._p.value(1)
        sleep_ms(duration)
        self._p.value(0)
