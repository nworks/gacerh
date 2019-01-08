# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class NominaDetalle(models.Model):
	idacerh = models.CharField(max_length=99999999, blank=True)
	idnomina = models.CharField(max_length=99999999, blank=True)
	numero_nomina = models.CharField(max_length=99999999, blank=True)
	periodo = models.CharField(max_length=10, blank=True)
	concepto1 = models.CharField(max_length=50, blank=True)
	concepto2 = models.CharField(max_length=50, blank=True)
	concepto3 = models.CharField(max_length=50, blank=True)
	concepto4 = models.CharField(max_length=50, blank=True)
	concepto5 = models.CharField(max_length=50, blank=True)
	
	def __unicode__(self):
		return self.nombre


# Create your models here.
class UserP(models.Model):
	user = models.OneToOneField(User)
	cedula = models.CharField(max_length=20, blank=True)
	empresa = models.CharField(max_length=100, blank=True)
	puesto = models.CharField(max_length=100, blank=True)
	telefono = models.CharField(max_length=20, blank=True)
	celular = models.CharField(max_length=20, blank=True)
	supervisor = models.TextField(blank=True)
	email_super = models.CharField(max_length=100, blank=True)
	sup_level = models.CharField(max_length=100, blank=True)


	def __unicode__(self):
		return self.user.username


class Novedades(models.Model):
	cedula = models.CharField(max_length=20, blank=True)
	nombre = models.CharField(max_length=50, blank=True)
	codigo = models.CharField(max_length=20, blank=True)
	h115 = models.CharField(max_length=20, blank=True)
	h135 = models.CharField(max_length=20, blank=True)
	h_descuento = models.CharField(max_length=20, blank=True)
	feriado = models.CharField(max_length=20, blank=True)
	inventivos = models.CharField(max_length=20, blank=True)
	comisiones = models.CharField(max_length=20, blank=True)
	ausencias = models.CharField(max_length=20, blank=True)
	descuento_hora = models.CharField(max_length=20, blank=True)
	descuento_almuerzo = models.CharField(max_length=20, blank=True)