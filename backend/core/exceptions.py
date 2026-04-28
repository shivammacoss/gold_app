from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Standardized error response format."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "error": {
                "code": response.status_code,
                "message": _get_error_message(response.data),
            },
        }

    return response


def _get_error_message(data):
    """Extract a flat error message from DRF error data."""
    if isinstance(data, list):
        return data[0] if data else "An error occurred."
    if isinstance(data, dict):
        messages = []
        for key, value in data.items():
            if isinstance(value, list):
                messages.append(f"{key}: {value[0]}")
            else:
                messages.append(f"{key}: {value}")
        return "; ".join(messages) if messages else "An error occurred."
    return str(data)


class InsufficientBalanceError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Insufficient wallet balance for this operation."
    default_code = "insufficient_balance"


class BlockchainTransactionError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = "Blockchain transaction failed. Please try again."
    default_code = "blockchain_error"


class WithdrawalLimitExceeded(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Withdrawal limit exceeded."
    default_code = "withdrawal_limit_exceeded"


class InvestmentNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Investment plan not found."
    default_code = "investment_not_found"
