from datetime import date
from typing import Literal, Optional
from .apierror import APIError


class TransactionsAPI:
    API_VERSION = "application/vnd.sparebank1.v1+json; charset=utf-8"

    def __init__(self, api):
        self.api = api

    def list_transactions(
        self,
        account_keys: list[str],
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        row_limit: Optional[int] = None,
        transaction_source: Optional[list[Literal["RECENT", "HISTORIC", "ALL"]]] = None,
        enrich_with_payment_details: Optional[bool] = None,
    ):
        """GET /transactions - List transactions entities"""
        if account_keys is str:
            account_keys = [account_keys]
        params = [("accountKey", k) for k in account_keys]
        if from_date:
            params.append(("fromDate", from_date.strftime("%Y-%m-%d")))
        if to_date:
            params.append(("toDate", to_date.strftime("%Y-%m-%d")))
        if row_limit:
            params.append(("rowLimit", str(row_limit)))
        if transaction_source:
            params.append(("transactionSource", ", ".join(transaction_source)))
        if enrich_with_payment_details is not None:
            params.append(
                ("enrichWithPaymentDetails", str(enrich_with_payment_details).lower())
            )
        response = self.api.get(
            "transactions", params=params, headers={"Accept": self.API_VERSION}
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def export_transactions_to_csv(self, account_key, from_date, to_date):
        """GET /transactions/export - Exports booked transactions to CSV for a given period"""
        response = self.api.get(
            "transactions/export",
            params={
                "accountKey": account_key,
                "fromDate": from_date,
                "toDate": to_date,
            },
            headers={"Accept": "application/csv;charset=UTF-8"},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.content

    def list_classified_transactions(
        self,
        account_keys: list[str],
        from_date: Optional[date] = None,
        to_date: Optional[date] = None,
        row_limit: Optional[int] = None,
        transaction_source: Optional[list[Literal["RECENT", "HISTORIC", "ALL"]]] = None,
        enrich_with_payment_details: Optional[bool] = None,
        enrich_with_merchant_logo: Optional[bool] = None,
    ):
        """GET /transactions/classified - List transactions entities with classification"""
        if account_keys is str:
            account_keys = [account_keys]
        params = [("accountKey", k) for k in account_keys]
        if from_date:
            params.append(("fromDate", from_date.strftime("%Y-%m-%d")))
        if to_date:
            params.append(("toDate", to_date.strftime("%Y-%m-%d")))
        if row_limit:
            params.append(("rowLimit", str(row_limit)))
        if transaction_source:
            params.append(("transactionSource", ", ".join(transaction_source)))
        if enrich_with_payment_details is not None:
            params.append(
                ("enrichWithPaymentDetails", str(enrich_with_payment_details).lower())
            )
        if enrich_with_merchant_logo is not None:
            params.append(
                ("enrichWithMerchantLogo", str(enrich_with_merchant_logo).lower())
            )
        response = self.api.get(
            "transactions/classified",
            params=params,
            headers={"Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_transaction_details(self, transaction_id):
        response = self.api.get(
            f"transactions/{transaction_id}/details",
            headers={"Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()

    def get_classified_transaction_details(
        self, transaction_id, enrich_with_merchant_data=None
    ):
        response = self.api.get(
            f"transactions/{transaction_id}/details/classified",
            params=(
                enrich_with_merchant_data is not None
                if {"enrichWithMerchantData": enrich_with_merchant_data}
                else None
            ),
            headers={"Accept": self.API_VERSION},
        )
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()
