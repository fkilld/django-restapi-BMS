# books/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('author', AuthorViewSet)
router.register('category', CategoryViewSet)
router.register('book', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
       path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]
