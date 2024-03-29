from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.cache import cache
from datetime import datetime

from .models import UserEnrolled,Asset

@receiver(post_save, sender=UserEnrolled)
def book_change_handler(sender, instance, **kwargs):
    cache.set('has_changes', True)

@receiver(pre_delete, sender=UserEnrolled)
def book_delete_handler(sender, instance, **kwargs):
    cache.set('has_changes', True)
