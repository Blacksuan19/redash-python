from types import SimpleNamespace
from typing import Optional

from .base import BaseObject, BaseService
from .mixins import CommonMixin, PublishMxin


class DashboardsService(CommonMixin, PublishMxin, BaseObject):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        CommonMixin.__init__(self, base)
        PublishMxin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/dashboards"

    def get_slug(self, dashboard_id: int) -> Optional[str]:
        """Get the slug for a dashboard by ID"""
        return self.get(dashboard_id).slug

    def get_id(self, slug: str) -> Optional[int]:
        """Get the ID for a dashboard by slug, or None if not found"""
        matches = list(filter(lambda d: d.slug == slug, self.get_all().results))
        if not matches:
            return None
        return matches.pop().id

    def get_by_slug(self, slug: str) -> SimpleNamespace:
        """Get a dashboard by slug"""
        return self.get(self.get_id(slug))

    def create(self, name: str) -> SimpleNamespace:
        """Create a new dashboard"""
        return self.__base.post(self.endpoint, {"name": name})

    def refresh(self, dashboard_id: int) -> None:
        """Refresh a dashboard"""
        widgets = self.get(dashboard_id).widgets

        for widget in widgets:
            if not hasattr(widget, "visualization"):
                continue
            query = widget.visualization.query
            self.__base.post(f"/api/queries/{query.id}/results", {"max_age": 0})
