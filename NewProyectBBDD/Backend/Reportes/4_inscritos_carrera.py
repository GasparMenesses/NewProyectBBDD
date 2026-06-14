from flask import Blueprint
from reportes.utils import ejecutar_consulta_reporte

r4_bp = Blueprint('r4', __name__)

@r4_bp.route('/api/reportes/4', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT e.carrera as nombre_carrera, e.facultad as facultad, COUNT(DISTINCT e.documento) as cantidad_inscriptos 
        FROM estudiantes e 
        LEFT JOIN inscripcion i ON e.documento = i.est_documento AND i.estado = 'confirmada' 
        GROUP BY e.carrera, e.facultad 
        ORDER BY cantidad_inscriptos DESC
    """
    return ejecutar_consulta_reporte(sql)