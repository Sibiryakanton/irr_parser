# coding: utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irr_parser.settings')

app = Celery('irr_parser')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
