from types import SimpleNamespace

from .base import BaseService
from .mixins import (
    CommonMixin,
    FavoriteMixin,
    NameMixin,
    PrintMixin,
    PublishMxin,
    TagsMixin,
)


class QueriesService(
    FavoriteMixin, CommonMixin, TagsMixin, PublishMxin, NameMixin, PrintMixin
):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        FavoriteMixin.__init__(self, base)
        CommonMixin.__init__(self, base)
        PublishMxin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/queries"

    def refresh(self, query_id: int) -> SimpleNamespace:
        """Refresh a query"""
        return self.__base.post(f"{self.endpoint}/{query_id}/results", dict(max_age=0))

    def fork(self, query_id: int) -> SimpleNamespace:
        """Fork a query"""
        return self.__base.post(f"{self.endpoint}/{query_id}/fork", {"id": "query_id"})
