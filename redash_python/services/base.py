from types import SimpleNamespace
from typing import Dict, Optional

import requests
from redash_python.utils.json_encoder import ModelEncoder


class BaseObject:
    def __repr__(self) -> str:
        object_methods = [
            method_name
            for method_name in dir(self)
            if callable(getattr(self, method_name)) and not method_name.startswith("_")
        ]
        return f"{self.__class__.__name__}(methods: {object_methods})"

    def __str__(self) -> str:
        return self.__repr__()


class BaseService(BaseObject):
    """Singleton Base Service class"""

    def __init__(self, base_url: str, api_key: str) -> None:
        self.base_url = base_url

        # configure session
        self.__session = requests.Session()
        self.__session.headers.update({"Authorization": f"Key {api_key}"})
        self.__encoder = ModelEncoder()

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        **kwargs,
    ) -> SimpleNamespace:
        """Perform a request to the endpoint with the given data"""
        url = self.base_url + endpoint

        if not isinstance(data, dict):
            data = self.__encoder.encode(data)
        try:
            response = self.__session.request(
                method, url, json=data if data else None, **kwargs
            )
        except requests.exceptions.RequestException as e:
            raise e
        return response.json(object_hook=lambda d: SimpleNamespace(**d))

    def post(self, endpoint: str, data: Dict, **kwargs) -> SimpleNamespace:
        """Perform a POST request to the endpoint with the given data"""
        return self._request("POST", endpoint, data, **kwargs)

    def get(
        self, endpoint: str, data: Optional[Dict] = None, **kwargs
    ) -> SimpleNamespace:
        """Perform a GET request to the endpoint"""
        return self._request("GET", endpoint, data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> SimpleNamespace:
        """Perform a DELETE request to the endpoint"""
        return self._request("DELETE", endpoint, **kwargs)
