from flask_jwt_extended import JWTManager

from app.models.user_model import User
from app.services.user_service import get_user_by_email

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return user.email


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # user's identity is the email
    identity = jwt_data['sub']
    return get_user_by_email(identity)
