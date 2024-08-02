from sys import path
from time import sleep_ms
path.append('/UI/')
path.append('/hardware/')
from UI import config_manager, menutils3, keypad_driver
from hardware import h2o_in, sr595, peristaltic, simplepH


#Pin definitions
KEYPAD_ROWS = [15, 2, 0, 4]
KEYPAD_COLLUMNS = [16, 17, 5, 18]
VALVE_PIN = 25
SR_SCK = 13
SR_RCK = 12
SR_Q = 14
I2C_SCL = 22
I2C_SDA = 23
PH_ADC = 36
#path definitions
HARDWARE_CONFIG_PATH = 'conf.json'
NUTRIENT_PROFILE_CONFIG_PATH = 'nutrients.json'
#hardware definitions
lcd = menutils3.lcd_output(scl = I2C_SCL, sda = I2C_SDA)
bus_12v = sr595.sr_595(ser = SR_Q, srclk = SR_SCK, rclk = SR_RCK)
water_inlet = h2o_in.water_inlet_valve(VALVE_PIN)
kp = keypad_driver.keypad(KEYPAD_ROWS, KEYPAD_COLLUMNS, keypad_driver.keypad.MAP_16X)
kp_api = keypad_driver.keypad_api(kp.get_char, lcd.lcd_write)
pH_sensor = simplepH.pH(sensor_pin = PH_ADC)
#nutrient pump definitions
nutrient_1 = peristaltic.instalize_595_pump(5, bus_12v, 'n1')
nutrient_2 = peristaltic.instalize_595_pump(6, bus_12v, 'n2')
nutrient_3 = peristaltic.instalize_595_pump(7, bus_12v, 'n3')
nutrient_4 = peristaltic.instalize_595_pump(8, bus_12v, 'n4')
pump_list = [nutrient_1, nutrient_2, nutrient_3, nutrient_4] #Includes every peristaltic pump
nutrient_pump_list = [nutrient_2, nutrient_3, nutrient_4] #Excludes pH control pumps
#config definitions
water_inlet_config = config_manager.config_item(get_item_callback = water_inlet.get_fill_rate,
                                                set_item_callback = water_inlet.set_fill_rate,
                                                name = 'Water In Flow Rate',
                                                path = HARDWARE_CONFIG_PATH)
nutrient_1_config = config_manager.config_item(get_item_callback = nutrient_1.get_config,
                                              set_item_callback = nutrient_1.set_config,
                                              name = 'Nutrient 1',
                                               path = HARDWARE_CONFIG_PATH)
nutrient_2_config = config_manager.config_item(get_item_callback = nutrient_2.get_config,
                                               set_item_callback = nutrient_2.set_config,
                                               name = 'Nutrient 2',
                                               path = HARDWARE_CONFIG_PATH)
nutrient_3_config = config_manager.config_item(get_item_callback = nutrient_3.get_config,
                                               set_item_callback = nutrient_3.set_config,
                                               name = 'Nutrient 3',
                                               path = HARDWARE_CONFIG_PATH)
nutrient_4_config = config_manager.config_item(get_item_callback = nutrient_4.get_config,
                                               set_item_callback = nutrient_4.set_config,
                                               name = 'Nutrient 4',
                                               path = HARDWARE_CONFIG_PATH)
pH_sensor_config = config_manager.config_item(get_item_callback = pH_sensor.get_config,
                                              set_item_callback = pH_sensor.set_config,
                                              name = 'pH Sensor',
                                              path = HARDWARE_CONFIG_PATH)
config_list = [water_inlet_config,
               nutrient_1_config,
               nutrient_2_config,
               nutrient_3_config,
               nutrient_4_config,
               pH_sensor_config]
#UI/hardware interface functions
def countdown(message, time_s):
    for t in range(time_s):
        remaining_time = time_s - t
        lcd.lcd_write(f'{message} {remaining_time}s')
        sleep_ms(1000)
    lcd.lcd_write(f'{message} 0s')
        
def update_all_config(config_list): #saves all current config values
    for config_item in config_list:
        config_item.update_config_value()

def incomplete_placeholder(): #temporary function shows feature is incomplete
    print('incomplete')

def generate_pump_dict(pump_list): #generates dictionary of pumps using names as keys, useful for other functions
    pump_menu = {}
    for pump in pump_list:
        pump_menu[pump.name] = pump
    return pump_menu

def select_pump_name(pump_list): #select a pump by name
    pump_dict = generate_pump_dict(pump_list)
    name_list = list(pump_dict.keys())
    selected_name = kp_api.incremental_selector(name_list)
    selected_pump = pump_dict[selected_name]
    return selected_pump

def dispense_selector(pump_list): #select a pump by name and select a quantity to dispense
    target_pump = select_pump_name(pump_list)
    mL = kp_api.get_int()
    target_pump.dispense_mL(mL)

def prime_all_pumps(pump_list): #run each pump for 5s to fill line and ensure accuracy
    for pump in pump_list:
        pump.prime()

def rename_pump(pump_list): #renames pump
    target_pump = select_pump_name(pump_list)
    new_name = kp_api.get_alphanum()
    target_pump.rename(new_name)
    update_all_config(config_list)

def calibrate_pump(pump_list): #allows for pump calibration using a graduated cylender
    target_pump = select_pump_name(pump_list)
    countdown(message = 'Dispensing 40 mL in', time_s = 10)
    target_pump.dispense_mL(40)
    lcd.lcd_write('Done, enter actual mL quantity')
    actual_mL = kp_api.get_float()
    target_pump.calibrate(40, actual_mL)
    update_all_config(config_list)

def calibrate_water_in(water_valve): #calibrates fill time for main tank
    countdown(message = 'Filling tank in', time_s = 10)
    water_valve.calibrate_fill_rate()
    update_all_config(config_list)

def calibrate_pH_sensor():
    countdown(message = 'Insert probe into 7pH fluid in', time_s = 10)
    countdown(message = 'Keep probe in fluid for', time_s = 30)
    pH_sensor.calibrate()
    update_all_config(config_list)

#menu_goto_functions
go_to = menutils3.Index.goto
goto_main = lambda: go_to('Main Menu')
goto_watering = lambda: go_to('Watering Menu')
goto_settings = lambda: go_to('Settings Menu')
goto_calibration = lambda: go_to('Calibration Menu')
#menu definitions
main_menu = {'Water': goto_watering, 
'Settings': goto_settings, 
'Calibration': goto_calibration}
watering_menu = {'Custom Watering': lambda: dispense_selector(pump_list), 
'Preset watering': incomplete_placeholder,
'Home': goto_main}
settings_menu = {'Prime pumps': lambda: prime_all_pumps(pump_list), 
'Create water preset': incomplete_placeholder,
'Alias nutrient pumps': lambda: rename_pump(pump_list),
'Home': goto_main}
calibration_menu = {'Tank Fill': lambda: calibrate_water_in(water_inlet), 
'pH sensor': calibrate_pH_sensor, 
'Dose pumps': lambda: calibrate_pump(pump_list),
'Home': goto_main}

Main_Menu = menutils3.Menu(main_menu, 'Main Menu')
Watering_Menu = menutils3.Menu(watering_menu, 'Watering Menu')
Settings_Menu = menutils3.Menu(settings_menu, 'Settings Menu')
Calibration_Menu = menutils3.Menu(calibration_menu, 'Calibration Menu')

if __name__ == '__main__':
    print('ready') #
    if __name__ == '__main__':
        menutils3.Index.goto('Main Menu')
        while True:
            target = kp_api.incremental_selector(menutils3.Index.current_index)
            menutils3.Index.execute_functions(target)
