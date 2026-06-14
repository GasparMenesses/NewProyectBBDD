from flask import request, jsonify
from database import get_db_connection
from mysql.connector import Error
from . import inscripciones_bp

@inscripciones_bp.route('/api/inscripciones', methods=['POST'])
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
        conn.start_transaction()
        
        cursor.execute("SELECT 1 FROM estudiantes WHERE documento = %s", (est_documento,))
        estudiante = cursor.fetchone()
        if not estudiante:
            conn.rollback()
            return jsonify({"error": "El estudiante no existe. Regístrelo primero en /api/estudiantes."}), 400

        # Bloqueamos la fila de la actividad para evitar race conditions en la inscripción
        cursor.execute("SELECT cupo_maximo, estado FROM actividad WHERE id_actividad = %s FOR UPDATE", (id_actividad,))
        actividad = cursor.fetchone()
        
        if not actividad or actividad['estado'] != 'abierta':
            conn.rollback()
            return jsonify({"error": "Inscripción denegada: Actividad no disponible"}), 400

        cursor.execute("SELECT id_inscripcion FROM inscripcion WHERE est_documento = %s AND id_actividad = %s", (est_documento, id_actividad))
        if cursor.fetchone():
            conn.rollback()
            return jsonify({"error": "El estudiante ya está inscrito"}), 400

        cursor.execute("SELECT COUNT(*) as ocupados FROM inscripcion WHERE id_actividad = %s AND estado = 'confirmada'", (id_actividad,))
        cupos_ocupados = cursor.fetchone()['ocupados']
        
        estado_final = 'confirmada' if cupos_ocupados < actividad['cupo_maximo'] else 'lista_espera'
        
        cursor.execute("INSERT INTO inscripcion (est_documento, id_actividad, estado, fecha_inscripcion) VALUES (%s, %s, %s, NOW())", (est_documento, id_actividad, estado_final))
        conn.commit()
        return jsonify({"message": f"Inscripción procesada con éxito ({estado_final})", "estado_asignado": estado_final}), 201
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@inscripciones_bp.route('/api/inscripciones/cancelar', methods=['POST'])
def cancelar_inscripcion():
    data = request.json or {}
    est_documento = data.get('est_documento')
    id_actividad = data.get('id_actividad')
    
    if not est_documento or not id_actividad:
        return jsonify({"error": "Faltan documento o actividad"}), 400

    conn = get_db_connection()
    if not conn: return jsonify({"error": "Error de BD"}), 500
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT id_inscripcion, estado FROM inscripcion WHERE est_documento = %s AND id_actividad = %s", (est_documento, id_actividad))
        insc = cursor.fetchone()
        
        if not insc:
            return jsonify({"error": "Inscripción no encontrada"}), 404
        
        if insc['estado'] == 'cancelada':
            return jsonify({"error": "La inscripción ya estaba cancelada"}), 400
            
        cursor.execute("UPDATE inscripcion SET estado = 'cancelada' WHERE id_inscripcion = %s", (insc['id_inscripcion'],))
        conn.commit()
        return jsonify({"message": "Inscripción cancelada con éxito. La lista de espera avanzó si correspondía."}), 200
    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
