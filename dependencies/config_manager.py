__all__ = ['video_source', 'update_video_source', 'rdl_config', 'update_block', 'detectors_config', 'editor_config']

import json
import sys

config_path = sys.path[0] + "/config.json"

with open(config_path, 'r') as file:
    cfg = json.load(file)
    print("Config file read successfully")


async def video_source():
    return cfg["video_source"]


async def update_video_source():
    return _update_block


async def rdl_config():
    return cfg["rules"]


async def update_block():
    return _update_block


async def detectors_config():
    return cfg["detectors"]


async def editor_config():
    return cfg["editor"]


def _update_block(name: str, contents: dict | str):
    with open(config_path, 'r+') as f:
        config = json.load(f)
        config[name] = contents
        f.seek(0)
        f.write(json.dumps(config))
        f.truncate()
