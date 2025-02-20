from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Look for the token in the "access_token" cookie
        access_token = request.COOKIES.get('access_token')

        if not access_token:
            return None  # No token found, let DRF handle it

        try:
            validated_token = self.get_validated_token(access_token)
        except AuthenticationFailed:
            return None  # Invalid token

        return self.get_user(validated_token), validated_token
