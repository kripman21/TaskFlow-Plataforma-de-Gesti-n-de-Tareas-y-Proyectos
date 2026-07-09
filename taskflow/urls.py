from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views # Importamos el auth de Django
from tareas import views as tareas_views # Improtamos nuestras vistas de tareas

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', tareas_views.dashboard, name='dashboard'),
    # Rutas de tareas
    path('crear_tarea/', tareas_views.crear_tarea, name='crear_tarea'),
    # Rutas de proyectos
    path('crear_proyecto/', tareas_views.crear_proyecto, name='crear_proyecto'),
    # Ruta de detalle de tarea
    path('tarea/<int:tarea_id>/', tareas_views.detalle_tarea, name='detalle_tarea'),
    # Ruta de eliminacion de tarea
    path('tarea/<int:tarea_id>/eliminar/', tareas_views.eliminar_tarea, name='eliminar_tarea'),
    # Ruta de eliminacion de proyecto
    path('proyecto/<int:proyecto_id>/eliminar/', tareas_views.eliminar_proyecto, name='eliminar_proyecto'),
    # Ruta de papelera
    path('papelera/', tareas_views.papelera, name='papelera'),
    # Ruta de restauracion de tarea
    path('tarea/<int:tarea_id>/restaurar/', tareas_views.restaurar_tarea, name='restaurar_tarea'),
    # Ruta de restauracion de proyecto
    path('proyecto/<int:proyecto_id>/restaurar/', tareas_views.restaurar_proyecto, name='restaurar_proyecto'),
    # Ruta de destruccion de tarea
    path('tarea/<int:tarea_id>/destruir/', tareas_views.destruir_tarea, name='destruir_tarea'),
    # Ruta de destruccion de proyecto
    path('proyecto/<int:proyecto_id>/destruir/', tareas_views.destruir_proyecto, name='destruir_proyecto'),
    # Ruta de edicion de tarea
    path('tarea/<int:tarea_id>/editar/', tareas_views.editar_tarea, name='editar_tarea'),
    # Ruta de edicion de proyecto
    path('proyecto/<int:proyecto_id>/editar/', tareas_views.editar_proyecto, name='editar_proyecto'),

]


