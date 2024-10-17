"""Конфигурация приложения для управления постами."""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Конфигурация приложения Posts."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
    verbose_name = 'Посты'
