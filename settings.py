# settings.py
import pathlib

import yaml

BASE_DIR = pathlib.Path(__file__).parent

config_path = BASE_DIR / 'config' / 'config.yaml'


def get_config(path):
    with open(path, encoding="utf8") as f:
        result = yaml.load(f)
    return result


config = get_config(config_path)
print("config: {}".format(config))
