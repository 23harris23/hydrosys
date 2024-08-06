import json
from collections import OrderedDict


class config_file:
    DEFAULT_PATH = 'conf.json'
    DEFAULT_CONF = '{}'
    def __init__(self, path):
        self.path = path
    def get_config_data(self):
        try:
            f = open(self.path, 'r')
            data = f.read()
            f.close()
        except OSError:
            f = open(self.path, 'w')
            f.write(config_file.DEFAULT_CONF)
            f.close()
            data = config_file.DEFAULT_CONF
        return data
    def parse_config(self):
        raw_conf_data = self.get_config_data()
        json_data = json.loads(raw_conf_data)
        return json_data
    def get_config_entry(self, config_key):
        conf_json = self.parse_config()
        if config_key in conf_json.keys():
            return conf_json[config_key]
        return None
    def set_config_entry(self, name, config_value):
        json_data = self.parse_config()
        json_data[name] = config_value
        raw_data = json.dumps(json_data)
        f = open(self.path, 'w')
        f.write(raw_data)
        f.close()

class watering_profile_config(config_file):
    def __init__(self, path):
        super().__init__(path)
    def get_watering_profiles(self):
        config_data = self.parse_config()
        watering_profile_names = list(config_data.keys())
        return watering_profile_names
    def generate_numbered_dict(self, data):
        output_dict = {}
        data = OrderedDict(data)
        i = 0
        for entry in data:
            output_dict[i] = (entry, data[entry])
            i += 1
        return output_dict
    def generate_ordered_list(self, numbered_dict):
        output_list = []
        for i in range(len(numbered_dict)):
            output_list.append(numbered_dict[str(i)])
        return output_list
    def get_watering_data(self, watering_profile_name):
        watering_profile_data = self.get_config_entry(watering_profile_name)
        ordered_profile_data = self.generate_ordered_list(watering_profile_data)
        #profile_data = OrderedDict(reversed(list(watering_profile_data.items())))
        return ordered_profile_data
    def update_watering_profile(self, profile_name, profile_data):
        profile_data = self.generate_numbered_dict(OrderedDict(profile_data))
        self.set_config_entry(profile_name, profile_data)

class config_item(config_file):
    def __init__(self, path, name, get_item_callback, set_item_callback):
        super().__init__(path)
        self.get_item_callback = get_item_callback
        self.set_item_callback = set_item_callback
        self.name = name
        self.check_config_file()
    def get_value(self):
        value = self.get_item_callback()
        return value
    def set_item(self, value):
        self.set_item_callback(value)
        self.set_config_entry(self.name, value)
    def check_config_file(self):
        entry = self.get_config_entry(self.name)
        if entry is not None:
            self.set_item(entry)
        else:
            entry = self.get_item_callback()
            self.set_config_entry(self.name, self.get_item_callback())
    def update_config_value(self):
        self.set_item(self.get_value())
