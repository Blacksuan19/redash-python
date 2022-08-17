from types import SimpleNamespace
from typing import List, Optional, final

from .base import BaseService


class PrintMixin:
    @final
    def __repr__(self) -> str:
        object_methods = [
            method_name
            for method_name in dir(self)
            if callable(getattr(self, method_name)) and not method_name.startswith("_")
        ]
        object_attributes = [
            attribute_name
            for attribute_name in dir(self)
            if not callable(getattr(self, attribute_name))
            and not attribute_name.startswith("_")
        ]
        return f"{self.__class__.__name__}(attributes: {object_attributes}, methods: {object_methods})"

    @final
    def __str__(self) -> str:
        return self.__repr__()


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

    def update(self, id: int, data: SimpleNamespace) -> SimpleNamespace:
        """Update by ID"""
        return self.__base.post(f"{self.endpoint}/{id}", data)

    def create(self, data: SimpleNamespace) -> SimpleNamespace:
        """Create a new object with data"""
        return self.__base.post(self.endpoint, data)

    def delete(self, id: int) -> SimpleNamespace:
        """Delete by ID"""
        return self.__base.delete(f"{self.endpoint}/{id}")


class NameMixin:
    def get_by_name(self, name: str) -> SimpleNamespace:
        """Get by name or slug"""
        return self.get(self.get_id(name))

    def get_id(self, name_or_slug: str) -> Optional[int]:
        """Get the ID for an object by name or slug, returns None if not found"""
        all_obj = self.get_all()
        if not all_obj.results:
            matches = list(filter(lambda d: d.slug == name_or_slug, all_obj))
        else:
            matches = list(filter(lambda d: d.name == name_or_slug, all_obj.results))

        if not matches:
            return None
        return matches.pop().id


class TagsMixin:
    """Mixin with methods for services with tags"""

    def get_by_tags(self, tags: List[str], without: bool = False) -> SimpleNamespace:
        """Get all objects with `tags` or all objects without any of `tags`"""
        all_objects = self.get_all()

        if without:
            return SimpleNamespace(
                results=[
                    obj
                    for obj in all_objects.results
                    if not any(tag in obj.tags for tag in tags)
                ]
            )

        return SimpleNamespace(
            results=[
                obj
                for obj in all_objects.results
                if any(tag in obj.tags for tag in tags)
            ]
        )


class PublishMxin:
    """Mixin for publishable objects"""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def publish(self, dashboard_id: int) -> SimpleNamespace:
        """Publish an object"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"is_draft": False})

    def unpublish(self, dashboard_id: int) -> SimpleNamespace:
        """Unpublish an object"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"is_draft": True})


class FavoriteMixin:
    """Mixin for favoriteable objects"""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def favorite(self, id: int) -> SimpleNamespace:
        """Favorite an object"""
        return self.__base.post(f"{self.endpoint}/{id}/favorite", {})

    def unfavorite(self, id: int) -> SimpleNamespace:
        """Unfavorite an object"""
        return self.__base.delete(f"{self.endpoint}/{id}/favorite")
