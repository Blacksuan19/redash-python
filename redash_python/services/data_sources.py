from .base import BaseService
from .mixins import CommonMixin, NameMixin, PrintMixin


class DataSourcesService(CommonMixin, NameMixin, PrintMixin):
    def __init__(self, base: BaseService) -> None:
        super().__init__(base=base)
        self.endpoint = "/api/data_sources"
