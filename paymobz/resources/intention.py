from typing import TYPE_CHECKING, Dict, Any
from paymobz.exceptions import APIError

if TYPE_CHECKING:
    from paymobz.client.sync import PaymobClient


class Intention:
    def __init__(self, client: "PaymobClient"):
        self.client = client

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.request(
            method="POST",
            endpoint="/v1/intention/",
            json=payload,
            use_legacy_auth=False,
        )

        if not response:
            raise APIError("Empty response from paymob API")

        if "client_secret" not in response:
            raise APIError(f"Invalid intention response: {response}")

        return response