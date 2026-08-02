from .base import BaseModel
from typing import Optional, Dict, Any


class Transaction(BaseModel):
    id: int

    pending: Optional[bool] = None
    success: Optional[bool] = None

    amount_cents: Optional[int] = None
    currency: Optional[str] = None

    is_auth: Optional[bool] = None
    is_capture: Optional[bool] = None
    is_voided: Optional[bool] = None

    is_refund: Optional[bool] = None
    is_refunded: Optional[bool] = None

    is_captured: Optional[bool] = None

    refunded_amount_cents: Optional[int] = None
    captured_amount_cents: Optional[int] = None

    parent_transaction: Optional[int] = None

    raw: Dict[str, Any] = {}