from functools import lru_cache
from typing import TypeVar

from pydantic import BaseSettings, Field

T = TypeVar("T", str, int)


def get_env(name: str, required: bool = False, default: T = None) -> T:
    if required and not default:
        default = ...  # type: ignore
    return Field(default, env=name)


class GoogleSettings(BaseSettings):
    GOOGLE_KEY_FILE_PATH: str = get_env("GOOGLE_KEY_FILE_PATH", default='google_key.json')


class GithubSettings(BaseSettings):
    GITHUB_OAUTH_TOKEN: str = get_env("GITHUB_OAUTH_TOKEN", required=True)


class Settings(GoogleSettings, GithubSettings):
    COURSES_CONFIG_DIRECTORY: str = get_env("COURSES_CONFIG_DIRECTORY", default='courses')
    RATE_LIMIT = "1/5min"


@lru_cache
def get_settings() -> Settings:
    return Settings()
