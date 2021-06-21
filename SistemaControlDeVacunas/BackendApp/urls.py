from django.urls import path, include

urlpatterns = [
    path('importarCsv/', include('Import_Csv.urls'))
]