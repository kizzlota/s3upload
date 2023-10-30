from pathlib import Path

import yaml
from pydantic import BaseModel


class AWSConfig(BaseModel, frozen=True):
    key: str
    secret: str
    region: str


class Config(BaseModel, frozen=True):
    aws: AWSConfig


def load_config_from_yaml(path: str | Path) -> Config:
    with open(path) as file:
        content = yaml.safe_load(file)
    return Config.model_validate(content)
