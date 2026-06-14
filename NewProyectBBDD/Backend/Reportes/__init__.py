from flask import Blueprint

# Creamos el Blueprint unificado de reportes empresarial
reportes_bp = Blueprint('reportes_master', __name__)

# Importamos las sub-rutas individuales
from .inscritos_actividad import r1_bp
from .cupos_disponibles import r2_bp
from .inscritos_disciplina import r3_bp
from .inscritos_carrera import r4_bp
from .porcentaje_ocupacion import r5_bp
from .porcentaje_asistencia import r6_bp
from .alertas_inasistencias import r7_bp
from .lista_espera import r8a_bp
from .disciplinas_sin_actividad import r8b_bp
from .espacios_fisicos import r8c_bp

# Lista de blueprints para iterar y registrar de forma limpia
sub_blueprints = [r1_bp, r2_bp, r3_bp, r4_bp, r5_bp, r6_bp, r7_bp, r8a_bp, r8b_bp, r8c_bp]

for bp in sub_blueprints:
    reportes_bp.register_blueprint(bp)