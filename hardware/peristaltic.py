from time import sleep_ms


class pump():
    def __init__(self, on_callback, off_callback, name, corrective_factor = 800):
        self.CF = corrective_factor
        self.on_callback = on_callback
        self.off_callback = off_callback
        self.name = name
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
    def rename(self, name):
        self.name = name
    def get_corrective_factor(self):
        return self.CF
    def get_name(self):
        return self.name
    def get_config(self):
        return (self.name, self.CF)
    def set_config(self, config):
        self.name = config[0]
        self.CF = config[1]

def instalize_595_pump(ID, shift_register, name):
    on_callback = lambda: shift_register.activate_pin(ID)
    off_callback = shift_register.clear_all
    return pump(on_callback, off_callback, name)
