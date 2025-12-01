from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field


class ProbeConfig(BaseModel):
    id: str
    name: str
    channel: int
    type: str = "thermocouple"


class MQTTConfig(BaseModel):
    host: str
    port: int = 1883
    topic_prefix: str


class HomeAssistantConfig(BaseModel):
    enabled: bool = False
    mqtt: Optional[MQTTConfig] = None


class CSVStorageConfig(BaseModel):
    path: str


class StorageConfig(BaseModel):
    backend: str = Field(default="csv", pattern="^(csv|sqlite)$")
    csv: Optional[CSVStorageConfig] = None
    # sqlite config later


class AppConfig(BaseModel):
    poll_interval_seconds: int = 5
    log_level: str = "INFO"


class NotificationsConfig(BaseModel):
    enabled: bool = False
    # add provider-specific fields later


class Config(BaseModel):
    app: AppConfig
    probes: List[ProbeConfig]
    storage: StorageConfig
    home_assistant: HomeAssistantConfig = HomeAssistantConfig()
    notifications: NotificationsConfig = NotificationsConfig()


def load_config(path: str | Path) -> Config:
    path = Path(path)
    with path.open("r") as f:
        data = yaml.safe_load(f)
    return Config(**data)
