# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from users.forms import LoginForm, UsuarioForm2, UserPr
from django.template import RequestContext
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from users.models import UserP
from ncf.models import Gasto, Detalleg
from django.contrib.auth.models import User
from xlsxwriter.workbook import Workbook
import sys
import StringIO
import io
import os
from datetime import datetime
import datetime
from django.core.mail.message import EmailMessage
# Create your views here.

def user_detail(request):

	return render(request, 'profile.html')



def user_edit(request):
	if request.method == 'POST':
		id = request.POST.get('id')
		telefono = request.POST.get('telefono')
		celular = request.POST.get('celular')
		supervisor = request.POST.get('supervisor')
		email_sup = request.POST.get('email_sup')


		print id
		print telefono
		print celular
		print email_sup
		user = User.objects.get(id=id)
		obj = UserP.objects.get(user=user)
		print user
		print obj.user
		obj.telefono = telefono
		obj.celular = celular
		obj.supervisor = supervisor
		obj.email_super = email_sup
		obj.save()
		return render(request, 'editprofile.html')

	return render(request, 'editprofile.html')


def LoginRequest(request):
	message = "Credenciales invalidas o No registradas"
	# Si el usuario ya ha iniciado sesion anteriormente.
	if request.user.is_authenticated():
		if request.user.is_staff:
			return HttpResponseRedirect('/pagos')
		else:
			return HttpResponseRedirect('/gastos')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		# Si el formulario es valido, iniciar la sesion y redireccionar
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			usuario = authenticate(username=username,password=password)
			if usuario is not None:
				login(request,usuario)
				if request.user.is_staff:
					return HttpResponseRedirect('/pagos')
				else:
					return HttpResponseRedirect('/gastos')
			# De lo contrario devolver al Login
			else:
				render(request, "loginmaterial.html", {'form':form})
				return render(request, "loginmaterial.html", {'form':form, 'message':message})
		# Si el formulario es invalido devolver al login
		else:

			return render(request, "loginmaterial", {'form':form } )
	else:
		form = LoginForm()
		context = {'form':form}
		return render(request, "loginmaterial.html", {'form':form})

def LogoutRequest(request):
	logout(request)
	return HttpResponseRedirect('/login')



def register(request):
	context = RequestContext(request)
	registered = False
	message = ""
	if request.method == 'POST':
		user_form = UsuarioForm2(data=request.POST)
		profile_form = UserPr(data=request.FILES)
		data2 = request.POST['username']
		if User.objects.filter(username=data2).exists():
			message = "Este Username ya se encuentra en uso, intente otro"
			return render (request,'registerbeta.html',{'user_form':user_form, 'profile_form': profile_form, 'message':message})


		data = request.POST['email']
		if User.objects.filter(email=data).exists():
			message = "Este correo electronico fue regustrado"
			return render (request,'registerbeta.html',{'user_form':user_form, 'profile_form': profile_form, 'message':message})



		else:
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save()
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.save()
				registered = True
				username = user_form.cleaned_data['username'].encode('utf8')
				password = user_form.cleaned_data['password'].encode('utf8')
				if 'file' in request.FILES:
					profile.file = request.FILES['file']
				else:
					profile.file = static('/nocv.txt')

				if 'picture' not in request.FILES:
					profile.picture =  static('/user.png')
				else:
					profile.picture = request.FILES['picture']

				profile.cedula = request.POST['cedula'].encode('utf8')
				profile.sexo = request.POST['sexo'].encode('utf8')
				profile.idioma = request.POST['idioma'].encode('utf8')
				profile.carrera = request.POST['carrera'].encode('utf8')
				profile.ar_int = request.POST['ar_int'].encode('utf8')
				profile.salario = request.POST['salario'].encode('utf8')
				profile.telefono = request.POST['telefono'].encode('utf8')
				profile.localidad = request.POST['localidad'].encode('utf8')
				profile.estudio = request.POST['estudio'].encode('utf8')
				profile.edad = request.POST['edad'].encode('utf8')
				profile.experiencia = request.POST['experiencia'].encode('utf8')
				profile.nacionalidad = request.POST['nacionalidad'].encode('utf8')
				profile.universidad = request.POST['universidad'].encode('utf8')
				profile.licencia = request.POST['licencia'].encode('utf8')
				profile.cat_licen = request.POST['cat_licen'].encode('utf8')
				profile.pais_apli = request.POST['pais_apli'].encode('utf8')

				profile.save()
				usuario = authenticate(username=username,password=password)
				login(request,usuario)
				return HttpResponseRedirect('/vacantes')

	else:
		user_form = UsuarioForm2()
		profile_form = UserPr()
		return render (request,'register.html',{'user_form':user_form, 'profile_form': profile_form})



