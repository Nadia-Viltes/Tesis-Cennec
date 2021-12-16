delimiter $$
CREATE EVENT change_ausente_status_event 
ON SCHEDULE EVERY 50 SECOND DO
BEGIN
DECLARE id_turno INT;
DECLARE id_tipo_turno INT;
DECLARE id_especialidad INT;
DECLARE id_profesional_asignado INT;
DECLARE id_paciente INT;
DECLARE fecha_turno DATE;
DECLARE hora_desde TIME;
DECLARE hora_hasta TIME;
DECLARE id_estado_turno INT;
DECLARE id_usuario_asignado INT;
DECLARE id_evolucion INT;
DECLARE id_historia_clinica INT;
DECLARE id_turno_ausente INT;

DECLARE cursor_turnos_asignados CURSOR FOR SELECT idTurno, idTipoTurno, idEspecialidad, idProfesional, idPaciente, FechaTurno, HoraDesde, HoraHasta, idEstadoTurno, idUsuarioAsignado from turno
where (( DATE_FORMAT(FechaTurno, "%d%-%m-%Y") < DATE_FORMAT(now(), "%d%-%m-%Y") )
OR ( DATE_FORMAT(FechaTurno, "%d%-%m-%Y") = DATE_FORMAT(now(), "%d%-%m-%Y") 
	AND (DATE_FORMAT(now(), '%H') > DATE_FORMAT(HoraDesde, '%H')))
OR ( DATE_FORMAT(FechaTurno, "%d%-%m-%Y") = DATE_FORMAT(now(), "%d%-%m-%Y") 
	AND (DATE_FORMAT(now(), '%H') = DATE_FORMAT(HoraDesde, '%H')
    AND (DATE_FORMAT(now(), '%i') - DATE_FORMAT(HoraDesde, '%i')) > 10)))
AND idEstadoTurno in (select idEstadoTurno from estadoturno
						where nombre = "Asignado")
AND fechabaja is null;

OPEN cursor_turnos_asignados;
LOOP
     FETCH cursor_turnos_asignados INTO id_turno, id_tipo_turno, id_especialidad, id_profesional_asignado, id_paciente, fecha_turno, hora_desde, hora_hasta, id_estado_turno, id_usuario_asignado;
        INSERT INTO turno(idTipoTurno, idEspecialidad, idProfesional,idPaciente,FechaTurno,HoraDesde,HoraHasta,idEstadoTurno,idUsuarioAsignado, IdTurnoOriginal) 
        VALUES (id_tipo_turno, id_especialidad, id_profesional_asignado, id_paciente, fecha_turno, hora_desde, hora_hasta, (select idEstadoTurno from estadoturno where nombre = "Ausente"), id_usuario_asignado, id_turno);
		
		#hago el update del turno asignado
		UPDATE turno
        SET Fechabaja = NOW()
        WHERE idTurno = id_turno;
		
		#busco la historia clinica
		SELECT idHistoriaClinica 
		INTO id_historia_clinica 
		FROM historiaclinica
		WHERE IdPaciente = id_paciente; 
		
		#obtengo la evolucion
		SELECT idEvolucion 
		INTO id_evolucion 
		FROM evolucion
		WHERE idHistoriaClinica = id_historia_clinica;
		
		#obtengo el id del turno ausente
		SELECT idTurno
		INTO id_turno_ausente
		FROM turno
		WHERE idEstadoTurno IN (select idEstadoTurno from estadoturno where nombre = "Ausente")
		AND IdTurnoOriginal = id_turno
		AND idPaciente = id_paciente;
		
		IF (id_evolucion IS NULL) THEN
			INSERT INTO evolucion(IdHistoriaClinica, FechaAlta)
			VALUES(id_historia_clinica, NOW());
			
			INSERT INTO detalleevolucion(idEvolucion, idTurno, idProfesional, ObservacionAvance, FechaAlta)
			VALUES((SELECT idEvolucion FROM evolucion WHERE idHistoriaClinica = id_historia_clinica), id_turno_ausente, id_profesional_asignado, 'El paciente no asistio a su sesion del día', NOW());
		ELSE
			INSERT INTO detalleevolucion(idEvolucion, idTurno, idProfesional, ObservacionAvance, FechaAlta)
			VALUES((SELECT idEvolucion FROM evolucion WHERE idHistoriaClinica = id_historia_clinica), id_turno_ausente, id_profesional_asignado, 'El paciente no asistio a su sesion del día', NOW());
		END IF;
END LOOP;
CLOSE cursor_turnos_asignados;
END;