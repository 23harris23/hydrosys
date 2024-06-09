from time import sleep_ms
from machine import Pin


class char_str:
    ENTER_CHAR = '#'
    BACKSPACE_CHAR = '*'
    def __init__(self, char_callback, update = print):
        self.char_callback = char_callback
        self.update = update
    def exclude_values(self, input_char, values):
        values = list(values) + [None]
        if input_char in values:
            input_char = ''
        return input_char
    def limit_char(self, input_char, input_string, target_char, n = 1):
        if target_char == '' or target_char is None:
            return input_char
        elif input_string.count(target_char) < n and input_char == target_char:
            return input_char
        elif input_char != target_char:
            return input_char
        return ''
    def get_str(self, forbidden_chars = [], limit_char = ''):
        out_str = ''
        char = ''
        while char is not('#'):
            char = self.exclude_values(self.char_callback(), forbidden_chars)
            char = str(char)
            char = self.limit_char(char, out_str, limit_char)
            if char == '*': #uses '*' as a backspace function
                out_str = out_str[:-1]
                char = ''
            out_str = out_str + char
            self.update(out_str)
        out_str = out_str[:-1]
        return out_str
    def get_int(self):
        int_output = (self.get_str(forbidden_chars = ['A', 'B', 'C', 'D']))
        if int_output[0] == '0':
            int_output = int(int_output[1:])
        return int_output
    '''
    def get_float(self):
        float_input =
    ''' 


class keypad:
    MAP_16X = [[1,2,3,'A'],
    [4,5,6,'B'],
    [7,8,9,'C'],
    ['*',0,'#','D']]
    def __init__(self, rows, collumns, key_map, debounce_time = 200):
        self.rows = [Pin(pin, Pin.OUT) for pin in rows]
        self.collumns = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in collumns]
        self.key_map = key_map
        self.debounce_time = debounce_time
    def get_key(self, row, collumn):
        state = None
        self.rows[row].value(1)
        if self.collumns[collumn].value() == 1:
            state = [row, collumn]
        self.rows[row].value(0)
        return state
    def get_keys(self):
        key = None
        for r in range(len(self.rows)):
            for c in range(len(self.collumns)):
                state = self.get_key(r, c)
                if state is not(None):
                    key = state
        return key
    def get_char(self):
        char = None
        state = self.get_keys()
        while state is None:
            state = self.get_keys()
            sleep_ms(self.debounce_time)
        char = self.key_map[state[0]][state[1]]
        return char


if __name__ == '__main__':
    ROWS = [14, 27, 26, 25]
    COLLUMNS = [33, 32, 12, 13]
    kp = keypad(ROWS, COLLUMNS, keypad.MAP_16X)
    kp_str = char_str(kp.get_char)
    '''
    for x in range(5):
        print(kp.get_char())
    print(kp_str.get_str())
    '''
    int_math_test = kp_str.get_int() + 3
    print(int_math_test)
