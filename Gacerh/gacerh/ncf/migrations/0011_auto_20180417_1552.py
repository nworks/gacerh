# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-17 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncf', '0010_auto_20180417_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalleg',
            name='fecha',
            field=models.CharField(max_length=10),
        ),
    ]
