from typing import TYPE_CHECKING

from paymobz.models.transaction_action import (
    TransactionActionRequest,
    TransactionActionResponse
)

from paymobz.exceptions import APIError


if TYPE_CHECKING:
    from paymobz.client.sync import PaymobClient


class VoidResource:

    def __init__(self, client: "PaymobClient"):
        self.client = client


    def create(
        self,
        data: TransactionActionRequest
    ) -> TransactionActionResponse:

        if hasattr(data, "model_dump"):
            payload = data.model_dump(exclude_none=True)
        else:
            payload = data.dict(exclude_none=True)


        response = self.client.request(
            method="POST",
            endpoint="/api/acceptance/void_refund/void",
            json=payload,
            use_legacy_auth=True
        )


        if not response:
            raise APIError(
                f"Invalid void response: {response}"
            )


        return TransactionActionResponse(
            id=response.get("id"),
            success=True,
            raw=response
        )