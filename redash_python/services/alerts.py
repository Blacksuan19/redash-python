from .base import BaseService
from .mixins import CommonMixin, NameMixin, PrintMixin


class AlertsService(CommonMixin, NameMixin, PrintMixin):
    def __init__(self, base: BaseService) -> None:
        CommonMixin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/alerts"
