"""Gacerh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from users.views import LoginRequest,LogoutRequest,register2,export_excel,user_detail,export_excel2,activate,active,user_edit
from ncf.views import compania, newgasto, gastodetalle,creargasto,creargastobase,removergasto,removerdetalle,admintable,pay,cerrargasto,pagos,paygasto,detalleadmin,range_date,PDF,reabierto,past

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/',LoginRequest ),
    url(r'logout/', LogoutRequest, name="logout"),
    url(r'^$',LoginRequest ),
    url(r'register/$', register2, name="register"),
    url(r'^gastos/',compania ),
    url(r'^nuevo/',newgasto ),
    url(r'^userdetail/',user_detail ,name="userdetail" ),
    url(r'^creargasto/',creargasto, name="creargasto" ),
    url(r'^creargastobase/',creargastobase, name="creargastobase" ),
    url(r'^detalle/(?P<id>\d+)/$',gastodetalle, name="detalle"),
    url(r'^removergasto/',removergasto, name="removergasto"),
    url(r'^removerdetalle/',removerdetalle, name="removerdetalle"),
    url(r'^admintable/',admintable, name="admintable" ),
    url(r'^pagos/',pagos, name="pagos" ),
    url(r'^pagospast/',past, name="pagospast" ),
    url(r'^pay/',pay, name="pay" ),
    url(r'^paygasto/',paygasto, name="paygasto" ),
    url(r'^cerrargasto/',cerrargasto, name="cerrargasto" ),
    url(r'^detalleadmin/(?P<id>\d+)/$',detalleadmin, name="detalleadmin" ),
    url(r'^excel/$', export_excel ,name="export_excel"),
    url(r'^excel2/$', export_excel2 ,name="export_excel2"),
    url(r'^activate/$', activate ,name="activate"),
    url(r'^active/$', active ,name="active"),
    url(r'^range_date/$', range_date ,name="range_date"),
    url(r'^user_edit/$', user_edit ,name="user_edit"),
    url(r'^PDF2/$', PDF ,name="PDF"),
    url(r'^PDF/(?P<id>\d+)/$',PDF, name="PDF"),
    url(r'^reopen/(?P<id>\d+)/$',reabierto, name="reopen"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
