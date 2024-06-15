from time import sleep_ms


class Pump:
    def __init__(self, on_callback, off_callback, corrective_factor = 800):
        self.CF = corrective_factor
        self.on_callback = on_callback
        self.off_callback = off_callback
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
        self.on_callback()
        sleep_ms(duration)
        self.off_callback()
