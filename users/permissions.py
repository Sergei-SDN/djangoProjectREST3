from rest_framework import permissions


class IsOwnerOrReadOnlyProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем пользователям (авторизованным и неавторизованным)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить редактирование только владельцу профиля
        return obj.user == request.user
