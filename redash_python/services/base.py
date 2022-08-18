from types import SimpleNamespace
from typing import Optional, final

import requests

from ..utils.json_encoder import ModelEncoder


class BaseService:
    """Singleton Base Service class"""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url

        # configure session
        self.__session = requests.Session()
        self.__session.headers.update({"Authorization": f"Key {api_key}"})
        self.__encoder = ModelEncoder()

    @final
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[SimpleNamespace] = None,
        **kwargs,
    ) -> SimpleNamespace:
        """Perform a request to the endpoint with the given data"""
        url = self.base_url + endpoint

        if not isinstance(data, dict):
            data = self.__encoder.encode(data)

        response = self.__session.request(
            method, url, json=data if data else None, **kwargs
        )

        response.raise_for_status()
        return response.json(object_hook=lambda d: SimpleNamespace(**d))

    @final
    def post(self, endpoint: str, data: SimpleNamespace, **kwargs) -> SimpleNamespace:
        """Perform a POST request to the endpoint with the given data"""
        return self._request("POST", endpoint, data, **kwargs)

    @final
    def get(
        self, endpoint: str, data: Optional[SimpleNamespace] = None, **kwargs
    ) -> SimpleNamespace:
        """Perform a GET request to the endpoint"""
        return self._request("GET", endpoint, data, **kwargs)

    @final
    def delete(self, endpoint: str, **kwargs) -> SimpleNamespace:
        """Perform a DELETE request to the endpoint"""
        return self._request("DELETE", endpoint, **kwargs)
