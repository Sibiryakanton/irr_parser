# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_main_app', '0011_auto_20170623_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='hour_shedule',
            field=models.ImageField(blank=True, null=True, upload_to='images/orders/shedules2017623188'),
        ),
        migrations.AlterField(
            model_name='ordermodel',
            name='week_shedule',
            field=models.ImageField(blank=True, null=True, upload_to='images/orders/shedules2017623188'),
        ),
    ]
