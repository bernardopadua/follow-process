#REST FRAMEWORK Core
from rest_framework.exceptions import APIException

class UserNotAuthorized(APIException):
    status_code = 401
    detail = ""
    default_code = 'user_not_authorized'
    def __init__(self, detail):
        self.detail = detail
