"""Unit tests for config loading"""

import os
import tempfile
import shutil
import pytest
from ruamel.yaml import YAML

from hello_cdk.utils.config import load_config


@pytest.fixture
def _temp_config_dir():
    """Create a temporary directory for config files"""

    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def write_yaml_config(temp_dir, env_name, data):
    """Helper to write a YAML config file"""

    config_dir = os.path.join(temp_dir, "config")
    os.makedirs(config_dir, exist_ok=True)
    file_path = os.path.join(config_dir, f"{env_name}.yml")
    with open(file_path, "w", encoding="utf-8") as f:
        YAML().dump(data, f)
    return file_path


def test_load_config_reads_yaml(monkeypatch, _temp_config_dir):
    """Test loading successfuly configuration from a YAML file"""

    # Prepare YAML config
    config_data = {"key": "value", "another_key": 123}
    env_name = "testenv"
    write_yaml_config(_temp_config_dir, env_name, config_data)

    # Change working directory to temp_config_dir
    monkeypatch.chdir(_temp_config_dir)
    result = load_config(env_name)
    assert result == config_data


def test_load_config_file_not_found(monkeypatch, _temp_config_dir):
    """Test loading configuration when file does not exist"""

    env_name = "missingenv"

    monkeypatch.chdir(_temp_config_dir)
    with pytest.raises(FileNotFoundError):
        load_config(env_name)
