from flask import Blueprint

inscripciones_bp = Blueprint('inscripciones_bp', __name__)

from . import routes
