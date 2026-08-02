import os
from typing import Optional


class PaymobConfig:
    DEFAULT_BASE_URL = "https://accept.paymob.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        public_key: Optional[str] = None,
        hmac_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("PAYMOB_API_KEY")
        self.secret_key = secret_key or os.getenv("PAYMOB_SECRET_KEY")
        self.public_key = public_key or os.getenv("PAYMOB_PUBLIC_KEY")
        self.hmac_key = hmac_key or os.getenv("PAYMOB_HMAC_KEY")

        self.base_url = (
            base_url
            or os.getenv("PAYMOB_BASE_URL")
            or self.DEFAULT_BASE_URL
        ).rstrip("/")

        self._validate()

    def _validate(self) -> None:
        if not self.api_key and not self.secret_key:
            raise ValueError(
                "Either api_key (legacy) or secret_key must be provided."
            )