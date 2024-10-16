"""Модуль, содержащий модели для управления постами."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Модель группы, содержащая информацию о заголовке, слагу и описании."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Возвращает заголовок группы в виде строки."""
        return self.title


class Post(models.Model):
    """Модель поста.

    Посты содержащие текст, дату публикации, автора,
    изображение и группу.
    """

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )  # поле для картинки
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        """Возвращает текст поста."""
        return self.text


class Comment(models.Model):
    """Модель комментария.

    Комментарии содержащие автора, связанный пост,
    текст и дату добавления.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
