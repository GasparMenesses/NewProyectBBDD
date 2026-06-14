from flask import request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection
from mysql.connector import Error
from . import auth_bp

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    mensaje = ""

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        if not usuario or not password:
            mensaje = "Debe completar usuario y contraseña"
        else:
            password_hash = generate_password_hash(password)

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            try:
                # Verificar si el usuario ya existe
                cursor.execute("""
                    SELECT usuario
                    FROM usuarios
                    WHERE usuario = %s
                """, (usuario,))

                if cursor.fetchone():
                    mensaje = "Ese nombre de usuario ya existe. Elegí otro."
                else:
                    cursor.execute("""
                        INSERT INTO usuarios (usuario, password_hash)
                        VALUES (%s, %s)
                    """, (usuario, password_hash))

                    conn.commit()
                    return redirect(url_for('auth_bp.login'))

            except Error as e:
                print("ERROR MYSQL:", e)
                mensaje = "Error al registrar usuario"

            finally:
                cursor.close()
                conn.close()

    return render_template('register.html', mensaje=mensaje)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = ""

    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM usuarios
            WHERE usuario = %s AND activo = TRUE
        """, (usuario,))

        usuario_db = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario_db and check_password_hash(usuario_db['password_hash'], password):
            session['usuario'] = usuario_db['usuario']
            return redirect(url_for('dashboard'))

        mensaje = "Usuario o contraseña incorrectos"

    return render_template('login.html', mensaje=mensaje)


@auth_bp.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('auth_bp.login'))
