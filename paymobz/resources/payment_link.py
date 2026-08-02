from typing import TYPE_CHECKING, Dict, Any
from paymobz.models.payment_link import PaymentLinkRequest, PaymentLinkResponse
from paymobz.exceptions import APIError

if TYPE_CHECKING:
    from paymobz.client.sync import PaymobClient


class PaymentLinkResource:
    def __init__(self, client: "PaymobClient"):
        self.client = client

    def create(self, link_data: PaymentLinkRequest) -> PaymentLinkResponse:
        if hasattr(link_data, "model_dump"):
            payload: Dict[str, Any] = link_data.model_dump(exclude_none=True)
        else:
            payload: Dict[str, Any] = link_data.dict(exclude_none=True)

        raw_response = self.client.request(
            method="POST",
            endpoint="/api/ecommerce/payment-links",
            json=payload,
        )

        if not raw_response:
            raise APIError("Empty response from paymob API")

        try:
            return PaymentLinkResponse(**raw_response)
        except Exception as e:
            raise APIError(f"Invalid response format: {raw_response}") from e