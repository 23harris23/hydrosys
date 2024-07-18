from water_in_test import water_inlet_valve
import json


VALVE_PIN = 23

class config_file:
    PATH = 'conf.json'
    DEFAULT_CONF = '{"test": 0}'
    def get_config_data():
        try:
            f = open(config_file.PATH, 'r')
            data = f.read()
            f.close()
        except OSError:
            f = open(config_file.PATH, 'w')
            f.write(config_file.DEFAULT_CONF)
            f.close()
            data = config_file.DEFAULT_CONF
        return data
    def parse_config():
        raw_conf_data = config_file.get_config_data()
        json_data = json.loads(raw_conf_data)
        return json_data
    def get_config_entry(config_key):
        conf_json = config_file.parse_config()
        if config_key in conf_json.keys():
            return conf_json[config_key]
        return None
    def set_config_entry(name, config_value):
        json_data = config_file.parse_config()
        json_data[name] = config_value
        raw_data = json.dumps(json_data)
        f = open(config_file.PATH, 'w')
        f.write(raw_data)
        f.close()
        

class config_item(config_file):
    def __init__(self, get_item_callback, set_item_callback, name):
        self.get_item_callback = get_item_callback
        self.set_item_callback = set_item_callback
        self.name = name
        self.check_config_file()
    def get_value(self):
        value = self.get_item_callback()
        return value
    def set_item(self, value):
        self.set_item_callback(value)
        config_file.set_config_entry(self.name, value)
    def check_config_file(self):
        entry = config_file.get_config_entry(self.name)
        if entry is not None:
            self.set_item(entry)
        else:
            entry = self.get_item_callback()
            config_file.set_config_entry(self.name, self.get_item_callback())


if __name__ == '__main__':
    valve1 = water_inlet_valve(VALVE_PIN)
    valve1_config = config_item(get_item_callback = valve1.get_fill_rate, set_item_callback = valve1.set_fill_rate, name = 'Water In Flow Rate')
    test_val = valve1_config.get_value()
    print(f'{test_val * 3} ms for test')
    valve1.fill_quantity(3)

    
