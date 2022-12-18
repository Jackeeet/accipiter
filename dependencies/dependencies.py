__all__ = ['rule_config']

import json
from pathlib import Path

config_path = Path(Path(__file__).parent.parent, "config.json")

with open(config_path, 'r') as file:
    cfg = json.load(file)
    print("Config file read successfully")


async def rule_config():
    return cfg["rules"]
