# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ncf.models import Gasto, Detalleg
from users.models import UserP, Area
# Register your models here.
admin.site.register(Gasto)
admin.site.register(Detalleg)
admin.site.register(UserP)
admin.site.register(Area)

