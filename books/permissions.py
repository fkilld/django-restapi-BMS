# Importing BasePermission from Django REST Framework to create custom permissions
from rest_framework.permissions import BasePermission  

# Defining a custom permission class to check if the logged-in user is the owner of a book
class IsBookOwner(BasePermission):  
    """
    Object-level permission that only allows owners of a book to access or modify it.
    Assumes that each Book's 'author' is linked to a User via an Author instance.
    """

    # Overriding has_object_permission to define object-level access control
    def has_object_permission(self, request, view, obj):  
        # Retrieve the currently logged-in user's associated Author instance
        user_author = getattr(request.user, 'author', None)  

        # Compare the book's author with the logged-in user's Author instance
        # If they match, the user has permission to access or modify the book
        return obj.author == user_author  


# Defining another custom permission to check if the logged-in user owns a given object
class IsOwner(BasePermission):  
    """
    Custom permission to allow only the owner of the object to edit or delete it.
    """

    # Overriding has_object_permission to define object-level access control
    def has_object_permission(self, request, view, obj):  
        # Check if the object's user field matches the currently logged-in user
        # If they match, the user is allowed to edit or delete the object
        return obj.user == request.user  
