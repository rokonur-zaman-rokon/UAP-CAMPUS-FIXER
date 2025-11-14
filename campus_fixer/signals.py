from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Issue
from .utils.sms import send_sms

@receiver(post_save, sender=Issue)
def issue_created_sms(sender, instance, created, **kwargs):
    if created:

        emergency_status = "🚨 EMERGENCY" if instance.is_emergency else "Normal"

        message = (
            f"New Issue Created!\n"
            f"Ticket: {instance.ticket_id}\n"
            f"Category: {instance.category}\n"
            f"Priority: {instance.priority}\n"
            f"Emergency: {emergency_status}"
        )

        send_sms(
            settings.SMS_API_KEY,
            message,
            settings.ADMIN_PHONE
        )
