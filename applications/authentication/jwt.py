import jwt
from jwt.exceptions import InvalidSignatureError
from django.conf import settings

from applications.accounts.managers.selectors import (
    UserSelector,
)


def verify_new_user(validated_data: dict):
    verification_token = validated_data.get('verification_token')
    if verification_token:
        user = None
        try:
            user_data = jwt.decode(
                verification_token, settings.SECRET_KEY, algorithms=['HS256']
            )
            user_id = user_data['id']
            user = UserSelector.fetch_record(id=user_id)
        except InvalidSignatureError:
            pass
        except Exception:
            pass

        if user is None or not user.exists():
            return user
        else:
            user.is_active = True
            user.save()
            return user
    return False
