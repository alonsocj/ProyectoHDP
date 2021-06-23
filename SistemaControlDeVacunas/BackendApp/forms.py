
from django import forms
from django.forms import ModelForm, widgets
from BackendApp.models import Persona, Registro,TipoVacuna,Dosis

#Formulario de persona para agregar una nueva.
class PersonaForm(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        labels = {
            'dui' : 'Dui',
            'id_municipio' : 'Municipio',
            'nombre' : 'Nombre',
            'apellido' : 'Apellido',
            'sexo' : 'Sexo',
            'edad' : 'Edad',
        }
        CHOICES = (
                ('', 'Seleccione su sexo'),
                ('F', 'F'), #First one is the value of select option and second is the displayed value in option
                ('M', 'M'),
                )
        widgets = { 'dui': forms.TextInput( attrs={'minlength':'10', 'class': 'form-control', 'placeholder' : 'Ingrese su dui', 'autocomplete' : 'off', 'data-mask':"00000000-0"}),
                    'id_municipio': forms.Select(attrs={ 'class': 'form-control','required': True}),
                    'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder' : 'Ingrese su nombre', 'autocomplete' : 'off'}),
                    'apellido': forms.TextInput(attrs={ 'class': 'form-control','placeholder' : 'Ingrese su apellido', 'autocomplete' : 'off'}),
                    'edad': forms.NumberInput(attrs={'min': '18', 'class': 'form-control'}),
                    'sexo': forms.Select(choices=CHOICES, attrs={'class': 'form-control','required': True})
        }
#Para actualizar
class PersonaForm1(ModelForm):
    class Meta:
        model = Persona
        fields = '__all__'
        labels = {
            'dui' : 'Dui',
            'id_municipio' : 'Municipio',
            'nombre' : 'Nombre',
            'apellido' : 'Apellido',
            'sexo' : 'Sexo',
            'edad' : 'Edad',
        }
        CHOICES = (
                ('', 'Seleccione su sexo'),
                ('F', 'F'), #First one is the value of select option and second is the displayed value in option
                ('M', 'M'),
                )
        widgets = { 'dui': forms.TextInput(attrs={ 'class': 'form-control', 'autocomplete' : 'off', 'data-mask':"00000000-0"}),
                    'id_municipio': forms.Select(attrs={ 'class': 'form-control','required': True}),
                    'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder' : 'Ingrese su nombre', 'autocomplete' : 'off'}),
                    'apellido': forms.TextInput(attrs={ 'class': 'form-control','placeholder' : 'Ingrese su apellido', 'autocomplete' : 'off'}),
                    'edad': forms.NumberInput(attrs={ 'class': 'form-control','min': '18'}),
                    'edad': forms.NumberInput(attrs={ 'class': 'form-control','max': '100'}),
                    'sexo': forms.Select(choices=CHOICES, attrs={'class': 'form-control','required': True})
        }
    def __init__(self, *args, **kwargs):
        super(PersonaForm1, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.dui:
            self.fields['dui'].required = False
            self.fields['dui'].widget.attrs['disabled'] = 'disabled'
    
    def clean_dui(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.dui
        else:
            return self.cleaned_data.get('dui', None)

#Para actualizar
class PersonaForm2(ModelForm):
    class Meta:
        model = Persona
        fields = ['dui']
        labels = {
            'dui' : 'Dui',
        }
        widgets = { 'dui': forms.TextInput(attrs={ 'class': 'form-control', 'autocomplete' : 'off', 'data-mask':"00000000-0"}),
        }
    def __init__(self, *args, **kwargs):
        super(PersonaForm2, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.dui:
            self.fields['dui'].required = False
            self.fields['dui'].widget.attrs['disabled'] = 'disabled'
    
    def clean_dui(self):
        # As shown in the above answer.
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.dui
        else:
            return self.cleaned_data.get('dui', None)

#Utilizado para dosis1
class RegistroForm1(ModelForm):
    class Meta:
        model = Registro
        fields = ['numero_dosis','nombre_vacuna','fecha_vacunacion']
        labels = {
            'numero_dosis' : 'Dosis',
            'id_vacuna': 'Vacuna',
            'fecha_vacunacion' : 'Fecha de Vacunacion',
        }
        widgets = {'fecha_vacunacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                    'id_vacuna': forms.Select(attrs={ 'class': 'form-control','required': True}),
                    'numero_dosis': forms.Select(attrs={ 'class': 'form-control','required': True}),
        }

#Utilizado para vacuna
class VacunaForm1(ModelForm):
    class Meta:
        model=TipoVacuna
        fields='__all__'
        labels={
            'nombre_vacuna': 'Nombre de vacuna',
            'fabricante': 'Fabricante',
            'pais_fabricacion':'Pais de Fabricación',
        }
        widgets={
            'nombre_vacuna':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el nombre de la vacuna','autocomplete':'off'}),
            'fabricante':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el fabricante de la vacuna','autocomplete':'off'}),
            'pais_fabricacion':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese el pais de fabricación de la vacuna','autocomplete':'off'})
        }

 #   def __init__(self, *args, **kwargs):
 #       super(VacunaForm1, self).__init__(*args, **kwargs)
 #       instance = getattr(self, 'instance', None)
 #       if instance and instance.nombre_vacuna:
 #           self.fields['nombre_vacuna'].required = False
 #           self.fields['nombre_vacuna'].widget.attrs['disabled'] = 'disabled'
    
 #   def clean_dui(self):
        # As shown in the above answer.
 #       instance = getattr(self, 'instance', None)
 #       if instance:
 #           return instance.nombre_vacuna
 #       else:
 #           return self.cleaned_data.get('nombre_vacuna', None)

class DosisForm1(ModelForm):
    class Meta:
        model = Dosis
        fields = ['numero_dosis']
        labels = {
            'numero_dosis' : 'Número de dosis',
        }
        widgets = {'numero_dosis': forms.NumberInput(attrs={ 'class': 'form-control','required': True,'min':'1','max':'4'}),}