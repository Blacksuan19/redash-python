from typing import Dict, Optional, final

import requests


class BaseService:
    """Singleton Base Service class"""

    def __init__(self, base_url: str, api_key: str, **kwargs) -> None:
        self.base_url = base_url
        super().__init__(**kwargs)

        # configure session
        self.__session = requests.Session()
        self.__session.headers.update({"Authorization": f"Key {api_key}"})
        self.__session.headers.update({"Content-Type": "application/json"})
        self.__session.headers.update({"Accept": "application/json"})

    @final
    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        **kwargs,
    ) -> requests.Response:
        """Perform a request to the endpoint with the given data"""
        url = self.base_url + endpoint
        response = self.__session.request(
            method,
            url,
            json=data if data else None,
            **kwargs,
        )
        response.raise_for_status()
        return response

    @final
    def post(self, endpoint: str, data: Dict, **kwargs) -> Dict:
        """Perform a POST request to the endpoint with the given data"""
        return self._request("POST", endpoint, data, **kwargs).json()

    @final
    def get(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> Dict:
        """Perform a GET request to the endpoint"""
        return self._request("GET", endpoint, data, **kwargs).json()

    @final
    def delete(self, endpoint: str, **kwargs) -> None:
        """Perform a DELETE request to the endpoint"""
        return self._request("DELETE", endpoint, **kwargs)
