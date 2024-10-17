"""Модуль представлений (views) для API."""
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.models import Post, Comment, Group
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешает доступ только автору для редактирования и удаления"""

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

    # def perform_update(self, serializer):
    #     """Обновляет существующий пост."""
    #     post = self.get_object()
    #     if post.author != self.request.user:
    #         raise PermissionDenied('Вы не можете редактировать чужие посты.')
    #     serializer.save()
    #
    # def perform_destroy(self, instance):
    #     """Удаляет пост, проверяя, что пользователь является его автором."""
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Вы не можете удалить чужой пост.')
    #     instance.delete()


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
        # post_id = self.kwargs['post_id']
        post = self.get_post()
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        """Сохраняет новый комментарий с автором и постом."""
        # post_id = self.kwargs['post_id']
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    # def perform_update(self, serializer):
    #     """Обновляет существующий комментарий."""
    #     comment = self.get_object()
    #     if comment.author != self.request.user:
    #         raise PermissionDenied(
    #             'Вы не можете редактировать чужие комментарии.'
    #         )
    #     serializer.save()
    #
    # def perform_destroy(self, instance):
    #     """Удаляет комментарий."""
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Вы не можете удалить чужой комментарий.')
    #     instance.delete()


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
