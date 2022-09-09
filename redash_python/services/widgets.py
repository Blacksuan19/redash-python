from typing import Dict, NoReturn, Optional

from .base import BaseService
from .mixins import CommonMixin, PrintMixin


class WidgetsService(CommonMixin, PrintMixin):
    """
    Service for managing widgets

    - only supports create, delete and update (DELETE, POST)
    - does not support get_all or get (GET)
    """

    def __init__(self, base: BaseService) -> None:
        CommonMixin.__init__(self, base)

        self.__base = base
        self.endpoint = "/api/widgets"

    def get_all(self) -> NoReturn:
        raise ValueError(f"{self.endpoint} does not support GET")

    def get(self, id: int) -> NoReturn:
        raise ValueError(f"{self.endpoint} does not support GET")

    def create(
        self,
        *,
        dashboard_id: int,
        visualization_id: Optional[int],
        options: Dict,
        text: str = "",
    ) -> Dict:
        """
        create new widget in given dashboard

        Args:
            dashboard_id: id of dashboard to create widget in
            visualization_id: id of visualization to use for widget (pass None for text widget)
            options: options to use for widget
            text: text to use for text widget
        """
        data = dict(
            dashboard_id=dashboard_id,
            text=text,
            options=options,
            visualization_id=visualization_id,
            width=1,
        )
        return self.__base.post("/api/widgets", data)
