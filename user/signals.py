from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from portfolio.models import Portfolio

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)


