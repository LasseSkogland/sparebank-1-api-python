# WIP - SpareBank1 API Client

This project is a Python client for SpareBank1 APIs, supporting OAuth2 authentication and all endpoints from the provided Swagger definitions.
Implements personal endpoints from: https://developer.sparebank1.no/

## Features
- OAuth2 Authorization Code Flow (authenticate, token exchange, refresh)
- All personal endpoints from the SpareBank1 Swagger definitions

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Configure your credentials in `config.ini` (or as UPPER_CASE environment variables):
   - `client_id`
   - `client_secret`
   - `redirect_uri`
   - `fin_inst`

## Usage
Run the CLI:
```sh
python main.py
```


## License
MIT
