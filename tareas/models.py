from django.db import models
from django.contrib.auth.models import User

class Proyecto(models.Model):
    # Se definen las opciones de estado (La base de datos guarda el primer valor, el usuario ve el segundo)
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('pausado', 'Pausado'),
        ('completado', 'Completado'),
    ]
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    
    # Se agrega el campo estado, con 'activo' por defecto
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    
    # Se agrega la fecha de entrega (permitimos que pueda quedar en blanco temporalmente)
    fecha_entrega = models.DateField(blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)

    # Sistema de Auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='proyectos_creados')

    # Soft delete
    en_papelera = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

class Tareas(models.Model):
    # Se definen las opciones de prioridad
    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    
    # Se definen las opciones de estado
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('terminada', 'Terminada'),
    ]


    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completada = models.BooleanField(default=False)

    # Se agrega prioridad por defecto media
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='media')

    # Se agrega estado por defecto pendiente
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    # Relacion con Proyecto
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    asignada_a = models.ForeignKey(User, on_delete=models.CASCADE)

    # Se define el metodo save para sincronizar el checkbox con el select
    def save(self, *args, **kwargs):
        # Si marcaron el checkbox, forzamos el estado a 'terminada'
        if self.completada:
            self.estado = 'terminada'
        # Si cambiaron el select a 'terminada', forzamos el checkbox a True
        elif self.estado == 'terminada':
            self.completada = True
        # Para cualquier otro estado (Pendiente, En progreso), aseguramos que el checkbox esté desmarcado
        else:
            self.completada = False

        # Llamamos al metodo save de la clase padre
        super().save(*args, **kwargs)

    # Sistema de Auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    # soft delete 
    en_papelera = models.BooleanField(default=False)
    
    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    # Relacion con Tareas
    tarea = models.ForeignKey('Tareas', on_delete=models.CASCADE)
    # Relacion con Usuario
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    # Contenido del comentario
    contenido = models.TextField()
    # Fecha de creacion (por defecto la fecha y hora actual)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.tarea.titulo}'