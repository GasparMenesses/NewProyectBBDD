from flask import Blueprint, jsonify, request
from database import get_db_connection
from mysql.connector import Error
import datetime

actividades_bp = Blueprint('actividades', __name__)


def serializar_fila(row):
    for key, value in row.items():
        if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
            row[key] = value.isoformat()
        elif isinstance(value, datetime.timedelta):
            row[key] = str(value)
    return row


@actividades_bp.route('/api/actividades', methods=['GET'])
def listar_actividades():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM actividad")
        actividades = cursor.fetchall()
        actividades = [serializar_fila(row) for row in actividades]
        return jsonify(actividades), 200
    finally:
        cursor.close()
        conn.close()

@actividades_bp.route('/api/actividades', methods=['POST'])
def crear_actividad():
    data = request.json or {}

    campos = [
        "nombre", "id_disciplina", "id_espacio", "cupo_maximo",
        "dia_semana", "horario_inicio", "horario_fin", "estado"
    ]

    if not all(data.get(campo) for campo in campos):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO actividad
            (nombre, id_disciplina, id_espacio, cupo_maximo,
             dia_semana, horario_inicio, horario_fin, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["nombre"],
            data["id_disciplina"],
            data["id_espacio"],
            data["cupo_maximo"],
            data["dia_semana"],
            data["horario_inicio"],
            data["horario_fin"],
            data["estado"]
        ))

        conn.commit()
        return jsonify({"message": "Actividad creada correctamente"}), 201

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@actividades_bp.route('/api/actividades/<int:id_actividad>', methods=['PUT'])
def modificar_actividad(id_actividad):
    data = request.json or {}

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE actividad
            SET nombre = %s,
                id_disciplina = %s,
                id_espacio = %s,
                cupo_maximo = %s,
                dia_semana = %s,
                horario_inicio = %s,
                horario_fin = %s,
                estado = %s
            WHERE id_actividad = %s
        """, (
            data.get("nombre"),
            data.get("id_disciplina"),
            data.get("id_espacio"),
            data.get("cupo_maximo"),
            data.get("dia_semana"),
            data.get("horario_inicio"),
            data.get("horario_fin"),
            data.get("estado"),
            id_actividad
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Actividad no encontrada"}), 404

        return jsonify({"message": "Actividad modificada correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

@actividades_bp.route('/api/actividades/<int:id_actividad>', methods=['DELETE'])
def eliminar_actividad(id_actividad):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM actividad WHERE id_actividad = %s", (id_actividad,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Actividad no encontrada"}), 404

        return jsonify({"message": "Actividad eliminada correctamente"}), 200

    except Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()