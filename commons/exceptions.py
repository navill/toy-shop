from rest_framework import status
from rest_framework.exceptions import APIException


class BaseExceptions(APIException):
    error_code = 999
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "internal_server_error"
    default_detail = "internal server error"


class MaxRetriesException(BaseExceptions):
    error_code = 998
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "max_retries_exceeded"
    default_detail = "Max Retries Exceeded"
