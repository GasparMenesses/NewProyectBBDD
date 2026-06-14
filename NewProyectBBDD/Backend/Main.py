import os
from flask import Flask, session, redirect, url_for, render_template

# IMPORTACIÓN CORPORATIVA LIMPIA (BLUEPRINTS)
from Reportes import reportes_bp
from ABM import abm_bp
from Auth import auth_bp
from Inscripciones import inscripciones_bp

app = Flask(__name__, static_folder="Styles", static_url_path="/Styles")
app.secret_key = "sistema_deportivo_universitario_2026"

# Registramos todos los Blueprints (Módulos separados según SOLID)
app.register_blueprint(reportes_bp)
app.register_blueprint(abm_bp)
app.register_blueprint(auth_bp) # Provee /login, /register, /logout
app.register_blueprint(inscripciones_bp) # Provee /api/inscripciones y /api/inscripciones/cancelar

# --- RUTAS PRINCIPALES ---

@app.route('/')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('auth_bp.login'))
    
    return render_template('dashboard.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)