"""Модуль представлений (views) для API."""
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.models import Post, Comment, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с постами."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Сохраняет новый пост с автором, указанным в запросе."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Обновляет существующий пост."""
        post = self.get_object()
        if post.author != self.request.user:
            raise PermissionDenied('Вы не можете редактировать чужие посты.')
        serializer.save()

    def perform_destroy(self, instance):
        """Удаляет пост, проверяя, что пользователь является его автором."""
        if instance.author != self.request.user:
            raise PermissionDenied('Вы не можете удалить чужой пост.')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Возвращает комментарии для указанного поста."""
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """Сохраняет новый комментарий с автором и постом."""
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

    def perform_update(self, serializer):
        """Обновляет существующий комментарий."""
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied(
                'Вы не можете редактировать чужие комментарии.'
            )
        serializer.save()

    def perform_destroy(self, instance):
        """Удаляет комментарий."""
        if instance.author != self.request.user:
            raise PermissionDenied('Вы не можете удалить чужой комментарий.')
        instance.delete()


class GroupViewSet(ReadOnlyModelViewSet):
    """Вьюсет для работы с группами."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
