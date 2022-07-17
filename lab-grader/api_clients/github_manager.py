from typing import Optional

from gidgethub import BadRequest, GitHubBroken

from api_clients.github.github_session import GithubSession
from apps.grader.models import GithubOrganization
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

    async def get_repositories(self, github_organization: GithubOrganization, username: str) -> list[str]:
        repositories = []
        async with GithubSession(self.__token) as github:
            async for repository in github.getiter(f"/orgs/{github_organization.organization}/repos"):
                if username in repository['name']:
                    repositories.append(repository['full_name'])
        return repositories

    async def get_default_branch_name(self, repository_name: str) -> str:
        async with GithubSession(self.__token) as github:
            repository_info = await github.getitem(f"/repos/{repository_name}")
        return repository_info['default_branch']

    async def get_builds(self, repository_name: str) -> list[dict]:
        default_branch = await self.get_default_branch_name(repository_name)
        async with GithubSession(self.__token) as github:
            builds = await github.getitem(f'/repos/{repository_name}/commits/{default_branch}/check-runs')
        return builds['check_runs']

    async def get_successful_build(
            self,
            repository_name: str,
            job_names: list[str],
            all_successful: bool = False,
    ) -> Optional[dict]:
        builds = await self.get_builds(repository_name)
        successful_builds = []
        for build in builds:
            for job_name in job_names:
                if all_successful and build['conclusion'] != 'success':
                    continue
                if job_name in build['name'] and build['conclusion'] == 'success':
                    successful_builds.append(build)
        last_build = max(successful_builds, key=lambda build: build['completed_at'], default=None)
        return last_build

    async def get_successful_build_log(self, repository_name: str, job_names: list[str]) -> Optional[str]:
        build = await self.get_successful_build(repository_name, job_names)
        if not build:
            return None
        async with GithubSession(self.__token) as github:
            try:
                log = await github.getitem(f"/repos/{repository_name}/actions/jobs/{build['id']}/logs")
            except GitHubBroken:
                return None  # fixme: error handling
        return log
