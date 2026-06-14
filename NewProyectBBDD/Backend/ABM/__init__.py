from flask import Blueprint

abm_bp = Blueprint('abm_master', __name__)

from .estudiantes import estudiantes_bp
from .disciplinas import disciplinas_bp
from .espacios import espacios_bp
from .actividades import actividades_bp
from .asistencias import asistencias_bp

abm_bp.register_blueprint(estudiantes_bp)
abm_bp.register_blueprint(disciplinas_bp)
abm_bp.register_blueprint(espacios_bp)
abm_bp.register_blueprint(actividades_bp)
abm_bp.register_blueprint(asistencias_bp)