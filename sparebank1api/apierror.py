class APIError(Exception):
    def __init__(self, status_code, error):
        self.status_code = status_code
        self.error = error
        super().__init__(f"API Error {status_code}: {error}")
