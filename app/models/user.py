from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, validator


class User(BaseModel):
    email: str
    password: str


class NewUser(BaseModel):
    email: str
    password: str

    @validator('email')
    def email_must_be_valid(cls, v: str):
        try:
            validation = validate_email(v, check_deliverability=False)
        except EmailNotValidError:
            raise ValueError('invalid email')
        except Exception:
            raise ValueError('invalid email')

        return validation.email

    @validator('password')
    def password_must_be_valid(cls, v: str):
        strip_v = v.strip()
        if len(strip_v) < 8:
            raise ValueError('password must be more than 8 characters')
        elif len(strip_v) > 20:
            raise ValueError('password must be less than 20 characters')

        return strip_v
