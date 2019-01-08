# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db import models

def upload_location(instancia, filename):
	return "CV/%s/%s" %(instancia.id, filename)

# Create your models here.
class Gasto(models.Model):
	numero = models.CharField(max_length=999999)
	referencia = models.CharField(max_length=100, blank=True)
	moneda = models.CharField(max_length=10, blank=True)
	fecha = models.DateTimeField(auto_now_add=True, auto_now=False)
	total_final = models.DecimalField(max_digits=999999,decimal_places=2)
	nota = models.TextField(blank=True)
	comprador = models.ForeignKey(User)
	estatus = models.CharField(max_length=20, blank=True)


	def __unicode__(self):
		return self.referencia


class Detalleg(models.Model):
	gasto = models.ForeignKey(Gasto)
	proveedor = models.CharField(max_length=100,blank=True)
	rnc = models.CharField(max_length=20, blank=True)
	ncf = models.CharField(max_length=20, blank=True)
	detalle = models.TextField(blank=True)
	itbis = models.DecimalField(max_digits=999999,decimal_places=2)
	fecha = models.CharField(max_length=10)
	tipo = models.CharField(max_length=50)
	subtotal = models.DecimalField(max_digits=999999,decimal_places=2)
	total = models.DecimalField(max_digits=999999,decimal_places=2)
	estatus = models.CharField(max_length=20, blank=True)
	file = models.FileField(upload_to=upload_location, blank=True)


	def __unicode__(self):
		return self.ncf



