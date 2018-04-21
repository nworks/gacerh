# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Sum
from decimal import Decimal
from django.http import HttpResponseRedirect ,HttpResponse
from django.http import JsonResponse
from xlsxwriter.workbook import Workbook
import sys
import StringIO
import io
import os
from datetime import datetime

from django.shortcuts import render
from ncf.models import Gasto, Detalleg
import datetime
# Create your views here.
def compania(request):
	gasto = Gasto.objects.filter(comprador=request.user);
	return render(request, 'gastotabla.html',{'gasto':gasto, 'gastos':gasto.all()})

def newgasto(request):
	gasto = Detalleg.objects.filter(gasto=1);
	return render(request, 'vacantetabla0.html',{'gasto':gasto, 'gastos':gasto.all()})

def gastodetalle (request, id=None):
	idview = id
	print id
	main =  Gasto.objects.get(id=id);
	gasto = Detalleg.objects.filter(gasto=idview);
	itbis = Detalleg.objects.filter(gasto=idview).aggregate(Sum('itbis'))['itbis__sum']
	suma_total = Detalleg.objects.filter(gasto=idview).aggregate(Sum('total'))['total__sum']
	subtotal = Detalleg.objects.filter(gasto=idview).aggregate(Sum('subtotal'))['subtotal__sum']
	if suma_total is not None:
		main.total_final = suma_total
		main.save()
	else:
		main.total_final = 0
		main.save()
		print "suma igual cero"
	print "cambiando de pagina"
	return render(request, 'detalletabla.html',{'subtotal':subtotal,'main':main,'itbis':itbis,'suma_total':suma_total,'gasto':gasto, 'gastos':gasto.all()})



def detalleadmin (request, id=None):
	idview = id
	print id
	main =  Gasto.objects.get(id=id);
	gasto = Detalleg.objects.filter(gasto=idview);
	itbis = Detalleg.objects.filter(gasto=idview).aggregate(Sum('itbis'))['itbis__sum']
	suma_total = Detalleg.objects.filter(gasto=idview).aggregate(Sum('total'))['total__sum']
	subtotal = Detalleg.objects.filter(gasto=idview).aggregate(Sum('subtotal'))['subtotal__sum']
	if suma_total is not None:
		main.total_final = suma_total
		main.save()
	else:
		main.total_final = 0
		main.save()
		print "suma igual cero"
	print "cambiando de pagina"
	return render(request, 'detalleadmin.html',{'subtotal':subtotal,'main':main,'itbis':itbis,'suma_total':suma_total,'gasto':gasto, 'gastos':gasto.all()})

def creargasto (request):
	id = request.POST.get('id')
	print id
	rnc = request.POST.get('rnc')
	print rnc
	ncf = request.POST.get('ncf')
	fecha = request.POST.get('fecha')

	detalle = request.POST.get('detalle')
	subtotal = request.POST.get('subtotal')

	itbis = Decimal(request.POST.get('itbis'))
	total = Decimal(request.POST.get('total'))
	gastot = Gasto.objects.get(id=id);
	gasto = Detalleg.objects.filter(gasto=gastot);

	subtotal = total - itbis

	solicit =  Detalleg.objects.create(gasto=gastot, rnc=rnc,ncf=ncf, fecha=fecha, detalle=detalle, subtotal=subtotal, itbis=itbis,total=total, estatus="No Procesado")
	solicit.save()
	objid = solicit.id
	Gastos = []

	subt = solicit.subtotal
	gasto = Detalleg.objects.filter(gasto=id);
	itbist = Detalleg.objects.filter(gasto=id).aggregate(Sum('itbis'))['itbis__sum']
	suma_totalt = Detalleg.objects.filter(gasto=id).aggregate(Sum('total'))['total__sum']
	subtotalt = Detalleg.objects.filter(gasto=id).aggregate(Sum('subtotal'))['subtotal__sum']
	suma_total = Detalleg.objects.filter(gasto=id).aggregate(Sum('total'))['total__sum']
	subtotal2 = Detalleg.objects.filter(gasto=id).aggregate(Sum('subtotal'))['subtotal__sum']

	record = {"id":objid, "gasto":gastot.id, "rnc":rnc,"ncf":ncf, "fecha":fecha, "detalle":detalle, "subtotal":subt, "itbis":itbis,"total":total, "estatus":"No Pagado", "suma_totalt":suma_total, "subtotalt":subtotalt, "itbist":itbist}
	Gastos.append(record)
	response_gasto={"Gastos":Gastos}
	print "Solicitud Atendida"
	return JsonResponse(response_gasto , safe=False)


def creargastobase (request):
	referencia = request.POST.get('referencia')
	print referencia
	referencia = request.POST.get('referencia')
	moneda = request.POST.get('moneda')
	print moneda

	solicit =  Gasto.objects.create(referencia=referencia, moneda=moneda,estatus='Abierto', total_final=0, comprador=request.user)
	solicit.save()
	print "Solicitud Atendida"
	return render(request, 'detalletabla.html')


def removergasto(request):
	idview = request.POST.get('id')
	print idview
	gasto = Gasto.objects.get(id=idview , comprador=request.user)
	gasto.delete()
	return render(request, 'gastotabla.html')


def removerdetalle(request, id=None):
	idview = request.POST.get('id')
	print idview
	gasto = Detalleg.objects.get(id=idview)
	gasto.delete()
	return render(request, 'detalletabla.html')

def admintable(request):
	today = datetime.date.today()
	print today
	gasto1 = Gasto.objects.filter(fecha__year=today.year).filter(fecha__month=today.month).values_list('id', flat=True)
	print gasto1
	gasto2 = Detalleg.objects.filter(gasto__in=gasto1)
	return render(request, 'adming.html',{'gasto':gasto2, 'gastos':gasto2.all()})



def pagos(request):
	today = datetime.date.today()
	gasto = Gasto.objects.filter(fecha__year=today.year).filter(fecha__month=today.month)
	return render(request, 'adminpago.html',{'gasto':gasto, 'gastos':gasto.all()})


def pay(request):
	idview = request.POST.get('id')
	print idview
	print "entro al pago"
	gasto = Detalleg.objects.get(id=idview);
	gasto.estatus = "PROCESADO"
	gasto.save()
	return render(request, 'adminpago.html',{'gasto':gasto})


def paygasto(request):
	idview = request.POST.get('id')
	print idview
	print "entro al pago"
	gasto = Gasto.objects.get(id=idview);
	gasto.estatus = "PROCESADO"
	gasto.save()

	gastod = Detalleg.objects.filter(gasto=gasto);
	for obj in gastod:
		obj.estatus = "PROCESADO"
		obj.save()

	return render(request, 'adming.html',{'gasto':gasto})


def cerrargasto(request):
	idview = request.POST.get('id')
	print idview
	print "Cerrando gasto"
	gasto = Gasto.objects.get(id=idview);
	gasto.estatus = "CERRADO"
	gasto.save()
	return render(request, 'adming.html',{'gasto':gasto})


def range_date(request):
	fechaini = request.POST.get('fechaini')
	fechafin = request.POST.get('fechafin')
	gasto = Gasto.objects.filter(fecha__range=[fechaini, fechafin])
	print "fechas"
	print gasto
	return render(request, 'adming2.html',{'gasto':gasto, 'gastos':gasto.all()})
