# tasks.py

from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Status

@shared_task
def remove_old_statuses():
    # Calculate the date 24 hours ago
    now = timezone.now()
    cutoff_date = now - timedelta(hours=24)

    # Delete status updates older than 24 hours
    Status.objects.filter(created__lt=cutoff_date).delete()
