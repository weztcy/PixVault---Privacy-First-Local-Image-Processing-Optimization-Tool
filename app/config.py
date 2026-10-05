import json
from pathlib import Path


CONFIG_FILE = Path("config.json")


class AppConfig:
    def __init__(self):
        self.data = {
            "theme": "dark",
            "default_quality": 85,
            "default_output": "source"
        }

        self.load()


    def load(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                self.data.update(json.load(file))


    def get(self, key, default=None):
        return self.data.get(key, default)