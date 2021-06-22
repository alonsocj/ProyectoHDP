from django.urls import path, include
from Import_Csv import urls
from .views import HomePage, RegistrarPersona, ConsultarPersona, ModificarPersona, EliminarPersona, ModificarPersonaTabla, EliminarPersonaTabla
from.views import registrarVacunado
urlpatterns = [
    path('importarCsv/', include('Import_Csv.urls')),
    path('', HomePage.as_view(), name = 'Home'),
    path('registrarpersona/', RegistrarPersona.as_view(), name = 'RegistrarPersona'),
    path('consultarpersona/', ConsultarPersona.as_view(), name = 'ConsultarPersona'),
    path('modificarpersona/', ModificarPersonaTabla.as_view(), name = 'ModificarPersonas'),
    path('modificarpersona/<str:pk>/', ModificarPersona.as_view(), name = 'ModificarPersona'),
    path('eliminarpersona/', EliminarPersonaTabla.as_view(), name = 'EliminarPersonas'),
    path('eliminarpersona/<str:pk>/', EliminarPersona.as_view(), name = 'EliminarPersona'),
    path('registrardosis/<str:pk>/', registrarVacunado.as_view(), name = 'AgregarDosis'),
    
]