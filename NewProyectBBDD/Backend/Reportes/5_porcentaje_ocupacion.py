from flask import Blueprint
from reportes.utils import ejecutar_consulta_reporte

r5_bp = Blueprint('r5', __name__)

@r5_bp.route('/api/reportes/5', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT a.id_actividad, a.nombre as nombre_actividad, a.cupo_maximo, COUNT(i.id_inscripcion) AS cupos_ocupados, 
               IFNULL((COUNT(i.id_inscripcion) * 100) / a.cupo_maximo, 0) AS porcentaje_ocupacion 
        FROM actividad a 
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada' 
        GROUP BY a.id_actividad, a.nombre, a.cupo_maximo 
        ORDER BY porcentaje_ocupacion DESC
    """
    return ejecutar_consulta_reporte(sql)