from crowapp.models import User
from rest_framework_simplejwt.tokens import AccessToken

def get_user_from_token(authorization):
    if authorization and authorization.startswith('Bearer '):
        token = authorization.split(' ')[1]
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    return None
