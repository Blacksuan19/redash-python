from .base import BaseService
from .mixins import CommonMixin, NameMixin, PrintMixin


class AlertsService(CommonMixin, NameMixin, PrintMixin):
    def __init__(self, base: BaseService) -> None:

        # init mixins
        CommonMixin.__init__(self, base)

        self.endpoint = "/api/alerts"
