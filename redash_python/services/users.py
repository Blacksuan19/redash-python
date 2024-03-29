from typing import Dict, List

from .base import BaseService
from .mixins import CommonMixin, NameMixin, PaginationMixin, PrintMixin


class UsersService(CommonMixin, NameMixin, PrintMixin, PaginationMixin):
    def __init__(self, base: BaseService) -> None:
        CommonMixin.__init__(self, base)
        PaginationMixin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/users"

    def get_all(self) -> List[Dict]:
        return self.paginate()

    def disable(self, user_id: int) -> None:
        """
        disable user
        """
        self.__base.post(f"/api/users/{user_id}/disable")

    def add_group(self, user_id: int, group_id: int) -> None:
        """
        add user to group
        """
        self.__base.post(f"/api/groups/{group_id}/members", {"user_id": user_id})

    def remove_group(self, user_id: int, group_id: int) -> None:
        """
        remove user from group
        """
        self.__base.delete(f"/api/groups/{group_id}/members/{user_id}")
