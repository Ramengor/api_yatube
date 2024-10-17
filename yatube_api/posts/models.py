"""Модуль, содержащий модели для управления постами."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Модель группы, содержащая информацию о заголовке, слагу и описании."""

    title = models.CharField(max_length=200, verbose_name='Название группы')
    slug = models.SlugField(unique=True, verbose_name='Слаг')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        """Возвращает заголовок группы в виде строки."""
        return self.title[:30]


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
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True,
        verbose_name='Группа'
    )

    def __str__(self):
        """Возвращает текст поста."""
        return self.text[:30]


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

    def __str__(self):
        """Возвращает текст комментария."""
        post_title = self.post.text[:30]
        author_name = self.author.username
        return f'{post_title} - {author_name} - {self.text[:30]}'
