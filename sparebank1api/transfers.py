from datetime import date
from .apierror import APIError
from typing import Optional


class TransfersAPI:
    API_VERSION = "application/vnd.sparebank1.v1+json; charset=utf-8"

    def __init__(self, api):
        self.api = api

    def transfer_to_credit_card(
        self,
        amount: float,
        from_account: str,
        credit_card_account_id: str,
        due_date: date = date.today(),
    ):
        response = self.api.postApi(
            "transfer/creditcard/transferTo",
            json={
                "amount": amount,
                "fromAccount": from_account,
                "creditCardAccountId": credit_card_account_id,
                "dueDate": due_date.strftime("%Y-%m-%d"),
            },
            headers={"Content-Type": self.API_VERSION, "Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def transfer_between_accounts(
        self,
        amount: float,
        from_account: str,
        to_account: str,
        currency_code: str = "NOK",
        due_date: date = date.today(),
        message: Optional[str] = None,
    ):
        url = f"{self.api.API_URL}/"
        data = {
            "amount": str(amount),
            "fromAccount": from_account,
            "toAccount": to_account,
            "currencyCode": currency_code,
            "dueDate": due_date.strftime("%Y-%m-%d"),
        }
        if message:
            data["message"] = message
        response = self.api.postApi(
            "transfer/debit",
            json=data,
            headers={"Content-Type": self.API_VERSION, "Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def transfer_to_pension(
        self,
        amount: float,
        from_account: str,
        policy_number: str,
        due_date: date = date.today(),
    ):
        response = self.api.postApi(
            "transfer/pension",
            json={
                "amount": str(amount),
                "fromAccount": from_account,
                "policyNumber": policy_number,
                "dueDate": due_date.strftime("%Y-%m-%d"),
            },
            headers={"Content-Type": self.API_VERSION, "Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()
