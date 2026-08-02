from .base import BaseModel
from typing import Any, Dict, Optional


class WebhookEvent(BaseModel):
    event_type: Optional[str]
    success: bool

    order_id: Optional[int]
    transaction_id: Optional[int]

    amount_cents: Optional[int]
    currency: Optional[str]

    raw: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebhookEvent":
        obj = data.get("obj") or {}

        return cls(
            event_type=data.get("type"),
            success=bool(obj.get("success")),
            order_id=(obj.get("order") or {}).get("id"),
            transaction_id=obj.get("id"),
            amount_cents=obj.get("amount_cents"),
            currency=obj.get("currency"),
            raw=data,
        )