"""Configuration file loader"""

import os
from ruamel.yaml import YAML

def load_config(environment: str) -> dict:
    """
    Import configuration settings from YAML config file
    :return: dict with configuration items
    """
    with open(os.path.join("config", f"{environment}.yml"), 'r') as config_file:
        config = YAML().load(config_file.read())
    return config
