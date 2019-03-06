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
from .forms import fechaform
from django.shortcuts import render
from ncf.models import Gasto, Detalleg
import datetime
from django.core.mail.message import EmailMessage


# Create your views here.
def compania(request):
	gasto = Gasto.objects.filter(comprador=request.user).order_by('-id');
	return render(request, 'gastotabla.html',{'gasto':gasto, 'gastos':gasto.all()})

def PDF(request, id=None):
	gastog = Gasto.objects.get(id=id);
	gasto = Detalleg.objects.filter(gasto=gastog);
	itbis = Detalleg.objects.filter(gasto=gastog).aggregate(Sum('itbis'))['itbis__sum']
	suma_total = Detalleg.objects.filter(gasto=gastog).aggregate(Sum('total'))['total__sum']
	subtotal = Detalleg.objects.filter(gasto=gastog).aggregate(Sum('subtotal'))['subtotal__sum']
	return render(request, 'PDF.html',{'gasto':gasto, 'gastos':gasto.all(),'subtotal':subtotal,'itbis':itbis,'suma_total':suma_total,'gastog':gastog})

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

	select = request.POST.get('select')

	detalle = request.POST.get('detalle')
	subtotal = request.POST.get('subtotal')

	itbis = Decimal(request.POST.get('itbis'))
	total = Decimal(request.POST.get('total'))
	gastot = Gasto.objects.get(id=id);
	gasto = Detalleg.objects.filter(gasto=gastot);

	subtotal = total - itbis

	solicit =  Detalleg.objects.create(gasto=gastot, rnc=rnc,ncf=ncf, fecha=fecha, detalle=detalle, subtotal=subtotal, itbis=itbis,total=total, estatus="No Procesado",tipo=select)
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

	main =  Gasto.objects.get(id=id);

	if suma_total is not None:
		main.total_final = suma_total
		main.save()
	else:
		main.total_final = 0
		main.save()
		print "suma igual cero"
	print "cambiando de pagina"

	record = {"id":objid, "gasto":gastot.id, "rnc":rnc,"ncf":ncf, "fecha":fecha, "detalle":detalle, "subtotal":subt, "itbis":itbis,"total":total, "estatus":"No Pagado", "suma_totalt":suma_total, "subtotalt":subtotalt, "itbist":itbist, 'tipo':select}
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


def removerdetalle(request):
	idview = request.POST.get('id')
	idview.replace(",", "")
	print idview
	gasto = Detalleg.objects.get(id=idview)
	gasto.delete()
	return render(request, 'detalletabla.html')

def admintable(request):
	if request.method == 'POST':
		mes = request.POST.get('mes')
		ano = request.POST.get('ano')
		print "entro al form"
		gasto1 = Gasto.objects.filter(fecha__year=int(ano)).filter(fecha__month=int(mes)).values_list('id', flat=True)
		gasto2 = Detalleg.objects.filter(gasto__in=gasto1)
		return render(request, 'adming.html',{'gasto':gasto2, 'gastos':gasto2.all()})

	elif request.method == 'GET':
		mes = request.GET.get('mes')
		ano = request.GET.get('ano')
		

		if mes == None:
			today = datetime.date.today()
			print today
			gasto1 = Gasto.objects.filter(fecha__year=today.year).filter(fecha__month=today.month).values_list('id', flat=True)
			print gasto1
			gasto2 = Detalleg.objects.filter(gasto__in=gasto1)
			return render(request, 'adming.html',{'gasto':gasto2, 'gastos':gasto2.all()})
		else:
			return export_excelfecha(request, mes, ano)
		

		



def pagos(request):
	today = datetime.date.today()
	gasto = Gasto.objects.filter(fecha__year=today.year).filter(fecha__month=today.month)
	return render(request, 'adminpago.html',{'gasto':gasto, 'gastos':gasto.all()})


def past(request):
	today = datetime.date.today()
	gasto = Gasto.objects.filter(fecha__year=today.year).filter(fecha__month=today.month-1)
	return render(request, 'adminpago.html',{'gasto':gasto, 'gastos':gasto.all()})


def pay(request):
	idview = request.POST.get('id')
	print idview
	print "entro al pago"
	gasto = Detalleg.objects.get(id=idview);
	gasto.estatus = "PROCESADO"
	gasto.save()
	return render(request, 'adminpago.html',{'gasto':gasto})



