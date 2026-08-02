
from .config import PaymobConfig
from .client.sync import PaymobClient


class Paymob:
    def __init__(
        self,
        api_key: str | None = None,
        secret_key: str | None = None,
        public_key: str = "",
        hmac_secret: str = "",
        base_url: str = "https://accept.paymob.com",
    ):
        self.config = PaymobConfig(
            api_key=api_key,
            secret_key=secret_key,
            public_key=public_key,
            hmac_key=hmac_secret,
            base_url=base_url,
        )

        self.client = PaymobClient(self.config)

        self.payment_links = self.client.payment_link
        self.unified_checkout = self.client.unified_checkout
        self.iframes = self.client.iframe
        self.webhooks = self.client.webhooks
        self.captures = self.client.captures
        self.voids = self.client.voids
        self.refunds = self.client.refunds
        self.transactions = self.client.transactions
  
        

    def close(self) -> None:
        self.client.close()

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc, tb):
        self.close()


__all__ = ["Paymob"]
