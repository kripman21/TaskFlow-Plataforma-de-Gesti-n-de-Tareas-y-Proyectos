from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test # Decoraadores que nos permiten proteger las vistas
from django.http import HttpResponse # Nos permite devolver una respuesta HTTP
from .forms import TareaForm, ProyectoForm, ComentarioForm
from .models import Tareas, Proyecto, Comentario

# Funcion auxiliar para saber si el usuario es admin
def es_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required # Si no esta logueado, no entra a la vista, lo redirige a login
def dashboard(request):
    # Verifica si el administrador esta logueado
    es_administrador = es_admin(request.user)

    vista_actual = request.GET.get('vista', 'lista')

    # Usamos un condicional para filtrar las tareas dependiendo de si el usuario es admin o no
    if es_administrador:
        # Ordenamos todas las tareas por id de forma descendente (las mas recientes primero)
        tareas = Tareas.objects.filter(en_papelera=False).order_by('-id')
        # Tareas.objects.all().order_by('-id')
    else:
        # Filtramos todas las tareas asignadas al usuario logueado y ordenamos por id de forma descendente (las mas recientes primero)
        tareas = Tareas.objects.filter(asignada_a=request.user, en_papelera=False).order_by('-id') 
    
    # Enviamos los datos al template
    return render(request, 'dashboard.html', {
        'usuario': request.user, 
        'es_administrador': es_administrador,
        'tareas': tareas,
        'vista_actual': vista_actual 
    })

@login_required
def detalle_tarea(request, tarea_id):
    # Obtenemos la tarea o devolvemos 404 si no existe
    tarea = get_object_or_404(Tareas, id=tarea_id)

    # Obtenemos los comentarios de la tarea ordenados por fecha de creacion descendente (los mas recientes primero)
    comentarios = Comentario.objects.filter(tarea=tarea).order_by('-fecha_creacion')

    # Si se envio el formulario
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        # Validamos que el formulario sea valido
        if form.is_valid():
            # Creamos el comentario
            comentario = form.save(commit=False)
            # Asignamos la tarea y el autor
            comentario.tarea = tarea
            comentario.autor = request.user
            # Guardamos el comentario
            comentario.save()
            # Redirigimos al detalle de la tarea
            return redirect('detalle_tarea', tarea_id=tarea_id)
    else:
        form = ComentarioForm()
    
    # Enviamos los datos al template
    return render(request, 'detalle_tarea.html', {
        'tarea': tarea,
        'comentarios': comentarios,
        'form': form
        })

@login_required
@user_passes_test(es_admin)
def crear_proyecto(request):
    if request.method == 'POST': 
        # Obtenemos el formulario
        form = ProyectoForm(request.POST)
        # Validamos el formulario
        if form.is_valid():
            # Pausamos en guardado con commit=false
            proyecto = form.save(commit=False)

            # Asignamos el creador del proyecto
            proyecto.creado_por = request.user

            # Guardamos el proyecto
            proyecto.save()
            
            # Redirigimos al dashboard
            return redirect('dashboard')
    else:
        form = ProyectoForm()
    return render(request, 'crear_proyecto.html', {'form': form})
    # Crear el modelo proyecto en admin.py

@login_required
def crear_tarea(request):
    if request.method == 'POST': 
        # Le pasamos el user al formulario (para que sepa si oculta campos)
        form = TareaForm(request.POST, user=request.user)
        # Validamos el formulario
        if form.is_valid():
            # Pausamos el guardado con commit=false
            tarea = form.save(commit=False)

            # Le asignamos el creador de la tarea
            tarea.creado_por = request.user

            # Si no es admin, le asignamos el usuario logueado al campo creado_por
            if not es_admin(request.user):
                tarea.asignada_a = request.user

            # Guardamos la tarea
            tarea.save()
            return redirect('dashboard') # Redirigimos al dashboard
    else:
        # Tambien pasamos el user al cargar el formulario
        form = TareaForm(user=request.user)

    return render(request, 'crear_tarea.html', {'form': form})

@login_required
def papelera(request):
    # Verificamos si es administrador
    if es_admin(request.user):
        # Mostramos todas las tareas y proyectos si cumple la condición
        tareas_borradas = Tareas.objects.filter(en_papelera=True).order_by('-id')
        proyectos_borrados = Proyecto.objects.filter(en_papelera=True).order_by('-id')
    else:
        # No mostramos proyectos
        proyectos_borrados = None
        # Si no, mostramos solo las tareas en papelera asignadas al usuario logueado
        tareas_borradas = Tareas.objects.filter(creado_por=request.user, en_papelera=True).order_by('-id')

    return render(request, 'papelera.html', {
        'tareas_borradas': tareas_borradas,
        'proyectos_borrados': proyectos_borrados
    })

@login_required
@user_passes_test(es_admin)
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        # En vez de .delete(), lo apagamos (Soft Delete)
        proyecto.en_papelera = True
        proyecto.save()
    return redirect('dashboard')

@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    
    # REGLA DE NEGOCIO: Si NO es admin, y TAMPOCO es el creador de la tarea, le prohibimos borrarla.
    if not es_admin(request.user) and tarea.creado_por != request.user:
        return redirect('dashboard')
        
    if request.method == 'POST':
        # Soft Delete
        tarea.en_papelera = True
        tarea.save()
    return redirect('dashboard')

@login_required
@user_passes_test(es_admin)
def restaurar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.en_papelera = False # Rescate del cesto
    proyecto.save()
    return redirect('papelera')


@login_required
def restaurar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    if not es_admin(request.user) and tarea.creado_por != request.user:
        return redirect('papelera')
    tarea.en_papelera = False # Rescate del cesto
    tarea.save()
    return redirect('papelera')


# --- DESTRUIR DEFINITIVAMENTE (HARD DELETE) ---
@login_required
@user_passes_test(es_admin)
def destruir_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.method == 'POST':
        proyecto.delete() # Trituradora
    return redirect('papelera')

    
@login_required
def destruir_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    if not es_admin(request.user) and tarea.creado_por != request.user:
        return redirect('papelera')
    if request.method == 'POST':
        tarea.delete() # Trituradora
    return redirect('papelera')

@login_required
@user_passes_test(es_admin)
def editar_proyecto(request, proyecto_id):
    # 1. Recuperamos el proyecto o devolvemos 404
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        # 2. Le pasamos los datos del POST y la instancia existente
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # 3. Si es GET, cargamos el formulario con los datos actuales
        form = ProyectoForm(instance=proyecto)
        
    return render(request, 'editar_proyecto.html', {'form': form, 'proyecto': proyecto})
    
@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    
    # REGLA DE NEGOCIO: Solo admin o el creador de la tarea pueden editarla
    if not es_admin(request.user) and tarea.creado_por != request.user:
        # Si intenta un vivo meterse por URL, lo mandamos al dashboard
        return redirect('dashboard')
    if request.method == 'POST':
        # Nota: Pasamos el 'user' porque TareaForm lo requiere en su __init__
        form = TareaForm(request.POST, instance=tarea, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TareaForm(instance=tarea, user=request.user)
        
    return render(request, 'editar_tarea.html', {'form': form, 'tarea': tarea})