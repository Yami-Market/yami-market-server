from enum import Enum


class ClientErrorMessage(str, Enum):
    method_not_allowed = 'Method Not Allowed'
    unsupported_media_type = 'Unsupported Media Type'

    wrong_email_or_password = 'Wrong Email or Password'
    email_already_exists = 'Email already exists'


class ServerErrorMessage(str, Enum):
    server_error = 'Server Error'
