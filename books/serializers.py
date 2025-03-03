# Importing Django's built-in User model for authentication and user management
from django.contrib.auth.models import User  

# Importing serializers from Django REST Framework to convert model instances to JSON format and vice versa
from rest_framework import serializers  

# Importing models to create serializers for them
from .models import Author, Category, Book  


# Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):  
    # Defining a password field and ensuring it's write-only (won't be exposed in responses)
    password = serializers.CharField(write_only=True)  

    class Meta:
        # Using the built-in User model for user serialization
        model = User  
        # Specifying fields to be included in the serializer
        fields = ('username', 'email', 'password')  

    # Overriding the create method to handle user creation and author creation
    def create(self, validated_data):  
        # Creating a new user using the create_user method (handles password hashing automatically)
        user = User.objects.create_user(**validated_data)  

        # Creating an associated Author instance for the newly registered user
        Author.objects.create(user=user, name=validated_data.get('username'))  

        # Returning the created user object
        return user  


# Serializer for Author model
class AuthorSerializer(serializers.ModelSerializer):  
    # Automatically assigns the currently logged-in user as the `user` field value
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  

    class Meta:
        # Using the Author model for serialization
        model = Author  
        # Including all fields from the model
        fields = '__all__'  

    # Overriding the create method to ensure the logged-in user is assigned as the author
    def create(self, validated_data):  
        # Setting the user field to the currently logged-in user from the request context
        validated_data['user'] = self.context['request'].user  

        # Calling the parent class's create method to save the object
        return super().create(validated_data)  


# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):  
    class Meta:
        # Using the Category model for serialization
        model = Category  
        # Including all fields from the model
        fields = '__all__'  


# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):  
    # Automatically assigns the currently logged-in user as the `user` field value
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  

    class Meta:
        # Using the Book model for serialization
        model = Book  
        # Including all fields from the model
        fields = '__all__'  

    # Overriding the create method to ensure the logged-in user is assigned as the book's owner
    def create(self, validated_data):  
        # Setting the user field to the currently logged-in user from the request context
        validated_data['user'] = self.context['request'].user  

        # Calling the parent class's create method to save the object
        return super().create(validated_data)  
