from flask import Blueprint
from .utils import ejecutar_consulta_reporte

r2_bp = Blueprint('r2', __name__)

@r2_bp.route('/api/reportes/2', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT a.id_actividad, a.nombre AS nombre_actividad, a.cupo_maximo, COUNT(i.id_inscripcion) AS ocupados, 
               (a.cupo_maximo - COUNT(i.id_inscripcion)) AS cupos_disponibles 
        FROM actividad a 
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada' 
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo 
        HAVING cupos_disponibles > 0
    """
    return ejecutar_consulta_reporte(sql)