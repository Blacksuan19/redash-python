from types import SimpleNamespace
from typing import Dict, Optional

from .base import BaseObject, BaseService
from .mixins import CommonMixin, PublishMxin


class QueriesService(CommonMixin, PublishMxin, BaseObject):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        CommonMixin.__init__(self, base)
        PublishMxin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/queries"

    def get_id(self, name: str) -> Optional[int]:
        """Get the ID for a query by slug, or None if not found"""
        matches = list(filter(lambda d: d.name == name, self.get_all().results))
        if not matches:
            return None
        return matches.pop().id

    def get_by_name(self, name: str) -> SimpleNamespace:
        """Get a query by name"""
        return self.get(self.get_id(name))

    def create(self, query_data: Dict) -> SimpleNamespace:
        """Create a new query"""
        return self.__base.post(self.endpoint, query_data)

    def refresh(self, query_id: int) -> SimpleNamespace:
        """Refresh a query"""
        return self.__base.post(f"{self.endpoint}/{query_id}/results", dict(max_age=0))
