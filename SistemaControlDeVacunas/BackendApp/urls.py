from os import name
from django.urls import path, include
from Import_Csv import urls
from .views import HomePage, RegistrarPersona, ConsultarPersona, ModificarPersona, EliminarPersona
from.views import AgregarRegistro, IngresarDui, ConsultarRegistro, ModificarRegistro, EliminarRegistro

urlpatterns = [
    path('', HomePage.as_view(), name = 'Home'),
    path('registrarpersona/', RegistrarPersona.as_view(), name = 'RegistrarPersona'),
    path('consultarpersona/', ConsultarPersona.as_view(), name = 'ConsultarPersona'),
    path('modificarpersona/<str:pk>/', ModificarPersona.as_view(), name = 'ModificarPersona'),
    path('eliminarpersona/<str:pk>/', EliminarPersona.as_view(), name = 'EliminarPersona'),
    path('ingresardui/', IngresarDui.as_view(), name = 'IngresarDui'),
    path('agregarregistro/<str:pk>/', AgregarRegistro.as_view(), name = 'AgregarRegistro'),
    path('consultarregistro/', ConsultarRegistro.as_view(), name = 'ConsultarRegistro'),
    path('modificarregistro/<str:pk>/', ModificarRegistro.as_view(), name = 'ModificarRegistro'),
    path('eliminarregistro/<str:pk>/', EliminarRegistro.as_view(), name = 'EliminarRegistro'),
    
]