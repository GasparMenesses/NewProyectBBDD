from flask import Blueprint
from .utils import ejecutar_consulta_reporte

r8c_bp = Blueprint('r8c', __name__)

@r8c_bp.route('/api/reportes/8c', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT e.ubicacion, e.nombre AS nombre_espacio, COUNT(a.id_actividad) AS cantidad_actividades
        FROM espacio e
        LEFT JOIN actividad a ON e.id_espacio = a.id_espacio
        GROUP BY e.id_espacio, e.ubicacion, e.nombre
        ORDER BY cantidad_actividades DESC;
    """
    return ejecutar_consulta_reporte(sql)
