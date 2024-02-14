from rest_framework import status
from rest_framework.exceptions import APIException


class OrderExceptions:
    class OrderException(APIException):
        error_code = 4000
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "order_exception"
        default_detail = "Order Exception"
