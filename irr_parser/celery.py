from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irr_parser.settings')
app = Celery('irr_parser')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()