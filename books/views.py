# books/views.py
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer
from .permissions import IsBookOwner
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Author, Category, Book
from .serializers import AuthorSerializer, CategorySerializer, BookSerializer
from .permissions import IsOwner  # Import custom permission


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # Ensure only owner can modify

    def get_queryset(self):
        """Return only the authors owned by the logged-in user."""
        return Author.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        """Ensure only the logged-in user can update their own profile."""
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]  # No restriction on category

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwner]  # Ensure only the owner can modify

    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)  # Show only books created by the user


from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class RegistrationView(APIView):
    permission_classes = []  # Allow any user to access registration

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This creates the User and Author
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                access_token = str(refresh.access_token)

                response = Response({"message": "Access token refreshed"}, status=status.HTTP_200_OK)
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='Lax'
                )

                return response
            except Exception:
                return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)
 

# books/views.py (continued)
class LogoutView(APIView):
    # Remove IsAuthenticated if you wish to allow logout without validating the access token
    permission_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                return Response({"error": "Invalid refresh token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to log in

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response({"message": "User logged in successfully"}, status=status.HTTP_200_OK)

            # Set access and refresh tokens in HTTP-only cookies
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,  # Prevents JavaScript access
                secure=True,  # Use True in production (HTTPS)
                samesite='Lax'  # Adjust if cross-origin requests are needed
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Lax'
            )

            return response

        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
