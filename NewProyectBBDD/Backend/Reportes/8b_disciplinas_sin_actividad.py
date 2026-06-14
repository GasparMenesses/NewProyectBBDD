from flask import Blueprint
from reportes.utils import ejecutar_consulta_reporte

r8b_bp = Blueprint('r8b', __name__)

@r8b_bp.route('/api/reportes/8b', methods=['GET'])
def obtener_reporte():
    sql = """
        SELECT dd.id_disciplina, dd.nombre as disciplina_deportiva 
        FROM disciplina_deportiva dd 
        LEFT JOIN actividad a ON dd.id_disciplina = a.id_disciplina 
        WHERE a.id_disciplina IS NULL
    """
    return ejecutar_consulta_reporte(sql)