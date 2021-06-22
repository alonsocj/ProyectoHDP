from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Departamento, Registro, Persona, Municipio
from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import PersonaForm, PersonaForm1, RegistroForm1, PersonaForm2
from django.contrib import messages

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
      
class RegistrarPersona(CreateView):
    model = Persona
    template_name = 'personas/ingresarPersona.html'
    form_class = PersonaForm
    success_url = reverse_lazy('ConsultarPersona')

class ModificarPersonaTabla(ListView):
    model = Persona
    template_name = 'personas/modificar.html'


class ModificarPersona(UpdateView):
    model = Persona
    template_name = 'personas/modificarPersona.html'
    form_class = PersonaForm1
    success_url = reverse_lazy('ModificarPersonas')

class EliminarPersonaTabla(ListView):
    model = Persona
    template_name = 'personas/eliminar.html'

class EliminarPersona(DeleteView):
    model = Persona
    template_name = 'personas/eliminarPersona.html'
    form_class = PersonaForm
    success_url = reverse_lazy('EliminarPersonas')

class ConsultarPersona(ListView):
    model = Persona
    template_name = 'personas/consultarPersona.html'

# vista del formulario de ingresar primera dosis
class registrarVacunado(CreateView):
    model = Registro
    second_model = Persona
    template_name = 'registro/agregarRegistro1.html'
    form_class = RegistroForm1
    second_form_class = PersonaForm2
    success_url = reverse_lazy('ConsultarPersona')

    def get_context_data(self, **kwargs):
        context = super(registrarVacunado, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        persona = self.second_model.objects.get(dui=pk)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona)
        context['id'] = pk
        return context   

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        persona = self.second_model.objects.get(dui=pk)
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST, instance=persona)
        if form.is_valid() and form2.is_valid():
            registro = form.save(commit=False)
            registro.dui = form2.save()
            a = form.cleaned_data['numero_dosis']
            if a.numero_dosis==1:
                registro.save()    
                return HttpResponseRedirect('ModificarPersonas')
            else:
                try:
                    registro1 = self.model.objects.get(dui=pk, numero_dosis=1)
                    try:
                        registro2 = self.model.objects.get(dui=pk, numero_dosis=form.cleaned_data['numero_dosis'])
                        return HttpResponseRedirect(self.success_url)
                    except:
                        registro.save()
                        return HttpResponseRedirect('ModificarPersonas')
                except:
                    return HttpResponseRedirect(self.success_url)

        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))

