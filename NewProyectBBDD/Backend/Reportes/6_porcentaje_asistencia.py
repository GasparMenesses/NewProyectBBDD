from flask import Blueprint
from reportes.utils import ejecutar_consulta_reporte

r6_bp = Blueprint('r6', __name__)

@r6_bp.route('/api/reportes/6', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT ac.id_actividad, ac.nombre as nombre_actividad, COUNT(asist.id_asistencia) AS asistencias_guardadas, 
               IFNULL(SUM(asist.asistio), 0) AS asistencias_reales, 
               IFNULL((SUM(asist.asistio) * 100) / COUNT(asist.id_asistencia), 0) AS porcentaje 
        FROM actividad ac 
        LEFT JOIN inscripcion i ON ac.id_actividad = i.id_actividad 
        LEFT JOIN asistencia asist ON i.id_inscripcion = asist.id_inscripcion 
        GROUP BY ac.id_actividad, ac.nombre 
        ORDER BY porcentaje DESC
    """
    return ejecutar_consulta_reporte(sql)