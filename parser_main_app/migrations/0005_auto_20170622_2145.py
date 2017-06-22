# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-22 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_main_app', '0004_auto_20170622_1712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='day_shedule',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='week_shedule',
            field=models.ImageField(null=True, upload_to='images/orders/shedules20176222145'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='hour_shedule',
            field=models.ImageField(null=True, upload_to='images/orders/shedules20176222145'),
        ),
    ]