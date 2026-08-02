from typing import TYPE_CHECKING, Dict, Any
from paymobz.models.unified_checkout import CheckoutRequest, CheckoutResponse
from paymobz.exceptions import APIError

if TYPE_CHECKING:
    from paymobz.client.sync import PaymobClient


class UnifiedCheckoutResource:
    def __init__(self, client: "PaymobClient", public_key: str, secret_key: str):
        self.client = client
        self.public_key = public_key
        self.secret_key = secret_key

    def create(self, checkout_data: CheckoutRequest) -> CheckoutResponse:
        if hasattr(checkout_data, "model_dump"):
            payload: Dict[str, Any] = checkout_data.model_dump(exclude_none=True)
        elif hasattr(checkout_data, "dict"):
            payload: Dict[str, Any] = checkout_data.dict(exclude_none=True)
        else:
            payload: Dict[str, Any] = checkout_data

        raw_response = self.client.request(
            method="POST",
            endpoint="/v1/intention/",
            json=payload,
            use_legacy_auth=False,
        )

        client_secret = raw_response.get("client_secret")

        if not client_secret:
            raise APIError(f"Invalid unified checkout response: {raw_response}")

        checkout_url = (
            f"https://accept.paymob.com/unifiedcheckout/"
            f"?publicKey={self.public_key}&clientSecret={client_secret}"
        )

        return CheckoutResponse(
            client_secret=client_secret,
            intention_url=checkout_url,
        )