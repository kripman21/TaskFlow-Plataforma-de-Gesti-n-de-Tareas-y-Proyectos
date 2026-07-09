# TaskFlow - Plataforma de Gestión de Tareas y Proyectos

TaskFlow es un sistema robusto de gestión de tareas desarrollado en **Django** y **Bootstrap 5**. Está diseñado para ayudar a equipos y organizaciones a administrar proyectos, asignar tareas y hacer un seguimiento detallado de la trazabilidad y los comentarios, con una arquitectura basada en Roles y Permisos (RBAC).

## 🚀 Funcionalidades Clave Implementadas

### 1. Autenticación y Autorización (RBAC)

* **Sistema de Roles:** Soporte nativo para usuarios estándar y Administradores (a través de Django Groups).
* **Control de Accesos:** Rutas protegidas (`@login_required`) y vistas restringidas exclusivamente para administradores (`@user_passes_test`).
* **Flujo Seguro:** Redirección automática tras login/logout.

### 2. Tableros y Dashboard Dinámico

* **Vista de Administrador:** Los administradores tienen una visión global de todos los proyectos y tareas del sistema.
* **Vista de Usuario:** Los usuarios estándar solo ven los proyectos relevantes y las tareas que tienen explícitamente asignadas.
* **Filtros de Interfaz:** Iconografía dinámica (Lucide Icons) e indicadores visuales de estado (Pendiente, En Progreso, Terminada) y prioridad.

### 3. Modelado de Datos Core

* **Proyectos:** Agrupaciones lógicas de trabajo.
* **Tareas:** Entidades asignables con fecha de entrega, prioridad, y estado (sincronización automática de estado al marcar como completada).
* **Bajas Lógicas (Soft Deletes):** Filtrado inteligente que impide asignar nuevas tareas a usuarios inactivos o despedidos (`is_active=False`), protegiendo el historial de la base de datos (evitando borrados en cascada destructivos).

### 4. Sistema de Auditoría y Trazabilidad

* **Historial Inmutable:** Todo registro de Tarea y Proyecto guarda quién fue el creador real (`creado_por`) y la `fecha_creacion`, independientemente de a quién se le haya asignado posteriormente.
* **Protección de Autoría:** Inyección del creador directamente en el backend mediante la sesión (`request.user`), evitando manipulaciones de identidad desde el HTML.

### 5. Historial y Comentarios

* **Comunicación Interna:** Vista de detalle que incluye un chat/historial de comentarios por tarea.
* **Patrón PRG:** Implementación de Post/Redirect/Get para procesar los comentarios sin generar envíos duplicados al recargar la página.

### 6. Papelera de Reciclaje y Ciclo de Vida del Dato

* **Bajas Lógicas:** Las tareas y proyectos no se borran inmediatamente de la base de datos, protegiendo contra pérdida accidental de información.
* **Papelera (Soft Undelete):** Interfaz dedicada donde los administradores y usuarios (solo de su propio contenido) pueden visualizar los elementos en la basura y restaurarlos.
* **Destrucción Definitiva:** Método protegido por POST para borrar permanente los datos (`Hard Delete`) cuando se confirme desde la Papelera.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.12, Django 4.2.11
* **Frontend:** HTML5, CSS3, Bootstrap 5 (integrado vía `django-bootstrap5`).
* **Iconografía:** Lucide Icons.
* **Base de Datos:** MySQL.

## 📅 Mapa de Ruta (Próximos Pasos)

* Finalizar operaciones CRUD (Formularios de Edición/Actualización) para Tareas y Proyectos.
* Mejoras de UX/UI mediante Modales de confirmación, notificaciones Toast, y refinamiento estético del Dashboard con múltiples vistas (Kanban, Grillas).
