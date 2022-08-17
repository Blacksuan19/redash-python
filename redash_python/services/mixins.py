from types import SimpleNamespace
from typing import Dict

from redash_python.services import BaseService


class CommonMixin:
    """Mixin with common methods for services."""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def get(self, id: int) -> SimpleNamespace:
        """Fetch one by ID"""
        return self.__base.get(f"{self.endpoint}/{id}")

    def get_all(self) -> SimpleNamespace:
        """fetch all objects."""
        return self.__base.get(self.endpoint)

    def get_by_tag(self, tag: str, without: bool = False) -> SimpleNamespace:
        """Get all objects with a tag or all objects without a tag"""
        all_objects = self.get_all()

        if without:
            return SimpleNamespace(
                results=[o for o in all_objects.results if tag not in o.tags]
            )

        return SimpleNamespace(
            results=[o for o in all_objects.results if tag in o.tags]
        )

    def update(self, id: int, data: Dict) -> SimpleNamespace:
        """Update by ID"""
        return self.__base.post(f"{self.endpoint}/{id}", data)

    def delete(self, id: int) -> SimpleNamespace:
        """Delete by ID"""
        return self.__base.delete(f"{self.endpoint}/{id}")


class PublishMxin:
    """Mixin for publishable objects"""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def publish(self, dashboard_id: int) -> SimpleNamespace:
        """Publish a dashboard"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"is_draft": False})

    def unpublish(self, dashboard_id: int) -> SimpleNamespace:
        """Unpublish a dashboard"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"is_draft": True})
