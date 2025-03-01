from django.contrib.auth import get_user_model
from django.db import models


LENGTH_CHARFIELD = 256
NUMBER_OF_CHARS = 15


# Модель пользователя
User = get_user_model()


class CreatedPublishedModel(models.Model):
    """
    Абстрактный класс, который добавляет к
    моделям поля is_published и creates_at.
    """

    is_published = models.BooleanField(
        default=True,
        blank=False,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class Category(CreatedPublishedModel):
    """Модель описывает категорию поста."""

    title = models.CharField(
        max_length=LENGTH_CHARFIELD,
        blank=False,
        verbose_name='Заголовок'
    )
    description = models.TextField(blank=False, verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:NUMBER_OF_CHARS]


class Location(CreatedPublishedModel):
    """Модель описывает локацию поста."""

    name = models.CharField(
        max_length=LENGTH_CHARFIELD,
        blank=False,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:NUMBER_OF_CHARS]


class Post(CreatedPublishedModel):
    """Модель описывает отдельный пост в проекте Блогикум."""

    title = models.CharField(
        max_length=LENGTH_CHARFIELD,
        blank=False,
        verbose_name='Заголовок'
    )
    text = models.TextField(blank=False, verbose_name='Текст')
    pub_date = models.DateTimeField(
        blank=False,
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем —'
                   ' можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(
        verbose_name='Фото',
        blank=True,
        upload_to='blog_images'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:NUMBER_OF_CHARS]