def activate(request):
	user = User.objects.filter(is_active=0)

	return render (request,'activate.html',{'user':user, 'users':user.all()})

def active(request):
	id = request.POST.get('id')
	user2 = User.objects.get(id=id)
	user2.is_active=1
	user2.save()

	print 'usuario activado'

	correo = EmailMessage()
	correo.subject = "Confirmación de acceso Portal Gastos"
	correo.body = """¡Bienvenido!
    Su solicitud fue confirmada. Ya puede ingresar al portal y registrar sus gastos, compras o
    consumos de tarjeta.
    Siempre a la orden.
    Equipo ACERH """
	correo.to = [user2.email]
	correo.send()


    

	user = User.objects.filter(is_active=0)
	return render (request,'activate.html',{'user':user, 'users':user.all()})


def register2(request):
	if request.method == 'POST':
		codigo = request.POST.get('codigo')
		password = request.POST.get('password')
		nombres = request.POST.get('nombres')
		apellidos = request.POST.get('apellidos')
		cedula = request.POST.get('cedula')
		empresa = request.POST.get('empresa')
		puesto = request.POST.get('puesto')
		email = request.POST.get('email')
		telefono = request.POST.get('telefono')
		celular = request.POST.get('celular')
		supervisor = request.POST.get('supervisor')
		sup_email = request.POST.get('sup_email')
		sup_level2 = '1'

		newuser = User.objects.create(first_name= nombres, last_name= apellidos, username = codigo,email=email)
		newuser.is_active = False
		newuser.set_password(password)
		newuser.save()


		print("usuario creado")

		profile = UserP.objects.create(user = newuser ,cedula= cedula, empresa=empresa, puesto=puesto,  telefono=telefono, celular=celular,supervisor=supervisor,email_super=sup_email,sup_level=sup_level2)
		profile.save()

		print("perfil creado")

		print("preparando correo")

		correo = EmailMessage()
		correo.subject = "Solicitud acceso Gastos ACERH"
		correo.body = """Hola """+ nombres + ' ' + apellidos +""",
        Hemos recibido tu solicitud de acceso a nuestro portal de gastos, tan pronto nuestro
        equipo de gestores o el administrador valide la información enviada, te notificamos
        nuevamente confirmando o rechazando tu solicitud.
        Recordando que tu usuario es: """ + codigo + """ y la contraseña es: """+ password +""".
        Gracias por utilizar nuestros servicios.
        Equipo ACERH """
		correo.to = [email]
		correo.send()

		correo = EmailMessage()
		correo.subject = "Solicitud acceso Gastos ACERH"
		correo.body = """Hola Administrador,
        Tienes una solicitud de acceso en el Portal de Gastos ACERH.
        Usuario:"""+ codigo + """
        Nombre:"""+ nombres + ' ' + apellidos +"""
        Email:"""+ email +""" 
        Empresa:"""+ empresa + """ """
		correo.to = ['controlinterno@acerhcaribe.com']
		correo.send()

		print("correo enviado")
		return render (request,'register.html')
	else:

		return render (request,'register.html')



