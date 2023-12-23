import json


class Settings:
    def __init__(self):
        self.user_settings = dict()
        self.open_json("config.json")

    def open_json(self, json_file):
        try:
            self.user_settings = json.load(open(json_file))
            for user_setting_key in self.user_settings:
                setattr(self, user_setting_key, self.user_settings[user_setting_key])
        except FileNotFoundError as exc:
            print(f"Settings file is not found. Exception: {exc}")
        except json.JSONDecodeError as exc:
            print(f'JSON error. Exception: {exc}')

    def update(self):
        for user_setting_key in self.user_settings:
            self.user_settings[user_setting_key] = getattr(self, user_setting_key)
        with open('config.json', 'w') as f:
            json.dump(self.user_settings, f, indent=2)

    def set_default(self): # Doesn't work
        self.open_json("default.json")


settings = Settings()

'''
d = {'name': 'Roman', 'coins': 100, 'car': 'BMW', 'score': 1000}
with open('config.json', 'w') as f:
    json.dump(d, f, indent=2, sort_keys=True, cls=MyEncoder)
'''
