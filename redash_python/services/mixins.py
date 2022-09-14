from typing import Dict, List, NoReturn, Optional, final

from .base import BaseService


class PrintMixin:
    """Mixin class for printing data"""

    @final
    def __repr__(self) -> str:
        object_methods = [
            method_name
            for method_name in dir(self)
            if callable(getattr(self, method_name))
            and not method_name.startswith("_")
            and getattr(self, method_name).__annotations__.get("return") is not NoReturn
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

    def get(self, id: int) -> Dict:
        """Fetch one by ID"""
        return self.__base.get(f"{self.endpoint}/{id}")

    def get_all(self) -> List[Dict]:
        """fetch all objects."""
        return self.__base.get(self.endpoint)

    def update(self, id: int, data: Dict) -> Dict:
        """Update by ID"""
        return self.__base.post(f"{self.endpoint}/{id}", data)

    def create(self, data: Dict) -> Dict:
        """Create a new object with data"""
        return self.__base.post(self.endpoint, data)

    def delete(self, id: int) -> None:
        """Delete by ID"""
        return self.__base.delete(f"{self.endpoint}/{id}")


class NameMixin:
    """Mixin for nameable services (by name or slug)."""

    def exists(self, name_or_slug: str) -> bool:
        """Check if an object with given `name_or_slug` exists"""
        return self.get_id(name_or_slug) is not None

    def get_by_name(self, name_or_slug: str) -> Optional[Dict]:
        """Get by name or slug"""
        obj_id = self.get_id(name_or_slug)
        if obj_id is None:
            return None

        return self.get(obj_id)

    def get_id(self, name_or_slug: str) -> Optional[int]:
        """Get the ID for an object by name or slug, returns None if not found"""
        for obj in self.get_all():
            if obj.get("name") == name_or_slug or obj.get("slug") == name_or_slug:
                return obj.get("id")

        return None


class TagsMixin:
    """Mixin for taggable services"""

    def get_by_tags(
        self, tags: List[str], without: bool = False, match_all: bool = True
    ) -> List[Dict]:
        """Get all objects with all or any of `tags` or all objects without any of `tags`"""
        all_objects = self.get_all()

        if without:
            return list(
                filter(
                    lambda obj: not self.__has_tags(obj, tags, match_all), all_objects
                )
            )

        return list(
            filter(lambda obj: self.__has_tags(obj, tags, match_all), all_objects)
        )

    def __has_tags(self, obj: Dict, tags: List[str], match_all: bool = True) -> bool:
        """Check if an object has all or any of `tags`"""
        if match_all:
            return all(tag in obj.get("tags", []) for tag in tags)

        return any(tag in obj.get("tags", []) for tag in tags)


class PublishMixin:
    """Mixin for publishable services"""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def publish(self, dashboard_id: int) -> Dict:
        """Publish an object"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"is_draft": False})

    def unpublish(self, dashboard_id: int) -> Dict:
        """Unpublish an object"""
        return self.__base.post(f"{self.endpoint}/{dashboard_id}", {"is_draft": True})


class FavoriteMixin:
    """Mixin for favoriteable services"""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def favorited(self) -> List[Dict]:
        """Get all favorited objects"""
        return list(filter(lambda x: x["is_favorite"], self.get_all()))

    def favorite(self, id: int) -> Dict:
        """Favorite an object"""
        return self.__base.post(f"{self.endpoint}/{id}/favorite", {})

    def unfavorite(self, id: int) -> Dict:
        """Unfavorite an object"""
        return self.__base.delete(f"{self.endpoint}/{id}/favorite")


class PaginationMixin:
    """Mixin for paginated services"""

    def __init__(self, base: BaseService) -> None:
        self.__base = base

    def paginate(self, page: int = 1, page_size: int = 100, **kwargs) -> List[Dict]:
        """Load all items of a paginated resource"""
        items = []
        while True:
            page_items = self.fetch_page(page, page_size, **kwargs)
            items.extend(page_items)
            if len(page_items) < page_size:
                break
            page += 1

        return items

    def fetch_page(self, page: int = 1, page_size: int = 100, **kwargs) -> List[Dict]:
        """Load a page of a paginated resource"""
        response = self.__base.get(
            self.endpoint, {"page": page, "page_size": page_size}, **kwargs
        )
        return response.get("results")
