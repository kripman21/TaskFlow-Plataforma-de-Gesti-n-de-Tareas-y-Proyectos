from django import forms
from django.contrib.auth.models import User
from .models import Tareas, Proyecto, Comentario

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tareas
        # No se agrego completada porque por defecto es false al crear la tarea
        fields = ['titulo', 'descripcion', 'proyecto', 'asignada_a', 'prioridad', 'estado']

    def __init__(self, *args, **kwargs):
        # Extraemos el usuario de los argumentos antes de inicializar el form
        user = kwargs.pop('user', None)
        super(TareaForm, self).__init__(*args, **kwargs)

        # Solo muestra usuarios activos
        self.fields['asignada_a'].queryset = User.objects.filter(is_active=True)

        # Si hay un usuario y NO es admin, eliminamos el campo 'asignada_a' del formulario HTML
        if user and not user.groups.filter(name='Admin').exists():
            del self.fields['asignada_a']  

    widgets = {
        'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        'proyecto': forms.Select(attrs={'class': 'form-control'}),
        'asignada_a': forms.Select(attrs={'class': 'form-control'}),
        'prioridad': forms.Select(attrs={'class': 'form-control'}),
        'estado': forms.Select(attrs={'class': 'form-control'}),
    }     

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'descripcion', 'estado', 'fecha_entrega']
        # No se agrego completada porque por defecto es false al crear la tarea
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }  

# Formulario para agregar comentarios
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Agrega un comentario...'
                }),
        }