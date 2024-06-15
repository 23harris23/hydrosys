from keypad import keypad, keypad_api
from menutils3 import *

lcd = lcd_output()
ROWS = [26, 25, 33, 32]
COLLUMNS = [35, 34, 39, 36]
kp = keypad(ROWS, COLLUMNS, keypad.MAP_16X)
kp_api = keypad_api(kp.get_char, lcd.lcd_write)


main_menu = {'Water': lambda: Index.goto('Watering Menu'), 
'Settings': lambda: Index.goto('Settings Menu'), 
'Calibration': lambda: Index.goto('Calibration Menu')}
watering_menu = {'Custom Watering': lcd.incomplete_placeholer, 
'Preset watering': lcd.incomplete_placeholer,
'Home': lambda: Index.goto('Main Menu')}
settings_menu = {'Prime pumps': lcd.incomplete_placeholer, 
'Create water preset': lcd.incomplete_placeholer,
'Alias nutrient pumps': lcd.incomplete_placeholer,
'Home': lambda: Index.goto('Main Menu')}
calibration_menu = {'Tank Fill': lcd.incomplete_placeholer, 
'pH sensor': lcd.incomplete_placeholer, 
'Dose pumps': lcd.incomplete_placeholer,
'Home': lambda: Index.goto('Main Menu')}

Main_Menu = Menu(main_menu, 'Main Menu')
Watering_Menu = Menu(watering_menu, 'Watering Menu')
Settings_Menu = Menu(settings_menu, 'Settings Menu')
Calibration_Menu = Menu(calibration_menu, 'Calibration Menu')


if __name__ == '__main__':
    Index.goto('Main Menu')

    while True:
        target = kp_api.incremental_selector(Index.current_index)
        Index.execute_functions(target)

    