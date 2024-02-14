from rest_framework import status
from rest_framework.exceptions import APIException


class CategoryExceptions:
    class CategoryException(APIException):
        error_code = 2000
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "invalid_category"
        default_detail = "Invalid category"

    class InvalidCategoryPosition(APIException):
        error_code = 2001
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "invalid_category_position"
        default_detail = "Invalid category position"

    class NotFoundCategory(APIException):
        error_code = 2004
        status_code = status.HTTP_404_NOT_FOUND
        default_code = "not_found_category"
        default_detail = "Not found category"


class ProductExceptions:
    class ProductException(APIException):
        error_code = 3000
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "invalid_product"
        default_detail = "Invalid product"

    class OutOfStockException(APIException):
        error_code = 3001
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "out_of_stock"
        default_detail = "Out of stock product"

    class OverStockException(APIException):
        error_code = 3002
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "over_stock"
        default_detail = "Overstock"

    class UnavailableForSale(APIException):
        error_code = 3003
        status_code = status.HTTP_400_BAD_REQUEST
        default_code = "unavailable_for_sale"
        default_detail = "Unavailable for sale"

    class NotFoundProduct(APIException):
        error_code = 3004
        status_code = status.HTTP_404_NOT_FOUND
        default_code = "not_found_product"
        default_detail = "Not found product"
