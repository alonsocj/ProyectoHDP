from os import name
from django.urls import path, include
from Import_Csv import urls
from .views import HomePage, RegistrarPersona, ConsultarPersona, ModificarPersona
from .views import EliminarPersona, ModificarPersonaTabla, EliminarPersonaTabla,registrarVacunado
from .views import  AgregarVacuna ,ConsultarVacuna,ModificarVacuna,EliminarVacuna,ConsultarDosis,AgregarDosis,EliminarDosis

urlpatterns = [
    path('', HomePage.as_view(), name = 'Home'),
    path('registrarpersona/', RegistrarPersona.as_view(), name = 'RegistrarPersona'),
    path('consultarpersona/', ConsultarPersona.as_view(), name = 'ConsultarPersona'),
    path('modificarpersona/', ModificarPersonaTabla.as_view(), name = 'ModificarPersonas'),
    path('modificarpersona/<str:pk>/', ModificarPersona.as_view(), name = 'ModificarPersona'),
    path('eliminarpersona/', EliminarPersonaTabla.as_view(), name = 'EliminarPersonas'),
    path('eliminarpersona/<str:pk>/', EliminarPersona.as_view(), name = 'EliminarPersona'),
    path('registrardosis/<str:pk>/', registrarVacunado.as_view(), name = 'AgregarDosis'),

#Vacuna
    path('agregarVacuna/', AgregarVacuna.as_view(), name = 'AgregarVacuna'),
    path('consultarVacuna/', ConsultarVacuna.as_view(), name = 'ConsultarVacuna'),
    path('modificarVacuna/<str:pk>/', ModificarVacuna.as_view(), name = 'ModificarVacuna'),
    path('eliminarVacuna/<str:pk>/', EliminarVacuna.as_view(), name = 'EliminarVacuna'),


#Dosis
    path('consultardosis/', ConsultarDosis.as_view(), name = 'ConsultarDosis'),
    path('agregardosis/', AgregarDosis.as_view(), name = 'AgregarDosis'),
    path('eliminardosis/<int:pk>/', EliminarDosis.as_view(), name = 'EliminarDosis'),


]