def export_excel(request):
	#Llamada a la libreria para escribir en bits
	output = io.BytesIO()

	#Se inicializa el workbook de excel en cache
	workbook = Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet()

	#se setea la variable cell con 8 para que empieze a escribir desde la celda 8
	cell = 8
	#ciclo que busca todos los objetos con estatus 195(por enviar) para ser escritos en el excel
	hoy = datetime.date.today()
	print hoy
	gasto1 = Gasto.objects.filter(fecha__year=hoy.year).filter(fecha__month=hoy.month).values_list('id', flat=True)
	print gasto1
	gasto2 = Detalleg.objects.filter(gasto__in=gasto1)




	for obj in gasto2:
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

		#Se realiza el aumento de la celda para seguir escribiendo hacia abajo
		cell = cell + 1




	#Variable que define el estilo de negrita
	bold = workbook.add_format({'bold': 1}) #letra negrita
	#Variable que define el tamanio de las letras
	size = workbook.add_format({'font_size': 20})
	#Define el color rojo de las celdas
	green = workbook.add_format({'bg_color': 'red', 'bold': 1})
	#Escriben los enunciados del reporte de excel y ejecuta el logo
	worksheet.write('C5', 'Reporte en excel de Acerh, Detalle de pago',size)
	worksheet.insert_image('B4', 'static/plugins/logo2.png', {'x_scale': 0.3, 'y_scale': 0.3})
	worksheet.set_column('A:A', 5)
	worksheet.write('A8', 'ID',green)
	worksheet.set_column('B:B', 50)
	worksheet.write('B8', 'rnc',green)
	worksheet.set_column('C:C', 40)
	worksheet.write('C8', 'ncf',green)
	worksheet.set_column('D:D', 100)
	worksheet.write('D8', 'fecha',green)
	worksheet.set_column('E:E', 100)
	worksheet.write('E8', 'detalle',green)
	worksheet.set_column('F:F', 100)
	worksheet.write('F8', 'subtotal',green)
	worksheet.set_column('G:G', 100)
	worksheet.write('G8', 'itbis',green)
	worksheet.set_column('H:H', 100)
	worksheet.write('H8', 'total',green)
	worksheet.set_column('I:I', 100)
	worksheet.write('I8', 'estatus',green)



	#worksheet.add_table('B3:F7') #TABLA
	#Cierra el workbook del excel para ser guardado
	workbook.close()

	output.seek(0)
	#response que contiene el archivo xlsx que sera devuelto a la ventana del navegador
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=PagoReport.xlsx"

	#funcion de retorno
	return response


def export_excel2(request):
	#Llamada a la libreria para escribir en bits
	output = io.BytesIO()

	#Se inicializa el workbook de excel en cache
	workbook = Workbook(output, {'in_memory': True})
	worksheet = workbook.add_worksheet()

	#se setea la variable cell con 8 para que empieze a escribir desde la celda 8
	cell = 8
	#ciclo que busca todos los objetos con estatus 195(por enviar) para ser escritos en el excel
	hoy = datetime.date.today()
	print hoy
	gasto1 = Gasto.objects.filter(fecha__year=hoy.year).filter(fecha__month=hoy.month)
	print gasto1



	for obj in gasto1:
		#indica desde que celda se escribe el titulo de los id de los objetos
		worksheet.write_string(cell,0, str(obj.id))
		#indica desde que celda se escribiran los emails
		worksheet.write_string(cell,1, str(obj.comprador))
		#indica desde que celda se escribiran los codigos de pss
		worksheet.write_string(cell,2, str(obj.referencia))
		#indica desde que celda se escribiran la ruta de los archivos
		worksheet.write_string(cell,3, str(obj.fecha))
		#escribre el username
		worksheet.write_string(cell,4, obj.moneda)

		worksheet.write_string(cell,5, str(obj.total_final))

		worksheet.write_string(cell,6, str(obj.estatus))


		#Se realiza el aumento de la celda para seguir escribiendo hacia abajo
		cell = cell + 1




	#Variable que define el estilo de negrita
	bold = workbook.add_format({'bold': 1}) #letra negrita
	#Variable que define el tamanio de las letras
	size = workbook.add_format({'font_size': 20})
	#Define el color rojo de las celdas
	green = workbook.add_format({'bg_color': 'red', 'bold': 1})
	#Escriben los enunciados del reporte de excel y ejecuta el logo
	worksheet.write('C5', 'Reporte en excel de Acerh, Detalle de pago',size)
	worksheet.insert_image('B4', 'static/plugins/logo2.png', {'x_scale': 0.3, 'y_scale': 0.3})
	worksheet.set_column('A:A', 5)
	worksheet.write('A8', 'ID',green)
	worksheet.set_column('B:B', 50)
	worksheet.write('B8', 'usuario',green)
	worksheet.set_column('C:C', 40)
	worksheet.write('C8', 'referencia',green)
	worksheet.set_column('D:D', 25)
	worksheet.write('D8', 'fecha',green)
	worksheet.set_column('E:E', 25)
	worksheet.write('E8', 'moneda',green)
	worksheet.set_column('F:F', 25)
	worksheet.write('F8', 'total_final',green)
	worksheet.set_column('G:G', 25)
	worksheet.write('G8', 'estatus',green)





	#worksheet.add_table('B3:F7') #TABLA
	#Cierra el workbook del excel para ser guardado
	workbook.close()

	output.seek(0)
	#response que contiene el archivo xlsx que sera devuelto a la ventana del navegador
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=PagoReport.xlsx"

	#funcion de retorno
	return response
