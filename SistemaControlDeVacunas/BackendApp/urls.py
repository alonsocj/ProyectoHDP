from django.urls import path, include
from Import_Csv import urls
from .views import HomePage

urlpatterns = [
    path('importarCsv/', include('Import_Csv.urls')),
    path('', HomePage.as_view(), name = 'Home'),
]