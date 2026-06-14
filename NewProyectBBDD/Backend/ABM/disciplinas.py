from flask import Blueprint, jsonify, request
from database import get_db_connection
from mysql.connector import Error

disciplinas_bp = Blueprint('disciplinas', __name__)

@disciplinas_bp.route('/api/disciplinas', methods=['GET'])
def listar_disciplinas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM disciplina_deportiva")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

@disciplinas_bp.route('/api/disciplinas', methods=['POST'])
def crear_disciplina():
    data = request.json or {}

    if not data.get("nombre"):
        return jsonify({"error": "El nombre es obligatorio"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO disciplina_deportiva (nombre)
            VALUES (%s)
        """, (data["nombre"],))

        conn.commit()
        return jsonify({"message": "Disciplina creada correctamente"}), 201

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@disciplinas_bp.route('/api/disciplinas/<int:id_disciplina>', methods=['PUT'])
def modificar_disciplina(id_disciplina):
    data = request.json or {}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE disciplina_deportiva
            SET nombre = %s
            WHERE id_disciplina = %s
        """, (data.get("nombre"), id_disciplina))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Disciplina no encontrada"}), 404

        return jsonify({"message": "Disciplina modificada correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@disciplinas_bp.route('/api/disciplinas/<int:id_disciplina>', methods=['DELETE'])
def eliminar_disciplina(id_disciplina):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM disciplina_deportiva WHERE id_disciplina = %s", (id_disciplina,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Disciplina no encontrada"}), 404

        return jsonify({"message": "Disciplina eliminada correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()