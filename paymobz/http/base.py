from __future__ import annotations

from typing import Any, Dict


class BaseHTTP:
    def __init__(
        self,
        base_url: str,
        timeout: float,
        user_agent: str,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
        }

    @staticmethod
    def remove_none(data: Dict[str, Any] | None) -> Dict[str, Any]:
        if not data:
            return {}

        return {
            key: value
            for key, value in data.items()
            if value is not None
        }