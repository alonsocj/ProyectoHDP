from django.urls import path
from .views import DatosPersona

from BackendApp.views import HomePage

app_name = 'csvs'

urlpatterns=[
    path('', HomePage.as_view(), name='home-page'),
    path('csv/',DatosPersona.as_view(), name='upload-view'),

]