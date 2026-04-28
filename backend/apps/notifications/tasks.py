from celery import shared_task
from django.core.mail import send_mail


@shared_task(name="send_email_notification")
def send_email_notification(subject, message, recipient_email):
    """Send email notification asynchronously via Celery."""
    send_mail(
        subject=subject,
        message=message,
        from_email="noreply@setupfx.com",
        recipient_list=[recipient_email],
        fail_silently=True,
    )
