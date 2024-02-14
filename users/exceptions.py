from rest_framework import status
from rest_framework.exceptions import APIException


class UserExceptions:
    class UserException(APIException):
        error_code = 1000
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "invalid_user"
        default_detail = "Invalid user"

    class AlreadyExists(APIException):
        error_code = 1001
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "user_already_exists"
        default_detail = "User already exists"