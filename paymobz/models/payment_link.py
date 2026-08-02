from .base import BaseModel
from typing import List, Dict, Any, Optional


class PaymentLinkRequest(BaseModel):
    amount_cents: int
    currency: str = "EGP"

    is_live: bool = False

    payment_methods: List[int]

    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None


class PaymentLinkResponse(BaseModel):
    id: int
    amount_cents: int

    shorten_url: str
    client_url: str

    state: str

    order: int | Dict[str, Any]

    client_info: Optional[Dict[str, Any]] = None