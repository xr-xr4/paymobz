from .base import BaseModel
from typing import List, Dict, Any, Optional


class CheckoutRequest(BaseModel):
    amount: int
    currency: str = "EGP"

    payment_methods: List[int]

    billing_data: Dict[str, Any]

    customer: Optional[Dict[str, Any]] = None
    extras: Optional[Dict[str, Any]] = None
    special_reference: Optional[str] = None

    expiration: Optional[int] = 3600


class CheckoutResponse(BaseModel):
    client_secret: str
    intention_url: str = ""