from django.contrib import admin
from .models import Proyecto, Tareas
# Register your models here.
# Le decimos a Django que muestre esta tabla en el panel
admin.site.register(Proyecto) # Muestra la tabla proyecto en el admin
admin.site.register(Tareas) # Muestra la tabla tareas en el admin