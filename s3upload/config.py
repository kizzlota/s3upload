from dataclasses import dataclass


@dataclass(frozen=True)
class Credentials:
    key: str
    secret: str
    region: str
