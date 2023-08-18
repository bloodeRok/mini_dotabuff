from rest_framework import status
from rest_framework.exceptions import APIException


class NotAcceptable(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = "User input not acceptable."
