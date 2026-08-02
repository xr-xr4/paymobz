import hmac
import hashlib
from typing import Dict, Any


class WebhookResource:
    def __init__(self, hmac_secret: str):
        self.hmac_secret = hmac_secret

    def verify_mac(self, data: Dict[str, Any], hmac_received: str) -> bool:
        obj = data.get("obj") or {}

        hmac_keys = [
            "amount_cents", "created_at", "currency", "error_occured",
            "has_parent_transaction", "id", "integration_id", "is_3d_secure",
            "is_auth", "is_capture", "is_refunded", "is_standalone_payment",
            "is_voided", "order.id", "owner", "pending", "source_data.pan",
            "source_data.sub_type", "source_data.type", "success"
        ]

        concatenated_string = ""

        for key in hmac_keys:
            if "." in key:
                parent, child = key.split(".")
                value = obj.get(parent, {}).get(child, "")
            else:
                value = obj.get(key, "")

            if isinstance(value, bool):
                value = str(value).lower()

            concatenated_string += str(value)

        calculated_hmac = hmac.new(
            self.hmac_secret.encode("utf-8"),
            concatenated_string.encode("utf-8"),
            hashlib.sha512
        ).hexdigest()

        return hmac.compare_digest(calculated_hmac, hmac_received)