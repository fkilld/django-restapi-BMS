# books/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Author, Category, Book

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(**validated_data)
        # Automatically create an Author instance for the new user
        Author.objects.create(user=user, name=validated_data.get('username'))
        return user

# Existing serializers...
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
