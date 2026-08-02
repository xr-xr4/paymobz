import httpx
from typing import Any, Dict

from paymobz.config import PaymobConfig
from paymobz.http.sync import SyncHTTP
from paymobz.exceptions import APIError, AuthenticationError


class PaymobClient:
    def __init__(self, config: PaymobConfig):
        self.config = config
        self._auth_token = None
        self.http = SyncHTTP(base_url=self.config.base_url)

        from paymobz.resources.iframe import IframeResource as Iframe
        from paymobz.resources.payment_link import PaymentLinkResource as PaymentLink
        from paymobz.resources.unified_checkout import UnifiedCheckoutResource as UnifiedCheckout
        from paymobz.resources.webhooks import WebhookResource as Webhooks
        from paymobz.resources.intention import Intention
        from paymobz.resources.refund import RefundResource as Refund
        from paymobz.resources.capture import CaptureResource
        from paymobz.resources.void import VoidResource
        from paymobz.resources.transactions import TransactionResource
        
        
        self.iframe = Iframe(self)
        self.payment_link = PaymentLink(self)

        self.unified_checkout = UnifiedCheckout(
            self,
            self.config.public_key,
            self.config.secret_key
        )

        self.webhooks = Webhooks(
            hmac_secret=self.config.hmac_key
        )

        self.intention = Intention(self)


        self.refunds = Refund(self)
        self.captures = CaptureResource(self)
        self.voids = VoidResource(self)
        self.transactions = TransactionResource(self)

    def _authenticate(self) -> str:
        if not self.config.api_key:
            raise ValueError("Legacy API Key is missing.")

        res = self.http.request(
            "POST",
            "/api/auth/tokens",
            json={"api_key": self.config.api_key},
        )

        token = res.get("token")

        if not token:
            raise AuthenticationError(
                "Failed to retrieve auth token"
            )

        self._auth_token = token

        return token


    def request(
        self,
        method: str,
        endpoint: str,
        use_legacy_auth: bool = True,
        retry: bool = True,
        **kwargs
    ) -> Dict[str, Any]:

        base_headers = kwargs.pop("headers", {}) or {}
        headers = dict(base_headers)

        if use_legacy_auth:

            if not self._auth_token:
                self._authenticate()

            headers["Authorization"] = (
                f"Bearer {self._auth_token}"
            )

        else:

            if not self.config.secret_key:
                raise ValueError(
                    "Secret Key is missing for this API request."
                )

            headers["Authorization"] = (
                f"Bearer {self.config.secret_key}"
            )


        headers.setdefault(
            "Content-Type",
            "application/json"
        )


        try:

            return self.http.request(
                method,
                endpoint,
                headers=headers,
                **kwargs
            )


        except AuthenticationError:

            if use_legacy_auth and retry:

                self._auth_token = None

                self._authenticate()

                return self.request(
                    method,
                    endpoint,
                    use_legacy_auth=use_legacy_auth,
                    retry=False,
                    headers=base_headers,
                    **kwargs
                )

            raise


        except httpx.HTTPError as e:
            raise APIError(str(e)) from e


    def close(self) -> None:
        self.http.close()


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc, tb):
        self.close()