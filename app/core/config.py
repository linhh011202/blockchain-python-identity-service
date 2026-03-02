import os
from pathlib import Path
import yaml
from pydantic import BaseModel, Field


class JwtConfig(BaseModel):
    algorithm: str = "HS256"
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 14
    secret: str = Field(min_length=1)


class SecurityConfig(BaseModel):
    jwt: JwtConfig


class DatabaseConfig(BaseModel):
    url: str = Field(min_length=1)


class RBACConfig(BaseModel):
    default_role: str = "user"


class AppConfig(BaseModel):
    name: str = "identity-service"
    env: str = "dev"


class Settings(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    security: SecurityConfig
    rbac: RBACConfig

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        data = dict(obj or {})
        database = dict(data.get("database") or {})
        url = database.get("url")
        if isinstance(url, str) and url.startswith("postgresql://"):
            database["url"] = url.replace("postgresql://", "postgresql+psycopg://", 1)
            data["database"] = database
        return super().model_validate(data, *args, **kwargs)


def _load_yaml(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p.resolve()}")
    with p.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def get_settings() -> Settings:
    config_path = os.getenv("APP_CONFIG", "config/config.dev.yaml")
    cfg = _load_yaml(config_path)

    secrets_path = os.getenv("APP_SECRETS", "")
    if secrets_path:
        cfg = _deep_merge(cfg, _load_yaml(secrets_path))

    return Settings.model_validate(cfg)


settings = get_settings()
