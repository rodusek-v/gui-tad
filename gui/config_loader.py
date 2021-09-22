import json
import os.path
from typing import List


class Config(object):

    def __init__(self) -> None:
        super().__init__()
        self.__config = {
            "default": {
                "last-loaded": None,
                "recent": []
            }
        }
        self.__conf_path = "config.json"
        self.load_config()
        self.__check_file_existance()

    def load_config(self) -> None:
        try:
            with open(self.__conf_path, "r", encoding="utf8") as file:
                self.__config = json.load(file)
        except IOError:
            self.save_config()

    def save_config(self) -> None:
        with open(self.__conf_path, "w", encoding="utf8") as file:
            json.dump(self.__config, file, indent=4)

    def __check_file_existance(self) -> None:
        last_loaded = self.__config['default']['last-loaded']
        if last_loaded is not None:
            if not os.path.exists(last_loaded):
                self.__config['default']['recent'].remove(last_loaded)
                self.__config['default']['last-loaded'] = None
                self.save_config()

        new_recent = []
        for recent in self.__config['default']['recent']:
            if os.path.exists(recent):
                new_recent.append(recent)

        self.__config['default']['recent'] = new_recent

    def get_last_loaded(self) -> str:
        return self.__config['default']['last-loaded']

    def set_last_loaded(self, value: str) -> None:
        self.__config['default']['last-loaded'] = value
        recent = self.__config['default']['recent']
        if value not in recent and value is not None:
            recent.append(value)
        self.save_config()

    def get_recent(self) -> List[str]:
        return self.__config['default']['recent']

    def remove_recent(self, value: str) -> None:
        self.__config['default']['recent'].remove(value)