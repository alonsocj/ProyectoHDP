
from django.contrib.auth.decorators import login_required

#from django.contrib import messages
from .models import Departamento, Dosis, Registro, Persona, Municipio, TipoVacuna

from django.views.generic.base import TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import PersonaForm, PersonaForm1, RegistroForm1, PersonaForm2, PersonaForm3, RegistroForm2,VacunaForm1,DosisForm1
from django.contrib import messages

# Create your views here.
def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'login.html')
    

class HomePage(TemplateView):
    model = Registro
    template_name = "inicio.html"

    def total_dosis(self):
        return self.cont_primerDosis() + self.cont_segundaDosis()

    def cont_primerDosis(self):
        return Registro.objects.filter(numero_dosis = 1).count()

    def cont_segundaDosis(self):
        return Registro.objects.filter(numero_dosis = 2).count()

    def cont_Mujeres(self):
        try:
            person = Persona.objects.filter(sexo = 'F')
            tot =0
            for i in range(0,person.count()):
                tot += Registro.objects.filter(dui = person[i]).count()

            averange = (tot/Registro.objects.filter().count())*100
            return averange
        except :
            return 0
    
    def cont_Hombres(self):
        try:
            person = Persona.objects.filter(sexo = 'M')
            tot =0
            for i in range(0,person.count()):
                tot += Registro.objects.filter(dui = person[i]).count()

            averange = (tot/Registro.objects.filter().count())*100
            return averange
        except :
            return 0
    
    def graf_vacunados(self):
        data = []
        try:
            for dep in range(1, Departamento.objects.all().count()+1):
                count = 0
                # se seleccionan los municipios relacionados con el departamento y se almacenan en un array de objetos tipo municipio
                datos = Municipio.objects.filter(id_departamento=Departamento.objects.get(id_departamento=dep))

                for mun in range(0, datos.count()):
                    # se hace un filtro de personas por municipio que estan relacionadas con el departamento que se esta iterando
                    person = Persona.objects.filter(id_municipio=datos[mun])
                    for p in range(0, person.count()):
                        count += Registro.objects.filter(dui = person[p]).count()

                # se almacena en un array los valores por departamento
                data.append(count)
        except:
            pass
        return data
          
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Home'] = 'Home'
        context['graf_vacunados'] = self.graf_vacunados()
        context['contador_Mujeres'] = self.cont_Mujeres()
        context['contador_Hombres'] = self.cont_Hombres()
        context['primer_dosis'] = self.cont_primerDosis()
        context['segunda_dosis'] = self.cont_segundaDosis()
        context['total_dosis'] = self.total_dosis()
        return context
      
class RegistrarPersona(CreateView):
    model = Persona
    template_name = 'personas/ingresarPersona.html'
    form_class = PersonaForm
    success_url = reverse_lazy('ConsultarPersona')


class ModificarPersonaTabla(ListView):
    model = Persona
    template_name = 'personas/modificar.html'

    def post(self, request, *args, **kwargs):
            self.object = self.get_object
            form = self.form_class(request.POST)
            if form.is_valid():
                    persona = form.save()
                    return HttpResponseRedirect(self.success_url)
            else:
                messages.warning(request, 'La persona con el dui ingresado ya esta registrada')
                return self.render_to_response(self.get_context_data(form=form))


class ModificarPersona(UpdateView):
    model = Persona
    template_name = 'personas/modificarPersona.html'
    form_class = PersonaForm1
    success_url = reverse_lazy('ConsultarPersona')

class EliminarPersona(DeleteView):
    model = Persona
    second_model = Registro
    template_name = 'personas/eliminarPersona.html'
    form_class = PersonaForm
    success_url = reverse_lazy('ConsultarPersona')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        pk = kwargs['pk']
        persona = self.model.objects.get(dui=pk)
        try:
            persona = self.model.objects.get(dui=pk)
            registro = self.second_model.objects.filter(dui=pk)
            a=len(registro)
            if(a==1):
                registro.delete()
                persona.delete()
            else:
                for re in registro:
                    re.delete()
                persona.delete()
            return HttpResponseRedirect(self.success_url)
        except self.model.DoesNotExist:
            persona = self.model.objects.get(dui=pk)
            persona.delete()
            return HttpResponseRedirect(self.success_url)

class ConsultarPersona(ListView):
    model = Persona
    template_name = 'personas/consultarPersona.html'

# vista del formulario de dosis 
class AgregarRegistro(CreateView):
    model = Registro
    second_model = Persona
    template_name = 'registro/agregarRegistro1.html'
    form_class = RegistroForm1
    second_form_class = PersonaForm2
    success_url = reverse_lazy('ConsultarRegistro')

    def get_context_data(self, **kwargs):
        context = super(AgregarRegistro, self).get_context_data(**kwargs)
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
                try:
                    registro3 = self.model.objects.get(dui=pk, numero_dosis=form.cleaned_data['numero_dosis'])
                    messages.success(request, 'Ya existe un registro creado con la dosis ingresada')
                    return redirect('AgregarRegistro',pk)
                except:
                    registro.save()    
                    return HttpResponseRedirect(self.success_url)
            else:
                try:
                    registro1 = self.model.objects.get(dui=pk, numero_dosis=1)
                    try:
                        registro2 = self.model.objects.get(dui=pk, numero_dosis=form.cleaned_data['numero_dosis'])
                        messages.warning(request, 'Ya existe un registro creado con la dosis ingresada')
                        return redirect('AgregarRegistro',pk)
                    except:
                        if registro.nombre_vacuna == registro1.nombre_vacuna:
                            if registro.fecha_vacunacion > registro1.fecha_vacunacion:
                                registro.save()
                                return HttpResponseRedirect(self.success_url)
                            else: 
                                messages.warning(request, 'La fecha debe ser posterior a la de dosis 1')
                                return redirect('AgregarRegistro', pk)
                        else:
                            messages.warning(request, 'El tipo de vacuna ingresada no coincide con el de la primera dosis')
                            return redirect('AgregarRegistro', pk)
                except:
                    messages.warning(request, 'No existe dosis 1 registrada con este dui')
                    return redirect('AgregarRegistro',pk)
        else:
            return redirect('AgregarRegistro',pk)

