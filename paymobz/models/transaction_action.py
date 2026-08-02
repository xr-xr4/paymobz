from .base import BaseModel
from typing import Optional, Dict, Any


class TransactionActionRequest(BaseModel):
    transaction_id: int
    amount_cents: Optional[int] = None


class TransactionActionResponse(BaseModel):
    id: Optional[int] = None
    success: bool
    pending: Optional[bool] = None
    is_refund: Optional[bool] = None
    is_void: Optional[bool] = None

    raw: Dict[str, Any] = {}