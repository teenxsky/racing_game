import json
import logging


logging.basicConfig(filename='errors.log', level=logging.ERROR, encoding='utf-8',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class FileObject:
    __LOGGER = logging.getLogger(__name__)

    def __init__(self, path, path_default=None):
        self.path = path
        self.path_default = path_default
        self.load(self.path)

    def load(self, path):
        try:
            file_object = json.load(open(path, 'r'))
            for key in file_object:
                setattr(self, key, file_object[key])
        except Exception as exc:
            self.__LOGGER.error(exc, exc_info=True)

    def update(self):
        file_object = dict()
        for key in vars(self):
            if key not in {"path", "path_default"}:
                file_object[key] = getattr(self, key)
        json.dump(file_object, open(self.path, 'w'), indent=2)

    def set_default(self):
        if self.path_default:
            self.load(self.path_default)
            with open(self.path, 'w') as f:
                json.dump(vars(self), f, indent=2)


config = FileObject("config.json")
settings = FileObject("Resources/settings.json", "Resources/default.json")
