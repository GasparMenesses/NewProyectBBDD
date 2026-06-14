from flask import Blueprint
from reportes.utils import ejecutar_consulta_reporte

r7_bp = Blueprint('r7', __name__)

@r7_bp.route('/api/reportes/7', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT documento, nombre, apellido, COUNT(id_asistencia) AS inasistencias 
        FROM estudiantes 
        JOIN inscripcion i ON documento = est_documento 
        JOIN asistencia ON i.id_inscripcion = asistencia.id_inscripcion 
        WHERE asistio = FALSE 
        GROUP BY documento, nombre, apellido 
        HAVING inasistencias >= 3
    """
    return ejecutar_consulta_reporte(sql)