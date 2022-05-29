from machine import Pin, SoftI2C, ADC
from time import sleep_ms, sleep
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from machine import I2C
import json

class pH:
    sensor = ADC(Pin(39))
    sensor.atten(ADC.ATTN_11DB)
    sensor.width(3)
    calibration_value = 0
    #calibration_value = config.data['pH_config']
    def get_volts():
        voltage = (pH.sensor.read()/4095) * 3.3
        return voltage
    def display_values():
        while True:
            volts = pH.get_volts()
            output_pH = pH.average_pH(100)
            print(f'{volts} v pH:{output_pH}')
            sleep_ms(100)
    def get_pH():
        output_pH = pH.calibration_value * pH.get_volts()
        return output_pH
    def average_pH(sample_size):
        output_pH = 0
        for i in range(sample_size):
            output_pH = output_pH + pH.get_pH()
            sleep_ms(10)
        output_pH = output_pH / sample_size
        return output_pH
    def calibrate_sensor():
        for i in range(5):
            remaining_time = 5 - i
            update_lcd(f'Calibrating in {remaining_time}s')
            sleep_ms(1000)
        avg_voltage = 0
        for i in range(100):
            avg_voltage = avg_voltage + pH.get_volts()
        avg_voltage = avg_voltage / 100
        pH.calibration_value = 7 / avg_voltage
        config.update('pH_config', pH.calibration_value)
        print(f'7 pH = {avg_voltage} V')

class config:
    default_values = {'pH_config': 6.0}
    data = None
    def read():
        try:
            with open('config.txt', 'r') as file:
                config.data = json.load(file)
                file.close()
        except OSError:
            config.default()
            with open('config.txt', 'r') as file:
                config.data = json.load(file)
                file.close()
    def default():
        with open('config.txt', 'w') as file:
            json.dump(config.default_values, file)
            file.close()
    def update(variable, value):
        if variable in config.data:
            del config.data[variable]
        new_data = {variable: value}
        config.data.update(new_data)
        with open('config.txt', 'w') as file:
            file.seek(0)
            json.dump(config.data, file)
            file.close()
    
class buttons:
    button1 = Pin(32, Pin.IN, Pin.PULL_UP)
    button2 = Pin(33, Pin.IN, Pin.PULL_UP)
    button3 = Pin(25, Pin.IN, Pin.PULL_UP)
    button4 = Pin(26, Pin.IN, Pin.PULL_UP)
    pump_selector = 1
    max_pumps = 5
    mL = 0
    def decriment_mL(irq):
        d =  debounce(buttons.button1)
        if d == None:
            return
        elif not d:
            if buttons.mL == 0:
                buttons.mL = 0
            else:
                buttons.mL -= 1
                print(f'{buttons.mL} mL')
                update_lcd(f'{buttons.mL} mL Pump {buttons.pump_selector}')
    def incriment_mL(irq):
        d = debounce(buttons.button2)
        if d == None:
            return
        elif not d:
            buttons.mL += 1
            print(f'{buttons.mL} mL')
            update_lcd(f'{buttons.mL} mL Pump {buttons.pump_selector}')
    def incriment_pump(irq):
        d = debounce(buttons.button3)
        if d == None:
            return
        elif not d:
            if buttons.pump_selector == 5:
                buttons.pump_selector = 1
            else:
                buttons.pump_selector += 1
            print(f'Pump {buttons.pump_selector} selected')
            update_lcd(f'{buttons.mL} mL Pump {buttons.pump_selector}')
    def dispense(irq):
        d = debounce(buttons.button4)
        if d == None:
            return
        elif not d:
            print(f'Dispensing {buttons.mL} mL on pump {buttons.pump_selector}')
            update_lcd(f'Dispensing {buttons.mL} mL on pump {buttons.pump_selector}')
            if buttons.pump_selector == 1:
                pumps.dispense_ml(pumps.pump1, buttons.mL, pumps.CF1)
            elif buttons.pump_selector == 2:
                pumps.dispense_ml(pumps.pump2, buttons.mL, pumps.CF2)
            elif buttons.pump_selector == 3:
                pumps.dispense_ml(pumps.pump3, buttons.mL, pumps.CF3)
            elif buttons.pump_selector == 4:
                pumps.dispense_ml(pumps.pump4, buttons.mL, pumps.CF4)
            elif buttons.pump_selector == 5:
                pumps.dispense_ml(pumps.pump5, buttons.mL, pumps.CF5)
            update_lcd('Done!')

class pumps:
    OVERALL_CF = 800 #Rough time in ms to pump 1 mL
    CF1 = 1.06
    CF2 = 1.16
    CF3 = 1.05
    CF4 = 1.09
    CF5 = 1
    pump1 = Pin(17, Pin.OUT)
    pump2 = Pin(16, Pin.OUT)
    pump3 = Pin(4, Pin.OUT)
    pump4 = Pin(0, Pin.OUT)
    pump5 = Pin(2, Pin.OUT)
    def run_pump(pump, duration):
        pump.value(0)
        sleep_ms(duration)
        pump.value(1)
    def init():
        pumps.pump1.value(1)
        pumps.pump2.value(1)
        pumps.pump3.value(1)
        pumps.pump4.value(1)
        pumps.pump5.value(1)
    def prime():
        pumps.run_pump(pumps.pump1, 5000)
        pumps.run_pump(pumps.pump2, 5000)
        pumps.run_pump(pumps.pump3, 5000)
        pumps.run_pump(pumps.pump4, 5000)
        pumps.run_pump(pumps.pump5, 5000)
    def correct_value(correction_factor, value):
        new_value = round(correction_factor * int(value) * pumps.OVERALL_CF)
        print(f'CV: {new_value}')
        return new_value
    def dispense_ml(pump, quantity, CF):
        CV = pumps.correct_value(CF, int(quantity))
        pumps.run_pump(pump, CV)

def update_lcd(msg):
    lcd.clear()
    lcd.putstr(msg)

def debounce(pin):
    prev = None
    for x in range(32):
        current_value = pin.value()
        if prev != None and prev != current_value:
            return None
        prev = current_value
        return prev
    
I2C_ADDR = 0x27
TOTAL_ROWS = 2
TOTAL_COLUMNS = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(23), freq=10000)
lcd = I2cLcd(i2c, I2C_ADDR, TOTAL_ROWS, TOTAL_COLUMNS)

if __name__ == '__main__':
    config.read()
    pH.calibrate_sensor()
    buttons.button1.irq(trigger = Pin.IRQ_FALLING, handler = buttons.decriment_mL)
    buttons.button2.irq(trigger = Pin.IRQ_FALLING, handler = buttons.incriment_mL)
    buttons.button3.irq(trigger = Pin.IRQ_FALLING, handler = buttons.incriment_pump)
    buttons.button4.irq(trigger = Pin.IRQ_FALLING, handler = buttons.dispense)
    update_lcd(f'{buttons.mL} mL Pump {buttons.pump_selector}')
    pumps.init()
    pH.display_values()
#    while True:
#        pass
        