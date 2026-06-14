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
            body {
                font-family: 'Segoe UI', sans-serif;
                background: #0D0D1A;
                margin: 0;
                padding: 30px;
                color: #F0F0FF;
            }
        
            body::before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
        
                background:
                    radial-gradient(circle at top right,
                        rgba(6,182,212,0.12),
                        transparent 35%),
                    radial-gradient(circle at bottom left,
                        rgba(124,58,237,0.15),
                        transparent 40%);
            }
        
            .container {
                max-width: 1200px;
                margin: auto;
                background: #1A1A2E;
                padding: 30px;
                border-radius: 20px;
                border: 1px solid rgba(124,58,237,0.25);
                box-shadow: 0 0 40px rgba(124,58,237,0.15);
                position: relative;
                z-index: 1;
            }
        
            h1 {
                color: #F0F0FF;
                border-bottom: 3px solid #7C3AED;
                padding-bottom: 10px;
                margin-top: 0;
            }
        
            h3 {
                color: #06B6D4;
                margin-top: 25px;
            }
        
            p {
                color: #CFCFFB;
            }
        
            .btn-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 15px;
            }
        
            .grid-two-column {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 16px;
            }
        
            .form-card {
                background: rgba(255,255,255,0.02);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid rgba(124,58,237,0.20);
                box-shadow: 0 0 20px rgba(124,58,237,0.10);
                margin-top: 25px;
            }
        
            .form-group {
                display: grid;
                gap: 12px;
                margin-bottom: 18px;
            }
        
            label {
                font-weight: 600;
                color: #E5E7EB;
            }
        
            input,
            select {
                width: 100%;
                padding: 10px 12px;
                background: #111827;
                color: #F0F0FF;
                border: 1px solid #374151;
                border-radius: 8px;
                font-size: 14px;
                box-sizing: border-box;
            }
        
            input:focus,
            select:focus {
                outline: none;
                border-color: #06B6D4;
                box-shadow: 0 0 10px rgba(6,182,212,0.4);
            }
        
            button[type="submit"] {
                background: linear-gradient(
                    135deg,
                    #7C3AED,
                    #5B21B6
                );
        
                color: white;
                border: none;
                border-radius: 10px;
                padding: 14px;
                cursor: pointer;
                font-weight: 600;
                transition: 0.3s;
            }
        
            button[type="submit"]:hover {
                background: linear-gradient(
                    135deg,
                    #06B6D4,
                    #0891B2
                );
        
                box-shadow: 0 0 15px rgba(6,182,212,0.5);
            }
        
            .btn {
                background: linear-gradient(
                    135deg,
                    #7C3AED,
                    #4C1D95
                );
        
                color: white;
                padding: 14px;
                text-decoration: none;
                text-align: center;
                border-radius: 10px;
                font-weight: 600;
        
                border: 1px solid rgba(124,58,237,0.4);
        
                transition: all 0.3s ease;
        
                box-shadow:
                    0 0 10px rgba(124,58,237,0.3),
                    0 0 20px rgba(124,58,237,0.15);
            }
        
            .btn:hover {
                background: linear-gradient(
                    135deg,
                    #06B6D4,
                    #0891B2
                );
        
                transform: translateY(-2px);
        
                box-shadow:
                    0 0 15px rgba(6,182,212,0.5),
                    0 0 25px rgba(6,182,212,0.25);
            }
        
            .btn-alt {
                background: linear-gradient(
                    135deg,
                    #06B6D4,
                    #155E75
                );
            }
        
            .btn-alt:hover {
                background: linear-gradient(
                    135deg,
                    #7C3AED,
                    #5B21B6
                );
            }
        
            .message {
                margin-top: 16px;
                padding: 14px;
                border-radius: 8px;
                font-weight: 600;
                display: none;
            }
        
            .message.success {
                background: rgba(34,197,94,0.15);
                color: #86EFAC;
                border: 1px solid rgba(34,197,94,0.4);
            }
        
            .message.error {
                background: rgba(239,68,68,0.15);
                color: #FCA5A5;
                border: 1px solid rgba(239,68,68,0.4);
            }
        
            .footer-status {
                margin-top: 40px;
                background: rgba(255,255,255,0.03);
                padding: 18px;
                border-left: 4px solid #06B6D4;
                border-radius: 10px;
                color: #E0E7FF;
            }
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
                            <input type="number" id="doc_nuevo" name="documento" placeholder="Ej. 52456789" min="1" required />
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