from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    message = "У вас недостаточно прав."

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsModerator(BasePermission):
    message = "У вас недостаточно прав."

    def has_permission(self, request, view):
        if request.user.role == UserRoles.MODERATOR:
            return True
        return False


class IsPublic(BasePermission):
    message = "Не опубликовано."

    def has_object_permission(self, request, view, obj):
        return obj.is_public
