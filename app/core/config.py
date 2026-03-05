from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def load_yaml_file(path: Path) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    if not isinstance(data, dict):
        raise ValueError("config.yaml must be a mapping (key: value).")
    
    return data


def get_config_path() -> Path:
    """Get the config file path from environment or default."""
    config_file = os.getenv("CONFIG_FILE")
    if config_file:
        return Path(config_file)
    
    # Default: look for config.yaml in project root
    return Path.cwd() / "config.yaml"


class Configs(BaseSettings):
    """Application configuration loaded from config.yaml."""
    
    # Project name
    PROJECT_NAME: str

    # API
    API: str = "/api"
    API_V1_STR: str = "/api/v1"

    # Database config
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int

    # Other config
    TZ: str = "Asia/Singapore"

    # BACKEND_CORS_ORIGINS is a list in YAML
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        """Generate database URL from configuration."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(case_sensitive=True)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """
        Define configuration sources priority.
        Priority: init_settings > env_settings > yaml_settings
        """
        def yaml_settings_source() -> Dict[str, Any]:
            config_path = get_config_path()
            return load_yaml_file(config_path)

        return (
            init_settings,
            env_settings,
            yaml_settings_source,
        )


# Load configuration instance
configs = Configs()