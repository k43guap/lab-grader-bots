from typing import Optional

from gidgethub import BadRequest

from api_clients.github.github_session import GithubSession
from config import Settings


class GithubManager:
    def __init__(self, settings: Settings):
        self.__token = settings.GITHUB_OAUTH_TOKEN

    async def get_user(self, username: str) -> Optional[dict]:
        async with GithubSession(self.__token) as github:
            try:
                return await github.getitem(f"/users/{username}")
            except BadRequest:
                return None
