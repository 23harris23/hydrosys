from i2c_lcd import I2cLcd
from machine import I2C, SoftI2C, Pin

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


class lcd_output:
    def __init__(self, scl = 23, sda = 22, addr = 0x27, debug = True):
        i2c = SoftI2C(scl = Pin(scl), sda = Pin(sda), freq = 10000)
        LCD_ADDR = addr
        self.lcd = I2cLcd(i2c, LCD_ADDR, 2, 16)
        self.debug = debug
    def lcd_write(self, output):
        self.lcd.clear()
        self.lcd.putstr(output)
        if self.debug is True:
            print(output)
    def incomplete_placeholer(self):
        self.lcd_write('Under development')