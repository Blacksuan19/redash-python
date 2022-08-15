from typing import List

from redash_python.services.base import BaseService
from redash_python.services.dashboards import DashboardsService


class Redash:
    """
    Top Class of The Redash API Client hierarchy.

    Args:
        base_url (str): The base URL of the Redash instance.
        api_key (str): The API key for the Redash instance.

    Usage:
        >>> from redash_python import Redash
        >>> redash = Redash("https://redash.example.com", "API_KEY")
        >>> redash.dashboards.get_all()
    """

    def __init__(self, base_url: str, api_key: str) -> None:

        self.__base = BaseService(base_url, api_key)

        # Initialize services
        self.dashboards = DashboardsService(self.__base)

        # keep track of services
        attr_dict = self.__dict__
        ignore_list = ["BaseService"]
        self.services = [
            attr_dict[k].__class__.__name__
            for k in self.__dict__
            if k not in ignore_list
        ]
        self.services.sort()

        # make __base methods available
        self.get = self.__base.get
        self.post = self.__base.post
        self.delete = self.__base.delete

    def __dir__(self) -> List[str]:
        return self.services + ["get", "post", "put", "delete"]

    def __repr__(self) -> str:
        return f"Redash(base_url: {self.__base.base_url}, services: {self.services})"

    def __str__(self) -> str:
        return self.__repr__()