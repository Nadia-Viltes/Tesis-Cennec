-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`TipoDocumento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`TipoDocumento` (
  `IdTipoDocumento` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Descripcion` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTipoDocumento`),
  UNIQUE INDEX `IdTipoDocumento_UNIQUE` (`IdTipoDocumento` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Tutoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Tutoria` (
  `IdTutoria` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellido` VARCHAR(50) NOT NULL,
  `IdTipoDocumento` INT(10) NOT NULL,
  `NumeroDocumento` VARCHAR(8) NOT NULL,
  `Ocupacion` VARCHAR(50) NULL,
  `TelefonoFijo` VARCHAR(15) NULL,
  `TelefonoCelular` VARCHAR(15) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTutoria`),
  UNIQUE INDEX `IdTutoria_UNIQUE` (`IdTutoria` ASC) VISIBLE,
  INDEX `IdTipoDocumento` (`IdTipoDocumento` ASC) INVISIBLE,
  INDEX `NumeroDocumento` (`NumeroDocumento` ASC) VISIBLE,
  CONSTRAINT `IdTipoDocumento_Tutoria`
    FOREIGN KEY (`IdTipoDocumento`)
    REFERENCES `mydb`.`TipoDocumento` (`IdTipoDocumento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Pais`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Pais` (
  `IdPais` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Detalle` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdPais`),
  UNIQUE INDEX `IdPais_UNIQUE` (`IdPais` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Provincia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Provincia` (
  `IdProvincia` INT(10) AUTO_INCREMENT NOT NULL,
  `IdPais` INT(10) NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Detalle` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdProvincia`),
  UNIQUE INDEX `IdProvincia_UNIQUE` (`IdProvincia` ASC) VISIBLE,
  INDEX `IdPais_idx` (`IdPais` ASC) VISIBLE,
  CONSTRAINT `IdPais_Provincia`
    FOREIGN KEY (`IdPais`)
    REFERENCES `mydb`.`Pais` (`IdPais`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Localidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Localidad` (
  `IdLocalidad` INT(10) AUTO_INCREMENT NOT NULL,
  `IdProvincia` INT(10) NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Detalle` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdLocalidad`),
  UNIQUE INDEX `IdLocalidad_UNIQUE` (`IdLocalidad` ASC) VISIBLE,
  INDEX `IdProvincia_idx` (`IdProvincia` ASC) VISIBLE,
  CONSTRAINT `IdProvincia_Localidad`
    FOREIGN KEY (`IdProvincia`)
    REFERENCES `mydb`.`Provincia` (`IdProvincia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Barrio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Barrio` (
  `IdBarrio` INT(10) AUTO_INCREMENT NOT NULL,
  `IdLocalidad` INT(10) NULL,
  `Nombre` VARCHAR(50) NULL,
  `Detalle` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdBarrio`),
  INDEX `IdLocalidad_idx` (`IdLocalidad` ASC) VISIBLE,
  CONSTRAINT `IdLocalidad_Barrio`
    FOREIGN KEY (`IdLocalidad`)
    REFERENCES `mydb`.`Localidad` (`IdLocalidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Domicilio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Domicilio` (
  `IdDomicilio` INT(10) AUTO_INCREMENT NOT NULL,
  `IdPais` INT(10) NULL,
  `IdProvincia` INT(10) NULL,
  `IdLocalidad` INT(10) NULL,
  `IdBarrio` INT(10) NULL,
  `Calle` VARCHAR(50) NULL,
  `Altura` VARCHAR(10) NULL,
  `Piso` VARCHAR(5) NULL,
  `Dpto` VARCHAR(5) NULL,
  `Barrio` VARCHAR(50) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdDomicilio`),
  INDEX `IdPais_idx` (`IdPais` ASC) VISIBLE,
  INDEX `IdProvincia_idx` (`IdProvincia` ASC) VISIBLE,
  INDEX `IdLocalidad_idx` (`IdLocalidad` ASC) VISIBLE,
  UNIQUE INDEX `IdDomicilio_UNIQUE` (`IdDomicilio` ASC) VISIBLE,
  INDEX `IdBarrio_idx` (`IdBarrio` ASC) VISIBLE,
  CONSTRAINT `IdPais_Domicilio`
    FOREIGN KEY (`IdPais`)
    REFERENCES `mydb`.`Pais` (`IdPais`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdProvincia_Domicilio`
    FOREIGN KEY (`IdProvincia`)
    REFERENCES `mydb`.`Provincia` (`IdProvincia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdLocalidad_Domicilio`
    FOREIGN KEY (`IdLocalidad`)
    REFERENCES `mydb`.`Localidad` (`IdLocalidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdBarrio_Domicilio`
    FOREIGN KEY (`IdBarrio`)
    REFERENCES `mydb`.`Barrio` (`IdBarrio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Paciente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Paciente` (
  `IdPaciente` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Apellido` VARCHAR(50) NOT NULL,
  `IdTipoDocumento` INT(10) NOT NULL,
  `NumeroDocumento` INT(8) NOT NULL,
  `Genero` VARCHAR(15) NULL,
  `FechaNacimiento` DATE NULL,
  `Fallecido` TINYINT NULL,
  `FechaFallecimiento` DATE NULL,
  `IdTutoria` INT(10) NOT NULL,
  `IdDomicilio` INT(10) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdPaciente`),
  UNIQUE INDEX `IdPaciente_UNIQUE` (`IdPaciente` ASC) VISIBLE,
  INDEX `IdTipoDocumento_idx` (`IdTipoDocumento` ASC) VISIBLE,
  INDEX `IdTutoria_idx` (`IdTutoria` ASC) VISIBLE,
  INDEX `IdDomicilio_idx` (`IdDomicilio` ASC) VISIBLE,
  CONSTRAINT `IdTipoDocumento_Paciente`
    FOREIGN KEY (`IdTipoDocumento`)
    REFERENCES `mydb`.`TipoDocumento` (`IdTipoDocumento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdTutoria_Paciente`
    FOREIGN KEY (`IdTutoria`)
    REFERENCES `mydb`.`Tutoria` (`IdTutoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdDomicilio_Paciente`
    FOREIGN KEY (`IdDomicilio`)
    REFERENCES `mydb`.`Domicilio` (`IdDomicilio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`HistoriaClinica`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`HistoriaClinica` (
  `IdHistoriaClinica` INT(10) AUTO_INCREMENT NOT NULL,
  `IdPaciente` INT(10) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdHistoriaClinica`),
  UNIQUE INDEX `IDHistoriaClinica_UNIQUE` (`IdHistoriaClinica` ASC) VISIBLE,
  INDEX `IdPaciente_idx` (`IdPaciente` ASC) VISIBLE,
  CONSTRAINT `IdPaciente_HistoriaClinica`
    FOREIGN KEY (`IdPaciente`)
    REFERENCES `mydb`.`Paciente` (`IdPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`TipoRecurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`TipoRecurso` (
  `IdTipoRecurso` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Descripcion` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTipoRecurso`),
  UNIQUE INDEX `IdTipoRecurso_UNIQUE` (`IdTipoRecurso` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Recurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Recurso` (
  `IdRecursos` INT(10) AUTO_INCREMENT NOT NULL,
  `IdTipoRecurso` INT(10) NOT NULL,
  `Nombre` VARCHAR(50) NULL,
  `Apellido` VARCHAR(50) NULL,
  `IdTipoDocumento` INT(10) NOT NULL,
  `NumeroDocumento` INT(8) NULL,
  `Genero` VARCHAR(15) NULL,
  `FechaNacimiento` DATETIME NULL,
  `Edad` INT(3) NULL,
  `Cuil` INT(13) NULL,
  `IdDomicilio` INT(10) NULL,
  `TelefonoCelular` VARCHAR(15) NULL,
  `Email` VARCHAR(50) NULL,
  `Legajo` VARCHAR(10) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdRecursos`),
  UNIQUE INDEX `IdRecurso_UNIQUE` (`IdRecursos` ASC) INVISIBLE,
  INDEX `IdTipoDocumento_idx` (`IdTipoDocumento` ASC) VISIBLE,
  INDEX `IdDomicilio_idx` (`IdDomicilio` ASC) VISIBLE,
  INDEX `IdTipoRecurso_idx` (`IdTipoRecurso` ASC) INVISIBLE,
  CONSTRAINT `IdTipoDocumento_Recurso`
    FOREIGN KEY (`IdTipoDocumento`)
    REFERENCES `mydb`.`TipoDocumento` (`IdTipoDocumento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdDomicilio_Recurso`
    FOREIGN KEY (`IdDomicilio`)
    REFERENCES `mydb`.`Domicilio` (`IdDomicilio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdTipoRecurso_Recurso`
    FOREIGN KEY (`IdTipoRecurso`)
    REFERENCES `mydb`.`TipoRecurso` (`IdTipoRecurso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Especialidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Especialidad` (
  `IdEspecialidad` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Codigo` VARCHAR(10) NULL,
  `Descripcion` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdEspecialidad`),
  UNIQUE INDEX `IdEspecialidad_UNIQUE` (`IdEspecialidad` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Profesional`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Profesional` (
  `IdProfesional` INT(10) AUTO_INCREMENT NOT NULL,
  `IdRecurso` INT(10) NOT NULL,
  `IdEspecialidad` INT(10) NOT NULL,
  `Matricula` VARCHAR(15) NOT NULL,
  `IdEstado` INT(10) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdProfesional`),
  INDEX `IdRecurso_idx` (`IdRecurso` ASC) VISIBLE,
  INDEX `IdEspecialidad_idx` (`IdEspecialidad` ASC) VISIBLE,
  UNIQUE INDEX `IdProfesional_UNIQUE` (`IdProfesional` ASC) VISIBLE,
  CONSTRAINT `IdRecurso_Profesional`
    FOREIGN KEY (`IdRecurso`)
    REFERENCES `mydb`.`Recurso` (`IdRecursos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdEspecialidad_Profesional`
    FOREIGN KEY (`IdEspecialidad`)
    REFERENCES `mydb`.`Especialidad` (`IdEspecialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Evolucion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Evolucion` (
  `IdEvolucion` INT(10) AUTO_INCREMENT NOT NULL,
  `IdHistoriaClinica` INT(10) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdEvolucion`),
  INDEX `IdHistoriaClinica_idx` (`IdHistoriaClinica` ASC) VISIBLE,
  CONSTRAINT `IdHistoriaClinica_Evolucion`
    FOREIGN KEY (`IdHistoriaClinica`)
    REFERENCES `mydb`.`HistoriaClinica` (`IdHistoriaClinica`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`EstadoTurno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`EstadoTurno` (
  `IdEstadoTurno` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NULL,
  `Detalle` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdEstadoTurno`),
  UNIQUE INDEX `IdEstadoTurno_UNIQUE` (`IdEstadoTurno` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`TipoTurno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`TipoTurno` (
  `IdTipoTurno` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Detalle` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTipoTurno`),
  UNIQUE INDEX `IdTipoTurno_UNIQUE` (`IdTipoTurno` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Motivo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Motivo` (
  `IdMotivo` INT(10) AUTO_INCREMENT NOT NULL,
  `NombreMotivo` VARCHAR(45) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdMotivo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Turno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Turno` (
  `IdTurno` INT(10) AUTO_INCREMENT NOT NULL,
  `IdTipoTurno` INT(10) NOT NULL,
  `IdEspecialidad` INT(10) NOT NULL,
  `IdPaciente` INT(10) NOT NULL,
  `FechaTurno` DATE NOT NULL,
  `HoraDesde` TIME NOT NULL,
  `HoraHasta` TIME NULL,
  `IdEstadoTurno` INT(10) NOT NULL,
  `FechaAsignado` DATETIME NULL,
  `FechaReceptado` DATETIME NULL,
  `FechaReasignado` DATETIME NULL,
  `FechaAnulado` DATETIME NULL,
  `FechaInicioAtencion` DATETIME NULL,
  `FechaFinalAtencion` DATETIME NULL,
  `IdMotivoAnulado` INT(10) NULL,
  `IdUsuarioAsignado` INT NULL,
  `IdUsuarioReceptado` INT NULL,
  `IdUsuarioReasignado` INT NULL,
  `IdUsuarioAnulado` INT NULL,
  `IdUsuarioInicioAtencion` INT NULL,
  `IdUsuarioFinalAtencion` INT NULL,
  `IdProfesionalReceptado` INT NULL,
  `TurnoReasignado` TINYINT NULL,
  `IdTurnoOriginal` INT NULL,
  `IdTurnoReasignado` INT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTurno`),
  INDEX `IdTipoTurno_idx` (`IdTipoTurno` ASC) VISIBLE,
  INDEX `IdEstadoTurno_idx` (`IdEstadoTurno` ASC) VISIBLE,
  INDEX `IdEspecialidad_idx` (`IdEspecialidad` ASC) VISIBLE,
  INDEX `IdPaciente_idx` (`IdPaciente` ASC) VISIBLE,
  UNIQUE INDEX `IdTurno_UNIQUE` (`IdTurno` ASC) VISIBLE,
  INDEX `IdMotivoAnulado_idx` (`IdMotivoAnulado` ASC) VISIBLE,
  CONSTRAINT `IdEstadoTurno_Turno`
    FOREIGN KEY (`IdEstadoTurno`)
    REFERENCES `mydb`.`EstadoTurno` (`IdEstadoTurno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdTipoTurno_Turno`
    FOREIGN KEY (`IdTipoTurno`)
    REFERENCES `mydb`.`TipoTurno` (`IdTipoTurno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdEspecialidad_Turno`
    FOREIGN KEY (`IdEspecialidad`)
    REFERENCES `mydb`.`Especialidad` (`IdEspecialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdPaciente_Turno`
    FOREIGN KEY (`IdPaciente`)
    REFERENCES `mydb`.`Paciente` (`IdPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdMotivoAnulado_Turno`
    FOREIGN KEY (`IdMotivoAnulado`)
    REFERENCES `mydb`.`Motivo` (`IdMotivo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DetalleEvolucion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DetalleEvolucion` (
  `IdDetalleEvolucion` INT(10) AUTO_INCREMENT NOT NULL,
  `IdEvolucion` INT(10) NOT NULL,
  `IdTurno` INT(10) NOT NULL,
  `IdProfesional` INT(10) NOT NULL,
  `ObservacionAvance` VARCHAR(5000) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdDetalleEvolucion`),
  UNIQUE INDEX `IdDetalleHC_UNIQUE` (`IdDetalleEvolucion` ASC) VISIBLE,
  INDEX `IdTurno_idx` (`IdTurno` ASC) VISIBLE,
  INDEX `IdProfesional_idx` (`IdProfesional` ASC) VISIBLE,
  INDEX `IdEvolucion_idx` (`IdEvolucion` ASC) VISIBLE,
  CONSTRAINT `IdEvolucion_DetalleEvolucion`
    FOREIGN KEY (`IdEvolucion`)
    REFERENCES `mydb`.`Evolucion` (`IdEvolucion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdTurno_DetalleEvolucion`
    FOREIGN KEY (`IdTurno`)
    REFERENCES `mydb`.`Turno` (`IdTurno`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdProfesional_DetalleEvolucion`
    FOREIGN KEY (`IdProfesional`)
    REFERENCES `mydb`.`Profesional` (`IdProfesional`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Dia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Dia` (
  `IdDia` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdDia`),
  UNIQUE INDEX `IdDia_UNIQUE` (`IdDia` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`HorarioRecurso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`HorarioRecurso` (
  `IdHorarioRecurso` INT(10) AUTO_INCREMENT NOT NULL,
  `IdRecurso` INT(10) NOT NULL,
  `IdDia` INT(10) NOT NULL,
  `HoraDesde` TIME NULL,
  `HoraHasta` TIME NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdHorarioRecurso`),
  INDEX `IdDia_idx` (`IdDia` ASC) VISIBLE,
  INDEX `IdRecurso_idx` (`IdRecurso` ASC) VISIBLE,
  UNIQUE INDEX `IdHorarioRecurso_UNIQUE` (`IdHorarioRecurso` ASC) VISIBLE,
  CONSTRAINT `IdDia_HorarioRecurso`
    FOREIGN KEY (`IdDia`)
    REFERENCES `mydb`.`Dia` (`IdDia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdRecurso_HorarioRecurso`
    FOREIGN KEY (`IdRecurso`)
    REFERENCES `mydb`.`Recurso` (`IdRecursos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Financiador`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Financiador` (
  `IdFinanciador` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `IdDomicilio` INT(10) NULL,
  `Telefono` INT(15) NULL,
  `E-mail` VARCHAR(50) NULL,
  `Observaciones` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdFinanciador`),
  UNIQUE INDEX `IdFinanciador_UNIQUE` (`IdFinanciador` ASC) VISIBLE,
  INDEX `IdDomicilio_idx` (`IdDomicilio` ASC) VISIBLE,
  CONSTRAINT `IdDomicilio_Financiador`
    FOREIGN KEY (`IdDomicilio`)
    REFERENCES `mydb`.`Domicilio` (`IdDomicilio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Rol`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Rol` (
  `IdRol` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Descripción` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdRol`),
  UNIQUE INDEX `IdRol_UNIQUE` (`IdRol` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Usuario` (
  `IdUsuario` INT(10) AUTO_INCREMENT NOT NULL,
  `IdRecurso` INT(10) NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Contraseña` VARCHAR(20) NOT NULL,
  `IdRol` INT(10) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdUsuario`),
  INDEX `IdRecurso_idx` (`IdRecurso` ASC) VISIBLE,
  INDEX `IdRol_idx` (`IdRol` ASC) VISIBLE,
  UNIQUE INDEX `IdUsuario_UNIQUE` (`IdUsuario` ASC) VISIBLE,
  CONSTRAINT `IdRecursos_Usuario`
    FOREIGN KEY (`IdRecurso`)
    REFERENCES `mydb`.`Recurso` (`IdRecursos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdRol_Usuario`
    FOREIGN KEY (`IdRol`)
    REFERENCES `mydb`.`Rol` (`IdRol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Privilegio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Privilegio` (
  `IdPrivilegio` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NOT NULL,
  `Descripcion` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdPrivilegio`),
  UNIQUE INDEX `IdPrivilegio_UNIQUE` (`IdPrivilegio` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`RolPrivilegio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`RolPrivilegio` (
  `IdRolPrivilegio` INT(10) AUTO_INCREMENT NOT NULL,
  `IdRol` INT(10) NOT NULL,
  `IdPrivilegio` INT(10) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  PRIMARY KEY (`IdRolPrivilegio`),
  INDEX `IdRol_idx` (`IdRol` ASC) VISIBLE,
  INDEX `IdPrivilegio_idx` (`IdPrivilegio` ASC) VISIBLE,
  UNIQUE INDEX `IdRolPrivilegio(10)_UNIQUE` (`IdRolPrivilegio` ASC) VISIBLE,
  CONSTRAINT `IdRol_RolPrivilegio`
    FOREIGN KEY (`IdRol`)
    REFERENCES `mydb`.`Rol` (`IdRol`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdPrivilegio_RolPrivilegio`
    FOREIGN KEY (`IdPrivilegio`)
    REFERENCES `mydb`.`Privilegio` (`IdPrivilegio`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`PreguntaAdmision`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`PreguntaAdmision` (
  `IdPreguntaAdmision` INT(10) AUTO_INCREMENT NOT NULL,
  `DescripcionPregunta` VARCHAR(500) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdPreguntaAdmision`),
  UNIQUE INDEX `IdPreguntaAdmision_UNIQUE` (`IdPreguntaAdmision` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`EntrevistaAdmision`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`EntrevistaAdmision` (
  `IdEntrevistaAdmision` INT(10) AUTO_INCREMENT NOT NULL,
  `IdHistoriaClinica` INT(10) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` VARCHAR(10) NULL,
  `IdUsuarioModificacion` VARCHAR(10) NULL,
  `IdUsuarioBaja` VARCHAR(10) NULL,
  PRIMARY KEY (`IdEntrevistaAdmision`),
  INDEX `IdHistoriaClinica_idx` (`IdHistoriaClinica` ASC) VISIBLE,
  CONSTRAINT `IdHistoriaClinica_EntrevistaAdmision`
    FOREIGN KEY (`IdHistoriaClinica`)
    REFERENCES `mydb`.`HistoriaClinica` (`IdHistoriaClinica`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DetalleAdmision`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DetalleAdmision` (
  `IdDetalleAdmision` INT(10) AUTO_INCREMENT NOT NULL,
  `IdEntrevistaAdmision` INT(10) NOT NULL,
  `IdPregunta` INT(10) NOT NULL,
  `Respuesta` VARCHAR(50) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdDetalleAdmision`),
  INDEX `IdPreguntas_idx` (`IdPregunta` ASC) VISIBLE,
  UNIQUE INDEX `IdDetalleAdmision_UNIQUE` (`IdDetalleAdmision` ASC) VISIBLE,
  INDEX `IdEntrevistaAdmision_idx` (`IdEntrevistaAdmision` ASC) VISIBLE,
  CONSTRAINT `IdPreguntas_DetalleAdmision`
    FOREIGN KEY (`IdPregunta`)
    REFERENCES `mydb`.`PreguntaAdmision` (`IdPreguntaAdmision`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdEntrevistaAdmision_DetalleAdmision`
    FOREIGN KEY (`IdEntrevistaAdmision`)
    REFERENCES `mydb`.`EntrevistaAdmision` (`IdEntrevistaAdmision`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`TipoPatologia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`TipoPatologia` (
  `IdTipoPatologia` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NULL,
  `Descripción` VARCHAR(100) NULL,
  `FechaAlta` VARCHAR(45) NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTipoPatologia`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`ConfiguracionTurno`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ConfiguracionTurno` (
  `IdConfiguracionTurno` INT(10) AUTO_INCREMENT NOT NULL,
  `IdPaciente` INT(10) NOT NULL,
  `IdEspecialidad` INT(10) NOT NULL,
  `IdTipoPatologia` INT(10) NULL,
  `CantidadDisponibles` INT(3) NULL,
  `CantidadComputados` INT(3) NULL,
  `Observaciones` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdConfiguracionTurno`),
  INDEX `IdPaciente_idx` (`IdPaciente` ASC) VISIBLE,
  INDEX `IdEspecialidad_idx` (`IdEspecialidad` ASC) VISIBLE,
  INDEX `IdTipoPatologia_idx` (`IdTipoPatologia` ASC) VISIBLE,
  CONSTRAINT `IdPaciente_ConfiguracionTurno`
    FOREIGN KEY (`IdPaciente`)
    REFERENCES `mydb`.`Paciente` (`IdPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdEspecialidad_ConfiguracionTurno`
    FOREIGN KEY (`IdEspecialidad`)
    REFERENCES `mydb`.`Especialidad` (`IdEspecialidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdTipoPatologia_ConfiguracionTurno`
    FOREIGN KEY (`IdTipoPatologia`)
    REFERENCES `mydb`.`TipoPatologia` (`IdTipoPatologia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Afiliacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Afiliacion` (
  `IdAfiliacion` INT(10) AUTO_INCREMENT NOT NULL,
  `IdPaciente` INT(10) NULL,
  `IdFinanciador` INT(10) NULL,
  `NumeroAfiliado` VARCHAR(20) NOT NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioBaja` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  PRIMARY KEY (`IdAfiliacion`),
  INDEX `IdPaciente_idx` (`IdPaciente` ASC) VISIBLE,
  INDEX `IdFinanciador_idx` (`IdFinanciador` ASC) VISIBLE,
  UNIQUE INDEX `IdAfiliacion_UNIQUE` (`IdAfiliacion` ASC) VISIBLE,
  CONSTRAINT `IdPaciente_Afiliacion`
    FOREIGN KEY (`IdPaciente`)
    REFERENCES `mydb`.`Paciente` (`IdPaciente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdFinanciador_Afiliacion`
    FOREIGN KEY (`IdFinanciador`)
    REFERENCES `mydb`.`Financiador` (`IdFinanciador`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`TipoReporte`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`TipoReporte` (
  `IdTipoReporte` INT(10) AUTO_INCREMENT NOT NULL,
  `Nombre` VARCHAR(50) NULL,
  `Descripcion` VARCHAR(100) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdTipoReporte`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`HistorialReportes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`HistorialReportes` (
  `IdHistorialReportes` INT(10) AUTO_INCREMENT NOT NULL,
  `IdTipoReporte` INT(10) NULL,
  `IdUsuario` INT(10) NULL,
  `LinkReporte` VARCHAR(50) NULL,
  `FechaAlta` DATETIME NULL,
  `FechaModificacion` DATETIME NULL,
  `FechaBaja` DATETIME NULL,
  `IdUsuarioAlta` INT(10) NULL,
  `IdUsuarioModificacion` INT(10) NULL,
  `IdUsuarioBaja` INT(10) NULL,
  PRIMARY KEY (`IdHistorialReportes`),
  INDEX `IdUsuario_idx` (`IdUsuario` ASC) VISIBLE,
  INDEX `IdTipoReporte_idx` (`IdTipoReporte` ASC) VISIBLE,
  CONSTRAINT `IdUsuario_HistorialReportes`
    FOREIGN KEY (`IdUsuario`)
    REFERENCES `mydb`.`Usuario` (`IdUsuario`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `IdTipoReporte_HistorialReportes`
    FOREIGN KEY (`IdTipoReporte`)
    REFERENCES `mydb`.`TipoReporte` (`IdTipoReporte`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
