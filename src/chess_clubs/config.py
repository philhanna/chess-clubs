from dataclasses import dataclass
import yaml
import os

import platform
from pathlib import Path

system = platform.system()
if system == "Windows":
    base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
else:
    base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
CONFIG_PATH = base / "chess-clubs" / "config.yaml"


@dataclass
class NetConfig:
    MAX_ATTEMPTS: int
    TIMEOUT: int
    RETRY_DELAY: int


@dataclass
class AppConfig:
    MIN_GAMES: int


@dataclass
class Config:
    net: NetConfig
    app: AppConfig


def load_config(path=CONFIG_PATH) -> Config:
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    return Config(
        net=NetConfig(**data['net']),
        app=AppConfig(**data['app'])
    )
