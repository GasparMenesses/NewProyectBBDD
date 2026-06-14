from flask import Blueprint
from reportes.utils import ejecutar_consulta_reporte

r3_bp = Blueprint('r3', __name__)

@r3_bp.route('/api/reportes/3', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT dd.id_disciplina, dd.nombre as nombre_disciplina, COUNT(i.id_inscripcion) as cantidad_inscriptos 
        FROM disciplina_deportiva dd 
        LEFT JOIN actividad a ON dd.id_disciplina = a.id_disciplina 
        LEFT JOIN inscripcion i ON a.id_actividad = i.id_actividad AND i.estado = 'confirmada' 
        GROUP BY dd.id_disciplina, dd.nombre
    """
    return ejecutar_consulta_reporte(sql)