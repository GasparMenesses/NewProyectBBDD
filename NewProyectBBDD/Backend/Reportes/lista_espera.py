from flask import Blueprint
from .utils import ejecutar_consulta_reporte

r8a_bp = Blueprint('r8a', __name__)

@r8a_bp.route('/api/reportes/8a', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT e.documento, e.nombre, e.apellido, a.nombre as nombre_actividad, i.fecha_inscripcion 
        FROM inscripcion i 
        JOIN estudiantes e ON i.est_documento = e.documento 
        JOIN actividad a ON a.id_actividad = i.id_actividad 
        WHERE i.estado = 'lista_espera'
    """
    return ejecutar_consulta_reporte(sql)