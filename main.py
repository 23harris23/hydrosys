from menutils2 import *
from simplepH import pH
from peristaltic import Pump

class mL:
    value = 0
    def set_value(val):
        mL.value = val

display = LCD()
pH_sensor = pH(34)
mL_value = 0
pump1 = Pump(18)
pump2 = Pump(5)
pump3 = Pump(17)
pump4 = Pump(16)
pump5 = Pump(4)
pump6 = Pump(0)
pump7 = Pump(2)

main_menu_template = {
    'Calibration': lambda: Index.goto('Calibration Menu'),
    'Dose nutrient': lambda: Index.goto('mL Menu'),
    'Display pH': lambda ph = pH_sensor.get_pH(): display.update(ph)
    }

mL_selection_template = {
    'mL': [lambda: mL.set_value(Index.counter), lambda: Index.goto('Nutrient Menu')]
    }

nutrient_menu_template = {
    'Flora Micro': [lambda: pump7.dispense_mL(mL.value), lambda: display.update(mL.value), lambda: Index.goto('Main Menu')],
    'Flora Gro': [lambda: pump1.dispense_mL(mL.value), lambda: Index.goto('Main Menu')],
    'Flora Bloom': [lambda: pump2.dispense_mL(mL.value), lambda: Index.goto('Main Menu')],
    'Rapid Start': [lambda: pump3.dispense_mL(mL.value), lambda: Index.goto('Main Menu')],
    'Flora +': [lambda: pump4.dispense_mL(mL.value), lambda: Index.goto('Main Menu')],
    'Kool Bloom': [lambda: pump5.dispense_mL(mL.value), lambda: Index.goto('Main Menu')]
    }

main_menu = Menu(disp_call = display.update, dic = main_menu_template, name = 'Main Menu')
mL_menu = Menu(disp_call = display.update, dic = mL_selection_template, name = 'mL Menu')
mL_menu.set_numerical_selection()
nutrient_menu = Menu(disp_call = display.update, dic = nutrient_menu_template, name = 'Nutrient Menu')
Index.goto('Main Menu')

if __name__ == '__main__':
    #inputs = Rotary_Input(menu = Index.current_menu, r_button_callback = Index.execute_functions)
    ctrl = Terminal_Input(Index.current_menu)
    while True:
        ctrl.select_item()