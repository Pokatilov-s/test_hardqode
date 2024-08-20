from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from courses.models import Course  # NEW
from product import settings  # NEW


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    # NEW
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='Пользователь'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Бонусы'

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
        db_table = 'balances'  # NEW
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    # NEW start
    def __str__(self):
        return f'Баланс для пользователя {self.user} равен {self.amount}'


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""
    # NEW start
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    # NEW end

    class Meta:
        db_table = 'subscriptions'  # NEW
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
        # NEW
        constraints = [
            models.UniqueConstraint(fields=('user', 'course'), name='unique_user_course')
        ]
        # NEW end
