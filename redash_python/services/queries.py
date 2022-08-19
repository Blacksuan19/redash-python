from typing import Dict, List

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

    def refresh(self, query_id: int) -> Dict:
        """Refresh a query"""
        return self.__base.post(f"{self.endpoint}/{query_id}/results", dict(max_age=0))

    def fork(self, query_id: int) -> Dict:
        """Fork a query"""
        return self.__base.post(f"{self.endpoint}/{query_id}/fork", {"id": query_id})

    def duplicate_query_table(
        self,
        *,
        query: Dict,
        table_map: Dict[str, str],
        tags: List[str],
        publish: bool = True,
    ) -> Dict:
        """
        Duplicate query with source tables replaced according to table_map.

        Args:
            query(Dict): query data object
            table_map(Dict): mapping of old to new tables
            tags(List): tags to add to new query
            publish(bool): whether to publish the new query

        Returns:
            Dict: new query data object

        Example:
            >>> query = queries.get(query_id)
            >>> table_map = {
            >>>     "old_table": "new_table",
            >>>     "old_table2": "new_table2",
            >>> }
            >>> tags = ["tag1", "tag2"]
            >>> new_query = queries.duplicate_query_table(
            >>>     query=query, table_map=table_map, tags=tags, publish=True
            >>> )
        """

        new_id = self.fork(query.get("id")).get("id")

        # update query
        new_query = self.get(new_id)
        new_query["name"] = query.get("name")
        new_query["tags"] = tags

        for old, new in list(table_map.items()):
            new_query["query"] = new_query.get("query").replace(old, new)
        self.update(new_id, new_query)

        # run updated query to update results
        self.refresh(new_query.get("id"))

        # finally publish the new query
        if publish:
            self.publish(new_id)

        return self.get(new_id)
