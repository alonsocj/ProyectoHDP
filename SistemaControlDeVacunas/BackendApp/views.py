from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Departamento, Registro, Persona, Municipio
from django.views.generic.base import TemplateView

# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'login.html')
    


class HomePage(TemplateView):
    model = Registro
    template_name = "inicio.html"
    
    def graf_vacunados(self):
        data = []
        try:
            for dep in range(1, Departamento.objects.all().count()+1):
                count = 0
                # se seleccionan los municipios relacionados con el departamento y se almacenan en un array de objetos tipo municipio
                datos = Municipio.objects.filter(id_departamento=Departamento.objects.get(id_departamento=dep))

                for mun in range(0, datos.count()):
                    # se hace un conteo de de personas por municipio que estan relacionadas con el departamento que se esta iterando
                    count += Persona.objects.filter(id_municipio=datos[mun]).count()

                # se almacena en un array los valores por departamento
                data.append(count)
        except:
            pass
        return data
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Home'] = 'Home'
        context['graf_vacunados'] = self.graf_vacunados()
        return context
