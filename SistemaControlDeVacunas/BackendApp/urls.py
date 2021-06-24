from os import name
from django.urls import path, include
from Import_Csv import urls

from .views import  AgregarVacuna ,ConsultarVacuna,ModificarVacuna,EliminarVacuna,ConsultarDosis,AgregarDosis,EliminarDosis
from .views import HomePage, RegistrarPersona, ConsultarPersona, ModificarPersona, EliminarPersona
from.views import AgregarRegistro, IngresarDui, ConsultarRegistro, ModificarRegistro, EliminarRegistro


urlpatterns = [
    path('', HomePage.as_view(), name = 'Home'),
    path('registrarpersona/', RegistrarPersona.as_view(), name = 'RegistrarPersona'),
    path('consultarpersona/', ConsultarPersona.as_view(), name = 'ConsultarPersona'),
    path('modificarpersona/<str:pk>/', ModificarPersona.as_view(), name = 'ModificarPersona'),
    path('eliminarpersona/<str:pk>/', EliminarPersona.as_view(), name = 'EliminarPersona'),

#Vacuna
    path('agregarVacuna/', AgregarVacuna.as_view(), name = 'AgregarVacuna'),
    path('consultarVacuna/', ConsultarVacuna.as_view(), name = 'ConsultarVacuna'),
    path('modificarVacuna/<str:pk>/', ModificarVacuna.as_view(), name = 'ModificarVacuna'),
    path('eliminarVacuna/<str:pk>/', EliminarVacuna.as_view(), name = 'EliminarVacuna'),


#Dosis
    path('consultardosis/', ConsultarDosis.as_view(), name = 'ConsultarDosis'),
    path('agregardosis/', AgregarDosis.as_view(), name = 'AgregarDosis'),
    path('eliminardosis/<int:pk>/', EliminarDosis.as_view(), name = 'EliminarDosis'),


    path('ingresardui/', IngresarDui.as_view(), name = 'IngresarDui'),
    path('agregarregistro/<str:pk>/', AgregarRegistro.as_view(), name = 'AgregarRegistro'),
    path('consultarregistro/', ConsultarRegistro.as_view(), name = 'ConsultarRegistro'),
    path('modificarregistro/<str:pk>/', ModificarRegistro.as_view(), name = 'ModificarRegistro'),
    path('eliminarregistro/<str:pk>/', EliminarRegistro.as_view(), name = 'EliminarRegistro'),
    
]
