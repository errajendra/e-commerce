from rest_framework.exceptions import APIException


class CartIsEmpaty(APIException):
    status_code = 404
    default_detail = {
        'status': 404,
        'message': "Your cart is empty."
    }
    default_code = 'not_found'
