import os
from flask import Flask, jsonify, request, render_template_string
from database import get_db_connection
from reportes import reportes_bp  # IMPORTACIÓN CORPORATIVA LIMPIA
from mysql.connector import Error

app = Flask(__name__)

# Registramos el bloque maestro de reportes con todos sus archivos separados
app.register_blueprint(reportes_bp)

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
            .footer-status { margin-top: 40px; background: #eff6ff; padding: 15px; border-left: 5px solid #2563eb; font-size: 14px; color: #1e40af; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sistema de Gestión Deportiva - UCU (Arquitectura Distribuida)</h1>
            <p>Módulos de Reportes completamente desacoplados en archivos independientes de clase empresarial.</p>
            
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
                <strong>Nota de Diseño de Arquitectura:</strong> Cada endpoint listado arriba es procesado de forma asíncrona por un módulo Python desacoplado. Esto permite escalabilidad horizontal ilimitada en el procesamiento de Big Data.
            </div>
        </div>
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