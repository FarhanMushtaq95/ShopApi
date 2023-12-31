from datetime import datetime

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserUsernameAndIdSerializer




class JwtExactritr(JWTAuthentication):
    def get_jwt_value(self, request):
        pass


def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
        "iss": "http://melardev.com",
        'roles': ['ROLE_ADMIN' if user.is_staff else 'ROLE_USER'],
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        # 'orig_iat': timegm(datetime.utcnow().utctimetuple())
    }

# get_user_model().USERNAME_FIELD
def jwt_response(token, user=None, request=None):
    roles = []
    if user.is_staff:
        roles.append('ROLE_ADMIN')
    else:
        roles.append('ROLE_USER')
    user_dto = UserUsernameAndIdSerializer(user, context={'request': request}).data
    user_dto.update({'roles': roles})
    refresh = RefreshToken.for_user(user)
    return {
        "success": True,
        'user': user_dto,
        'token': {
            'access': str(token),
            'refresh': str(refresh),
        }
    }

from rest_framework_simplejwt.tokens import AccessToken

def test(user):
    payload = AccessToken.for_user(user)
    token = str(payload)


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                (request.user and
                 request.user.is_staff)
        )


class IsAdminOrOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and (request.user.is_staff or obj.user == request.user)
