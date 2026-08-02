from typing import TYPE_CHECKING

from paymobz.models.transaction import Transaction
from paymobz.exceptions import APIError


if TYPE_CHECKING:
    from paymobz.client.sync import PaymobClient


class TransactionResource:

    def __init__(self, client: "PaymobClient"):
        self.client = client


    def retrieve(self, transaction_id: int) -> Transaction:

        response = self.client.request(
            method="GET",
            endpoint=f"/api/acceptance/transactions/{transaction_id}",
            use_legacy_auth=True
        )

        if not response:
            raise APIError(
                f"Invalid transaction response: {response}"
            )


        return Transaction(
            id=response.get("id"),
            pending=response.get("pending"),
            success=response.get("success"),

            amount_cents=response.get("amount_cents"),
            currency=response.get("currency"),

            is_auth=response.get("is_auth"),
            is_capture=response.get("is_capture"),
            is_voided=response.get("is_voided"),
            is_refund=response.get("is_refund"),
            is_refunded=response.get("is_refunded"),
            refunded_amount_cents=response.get(
                "refunded_amount_cents"
            ),
            captured_amount_cents=response.get(
                "captured_amount_cents"
            ),
            is_captured=response.get("is_captured"),
            parent_transaction=response.get(
                "parent_transaction"
            ),

            raw=response
        )