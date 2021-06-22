from django.shortcuts import render
from .forms import CsvModelForm
from django.views.generic.base import TemplateView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Csv
from BackendApp.models import Persona, Registro, Municipio, TipoVacuna,Departamento
import csv


#from django.http import HttpResponse
# Create your views here.


class DatosPersona(TemplateView):
    form_class = CsvModelForm
    template_name = 'csvs/csv.html'
    success_url = reverse_lazy('home-page')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = CsvModelForm()
            obj = Csv.objects.get(activated=False)
            with open(obj.file_name.path, 'r') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    #row = "".join(row)
                    #row = row.replace(",", "")
                    #row = row.split()
                    dui = row[0]
                    nombre = row[1]
                    apellido = row[2]
                    sexo = row[3]
                    edad = row[4]
                    municipio = row[5]
                    Persona.objects.create(
                        dui=dui,
                        id_municipio= Municipio.objects.get(id_municipio = municipio),
                        nombre=nombre,
                        apellido=apellido,
                        sexo=sexo,
                        edad=int(edad)
                    )
                obj.activated = True
                obj.save()
        return HttpResponseRedirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upload-view'] = self.get()
        return context