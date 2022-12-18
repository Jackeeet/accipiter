__all__ = ['rule_config', 'update_block']

import json
import sys

config_path = sys.path[0] + "/config.json"

with open(config_path, 'r') as file:
    cfg = json.load(file)
    print("Config file read successfully")


async def rule_config():
    return cfg["rules"]


async def update_block():
    return _update_block


def _update_block(name: str, contents: dict):
    with open(config_path, 'r+') as f:
        config = json.load(f)
        config[name] = contents
        f.seek(0)
        f.write(json.dumps(config))
        f.truncate()

# async def update_all(contents: dict):
#     with open(config_path, 'w') as f:
#         f.write(json.dumps(contents))
#         f.truncate()

# class ConfigReader:
#     def __init__(self):
#         self._config_path = sys.path[0] + "/config.json"
#         with open(self._config_path, 'r') as file:
#             self._config = json.load(file)
#             print("Config file read successfully")
#
#         self.rules = self._config["rules"]
