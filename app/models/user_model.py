from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, validator


class UserBodyParams(BaseModel):
    email: str
    password: str


class User(BaseModel):
    id: str
    email: str
    password: str
    first_name: str | None
    last_name: str | None
    gender: str | None


class NewUser(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_must_be_valid(cls, v: str):
        try:
            validation = validate_email(v, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError('Invalid Email')
        except Exception:
            raise ValueError('Invalid Email')

        return validation.email

    @validator('password')
    def password_must_be_valid(cls, v: str):
        strip_v = v.strip()
        if len(strip_v) < 8:
            raise ValueError('Password must be more than 8 characters')
        elif len(strip_v) > 20:
            raise ValueError('Password must be less than 20 characters')

        return strip_v
