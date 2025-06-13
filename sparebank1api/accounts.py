from typing import Any
from .apierror import (
    APIError,
)


class AccountsAPI:
    API_VERSION = "application/vnd.sparebank1.v5+json; charset=utf-8"

    def __init__(self, api):  # Remove type hint to avoid circular import at runtime
        self.api = api

    def list_accounts(
        self,
        include_nok_accounts=True,
        include_currency_accounts=False,
        include_bsu_accounts=False,
        include_creditcard_accounts=False,
        include_ask_accounts=False,
        include_pension_accounts=False,
    ) -> list[dict[str, Any]]:
        response = self.api.get(
            "accounts",
            params={
                "includeNokAccounts": include_nok_accounts,
                "includeCurrencyAccounts": include_currency_accounts,
                "includeBsuAccounts": include_bsu_accounts,
                "includeCreditcardAccounts": include_creditcard_accounts,
                "includeAskAccounts": include_ask_accounts,
                "includePensionAccounts": include_pension_accounts,
            },
            headers={"Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json().get("accounts", [])

    def get_account_keys(self, account_numbers: list[str]):
        response = self.api.get(
            "accounts/keys",
            params=[("accountNumber", n) for n in account_numbers],
            headers={"Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_account_balance(self, account_number: str):
        response = self.api.post(
            "accounts/balance",
            json={"accountNumber": account_number},
            headers={"Content-Type": self.API_VERSION, "Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_default_account(self):
        response = self.api.get(
            "accounts/default", headers={"Accept": self.API_VERSION}
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_account(self, account_key):
        response = self.api.get(
            f"accounts/{account_key}", headers={"Accept": self.API_VERSION}
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_account_roles(self, account_key):
        response = self.api.get(
            f"accounts/{account_key}/roles", headers={"Accept": self.API_VERSION}
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_account_details(self, account_key):
        response = self.api.get(
            f"accounts/{account_key}/details", headers={"Accept": self.API_VERSION}
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()
