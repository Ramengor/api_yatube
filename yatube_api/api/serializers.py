"""Модуль сериализаторов для приложения API."""
from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Настройки сериализатора для модели Post."""

        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Настройки сериализатора для модели Comment."""

        model = Comment
        fields = ['id', 'author', 'post', 'text', 'created']
        read_only_fields = ['post']


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        """Настройки сериализатора для модели Group."""

        model = Group
        fields = ['id', 'title', 'slug', 'description']
