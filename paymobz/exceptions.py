class PaymobError(Exception):
    pass

class APIError(PaymobError):
    pass

class AuthenticationError(APIError):
    pass

class ValidationError(APIError):
    pass

class NetworkError(PaymobError):
    pass