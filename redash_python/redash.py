from typing import List

import requests

from redash_python.services import (
    AlertsService,
    BaseService,
    DashboardsService,
    DataSourcesService,
    DestService,
    GroupsService,
    QSnipsService,
    QueriesService,
    UsersService,
    WidgetsService,
)

version = "0.3.17"


class Redash:
    """
    Top Class of The Redash API Client hierarchy.

    Args:
        base_url (str): The base URL of the Redash instance.
        api_key (str): The API key for the Redash instance.

    Usage:
        >>> from redash_python import Redash
        >>> rd = Redash("https://redash.example.com", "API_KEY")
        >>> rd.dashboards.get_all()
    """

    def __init__(self, base_url: str, api_key: str) -> None:
        self.version = version

        self.__base = BaseService(base_url, api_key)

        # Initialize services
        self.dashboards = DashboardsService(self.__base)
        self.queries = QueriesService(self.__base)
        self.data_sources = DataSourcesService(self.__base)
        self.alerts = AlertsService(self.__base)
        self.destinations = DestService(self.__base)
        self.users = UsersService(self.__base)
        self.groups = GroupsService(self.__base)
        self.query_snippets = QSnipsService(self.__base)
        self.widgets = WidgetsService(self.__base)

        # keep track of services
        attr_dict = self.__dict__
        ignore_list = ["_Redash__base", "__base", "version"]
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

    def test_credentials(self):
        """Test whether current credentials are valid"""
        try:
            response = self.get("/api/session")
            return True
        except requests.exceptions.HTTPError:
            return False

    def __dir__(self) -> List[str]:
        return self.services + ["get", "post", "delete"]

    def __repr__(self) -> str:
        return f"Redash(base_url: {self.__base.base_url}, services: {self.services})"

    def __str__(self) -> str:
        return self.__repr__()
