from rest_framework import status
from rest_framework.exceptions import APIException


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Entity already exists."


class UserConflict(Conflict):
    default_detail = "User with this name already exists."
