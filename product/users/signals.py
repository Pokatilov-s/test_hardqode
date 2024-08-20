# NEW start
from django.db.models.signals import post_save
from django.dispatch import receiver
from product import settings
from .models import Balance


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_users(sender, instance, created, **kwargs):
    """Добавление баланса пользователю - студенту"""
    if created:
        Balance.objects.create(user=instance, amount=1000)

# NEW start
