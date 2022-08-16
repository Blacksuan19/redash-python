from types import SimpleNamespace
from typing import Dict, Optional

from .base import BaseObject, BaseService
from .mixins import CommonMixin, PublishMxin


class DataSourcesService(CommonMixin, PublishMxin, BaseObject):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        CommonMixin.__init__(self, base)
        PublishMxin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/data_sources"

    def get_id(self, name: str) -> Optional[int]:
        """Get the ID for a query by slug, or None if not found"""
        matches = list(filter(lambda d: d.name == name, self.get_all()))
        if not matches:
            return None
        return matches.pop().id

    def get_by_name(self, name: str) -> SimpleNamespace:
        """Get a query by name"""
        return self.get(self.get_id(name))

    def create(self, query_data: Dict) -> SimpleNamespace:
        """Create a new query"""
        return self.__base.post(self.endpoint, query_data)
