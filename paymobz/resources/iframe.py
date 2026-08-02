from typing import Dict, Any
from paymobz.exceptions import APIError


class IframeResource:
    def __init__(self, client):
        self.client = client

    def get_url(
        self,
        amount_cents: int,
        billing_data: Dict[str, Any],
        integration_id: int,
        iframe_id: int,
        currency: str = "EGP",
    ) -> str:

        if not self.client._auth_token:
            self.client._authenticate()

        auth_token = self.client._auth_token

        order_res = self.client.request(
            method="POST",
            endpoint="/api/ecommerce/orders",
            json={
                "auth_token": auth_token,
                "amount_cents": amount_cents,
                "currency": currency,
                "items": [],
                "delivery_needed": False,
            },
        )

        order_id = order_res.get("id")
        if not order_id:
            raise APIError("Failed to create order")

        payment_key_res = self.client.request(
            method="POST",
            endpoint="/api/acceptance/payment_keys",
            json={
                "auth_token": auth_token,
                "amount_cents": amount_cents,
                "expiration": 3600,
                "order_id": order_id,
                "billing_data": billing_data,
                "currency": currency,
                "integration_id": integration_id,
            },
        )

        payment_token = payment_key_res.get("token")
        if not payment_token:
            raise APIError("Failed to generate payment token")

        return f"https://accept.paymob.com/api/acceptance/iframes/{iframe_id}?payment_token={payment_token}"