from abc import ABC
from typing import List

from superagi.tools.base_tool import BaseToolkit, BaseTool
from superagi.tools.github_info.github_info import GitHubInfoTool


class GitHubInfoToolkit(BaseToolkit, ABC):
    name: str = "GitHub Info Toolkit"
    description: str = "Toolkit containing tools for getting basic GitHub user and repository information"

    def get_tools(self) -> List[BaseTool]:
        return [GitHubInfoTool()]

    def get_env_keys(self) -> List:
        return []
