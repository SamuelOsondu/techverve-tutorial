from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_task(username, email):
    message = f"Hi {username}, thank you for registering to our site"
    subject = "Email Sending for registeration"

    send_mail(subject,
              message,
              settings.DEFAULT_FROM_EMAIL,
              [email],
              fail_silently=False
              )

    return "Email sent successfully"



