"""Модуль представлений (views) для API."""
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.models import Post, Comment, Group
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает доступ только автору для редактирования и удаления."""

    def has_object_permission(self, request, view, obj):
        """Проверяет авторизован ли пользователь."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Сохраняет новый пост с автором, указанным в запросе."""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def get_post(self):
        """Возвращает объект поста или вызывает 404."""
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        """Возвращает комментарии для указанного поста."""
        post = self.get_post()
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """Сохраняет новый комментарий с автором и постом."""
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
