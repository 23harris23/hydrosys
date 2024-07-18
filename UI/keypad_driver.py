from time import sleep_ms
from machine import Pin


class keypad_api:
    ENTER_CHAR = '#'
    BACKSPACE_CHAR = '*'
    CHAR_ROW0 = [0, ' ']
    CHAR_ROW1 = [1, 'A', 'B', 'C']
    CHAR_ROW2 = [2, 'D', 'E', 'F']
    CHAR_ROW3 = [3, 'G', 'H', 'I']
    CHAR_ROW4 = [4, 'J', 'K', 'L']
    CHAR_ROW5 = [5, 'L', 'M', 'N']
    CHAR_ROW6 = [6, 'O', 'P', 'R']
    CHAR_ROW7 = [7, 'S', 'T', 'U']
    CHAR_ROW8 = [8, 'V', 'W', 'X']
    CHAR_ROW9 = [9, 'Y', 'Z']
    NULL_ROW = ['']
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
    def no_leading_0 (self, input_str):
        while input_str[0] == '0':
            input_str = input_str[1:]
        return input_str
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
        if int_output == '':
            return 0
        else:
            int_output = int(self.no_leading_0(int_output))
            return int_output
    def get_float(self):
        float_input = self.get_str(forbidden_chars = ['A', 'B', 'C'], limit_char = 'D')
        if float_input == '':
            return 0
        else:
            float_input = float_input.replace('D', '.')
            float_input = self.no_leading_0(float_input)
            return float(float_input)
    def incremental_selector(self, input_list):
        char = ''
        position = 0
        max_position = len(input_list) - 1
        while char is not('#'):
            char =  self.exclude_values(self.char_callback(), [1,2,3,4,5,6,7,8,9,'*','C','D'])
            if char == 'A':
                position -= 1
                if position < 0:
                    position = max_position
            elif char == 'B':
                position += 1
                if position > max_position:
                    position = 0
            if char == 'A' or char == 'B':
                self.update(input_list[position])
                char = ''
            sleep_ms(100)
        self.update(f'{input_list[position]} Selected')
        return input_list[position]
    def get_char_row(self, value):
        if value == 0:
            return keypad_api.CHAR_ROW0
        elif value == 1:
            return keypad_api.CHAR_ROW1
        elif value == 2:
            return keypad_api.CHAR_ROW2
        elif value == 3:
            return keypad_api.CHAR_ROW3
        elif value == 4:
            return keypad_api.CHAR_ROW4
        elif value == 5:
            return keypad_api.CHAR_ROW5
        elif value == 6:
            return keypad_api.CHAR_ROW6
        elif value == 7:
            return keypad_api.CHAR_ROW7
        elif value == 8:
            return keypad_api.CHAR_ROW8
        elif value == 9:
            return keypad_api.CHAR_ROW9
        else:
            return keypad_api.NULL_ROW
    def cycle_char_row(self, update_text = ''):
        #fix need to press buttons multiple times to cycle inputs
        starting_char = self.exclude_values(self.char_callback(), ['A', 'B', 'D'])
        position = 0
        char_select = self.get_char_row(starting_char)
        output_char = ''
        if starting_char == '*' or starting_char == '#':
            return starting_char
        char = self.exclude_values(self.char_callback(), ['A', 'B', 'D'])
        while char == starting_char or char == '':
            char = self.exclude_values(self.char_callback(), ['A', 'B', 'D'])
            if char == starting_char:
                position += 1
                if position >= len(char_select):
                    position = 0
                self.update(update_text + str(char_select[position]))
                output_char = char_select[position]
        return output_char
    def get_alphanum(self):
        char = ''
        output = ''
        while char is not('#'):
            char = self.cycle_char_row(output)
            if char == '*':
                output = output[:-1]
                char = ''
                self.update(output)
            output += str(char)
            self.update(output)
        output = output[:-1]
        return output


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

def dummy_keypad():
    char = input('char: ')
    try:
        char = int(char)
    except:
        pass
    return char

if __name__ == '__main__':
    
    ROWS = [26, 25, 33, 32]
    COLLUMNS = [35, 34, 39, 36]
    kp = keypad(ROWS, COLLUMNS, keypad.MAP_16X)
    kp_str = keypad_api(kp.get_char)
    kp_str = keypad_api(dummy_keypad)
    '''
    for x in range(5):
        print(kp.get_char())
    print(kp_str.get_str())
    '''
    #int_math_test = kp_str.get_int() + 3
    #print(int_math_test)
    #print(kp_str.get_float())
    print(kp_str.incremental_selector(['a', 'b', 'c']))
    #print(kp_str.cycle_char_row())
    #print(kp_str.get_alphanum())

