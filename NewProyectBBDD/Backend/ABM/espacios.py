from flask import Blueprint, jsonify, request
from database import get_db_connection
from mysql.connector import Error

espacios_bp = Blueprint('espacios', __name__)

@espacios_bp.route('/api/espacios', methods=['GET'])
def listar_espacios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM espacio")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

@espacios_bp.route('/api/espacios', methods=['POST'])
def crear_espacio():
    data = request.json or {}

    if not data.get("nombre") or not data.get("ubicacion"):
        return jsonify({"error": "Nombre y ubicación son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO espacio (nombre, ubicacion)
            VALUES (%s, %s)
        """, (data["nombre"], data["ubicacion"]))

        conn.commit()
        return jsonify({"message": "Espacio creado correctamente"}), 201

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@espacios_bp.route('/api/espacios/<int:id_espacio>', methods=['PUT'])
def modificar_espacio(id_espacio):
    data = request.json or {}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE espacio
            SET nombre = %s,
                ubicacion = %s
            WHERE id_espacio = %s
        """, (data.get("nombre"), data.get("ubicacion"), id_espacio))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Espacio no encontrado"}), 404

        return jsonify({"message": "Espacio modificado correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@espacios_bp.route('/api/espacios/<int:id_espacio>', methods=['DELETE'])
def eliminar_espacio(id_espacio):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM espacio WHERE id_espacio = %s", (id_espacio,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Espacio no encontrado"}), 404

        return jsonify({"message": "Espacio eliminado correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()