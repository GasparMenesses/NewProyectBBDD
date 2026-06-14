from flask import Blueprint, jsonify, request
from database import get_db_connection
from mysql.connector import Error

asistencias_bp = Blueprint('asistencias', __name__)

@asistencias_bp.route('/api/asistencias', methods=['GET'])
def listar_asistencias():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM asistencia")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

@asistencias_bp.route('/api/asistencias', methods=['POST'])
def registrar_asistencia():
    data = request.json or {}

    if not data.get("id_inscripcion") or not data.get("fecha") or data.get("asistio") is None:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT estado
            FROM inscripcion
            WHERE id_inscripcion = %s
        """, (data["id_inscripcion"],))

        inscripcion = cursor.fetchone()

        if not inscripcion:
            return jsonify({"error": "La inscripción no existe"}), 404

        if inscripcion["estado"] != "confirmada":
            return jsonify({"error": "Solo se puede registrar asistencia de estudiantes confirmados"}), 400

        cursor.execute("""
            INSERT INTO asistencia
            (id_inscripcion, fecha, asistio)
            VALUES (%s, %s, %s)
        """, (
            data["id_inscripcion"],
            data["fecha"],
            data["asistio"]
        ))

        conn.commit()
        return jsonify({"message": "Asistencia registrada correctamente"}), 201

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()