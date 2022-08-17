from types import SimpleNamespace
from typing import Optional

from .base import BaseService
from .mixins import (
    CommonMixin,
    FavoriteMixin,
    NameMixin,
    PrintMixin,
    PublishMxin,
    TagsMixin,
)


class DashboardsService(
    FavoriteMixin, CommonMixin, TagsMixin, PublishMxin, NameMixin, PrintMixin
):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        FavoriteMixin.__init__(self, base)
        CommonMixin.__init__(self, base)
        PublishMxin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/dashboards"

    def get_slug(self, dashboard_id: int) -> Optional[str]:
        """Get the slug for a dashboard by ID"""
        return self.get(dashboard_id).slug

    def refresh(self, dashboard_id: int) -> None:
        """Refresh a dashboard"""
        widgets = self.get(dashboard_id).widgets

        for widget in widgets:
            if not hasattr(widget, "visualization"):
                continue
            query = widget.visualization.query
            self.__base.post(f"/api/queries/{query.id}/results", {"max_age": 0})

    def create_widget(
        self,
        dashboard_id: int,
        visualization_id: Optional[int],
        options: SimpleNamespace,
        text: str = "",
    ) -> SimpleNamespace:
        """
        create new widget in given dashboard

        Args:
            dashboard_id: id of dashboard to create widget in
            visualization_id: id of visualization to use for widget (pass None for text widget)
            options: options to use for widget
            text: text to use for text widget
        """
        data = SimpleNamespace(
            dashboard_id=dashboard_id,
            text=text,
            options=options,
            visualization_id=visualization_id,
            width=1,
        )
        return self.__base.post("/api/widgets", data)
