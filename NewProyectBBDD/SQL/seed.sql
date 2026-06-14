USE deportes_ucu;

-- Carga de alumnos
INSERT INTO estudiantes (documento, nombre, apellido, correo_electronico, carrera, facultad) VALUES 
(41234567,'Federico','Valverde','fvalverde@ucu.edu.uy','Ingenieria Informatica','Ingenieria'), 
(42345678,'Ronald','Araujo','raraujo@ucu.edu.uy','Ingenieria Informatica','Ingenieria'), 
(43456789,'Darwin','Nunez','dnunez@ucu.edu.uy','Marketing','Empresariales'), 
(44567890,'Rodrigo','Bentancur','rbentancur@ucu.edu.uy','Contador Publico','Empresariales'), 
(45678901,'Manuel','Ugarte','mugarte@ucu.edu.uy','Derecho','Derecho'), 
(46789012,'Sergio','Rochet','srochet@ucu.edu.uy','Psicologia','Ciencias Humanas'), 
(47890123,'Jose Maria','Gimenez','jgimenez@ucu.edu.uy','Medicina','Salud'), 
(48901234,'Mathias','Olivera','molivera@ucu.edu.uy','Arquitectura','Arquitectura'), 
(49012345,'Giorgian','De Arrascaeta','garrascaeta@ucu.edu.uy','Comunicacion','Ciencias Humanas'), 
(50123456,'Nicolas','De La Cruz','ndelacruz@ucu.edu.uy','Economia','Empresariales'), 
(51234567,'Facundo','Pellistri','fpellistri@ucu.edu.uy','Ingenieria Industrial','Ingenieria'), 
(52345678,'Brian','Rodriguez','brodriguez@ucu.edu.uy','Administracion','Empresariales')
ON DUPLICATE KEY UPDATE documento=documento; 
 
-- Carga de disciplinas
INSERT INTO disciplina_deportiva (nombre) VALUES 
('Futbol'), ('Basquetbol'), ('Atletismo'), ('Voleibol'), ('Yoga'), ('Funcional'), ('Gimnasio'); 
 
-- Carga de espacios
INSERT INTO espacio (nombre, ubicacion) VALUES 
('Cancha Principal','Campus Montevideo'), 
('Cancha Auxiliar','Campus Montevideo'), 
('Gimnasio Deportivo','Campus Salto'), 
('Pista Atletica','Campus Salto'), 
('Sala Funcional','Campus Maldonado'); 
 
-- Carga de actividades
INSERT INTO actividad (nombre,id_disciplina,id_espacio,cupo_maximo,dia_semana,horario_inicio,horario_fin,estado) VALUES 
('Futbol Recreativo',1,1,5,'lunes','18:15:00','20:00:00','abierta'), 
('Basquetbol Mixto',2,3,4,'martes','19:30:00','20:30:00','abierta'), 
('Atletismo Inicial',3,4,8,'miercoles','17:00:00','18:30:00','abierta'), 
('Yoga Universitario',5,5,6,'jueves','18:00:00','19:00:00','abierta'), 
('Funcional Turno Manana',6,5,4,'viernes','09:00:00','10:00:00','abierta'); 
 
-- Historial de inscripciones
INSERT INTO inscripcion (est_documento, id_actividad, estado, fecha_inscripcion) VALUES 
(41234567,1,'confirmada',NOW()), (42345678,1,'confirmada',NOW()), (43456789,1,'confirmada',NOW()), (44567890,1,'confirmada',NOW()), (45678901,1,'confirmada',NOW()), (46789012,1,'lista_espera',NOW()), 
(47890123,2,'confirmada',NOW()), (48901234,2,'confirmada',NOW()), (49012345,2,'confirmada',NOW()), (50123456,2,'confirmada',NOW()), (51234567,2,'lista_espera',NOW()), 
(52345678,3,'confirmada',NOW()), (41234567,3,'confirmada',NOW()), (42345678,3,'confirmada',NOW()), (43456789,3,'confirmada',NOW()), 
(44567890,4,'confirmada',NOW()), (45678901,4,'confirmada',NOW()), (46789012,4,'confirmada',NOW()), 
(47890123,5,'confirmada',NOW()), (48901234,5,'confirmada',NOW()), (49012345,5,'confirmada',NOW()); 

-- Historial de asistencias
INSERT INTO asistencia (id_inscripcion,fecha,asistio) VALUES 
(1,'2026-06-15',TRUE), (2,'2026-06-15',TRUE), (3,'2026-06-15',FALSE), (4,'2026-06-15',TRUE), (5,'2026-06-15',FALSE), 
(7,'2026-06-16',TRUE), (8,'2026-06-16',FALSE), (9,'2026-06-16',TRUE), (10,'2026-06-16',TRUE), 
(12,'2026-06-17',FALSE), (13,'2026-06-17',TRUE), (14,'2026-06-17',TRUE), (15,'2026-06-17',TRUE), 
(16,'2026-06-18',TRUE), (17,'2026-06-18',FALSE), (18,'2026-06-18',TRUE), 
(19,'2026-06-19',TRUE), (20,'2026-06-19',TRUE), (21,'2026-06-19',FALSE),
(3, '2026-06-22', FALSE), (3, '2026-06-29', FALSE);