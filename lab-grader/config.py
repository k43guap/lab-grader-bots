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
    STUDENT_FULLNAME_COLUMN: str = 'Ф.И.О.'
    GITHUB_COLUMN: str = 'GitHub'


class GithubSettings(BaseSettings):
    GITHUB_OAUTH_TOKEN: str = get_env("GITHUB_OAUTH_TOKEN", required=True)


class GithubBuildLogSettings(BaseSettings):
    PREFIX_LOG_TASK_ID: str = "TASKID is"
    PREFIX_LOG_SCORE: str = "Score is"
    PREFIX_LOG_POINTS: str = "Points"
    PREFIX_LOG_REDUCTION: str = "Grading reduced by"


class Settings(GoogleSettings, GithubSettings, GithubBuildLogSettings):
    COURSES_CONFIG_DIRECTORY: str = get_env("COURSES_CONFIG_DIRECTORY", default='courses')
    DEFAULT_CI_JOBS: list = ["Autograding", "test", "build"]
    WRONG_TASK_ID_MARK: str = "?! Wrong TASKID!"


@lru_cache
def get_settings() -> Settings:
    return Settings()
