from sys import path
path.append('/UI/')
path.append('/hardware/')
from UI import config_manger, menutils3, keypad_driver
from hardware import h2o_in, sr595, peristaltic
from time import sleep_ms


#Pin definitions
KEYPAD_ROWS = [26, 25, 33, 32]
KEYPAD_COLLUMNS = [35, 34, 39, 36]
VALVE_PIN = 23
SR_SCK = 14
SR_RCK = 12
SR_Q = 27
#hardware definitions
bus_12v = sr595.sr_595(SR_Q, SR_SCK, SR_RCK)
water_inlet = h2o_in.water_inlet_valve(VALVE_PIN)
kp = keypad_driver.keypad(KEYPAD_ROWS, KEYPAD_COLLUMNS, keypad_driver.keypad.MAP_16X)
kp_api = keypad_driver.keypad_api(keypad_driver.dummy_keypad)
#nutrient pump definitions
nutrient_1 = peristaltic.instalize_595_pump(1, bus_12v, 'n1')
nutrient_2 = peristaltic.instalize_595_pump(2, bus_12v, 'n2')
nutrient_3 = peristaltic.instalize_595_pump(3, bus_12v, 'n3')
nutrient_4 = peristaltic.instalize_595_pump(4, bus_12v, 'n4')
pump_list = [nutrient_1, nutrient_2, nutrient_3, nutrient_4]
#config definitions
water_inlet_config = config_manger.config_item(get_item_callback = water_inlet.get_fill_rate,
                                                   set_item_callback = water_inlet.set_fill_rate,
                                                   name = 'Water In Flow Rate')
nutrient_1_config = config_manger.config_item(get_item_callback = nutrient_1.get_config,
                                              set_item_callback = nutrient_1.set_config,
                                              name = 'Nutrient 1')
nutrient_2_config = config_manger.config_item(get_item_callback = nutrient_2.get_config,
                                              set_item_callback = nutrient_2.set_config,
                                              name = 'Nutrient 2')
nutrient_3_config = config_manger.config_item(get_item_callback = nutrient_3.get_config,
                                              set_item_callback = nutrient_3.set_config,
                                              name = 'Nutrient 3')
nutrient_4_config = config_manger.config_item(get_item_callback = nutrient_4.get_config,
                                              set_item_callback = nutrient_4.set_config,
                                              name = 'Nutrient 4')
config_list = [water_inlet_config, nutrient_1_config, nutrient_2_config, nutrient_3_config, nutrient_4_config]
#menu definitions
def update_all_config(config_list): #saves all current config values
    for config_item in config_list:
        config_item.update_config_value()

def incomplete_placeholder():
    print('incomplete')

def generate_pump_dict(pump_list):
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

def prime_all_pumps(pump_list):
    for pump in pump_list:
        pump.prime()

def rename_pump(pump_list):
    target_pump = select_pump_name(pump_list)
    new_name = kp_api.get_alphanum()
    target_pump.rename(new_name)
    update_all_config(config_list)

def calibrate_pump(pump_list):
    target_pump = select_pump_name(pump_list)
    print('dispensing 40 mL in 10s')
    sleep_ms(10000)
    target_pump.dispense_mL(40)
    print('Done, enter actual mL quantity')
    sleep_ms(3000)
    actual_mL = kp_api.get_float()
    target_pump.calibrate(40, actual_mL)

def calibrate_water_in(water_valve):
    water_valve.calibrate_fill_rate()
    update_all_config(config_list)

main_menu = {'Water': lambda: menutils3.Index.goto('Watering Menu'), 
'Settings': lambda: menutils3.Index.goto('Settings Menu'), 
'Calibration': lambda: menutils3.Index.goto('Calibration Menu')}
watering_menu = {'Custom Watering': lambda: dispense_selector(pump_list), 
'Preset watering': incomplete_placeholder,
'Home': lambda: menutils3.Index.goto('Main Menu')}
settings_menu = {'Prime pumps': lambda: prime_all_pumps(pump_list), 
'Create water preset': incomplete_placeholder,
'Alias nutrient pumps': lambda: rename_pump(pump_list),
'Home': lambda: menutils3.Index.goto('Main Menu')}
calibration_menu = {'Tank Fill': lambda: calibrate_water_in(water_inlet), 
'pH sensor': incomplete_placeholder, 
'Dose pumps': lambda: calibrate_pump(pump_list),
'Home': lambda: menutils3.Index.goto('Main Menu')}

Main_Menu = menutils3.Menu(main_menu, 'Main Menu')
Watering_Menu = menutils3.Menu(watering_menu, 'Watering Menu')
Settings_Menu = menutils3.Menu(settings_menu, 'Settings Menu')
Calibration_Menu = menutils3.Menu(calibration_menu, 'Calibration Menu')

if __name__ == '__main__':
    test_val = water_inlet_config.get_value()
    print(f'{test_val} ms for test')
    prime_all_pumps(pump_list)
    #dispense_selector(pump_list)
    if __name__ == '__main__':
        menutils3.Index.goto('Main Menu')
        while True:
            target = kp_api.incremental_selector(menutils3.Index.current_index)
            menutils3.Index.execute_functions(target)

