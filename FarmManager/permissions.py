"""
Custom permissions for the Farm Manager application
"""

from rest_framework import permissions


class AdminGetOnlyPermission(permissions.BasePermission):
    """
    Custom permission that allows:
    - GET requests only for authenticated admin users
    - All other operations are allowed without authentication (maintains existing behavior)
    """
    
    def has_permission(self, request, view):
        # For GET requests, require admin authentication
        if request.method == 'GET':
            return (
                request.user and 
                request.user.is_authenticated and 
                request.user.is_staff
            )
        
        # For all other methods (POST, PUT, PATCH, DELETE), allow access
        # This maintains the existing behavior where these operations don't require auth
        return True
    
    def has_object_permission(self, request, view, obj):
        # For GET requests on specific objects, require admin authentication
        if request.method == 'GET':
            return (
                request.user and 
                request.user.is_authenticated and 
                request.user.is_staff
            )
        
        # For all other methods, allow access
        return True


class ReadOnlyAdminPermission(permissions.BasePermission):
    """
    Permission for read-only viewsets (like choice models) that only allows admin access
    """
    
    def has_permission(self, request, view):
        # Only allow GET requests and only for admin users
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user and 
                request.user.is_authenticated and 
                request.user.is_staff
            )
        
        # Deny all write operations
        return False 