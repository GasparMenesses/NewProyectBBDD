# UCU Deportes - Instrucciones para ejecutar localmente

## Descripción
Este proyecto es un backend Flask para un sistema de gestión deportiva de la UCU.
Incluye un servicio web en Python que consulta una base de datos MySQL con tablas de estudiantes, disciplinas, actividades, inscripciones y asistencias.

## Estructura clave
- `docker-compose.yml` - define los servicios `db` (MySQL) y `web` (Flask).
- `Backend/` - contiene el backend Python.
- `Backend/Main.py` - aplicación Flask principal.
- `Backend/database.py` - conexión a MySQL usando variables de entorno.
- `SQL/schema.sql` - crea la base de datos y las tablas.
- `SQL/seed.sql` - inserta datos iniciales.

## Requisitos previos
- Docker Desktop instalado
- Docker Compose (incluido en Docker Desktop)
- Windows PowerShell o terminal compatible

## Opción 1: Ejecutar con Docker Compose (recomendado)

### 1. Ir al directorio del proyecto
Abre una terminal en:

```powershell
cd C:\Users\gdico\PycharmProjects\NewProyectBBDD\NewProyectBBDD
```

### 2. Detener y limpiar cualquier ejecución previa

```powershell
docker compose down -v
```

Esto eliminará contenedores, red y volumen de MySQL para forzar la inicialización limpia.

### 3. Levantar los servicios

```powershell
docker compose up --build
```

### 4. Esperar a que arranque
- MySQL se inicializa y carga `SQL/schema.sql` y `SQL/seed.sql`
- Flask arranca el servidor en `http://localhost:5000`

### 5. Probar el servicio
Abre en tu navegador:

- `http://localhost:5000` - página principal del dashboard
- `http://localhost:5000/api/reportes/1` - primer reporte

## Endpoints disponibles
- `GET /api/reportes/1` - Actividades con más inscriptos
- `GET /api/reportes/2` - Actividades con cupos disponibles
- `GET /api/reportes/3` - Inscriptos por disciplina
- `GET /api/reportes/4` - Inscriptos por carrera/facultad
- `GET /api/reportes/5` - Porcentaje de ocupación
- `GET /api/reportes/6` - Porcentaje de asistencia
- `GET /api/reportes/7` - Alertas alumnos >= 3 faltas
- `GET /api/reportes/8a` - Estudiantes en lista de espera
- `GET /api/reportes/8b` - Disciplinas sin actividad
- `POST /api/inscripciones` - registrar inscripción

### Ejemplo de POST para inscripciones

```json
{
  "est_documento": 41234567,
  "id_actividad": 1
}
```

## Opción 2: Ejecutar localmente sin Docker

### 1. Instalar Python
Asegúrate de tener Python 3.11 o superior.

### 2. Crear entorno virtual y dependencias

```powershell
cd C:\Users\gdico\PycharmProjects\NewProyectBBDD\NewProyectBBDD\Backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configurar la base de datos
Debes tener MySQL ejecutándose localmente y una base de datos `deportes_ucu` con las mismas tablas.

### 4. Archivo `.env`
El backend lee estas variables desde `Backend/.env` si ejecutas localmente.

Ejemplo de `.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=deportes_ucu
DB_PORT=3306
FLASK_APP=Main.py
FLASK_ENV=development
```

### 5. Ejecutar la aplicación

```powershell
python Main.py
```

Luego abre `http://localhost:5000`.

## Problemas comunes

### Misma ruta SQL en Docker
Asegúrate de que `docker-compose.yml` use estas rutas:

```yaml
- ./SQL/schema.sql:/docker-entrypoint-initdb.d/1-schema.sql
- ./SQL/seed.sql:/docker-entrypoint-initdb.d/2-seed.sql
```

### Error de conexión a la base de datos
- Si usas Docker Compose, el backend ya recibe las variables desde el `docker-compose.yml`.
- Si ejecutas localmente, comprueba `Backend/.env` y que MySQL esté accesible en `DB_HOST`.

### Forzar reinicio de la base de datos
Si ya levantaste el proyecto antes y hay datos o volumen corruptos:

```powershell
docker compose down -v
docker compose up --build
```

## Notas adicionales
- La aplicación web corre en el puerto `5000`.
- El contenedor `db` usa MySQL 8.0.
- El contenedor `web` ejecuta `python Main.py` automáticamente.

---

Con esto ya tienes todo lo necesario para ejecutar el proyecto localmente y probar sus endpoints.
