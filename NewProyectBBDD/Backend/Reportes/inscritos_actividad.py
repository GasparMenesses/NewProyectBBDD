from flask import Blueprint
from .utils import ejecutar_consulta_reporte

r1_bp = Blueprint('r1', __name__)

@r1_bp.route('/api/reportes/1', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT a.id_actividad, a.nombre AS nombre_actividad, COUNT(i.id_inscripcion) AS cantidad_de_inscriptos 
        FROM actividad a 
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada' 
        GROUP BY a.id_actividad, a.nombre 
        ORDER BY cantidad_de_inscriptos DESC
    """
    return ejecutar_consulta_reporte(sql)