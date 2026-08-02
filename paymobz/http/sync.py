from __future__ import annotations

from typing import Any, Literal, Dict

import httpx

from .base import BaseHTTP
from ..exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    ValidationError,
)


class SyncHTTP(BaseHTTP):
    def __init__(
        self,
        base_url: str,
        timeout: float = 30.0,
        user_agent: str = "paymob-python-sdk",
        debug: bool = False,
    ) -> None:
        super().__init__(base_url, timeout, user_agent)

        self.debug = debug

        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        )

    def request(
        self,
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        endpoint: str,
        *,
        headers: Dict[str, str] | None = None,
        params: Dict[str, Any] | None = None,
        json: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        merged_headers = {**self.headers, **(headers or {})}

        try:
            response = self.client.request(
                method=method,
                url=endpoint.lstrip("/"),  
                headers=merged_headers,
                params=self.remove_none(params),
                json=self.remove_none(json),
            )

            return self._handle_response(response)

        except httpx.TimeoutException as exc:
            raise NetworkError("Request timed out") from exc

        except httpx.ConnectError as exc:
            raise NetworkError("Failed to connect to Paymob API") from exc

        except httpx.HTTPError as exc:
            raise NetworkError(str(exc)) from exc

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:

        if self.debug:
            print(f"[Paymob DEBUG] {response.status_code} - {response.text}")

        if response.status_code in (200, 201, 202, 204):
            if not response.content:
                return {}
            return response.json()

        try:
            error_data = response.json()
        except Exception:
            error_data = {"message": response.text}

        message = error_data.get("message") or error_data

        if response.status_code == 400:
            raise ValidationError(message)

        if response.status_code in (401, 403):
            raise AuthenticationError(message)

        raise APIError(
            f"Paymob API error ({response.status_code}): {message}"
        )

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> SyncHTTP:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()