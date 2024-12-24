from django.db import models
from django.contrib.auth import get_user_model
from blogicum.models import BaseModel
from django.utils.timezone import now

User = get_user_model()


class Category(BaseModel):
    title = models.CharField("Заголовок", max_length=256)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=("Идентификатор страницы для URL; "
                   "разрешены символы латиницы, "
                   "цифры, дефис и подчёркивание."),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(BaseModel):
    name = models.CharField("Название места", max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(BaseModel):
    title = models.CharField("Заголовок", max_length=256)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text="Если установить дату и время в будущем — "
        "можно делать отложенные публикации.",
    )
    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        null=True,
        related_name='posts',
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category, null=True,
        related_name='posts',
        on_delete=models.SET_NULL,
        verbose_name="Категория"
    )

    @staticmethod
    def get_published_posts():
        return Post.objects.filter(
            is_published=True,
            category__is_published=True,
            pub_date__date__lte=now(),
        )

    class Meta:
        ordering = ["-id"]
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
