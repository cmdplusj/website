from celery.decorators import task
from celery.utils.log import get_task_logger
from django.utils.html import strip_tags
from django.core import mail
from .models import Appointment
from datetime import datetime, timedelta

logger = get_task_logger(__name__)


@task(name="send_email_task")
def send_email_task(subject, message, to):
    """sends an email"""
    logger.info("Sent email")
    plain_message = strip_tags(message)
    from_email = 'Command+J <alerts.commandj@gmail.com>'
    return mail.send_mail(subject, plain_message, from_email, to, html_message=message)

