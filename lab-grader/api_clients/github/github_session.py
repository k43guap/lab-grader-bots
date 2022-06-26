from types import TracebackType
from typing import Optional, Type

from aiohttp import ClientSession
from gidgethub.aiohttp import GitHubAPI


class GithubSession:
    def __init__(self, token: str):
        self.__token = token
        self.__session: Optional[ClientSession] = None

    async def __aenter__(self) -> GitHubAPI:
        self.__session = ClientSession()
        return GitHubAPI(self.__session, "", oauth_token=self.__token)

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> None:
        if self.__session:
            await self.__session.close()
