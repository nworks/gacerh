# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-06 03:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NominaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idacerh', models.CharField(blank=True, max_length=99999999)),
                ('idnomina', models.CharField(blank=True, max_length=99999999)),
                ('numero_nomina', models.CharField(blank=True, max_length=99999999)),
                ('periodo', models.CharField(blank=True, max_length=10)),
                ('concepto1', models.CharField(blank=True, max_length=50)),
                ('concepto2', models.CharField(blank=True, max_length=50)),
                ('concepto3', models.CharField(blank=True, max_length=50)),
                ('concepto4', models.CharField(blank=True, max_length=50)),
                ('concepto5', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Novedades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(blank=True, max_length=20)),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('codigo', models.CharField(blank=True, max_length=20)),
                ('h115', models.CharField(blank=True, max_length=20)),
                ('h135', models.CharField(blank=True, max_length=20)),
                ('h_descuento', models.CharField(blank=True, max_length=20)),
                ('feriado', models.CharField(blank=True, max_length=20)),
                ('inventivos', models.CharField(blank=True, max_length=20)),
                ('comisiones', models.CharField(blank=True, max_length=20)),
                ('ausencias', models.CharField(blank=True, max_length=20)),
                ('descuento_hora', models.CharField(blank=True, max_length=20)),
                ('descuento_almuerzo', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(blank=True, max_length=20)),
                ('empresa', models.CharField(blank=True, max_length=100)),
                ('puesto', models.CharField(blank=True, max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('celular', models.CharField(blank=True, max_length=20)),
                ('supervisor', models.TextField(blank=True)),
                ('email_super', models.CharField(blank=True, max_length=100)),
                ('sup_level', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
