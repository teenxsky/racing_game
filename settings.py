import json


class Settings:
    def __init__(self):
        try:
            settings_file = "config.json"
            self.user_settings = json.load(open(settings_file))

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

    def set_default(self):
        with open('config.json', 'w') as f:
            with open('default.json', 'r') as data:
                data_default = json.load(data)
                json.dump(data_default, f, indent=2)


settings = Settings()

'''
d = {'name': 'Roman', 'coins': 100, 'car': 'BMW', 'score': 1000}
with open('config.json', 'w') as f:
    json.dump(d, f, indent=2, sort_keys=True, cls=MyEncoder)
'''
