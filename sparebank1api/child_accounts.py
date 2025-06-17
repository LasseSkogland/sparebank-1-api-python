from .apierror import APIError


class ChildAccountsAPI:
    API_VERSION = "application/vnd.sparebank1.v5+json; charset=utf-8"

    def __init__(self, api):
        self.api = api

    def get_child_account(self, child_id):
        response = self.api.getApi(f"accounts/child/{child_id}", headers={"Accept": self.API_VERSION})
        if not response.ok:
            raise APIError(response.status_code, response.text)
        return response.json()
