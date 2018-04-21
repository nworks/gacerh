# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


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

	def __unicode__(self):
		return self.user.username
