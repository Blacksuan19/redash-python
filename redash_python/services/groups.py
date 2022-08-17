from .base import BaseObject, BaseService
from .mixins import CommonMixin, NameMixin


class GroupsService(CommonMixin, NameMixin, BaseObject):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        CommonMixin.__init__(self, base)

        self.endpoint = "/api/groups"
