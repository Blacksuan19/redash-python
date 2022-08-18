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

    def share(self, dashboard_id: int) -> str:
        """get public url for dashboard"""
        response = self.__base.post(f"{self.endpoint}/{dashboard_id}/share", {})
        return response.public_url

    def duplicate(
        self, dashboard_id: int, new_name: Optional[str] = None
    ) -> SimpleNamespace:
        """Duplicate a dashboard and all its widgets with `new_name`"""
        current = self.get(dashboard_id)

        if new_name is None:
            new_name = f"Copy of: {current.name}"

        new_dash = self.create(new_name)

        if current.tags:
            self.update(new_dash.id, SimpleNamespace(tags=current.tags))

        for widget in current.widgets:
            visualization_id = None
            if hasattr(widget, "visualization"):
                visualization_id = widget.visualization.id

            self.create_widget(
                dashboard_id=new_dash.id,
                visualization_id=visualization_id,
                options=widget.options,
                text=widget.text,
            )

    def create_widget(
        self,
        *,
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
