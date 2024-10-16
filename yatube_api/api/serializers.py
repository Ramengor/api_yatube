"""Модуль сериализаторов для приложения API."""
from rest_framework import serializers

from posts.models import Post, Comment, Group


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.SerializerMethodField()

    class Meta:
        """Настройки сериализатора для модели Post."""

        model = Post
        fields = ['id', 'text', 'pub_date', 'author', 'image', 'group']

    def get_author(self, obj):
        """Возвращает имя пользователя автора поста."""
        return obj.author.username


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Настройки сериализатора для модели Comment."""

        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']
        read_only_fields = ['author', 'post', 'created']

    def get_author(self, obj):
        """Возвращает имя пользователя автора комментария."""
        return obj.author.username


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Настройки сериализатора для модели Group."""

        model = Group
        fields = ['id', 'title', 'slug', 'description']
