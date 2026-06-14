from flask import Blueprint, jsonify, request
from database import get_db_connection
from mysql.connector import Error

estudiantes_bp = Blueprint('estudiantes', __name__)

@estudiantes_bp.route('/api/estudiantes', methods=['GET'])
def listar_estudiantes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM estudiantes")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

@estudiantes_bp.route('/api/estudiantes', methods=['POST'])
def crear_estudiante():
    data = request.json or {}

    campos = ["documento", "nombre", "apellido", "correo_electronico", "carrera", "facultad"]
    if not all(data.get(campo) for campo in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO estudiantes
            (documento, nombre, apellido, correo_electronico, carrera, facultad)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data["documento"],
            data["nombre"],
            data["apellido"],
            data["correo_electronico"],
            data["carrera"],
            data["facultad"]
        ))

        conn.commit()
        return jsonify({"message": "Estudiante creado correctamente"}), 201

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@estudiantes_bp.route('/api/estudiantes/<int:documento>', methods=['PUT'])
def modificar_estudiante(documento):
    data = request.json or {}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE estudiantes
            SET nombre = %s,
                apellido = %s,
                correo_electronico = %s,
                carrera = %s,
                facultad = %s
            WHERE documento = %s
        """, (
            data.get("nombre"),
            data.get("apellido"),
            data.get("correo_electronico"),
            data.get("carrera"),
            data.get("facultad"),
            documento
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        return jsonify({"message": "Estudiante modificado correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@estudiantes_bp.route('/api/estudiantes/<int:documento>', methods=['DELETE'])
def eliminar_estudiante(documento):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM estudiantes WHERE documento = %s", (documento,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        return jsonify({"message": "Estudiante eliminado correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()