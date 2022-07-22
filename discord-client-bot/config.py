from functools import lru_cache
from typing import TypeVar

from pydantic import BaseSettings, Field

T = TypeVar("T", str, int)


def get_env(name: str, required: bool = False, default: T = None) -> T:
    if required and not default:
        default = ...  # type: ignore
    return Field(default, env=name)


class Settings(BaseSettings):
    API_TOKEN: str = get_env("API_TOKEN", required=True)
    LAB_GRADER_HOST: str = get_env("LAB_GRADER_HOST", default='http://lab-grader:8000')


@lru_cache
def get_settings() -> Settings:
    return Settings()
