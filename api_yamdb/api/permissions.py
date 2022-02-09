from rest_framework import permissions

from reviews.models import ADMIN, MODER, USER


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """
    Permission that allows the administrator, moderator and owner to change the
    object or just read objects by anyone(even user without tokens).
    """

    def has_permission(self, request, view):
        try:
            if (
                request.method in permissions.SAFE_METHODS
                or request.user.role == USER
                or request.user.role == ADMIN
                or request.user.role == MODER
                or request.user.is_superuser == 1
            ):
                return True
        except AttributeError:
            return False

    def has_object_permission(self, request, view, obj):
        try:
            if (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == ADMIN
                or request.user.role == MODER
                or request.user.is_superuser == 1
            ):
                return True
        except AttributeError:
            return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows the administrator to change the object
    or just read objects by anyone(even user without tokens).
    """
    def has_permission(self, request, view):
        try:
            if (
                request.method in permissions.SAFE_METHODS
                or request.user.role == ADMIN
                or request.user.is_superuser == 1
            ):
                return True
        except AttributeError:
            return False


class IsOnlyAdmin(permissions.BasePermission):
    """
    Permission that allows only administrator to do everything and nobody else.
    """
    def has_permission(self, request, view):
        try:
            if (
                request.user.role == ADMIN
                or request.user.is_superuser == 1
            ):
                return True
        except AttributeError:
            return False
