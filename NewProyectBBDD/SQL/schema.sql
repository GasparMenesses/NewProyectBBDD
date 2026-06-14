CREATE DATABASE IF NOT EXISTS deportes_ucu;
USE deportes_ucu;

CREATE TABLE IF NOT EXISTS estudiantes ( 
    documento INT PRIMARY KEY, 
    nombre VARCHAR(100), 
    apellido VARCHAR(100), 
    correo_electronico VARCHAR(100), 
    carrera VARCHAR(100), 
    facultad VARCHAR(100) 
); 
 
CREATE TABLE IF NOT EXISTS disciplina_deportiva ( 
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100) 
); 
 
CREATE TABLE IF NOT EXISTS espacio ( 
    id_espacio INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100), 
    ubicacion VARCHAR(100) 
); 


CREATE TABLE IF NOT EXISTS actividad ( 
    id_actividad INT NOT NULL AUTO_INCREMENT, 
    nombre VARCHAR(100) NOT NULL, 
    id_disciplina INT NOT NULL, 
    id_espacio INT NOT NULL, 
    cupo_maximo INT NOT NULL, 
    dia_semana ENUM('lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo') NOT NULL, 
    horario_inicio TIME NOT NULL, 
    horario_fin TIME NOT NULL, 
    estado ENUM ('abierta', 'cerrada', 'finalizada', 'cancelada') NOT NULL DEFAULT 'abierta', 
    PRIMARY KEY (id_actividad), 
    FOREIGN KEY (id_disciplina) REFERENCES disciplina_deportiva(id_disciplina), 
    FOREIGN KEY (id_espacio) REFERENCES espacio(id_espacio) 
); 
 
CREATE TABLE IF NOT EXISTS inscripcion ( 
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY, 
    est_documento INT, 
    id_actividad INT, 
    estado ENUM ('confirmada', 'lista_espera') NOT NULL, 
    fecha_inscripcion DATETIME,	 
    FOREIGN KEY (est_documento) REFERENCES estudiantes(documento),  
    FOREIGN KEY (id_actividad) REFERENCES actividad(id_actividad),      
    UNIQUE(est_documento, id_actividad) 
); 
 
CREATE TABLE IF NOT EXISTS asistencia ( 
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY, 
    id_inscripcion INT NOT NULL, 
    fecha DATE NOT NULL, 
    asistio BOOLEAN NOT NULL, 
    FOREIGN KEY (id_inscripcion) REFERENCES inscripcion(id_inscripcion), 
    UNIQUE(id_inscripcion, fecha) 
);
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- TRIGGER: Validación estricta en Base de Datos (Regla de negocio 5)
DELIMITER //
CREATE TRIGGER tg_validar_asistencia_confirmada
BEFORE INSERT ON asistencia
FOR EACH ROW
BEGIN
    DECLARE v_estado VARCHAR(20);
    SELECT estado INTO v_estado FROM inscripcion WHERE id_inscripcion = NEW.id_inscripcion;
    IF v_estado != 'confirmada' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error de Regla de Negocio: Solo se puede registrar asistencia de alumnos con inscripcion confirmada.';
    END IF;
END //
DELIMITER ;