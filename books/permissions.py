# books/permissions.py
from rest_framework.permissions import BasePermission

class IsBookOwner(BasePermission):
    """
    Object-level permission that only allows owners of a book to access or modify it.
    Assumes that each Book's 'author' is linked to a User via an Author instance.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the Book's author corresponds to the logged-in user's associated Author.
        return obj.author == getattr(request.user, 'author', None)
