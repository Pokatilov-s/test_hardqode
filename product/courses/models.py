from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса',
    )
    # NEW start
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата создания'
    )
    is_available = models.BooleanField(
        default=True
    )
    # NEW end

    class Meta:
        db_table = 'courses'  # NEW
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    # NEW start
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='ID Курса',
        related_name='lessons'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name='Дата создания'
    )
    # NEW end

    class Meta:
        db_table = 'lessons'  # NEW
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    # TODO

    class Meta:
        db_table = 'groups'  # NEW
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
