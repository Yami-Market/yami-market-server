from enum import Enum


class ClientErrorMessage(str, Enum):
    method_not_allowed = 'Method Not Allowed'

    invalid_json_body = 'Request Body is not JSON'
    empty_json_body = 'Request Body is Empty'

    wrong_email_or_password = 'Wrong Email or Password'
    email_already_exists = 'Email already exists'


class ServerErrorMessage(str, Enum):
    server_error = 'Server Error'
