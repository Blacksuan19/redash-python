from .base import BaseObject, BaseService
from .mixins import CommonMixin, NameMixin


class DataSourcesService(CommonMixin, NameMixin, BaseObject):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        CommonMixin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/data_sources"
