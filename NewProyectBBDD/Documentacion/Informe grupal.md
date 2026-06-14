Trabajo Obligatorio - Bases de Datos 1 
-

**1. Introducción**

El trabajo consiste en el desarrollo de un Sistema de Gestión de Actividades Deportivas Universitarias. El objetivo principal es permitir la administración de estudiantes, disciplinas deportivas, espacios, actividades, inscripciones y asistencias, sustituyendo el uso de planillas.
La aplicación fue desarrollada utilizando MySQL como sistema gestor de bases de datos y Python con Flask para el backend.

**2. Diseño de la Base de Datos**

Para realizar la solución se identificaron las siguientes entidades principales: Estudiantes, Disciplinas deportivas, Espacios, Actividades, Inscripciones, Asistencias, Usuarios.
Cada entidad cuenta con una clave primaria que permite identificar de forma única. Además, se definieron claves foráneas para mantener la integridad entre las tablas.

**3. Arquitectura de la Aplicación**

La aplicación fue desarrollada siguiendo una arquitectura organizada.

*Base de Datos:*

Responsable del almacenamiento de la información y de la aplicación.

*Backend*

Implementado en Python utilizando Flask. Se encarga de:
- Ejecutar consultas SQL. 
- Registrar inscripciones y asistencias. 
- Gestionar usuarios y autenticación.

*Frontend*

Se desarrolló una interfaz web que permite interactuar con el sistema.

*Docker*

Se utilizó Docker Compose para facilitar la ejecución del proyecto y aseguridad integridad. 

**4. Reportes implementado:**

Se desarrollaron las consultas requeridas por la consigna:
1.	Actividades con mayor cantidad de inscriptos confirmados.
2.	Actividades con cupos disponibles.
3.	Cantidad de inscriptos por disciplina deportiva.
4.	Cantidad de inscriptos por carrera o facultad.
5.	Porcentaje de ocupación por actividad.
6.	Porcentaje de asistencia por actividad.
7.	Estudiantes con tres o más inasistencias registradas.

Además, se agregaron consultas adicionales para ampliar la funcionalidad del sistema:

- Estudiantes en lista de espera. 
- Disciplinas sin actividades asociadas.


