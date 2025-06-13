import json
from sparebank1api.config import Config
from sparebank1api.client import SpareBank1API


def main():
    config = Config()
    api = SpareBank1API(config)

    api.authenticate()
    accounts = api.accounts.list_accounts()
    print(json.dumps(accounts, indent=2))


if __name__ == "__main__":
    main()
