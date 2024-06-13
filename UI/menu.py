from keypad import keypad, keypad_api


class Index:
    master_dict = {}
    current_menu = None
    current_index = None
    def goto(name):
        Index.current_menu = Index.master_dict[name]
        Index.current_index = Index.current_menu.get_index()
        
    def execute_functions(target):
        Index.current_menu.execute_menu_functions(target)
    

class Menu(Index):
    #menu format dictionary format: {'menu option': [function 1, function 2,],} functions execute in order of list
    #display callbacks handle string output
    #change mode series of constants defined in the index
    def __init__(self, dic, name):
        self._dic = dic 
        self._index = list(self._dic.keys())
        self.name = name
        self.master_dict[self.name] = self

    def get_index(self):
        return self._index
    
    def execute_menu_functions(self, target):
        selected_item = self._get_item(target)
        if isinstance(selected_item, list):
            [f() for f in selected_item]
        elif callable(selected_item):
            selected_item()
        else:
            print(type(selected_item))
            print('error')
    #possibly remove try/except loop
    def _get_item(self, target):
        try:
            return self._dic[target]
        except IndexError:
            return self._dic[self._index[0]]


ROWS = [26, 25, 33, 32]
COLLUMNS = [35, 34, 39, 36]
kp = keypad(ROWS, COLLUMNS, keypad.MAP_16X)
kp_api = keypad_api(kp.get_char)

def incomplete_placeholer():
    print('Under development')

main_menu = {'Water': lambda: Index.goto('Watering Menu'), 
'Settings': lambda: Index.goto('Settings Menu'), 
'Calibration': lambda: Index.goto('Calibration Menu')}
watering_menu = {'Custom Watering': incomplete_placeholer, 
'Preset watering': incomplete_placeholer,
'Home': lambda: Index.goto('Main Menu')}
settings_menu = {'Prime pumps': incomplete_placeholer, 
'Create water preset': incomplete_placeholer,
'Alias nutrient pumps': incomplete_placeholer,
'Home': lambda: Index.goto('Main Menu')}
calibration_menu = {'Tank Fill': incomplete_placeholer, 
'pH sensor': incomplete_placeholer, 
'Dose pumps': incomplete_placeholer,
'Home': lambda: Index.goto('Main Menu')}

Main_Menu = Menu(main_menu, 'Main Menu')
Watering_Menu = Menu(watering_menu, 'Watering Menu')
Settings_Menu = Menu(settings_menu, 'Settings Menu')
Calibration_Menu = Menu(calibration_menu, 'Calibration Menu')
'''

'''

if __name__ == '__main__':
    Index.goto('Main Menu')

    while True:
        target = kp_api.incremental_selector(Index.current_index)
        Index.execute_functions(target)
    '''
    menu1 = {'a': lambda: print('a'), 'b': lambda: print('b')}
    menu2 = {'c': lambda: print('c'), 'd': lambda: print('d')}
    m1 = Menu(menu1, 'Menu A')
    m2 = Menu(menu2, 'Menu B')
    Index.goto('Menu A')
    Index.execute_functions('a')
    Index.execute_functions('b')
    '''

    