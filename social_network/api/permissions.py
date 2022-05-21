from rest_framework import permissions


class AuthorScoreAndFavoriteOrReadOnly(permissions.BasePermission):
    """Permission для понравившегося и избранного"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class AuthorArticleOrReadOnly(permissions.BasePermission):
    """Permission для новостей"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user
