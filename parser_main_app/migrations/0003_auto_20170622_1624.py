# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-22 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_main_app', '0002_auto_20170622_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='day_shedule',
            field=models.ImageField(upload_to='images/orders/shedules20176221624'),
        ),
    ]