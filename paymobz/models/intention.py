from .base import BaseModel
from typing import List, Dict, Any, Optional


class IntentionRequest(BaseModel):
    amount: int
    currency: str = "EGP"

    payment_methods: List[int]

    billing_data: Dict[str, Any]

    customer: Optional[Dict[str, Any]] = None
    extras: Optional[Dict[str, Any]] = None

    expiration: Optional[int] = 3600