from types import SimpleNamespace
from typing import Dict, Optional

from .base import BaseObject, BaseService


class DashboardsService(BaseObject):
    def __init__(self, base: BaseService) -> None:
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

    def get(self, dashboard_id: int) -> SimpleNamespace:
        """Fetch a dashboard by ID or slug"""
        return self.__base.get(f"{self.endpoint}/{dashboard_id}")

    def get_by_slug(self, slug: str) -> SimpleNamespace:
        """Get a dashboard by slug"""
        return self.get(self.get_id(slug))

    def get_all(self) -> SimpleNamespace:
        """fetch all dashboards."""
        return self.__base.get(self.endpoint)

    def create(self, name: str) -> SimpleNamespace:
        """Create a new dashboard"""
        return self.__base.post(self.endpoint, {"name": name})

    def update(self, dashboard_id: int, properties: Dict) -> SimpleNamespace:
        """Update a dashboard by ID"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", properties)

    def archive(self, dashboard_id: int) -> SimpleNamespace:
        """Archive a dashboard"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"archived": True})

    def unarchive(self, dashboard_id: int) -> SimpleNamespace:
        """Unarchive a dashboard"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"archived": False})

    def publish(self, dashboard_id: int) -> SimpleNamespace:
        """Publish a dashboard"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"draft": False})

    def unpublish(self, dashboard_id: int) -> SimpleNamespace:
        """Unpublish a dashboard"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"draft": True})
