# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-06 00:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu', '0003_offering_is_enrollable'),
    ]

    operations = [
        migrations.AddField(
            model_name='offering',
            name='available_capacity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
