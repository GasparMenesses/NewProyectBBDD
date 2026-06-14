from flask import jsonify
from database import get_db_connection
from mysql.connector import Error

def ejecutar_consulta_reporte(query, params=None):
    conectar = get_db_connection()
    if not conectar:
        return jsonify({"error": "Error crítico: No se pudo conectar a la base de datos."}), 500
    
    cursor = conectar.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
    except Error as e:
        return jsonify({"error": f"Error de ejecución: {str(e)}"}), 400
    finally:
        cursor.close()
        conectar.close()