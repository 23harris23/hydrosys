from machine import Pin, SoftI2C
import time
from rotary_irq_esp import RotaryIRQ
from i2c_lcd import I2cLcd
from machine import I2C

def catch_none_types(var, default):
    if (var is None):
        var =  default
    return var

def _none():
    pass

DUMMY_DIC = {'test': _none}

class Index:
    ITEM_SELECTION = 0
    NUMERICAL_SELECTION = 1
    master_dict = {}
    counter = 0
    current_menu = None
    current_index = None
    def goto(name):
        Index.current_menu = Index.master_dict[name]
        
    def execute_functions():
        Index.current_menu.execute_menu_functions()
    

class Menu(Index):
    #menu format dictionary format: {'menu option': [function 1, function 2,],} functions execute in order of list
    #display callbacks handle string output
    #change mode series of constants defined in the index
    def __init__(self, disp_call=print, dic=DUMMY_DIC, name = None):
        self._mode = None
        self._incriment_callback = None
        self._display_callback = disp_call
        self._dic = dic 
        self.set_item_selection() #sets item selection by default
        self._index = list(self._dic.keys())
        self.counter_max = len(self._index)
        self.name = name
        self.master_dict[self.name] = self
    #move incriment functions to index class
    def set_display_callback(self, callback):
        self._display_callback = callback
        self._incriment_callback()

    def incriment_counter(self):
        Index.counter += 1
        self._incriment_callback()

    def decriment_counter(self):
        Index.counter -= 1
        self._incriment_callback()

    def set_counter_val(self, val):
        Index.counter = val
        self._incriment_callback()

    def set_item_selection(self):
        self._mode = "Item Selection"
        self._incriment_callback = self._item_selection

    def set_numerical_selection(self):
        self._mode = "Numerical Selection"
        self._incriment_callback = self._numerical_selection

    def get_max(self):
        return self.counter_max
    
    def get_mode(self):
        return self._mode

    def execute_menu_functions(self):
        selected_item = self._get_item()
        if isinstance(selected_item, list):
            [f() for f in selected_item]
        elif callable(selected_item):
            selected_item()
        else:
            print(type(selected_item))
            print('error')

    def _item_selection(self):
        self._limit_to_max()
        self._display_callback(self._index[self.counter])

    def _numerical_selection(self):
        self._nat_ints_only()
        self._display_callback(f"{self.counter} {self._index[0]}")

    def _nat_ints_only(self):
        if self.counter < 0:
            self.counter = 0

    def _limit_to_max(self):
        self._nat_ints_only()
        if Index.counter > self.counter_max:
            Index.counter = self.counter_max

    def _get_item(self):
        try:
            return self._dic[self._index[Index.counter]]
        except IndexError:
            return self._dic[self._index[0]]
    


class Rotary_Input:
    def __init__(
        self,
        r_pinA=32,
        r_pinB=33,
        r_Button=25,
        r_max_val=10,
        r_button_callback=None,
        menu=None,
    ):
        self._imported_menu = Index.current_menu #make definable again.
        self._rotary_button_callback = r_button_callback
        self._rotary_button_callback = catch_none_types(r_button_callback, _none)
        self._rotary_callback_function = _none
        self.rotary_encoder = RotaryIRQ(
            pin_num_clk=r_pinA,
            pin_num_dt=r_pinB,
            min_val=0,
            max_val=r_max_val - 1,
            reverse=True,
            range_mode=RotaryIRQ.RANGE_WRAP,
            pull_up=True,
        )
        self.rotary_encoder.add_listener(self._rotary_callback)
        self._sync_mode()
        self.rotary_button = Pin(25, Pin.IN, Pin.PULL_UP)
        self.rotary_button.irq(trigger=Pin.IRQ_FALLING, handler=self._debounce)
    def update_menu(self, menu=None):
        self._imported_menu = Index.current_menu
    def _rotary_callback(self):
        self._nat_ints_only()
        self._imported_menu.set_counter_val(self.rotary_encoder.value())
    def _update_listener(self, listner):
        self.rotary_encoder.remove_listener()
    def _debounce(self, irq):
        self.rotary_button.irq(handler=None)
        self._rotary_button_callback()
        self.update_menu()
        self._sync_mode()
        print('button pressed')
        time.sleep_ms(200)
        self.rotary_button.irq(trigger=Pin.IRQ_FALLING, handler=self._debounce)
    def _sync_mode(self):
        mode = self._imported_menu.get_mode()
        if mode == 'Item Selection':
            self._limit_to_index()
        elif mode == 'Numerical Selection':
            self._all_nat_ints()
    def _nat_ints_only(self):
        if self.rotary_encoder.value() < 0:
            self.rotary_encoder.set(value = 0)
    def _limit_to_index(self):
        max = self._imported_menu.get_max() - 1
        self.rotary_encoder.set(max_val = max, range_mode = RotaryIRQ.RANGE_WRAP)
    def _all_nat_ints(self):
        self.rotary_encoder.set(range_mode = RotaryIRQ.RANGE_UNBOUNDED)

class Terminal_Input:
    def __init__(self, menu = Index.current_menu):
        self._imported_menu = menu
        self._max_val = self._imported_menu.get_max()
    def display_menu(self):
        for i in range(len(self._imported_menu._index)):
            print(f'{i}: {self._imported_menu._index[i]}\n')
    def update_menu(self):
        self._imported_menu = Index.current_menu
    def select_item(self):
        self.update_menu()
        self.display_menu()
        keyboard_str = input(': ')
        selection = self.eval_input(keyboard_str)
        self._imported_menu.set_counter_val(selection)
        self._imported_menu.execute_menu_functions()
        return(keyboard_str)
    def eval_input(self, inp):
        try:
            inp = int(inp)
            return inp
        except ValueError:
            return inp
    
    
        

class LCD:
    def __init__(self):
        self.lcd_connection = True
        self.I2C_ADDR = 0x27
        self.TOTAL_ROWS = 2
        self.TOTAL_COLUMNS = 16
        self.i2c = SoftI2C(scl=Pin(22), sda=Pin(23), freq=10000)
        self.lcd = None
        try:
            self.lcd = I2cLcd(
                self.i2c, self.I2C_ADDR, self.TOTAL_ROWS, self.TOTAL_COLUMNS
            )
        except OSError as e:
            print("LCD not connected, debug over serial initiated")
            self.lcd_connection = False

    def update(self, msg):
        if self.lcd_connection is True:
            self.lcd.clear()
            self.lcd.putstr(msg)
        else:
            print(msg)

