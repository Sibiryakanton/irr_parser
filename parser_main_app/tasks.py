from celery import task, shared_task
from django.core.mail import send_mail
from .models import Order


@task
def test_task(number):
    print('hi, there is a number of order: {}'.format(number))


@shared_task
def test_shared_task():
    print('If you see that, the shared task and Celery in general works fine.')