class IngresarDui(CreateView):
    model = Persona
    form_class = PersonaForm3
    template_name = 'registro/ingresarDui.html'
    success_url = reverse_lazy('IngresarDui')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        try:
            persona = self.model.objects.get(dui=request.POST.get('dui'))
            form = self.form_class(request.POST, instance=persona)
            if form.is_valid():
                    a = form.cleaned_data['dui']
                    return redirect('AgregarRegistro', a)
            else:
                messages.warning(request, 'Datos ingresados incorrectos')
                return HttpResponseRedirect(self.success_url)
        except self.model.DoesNotExist:
            messages.warning(request, 'El dui ingresado no esta registrado')
            return HttpResponseRedirect(self.success_url)

class ConsultarRegistro(ListView):
    model = Registro
    template_name = 'registro/consultarRegistro.html'

class ModificarRegistro(UpdateView):
    model = Registro
    template_name = 'registro/modificarRegistro.html'
    form_class = RegistroForm2
    success_url = reverse_lazy('ConsultarRegistro')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_re = kwargs['pk']
        registro = self.model.objects.get(id_registro=id_re)
        form = self.form_class(request.POST, instance=registro)
        if form.is_valid():
            registros = self.model.objects.filter(dui=registro.dui.dui)
            if registro.numero_dosis.numero_dosis == 1:
                for re in registros:
                    re.nombre_vacuna = form.cleaned_data['nombre_vacuna']
                    re.save()
                form.save()
                return HttpResponseRedirect(self.success_url)
            else:
                registro2 = self.model.objects.get(numero_dosis = 1)
                if form.cleaned_data['nombre_vacuna'] == registro2.nombre_vacuna:
                    if form.cleaned_data['fecha_vacunacion'] > registro2.fecha_vacunacion:
                        form.save()
                        return HttpResponseRedirect(self.success_url)
                    else: 
                        messages.warning(request, 'La fecha debe ser posterior a la de dosis 1')
                        return redirect('ModificarRegistro', id_re)
                else:
                    messages.warning(request, 'La vacuna debe ser las misma en ambas dosis. Modifique el tipo de vacuna en dosis 1')
                    return redirect('ModificarRegistro', id_re)
        else:
            return HttpResponseRedirect(self.success_url)
          
#CRUD DE VACUNA
class ConsultarVacuna(ListView):
    model=TipoVacuna
    template_name='vacunas/consultarVacuna.html'
   
class AgregarVacuna(CreateView):
    model=TipoVacuna
    form_class=VacunaForm1
    template_name='vacunas/ingresarVacuna.html'
    success_url=reverse_lazy('ConsultarVacuna')

class ModificarVacuna(UpdateView):
    model=TipoVacuna
    form_class=VacunaForm1
    template_name='vacunas/ingresarVacuna.html'
    success_url=reverse_lazy('ConsultarVacuna')

   # def post(self,request,*args,**kwargs):
   #     self.object=self.get_object
    #    form=self.form_class(request.POST)
     #   if form.is_valid():
      #      form=form.save()
       #     return HttpResponseRedirect(self.success_url)
       # else:
            # return redirect('ModificarVacuna',id_re)
         #  return self.render_to_response(self.get_context_data(form=form))

class EliminarVacuna(DeleteView):
    model=TipoVacuna
    template_name='vacunas/eliminarVacuna.html'
    success_url=reverse_lazy('ConsultarVacuna')

#DOSIS
class ConsultarDosis(ListView):
    model=Dosis
    template_name='dosis/consultarDosis.html'

class AgregarDosis(CreateView):
    model=Dosis
    form_class=DosisForm1
    template_name='dosis/agregarDosis.html'
    success_url=reverse_lazy('ConsultarDosis')

class EliminarDosis(DeleteView):
    model=Dosis
    template_name='dosis/eliminarDosis.html'
    success_url=reverse_lazy('ConsultarDosis')

class EliminarRegistro(DeleteView):
    model = Registro
    template_name = 'registro/eliminarRegistro.html'
    form_class = RegistroForm1
    success_url = reverse_lazy('ConsultarRegistro')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        id_re = kwargs['pk']
        registro = self.model.objects.get(id_registro=id_re)
        if(registro.numero_dosis.numero_dosis == 1):
            try:
                registro1 = self.model.objects.get(dui=registro.dui, numero_dosis=2)
                messages.warning(request, 'Para eliminar el registro debe eliminar antes los registros de las otras dosis')
                return redirect('EliminarRegistro', id_re)
            except self.model.DoesNotExist:
                registro.delete()
                return HttpResponseRedirect(self.success_url)
        else:
            registro.delete()
            return HttpResponseRedirect(self.success_url)

