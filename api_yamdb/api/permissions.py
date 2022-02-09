from rest_framework import permissions


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """
    Permission that allows the administrator, moderator and owner to change the
    object or just read objects by anyone(even user without tokens).
    """

    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_user
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user.is_superuser)
        ):
            return True

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (obj.author == request.user
                 or request.user.is_admin
                 or request.user.is_moderator
                 or request.user.is_superuser)
        ):
            return True


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows the administrator to change the object
    or just read objects by anyone(even user without tokens).
    """
    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        ):
            return True


class IsOnlyAdmin(permissions.BasePermission):
    """
    Permission that allows only administrator to do everything and nobody else.
    """
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_superuser)
        ):
            return True
