# Importing JWTAuthentication from SimpleJWT to handle JWT-based authentication
from rest_framework_simplejwt.authentication import JWTAuthentication 

# Importing AuthenticationFailed exception to handle authentication errors
from rest_framework.exceptions import AuthenticationFailed  

# Defining a custom authentication class by extending JWTAuthentication
class CustomJWTAuthentication(JWTAuthentication):  
    # Overriding the authenticate method to customize JWT token extraction
    def authenticate(self, request):  
        # Attempt to retrieve the JWT token from the cookies using the key 'access_token'
        access_token = request.COOKIES.get('access_token')  

        # If no token is found in the cookies, return None
        # This allows Django Rest Framework (DRF) to handle authentication normally
        if not access_token:  
            return None  

        try:
            # Validate the retrieved token using the parent class's method
            validated_token = self.get_validated_token(access_token)  
        except AuthenticationFailed:  
            # If validation fails (e.g., expired or tampered token), return None
            # This prevents unauthorized access instead of raising an exception
            return None  

        # Return a tuple containing the authenticated user and the validated token
        # `get_user(validated_token)` retrieves the user associated with the token
        return self.get_user(validated_token), validated_token  
