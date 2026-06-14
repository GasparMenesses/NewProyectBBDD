import os
from flask import Flask, jsonify, request, render_template_string
from database import get_db_connection
from Reportes import reportes_bp  # IMPORTACIÓN CORPORATIVA LIMPIA
from mysql.connector import Error
from ABM import abm_bp

app = Flask(__name__)

# Registramos el bloque maestro de reportes con todos sus archivos separados
app.register_blueprint(reportes_bp)
app.register_blueprint(abm_bp)

@app.route('/')
def dashboard():
    html_layout = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>UCU Deportes - Arquitectura Empresarial</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background-color: #f3f4f6; margin: 0; padding: 30px; }
            .container { max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
            h1 { color: #1e3a8a; border-bottom: 3px solid #3b82f6; padding-bottom: 10px; margin-top: 0; }
            h3 { color: #4b5563; margin-top: 25px; }
            .btn-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }
            .btn { background: #2563eb; color: white; padding: 12px; text-decoration: none; text-align: center; border-radius: 6px; font-weight: 500; transition: 0.2s; }
            .btn:hover { background: #1d4ed8; }
            .btn-alt { background: #10b981; } .btn-alt:hover { background: #059669; }
            .form-card { background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; margin-top: 25px; }
            .grid-two-column { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }
            .form-group { display: grid; gap: 12px; margin-bottom: 18px; }
            label { font-weight: 600; color: #334155; }
            input, select { width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 14px; }
            button[type="submit"] { background: #2563eb; color: white; border: none; border-radius: 8px; padding: 14px 18px; cursor: pointer; font-weight: 600; }
            button[type="submit"]:hover { background: #1d4ed8; }
            .message { margin-top: 16px; padding: 14px 16px; border-radius: 8px; font-weight: 600; display: none; }
            .message.success { background: #dcfce7; color: #166534; border: 1px solid #bef264; }
            .message.error { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
            .footer-status { margin-top: 40px; background: #eff6ff; padding: 15px; border-left: 5px solid #2563eb; font-size: 14px; color: #1e40af; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sistema de Gestión Deportiva - UCU (Arquitectura Distribuida)</h1>
            <p>Módulos de Reportes y gestión de inscripciones desde la misma aplicación Flask.</p>

            <div class="grid-two-column">
                <div class="form-card">
                    <h3>Registrar Inscripción</h3>
                    <form id="inscripcion-form">
                        <div class="form-group">
                            <label for="est_documento">Documento del Estudiante</label>
                            <select id="est_documento" name="est_documento" required>
                                <option value="">Cargando estudiantes...</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="id_actividad">Actividad</label>
                            <select id="id_actividad" name="id_actividad" required>
                                <option value="">Cargando actividades...</option>
                            </select>
                        </div>
                        <button type="submit">Enviar inscripción</button>
                    </form>
                    <div id="inscripcion-message" class="message"></div>
                </div>

                <div class="form-card">
                    <h3>Crear Estudiante</h3>
                    <form id="crear-estudiante-form">
                        <div class="form-group">
                            <label for="doc_nuevo">Documento</label>
                            <input type="number" id="doc_nuevo" name="documento" placeholder="Ej. 52456789" required />
                        </div>
                        <div class="form-group">
                            <label for="nombre_nuevo">Nombre</label>
                            <input type="text" id="nombre_nuevo" name="nombre" placeholder="Nombre" required />
                        </div>
                        <div class="form-group">
                            <label for="apellido_nuevo">Apellido</label>
                            <input type="text" id="apellido_nuevo" name="apellido" placeholder="Apellido" required />
                        </div>
                        <div class="form-group">
                            <label for="correo_nuevo">Correo electrónico</label>
                            <input type="email" id="correo_nuevo" name="correo_electronico" placeholder="correo@ucu.edu.uy" required />
                        </div>
                        <div class="form-group">
                            <label for="carrera_nueva">Carrera</label>
                            <input type="text" id="carrera_nueva" name="carrera" placeholder="Ingenieria" required />
                        </div>
                        <div class="form-group">
                            <label for="facultad_nueva">Facultad</label>
                            <input type="text" id="facultad_nueva" name="facultad" placeholder="Empresariales" required />
                        </div>
                        <button type="submit">Crear estudiante</button>
                    </form>
                    <div id="estudiante-message" class="message"></div>
                </div>
            </div>

            <div class="grid-two-column">
                <div class="form-card">
                    <h3>Crear Disciplina</h3>
                    <form id="crear-disciplina-form">
                        <div class="form-group">
                            <label for="nombre_disciplina">Nombre de disciplina</label>
                            <input type="text" id="nombre_disciplina" name="nombre" placeholder="Futbol" required />
                        </div>
                        <button type="submit">Crear disciplina</button>
                    </form>
                    <div id="disciplina-message" class="message"></div>
                </div>

                <div class="form-card">
                    <h3>Crear Espacio</h3>
                    <form id="crear-espacio-form">
                        <div class="form-group">
                            <label for="nombre_espacio">Nombre del espacio</label>
                            <input type="text" id="nombre_espacio" name="nombre" placeholder="Gimnasio Deportivo" required />
                        </div>
                        <div class="form-group">
                            <label for="ubicacion_espacio">Ubicación</label>
                            <input type="text" id="ubicacion_espacio" name="ubicacion" placeholder="Campus Montevideo" required />
                        </div>
                        <button type="submit">Crear espacio</button>
                    </form>
                    <div id="espacio-message" class="message"></div>
                </div>
            </div>

            <div class="form-card">
                <h3>Registrar Asistencia</h3>
                <form id="crear-asistencia-form">
                    <div class="form-group">
                        <label for="id_inscripcion">ID de Inscripción</label>
                        <input type="number" id="id_inscripcion" name="id_inscripcion" placeholder="Ej. 1" required />
                    </div>
                    <div class="form-group">
                        <label for="fecha_asistencia">Fecha</label>
                        <input type="date" id="fecha_asistencia" name="fecha" required />
                    </div>
                    <div class="form-group">
                        <label>Asistió</label>
                        <select id="asistio" name="asistio" required>
                            <option value="">Seleccione</option>
                            <option value="true">Sí</option>
                            <option value="false">No</option>
                        </select>
                    </div>
                    <button type="submit">Registrar asistencia</button>
                </form>
                <div id="asistencia-message" class="message"></div>
            </div>

            <h3>Endpoints Separados por Capas (JSON)</h3>
            <div class="btn-grid">
                <a class="btn" href="/api/reportes/1" target="_blank">1. Actividades con más Inscriptos</a>
                <a class="btn" href="/api/reportes/2" target="_blank">2. Actividades con Cupos Disponibles</a>
                <a class="btn" href="/api/reportes/3" target="_blank">3. Inscriptos por Disciplina</a>
                <a class="btn" href="/api/reportes/4" target="_blank">4. Inscriptos por Carrera/Facultad</a>
                <a class="btn" href="/api/reportes/5" target="_blank">5. Porcentaje de Ocupación</a>
                <a class="btn" href="/api/reportes/6" target="_blank">6. Porcentaje de Asistencia</a>
                <a class="btn" href="/api/reportes/7" target="_blank">7. Alertas Alumnos >= 3 Faltas</a>
            </div>

            <h3>Consultas Adicionales</h3>
            <div class="btn-grid">
                <a class="btn btn-alt" href="/api/reportes/8a" target="_blank">8a. Estudiantes en Lista de Espera</a>
                <a class="btn btn-alt" href="/api/reportes/8b" target="_blank">8b. Disciplinas sin Actividades</a>
            </div>

            <div class="footer-status">
                <strong>Nota de Diseño de Arquitectura:</strong> El formulario de inscripción envía datos al endpoint `POST /api/inscripciones` y muestra el resultado sin recargar la página.
            </div>
        </div>
        <script>
            async function cargarActividades() {
                const select = document.getElementById('id_actividad');
                try {
                    const response = await fetch('/api/actividades');
                    if (!response.ok) throw new Error('No se pudo cargar la lista de actividades');
                    const actividades = await response.json();
                    select.innerHTML = '<option value="">Selecciona una actividad</option>' + actividades.map(a => `
                        <option value="${a.id_actividad}">${a.id_actividad} - ${a.nombre} (${a.estado})</option>
                    `).join('');
                } catch (error) {
                    select.innerHTML = '<option value="">Error al cargar actividades</option>';
                    console.error(error);
                }
            }

            async function cargarEstudiantes() {
                const select = document.getElementById('est_documento');
                try {
                    const response = await fetch('/api/estudiantes');
                    if (!response.ok) throw new Error('No se pudo cargar la lista de estudiantes');
                    const estudiantes = await response.json();
                    select.innerHTML = '<option value="">Selecciona un estudiante</option>' + estudiantes.map(e => `
                        <option value="${e.documento}">${e.documento} - ${e.nombre} ${e.apellido} (${e.carrera})</option>
                    `).join('');
                } catch (error) {
                    select.innerHTML = '<option value="">Error al cargar estudiantes</option>';
                    console.error(error);
                }
            }

            async function enviarFormulario(formId, url, messageId) {
                const form = document.getElementById(formId);
                const message = document.getElementById(messageId);
                const payload = {};

                new FormData(form).forEach((value, key) => {
                    if (value === 'true') value = true;
                    if (value === 'false') value = false;
                    if (['documento', 'id_inscripcion', 'id_actividad'].includes(key)) value = Number(value);
                    payload[key] = value;
                });

                try {
                    const response = await fetch(url, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    const resultado = await response.json();
                    if (!response.ok) {
                        message.textContent = resultado.error || 'Error al procesar la solicitud';
                        message.className = 'message error';
                        message.style.display = 'block';
                        return;
                    }

                    message.textContent = resultado.message;
                    message.className = 'message success';
                    message.style.display = 'block';
                    form.reset();
                    if (formId === 'crear-estudiante-form') {
                        cargarEstudiantes();
                    }
                } catch (error) {
                    message.textContent = 'Error de conexión con el servidor.';
                    message.className = 'message error';
                    message.style.display = 'block';
                    console.error(error);
                }
            }

            document.getElementById('inscripcion-form').addEventListener('submit', function(event) {
                event.preventDefault();
                enviarFormulario('inscripcion-form', '/api/inscripciones', 'inscripcion-message');
            });

            document.getElementById('crear-estudiante-form').addEventListener('submit', function(event) {
                event.preventDefault();
                enviarFormulario('crear-estudiante-form', '/api/estudiantes', 'estudiante-message');
            });

            document.getElementById('crear-disciplina-form').addEventListener('submit', function(event) {
                event.preventDefault();
                enviarFormulario('crear-disciplina-form', '/api/disciplinas', 'disciplina-message');
            });

            document.getElementById('crear-espacio-form').addEventListener('submit', function(event) {
                event.preventDefault();
                enviarFormulario('crear-espacio-form', '/api/espacios', 'espacio-message');
            });

            document.getElementById('crear-asistencia-form').addEventListener('submit', function(event) {
                event.preventDefault();
                enviarFormulario('crear-asistencia-form', '/api/asistencias', 'asistencia-message');
            });

            cargarActividades();
            cargarEstudiantes();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_layout)

# --- CAPA DE INSCRIPCIONES CON REGLAS DE NEGOCIO ---
@app.route('/api/inscripciones', methods=['POST'])
def registrar_inscripcion():
    data = request.json or {}
    est_documento = data.get('est_documento')
    id_actividad = data.get('id_actividad')
    
    if not est_documento or not id_actividad:
        return jsonify({"error": "Datos requeridos faltantes"}), 400
        
    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de BD"}), 500
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT 1 FROM estudiantes WHERE documento = %s", (est_documento,))
        estudiante = cursor.fetchone()
        if not estudiante:
            return jsonify({"error": "El estudiante no existe. Regístrelo primero en /api/estudiantes."}), 400

        cursor.execute("SELECT cupo_maximo, estado FROM actividad WHERE id_actividad = %s", (id_actividad,))
        actividad = cursor.fetchone()
        
        if not actividad or actividad['estado'] != 'abierta':
            return jsonify({"error": "Inscripción denegada: Actividad no disponible"}), 400

        cursor.execute("SELECT id_inscripcion FROM inscripcion WHERE est_documento = %s AND id_actividad = %s", (est_documento, id_actividad))
        if cursor.fetchone():
            return jsonify({"error": "El estudiante ya está inscrito"}), 400

        cursor.execute("SELECT COUNT(*) as ocupados FROM inscripcion WHERE id_actividad = %s AND estado = 'confirmada'", (id_actividad,))
        cupos_ocupados = cursor.fetchone()['ocupados']
        
        estado_final = 'confirmada' if cupos_ocupados < actividad['cupo_maximo'] else 'lista_espera'
        
        cursor.execute("INSERT INTO inscripcion (est_documento, id_actividad, estado, fecha_inscripcion) VALUES (%s, %s, %s, NOW())", (est_documento, id_actividad, estado_final))
        conn.commit()
        return jsonify({"message": "Inscripción procesada con éxito", "estado_asignado": estado_final}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)