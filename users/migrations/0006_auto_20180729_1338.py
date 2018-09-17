# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-29 17:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_userp_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('supervisor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='area',
            name='supervisor',
        ),
        migrations.AlterField(
            model_name='userp',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Area2'),
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]