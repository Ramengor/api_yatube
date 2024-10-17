"""Модуль управления правами доступа."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает доступ только автору для редактирования и удаления."""

    def has_object_permission(self, request, view, obj):
        """Проверяет авторизован ли пользователь."""
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