def reabierto(request,id=None):
	idview = id.replace(',', '')
	print idview
	print "abriendo gasto de nuevo"
	gasto = Gasto.objects.get(id=idview);
	gasto.estatus = "Abierto"
	gasto.save()

	gastod = Detalleg.objects.filter(gasto=gasto);
	for obj in gastod:
		obj.estatus = "Abierto"
		obj.save()

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
	
	correo = EmailMessage()
	correo.subject = " Reporte de Gastos ACERH"
	correo.body = """Hola Administrador,
	El usuario """+ gasto.comprador.username +','+ gasto.comprador.first_name + ' ' + gasto.comprador.last_name +""", acaba de finalizar el reporte """+ gasto.referencia + """ de un monto total de """+ str(gasto.total_final) + """
	Notificaciones de Gastos ACERH """
	correo.to = ['controlinterno@acerhcaribe.com']
	correo.send()


	return render(request, 'adming.html',{'gasto':gasto})


def range_date(request):
	fechaini = request.POST.get('fechaini')
	fechafin = request.POST.get('fechafin')
	gasto = Gasto.objects.filter(fecha__range=[fechaini, fechafin])
	print "fechas"
	print gasto
	return render(request, 'adming2.html',{'gasto':gasto, 'gastos':gasto.all()})


def export_excelfecha(request, mes, ano):
	#Llamada a la libreria para escribir en bits
	output = io.BytesIO()

	#Se inicializa el workbook de excel en cache
	workbook = Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet()

	#se setea la variable cell con 8 para que empieze a escribir desde la celda 8
	cell = 1
	#ciclo que busca todos los objetos con estatus 195(por enviar) para ser escritos en el excel
	hoy = datetime.date.today()
	print hoy
	gasto1 = Gasto.objects.filter(fecha__year=int(ano)).filter(fecha__month=int(mes)).values_list('id', flat=True)
	print gasto1
	gasto2 = Detalleg.objects.filter(gasto__in=gasto1)




	for obj in gasto2:
		gasto3 = Gasto.objects.get(id=obj.gasto.id)
		#indica desde que celda se escribe el titulo de los id de los objetos
		worksheet.write_string(cell,0, str(obj.id))
		#indica desde que celda se escribiran los emails
		worksheet.write_string(cell,1, obj.rnc)
		#indica desde que celda se escribiran los codigos de pss
		worksheet.write_string(cell,2, str(obj.ncf))
		#indica desde que celda se escribiran la ruta de los archivos
		worksheet.write_string(cell,3, obj.fecha)
		#escribre el username
		worksheet.write_string(cell,4, obj.detalle)

		worksheet.write_string(cell,5, str(obj.subtotal))

		worksheet.write_string(cell,6, str(obj.itbis))

		worksheet.write_string(cell,7, str(obj.total))

		worksheet.write_string(cell,8, obj.estatus)

		worksheet.write_string(cell,9, gasto3.comprador.username)

		worksheet.write_string(cell,10, gasto3.referencia)

		#Se realiza el aumento de la celda para seguir escribiendo hacia abajo
		cell = cell + 1




	#Variable que define el estilo de negrita
	bold = workbook.add_format({'bold': 1}) #letra negrita
	#Variable que define el tamanio de las letras
	size = workbook.add_format({'font_size': 20})
	#Define el color rojo de las celdas
	green = workbook.add_format({'bg_color': 'red', 'bold': 1})
	#Escriben los enunciados del reporte de excel y ejecuta el logo
	worksheet.set_column('A:A', 5)
	worksheet.write('A1', 'ID',green)
	worksheet.set_column('B:B', 20)
	worksheet.write('B1', 'rnc',green)
	worksheet.set_column('C:C', 20)
	worksheet.write('C1', 'ncf',green)
	worksheet.set_column('D:D', 10)
	worksheet.write('D1', 'fecha',green)
	worksheet.set_column('E:E', 50)
	worksheet.write('E1', 'detalle',green)
	worksheet.set_column('F:F', 20)
	worksheet.write('F1', 'subtotal',green)
	worksheet.set_column('G:G', 20)
	worksheet.write('G1', 'itbis',green)
	worksheet.set_column('H:H', 20)
	worksheet.write('H1', 'total',green)
	worksheet.set_column('I:I', 20)
	worksheet.write('I1', 'estatus',green)
	worksheet.set_column('J:J', 20)
	worksheet.write('J1', 'usuario',green)
	worksheet.set_column('K:K', 20)
	worksheet.write('K1', 'referencia',green)



	#worksheet.add_table('B3:F7') #TABLA
	#Cierra el workbook del excel para ser guardado
	workbook.close()

	output.seek(0)
	#response que contiene el archivo xlsx que sera devuelto a la ventana del navegador
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=PagoReport.xlsx"

	#funcion de retorno
	return response
	


def novedadesreg (request, id=None):
	idview = id
	print id
	main =  Gasto.objects.all()

	
	return render(request, 'novedadesregistro.html',{'main':main})


def email(request):
	email = EmailMessage()
	email.subject = "Hola mensaje de prueba desde el servidor de acerh"
	email.body = "Coneccion totalmente lograda, prueba test #2"
	email.to = [ "nworks16@gmail.com"]
	email.send()