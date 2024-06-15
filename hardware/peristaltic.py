from time import sleep_ms


class pump_index:
    master_dict = {}
    def activate_pump(target_pump):
        pump_index.master_dict[target_pump].on_callback()
    def deactivate_pump(target_pump):
        pump_index.master_dict[target_pump].off_callback()
    def rename_pump(target_pump, name):
        pump_index.master_dict[target_pump].name = name
        pump_index.master_dict[name] = pump_index.master_dict.pop(target_pump)
    
class pump(pump_index):
    def __init__(self, on_callback, off_callback, name = None, corrective_factor = 800):
        self.CF = corrective_factor
        self.on_callback = on_callback
        self.off_callback = off_callback
        self.name = name
        if self.name is None:
            self.name = len(self.master_dict)
        self.master_dict[self.name] = self
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
