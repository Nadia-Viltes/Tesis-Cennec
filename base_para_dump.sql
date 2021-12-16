-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `afiliacion`
--

DROP TABLE IF EXISTS `afiliacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `afiliacion` (
  `IdAfiliacion` int NOT NULL AUTO_INCREMENT,
  `IdPaciente` int DEFAULT NULL,
  `IdFinanciador` int DEFAULT NULL,
  `NumeroAfiliado` varchar(20) NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  PRIMARY KEY (`IdAfiliacion`),
  UNIQUE KEY `IdAfiliacion_UNIQUE` (`IdAfiliacion`),
  KEY `IdPaciente_idx` (`IdPaciente`),
  KEY `IdFinanciador_idx` (`IdFinanciador`),
  CONSTRAINT `IdFinanciador_Afiliacion` FOREIGN KEY (`IdFinanciador`) REFERENCES `financiador` (`IdFinanciador`),
  CONSTRAINT `IdPaciente_Afiliacion` FOREIGN KEY (`IdPaciente`) REFERENCES `paciente` (`IdPaciente`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `barrio`
--

DROP TABLE IF EXISTS `barrio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `barrio` (
  `IdBarrio` int NOT NULL AUTO_INCREMENT,
  `IdLocalidad` int DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdBarrio`),
  KEY `IdLocalidad_idx` (`IdLocalidad`),
  CONSTRAINT `IdLocalidad_Barrio` FOREIGN KEY (`IdLocalidad`) REFERENCES `localidad` (`IdLocalidad`)
) ENGINE=InnoDB AUTO_INCREMENT=410 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `configuracionturno`
--

DROP TABLE IF EXISTS `configuracionturno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configuracionturno` (
  `IdConfiguracionTurno` int NOT NULL AUTO_INCREMENT,
  `IdPaciente` int NOT NULL,
  `IdEspecialidad` int NOT NULL,
  `IdTipoPatologia` int DEFAULT NULL,
  `CantidadDisponibles` int DEFAULT NULL,
  `CantidadComputados` int DEFAULT NULL,
  `Observaciones` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdConfiguracionTurno`),
  KEY `IdPaciente_idx` (`IdPaciente`),
  KEY `IdEspecialidad_idx` (`IdEspecialidad`),
  KEY `IdTipoPatologia_idx` (`IdTipoPatologia`),
  CONSTRAINT `IdEspecialidad_ConfiguracionTurno` FOREIGN KEY (`IdEspecialidad`) REFERENCES `especialidad` (`IdEspecialidad`),
  CONSTRAINT `IdPaciente_ConfiguracionTurno` FOREIGN KEY (`IdPaciente`) REFERENCES `paciente` (`IdPaciente`),
  CONSTRAINT `IdTipoPatologia_ConfiguracionTurno` FOREIGN KEY (`IdTipoPatologia`) REFERENCES `tipopatologia` (`IdTipoPatologia`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detalleadmision`
--

DROP TABLE IF EXISTS `detalleadmision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleadmision` (
  `IdDetalleAdmision` int NOT NULL AUTO_INCREMENT,
  `IdEntrevistaAdmision` int NOT NULL,
  `IdPregunta` int NOT NULL,
  `Respuesta` varchar(50) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdDetalleAdmision`),
  UNIQUE KEY `IdDetalleAdmision_UNIQUE` (`IdDetalleAdmision`),
  KEY `IdPreguntas_idx` (`IdPregunta`),
  KEY `IdEntrevistaAdmision_idx` (`IdEntrevistaAdmision`),
  CONSTRAINT `IdEntrevistaAdmision_DetalleAdmision` FOREIGN KEY (`IdEntrevistaAdmision`) REFERENCES `entrevistaadmision` (`IdEntrevistaAdmision`),
  CONSTRAINT `IdPreguntas_DetalleAdmision` FOREIGN KEY (`IdPregunta`) REFERENCES `preguntaadmision` (`IdPreguntaAdmision`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `detalleevolucion`
--

DROP TABLE IF EXISTS `detalleevolucion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleevolucion` (
  `IdDetalleEvolucion` int NOT NULL AUTO_INCREMENT,
  `IdEvolucion` int NOT NULL,
  `IdTurno` int DEFAULT NULL,
  `IdProfesional` int NOT NULL,
  `ObservacionAvance` varchar(5000) NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdDetalleEvolucion`),
  UNIQUE KEY `IdDetalleHC_UNIQUE` (`IdDetalleEvolucion`),
  KEY `IdTurno_idx` (`IdTurno`),
  KEY `IdProfesional_idx` (`IdProfesional`),
  KEY `IdEvolucion_idx` (`IdEvolucion`),
  CONSTRAINT `IdEvolucion_DetalleEvolucion` FOREIGN KEY (`IdEvolucion`) REFERENCES `evolucion` (`IdEvolucion`),
  CONSTRAINT `IdProfesional_DetalleEvolucion` FOREIGN KEY (`IdProfesional`) REFERENCES `profesional` (`IdProfesional`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dia`
--

DROP TABLE IF EXISTS `dia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dia` (
  `IdDia` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdDia`),
  UNIQUE KEY `IdDia_UNIQUE` (`IdDia`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domicilio`
--

DROP TABLE IF EXISTS `domicilio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `domicilio` (
  `IdDomicilio` int NOT NULL AUTO_INCREMENT,
  `IdPais` int DEFAULT NULL,
  `IdProvincia` int DEFAULT NULL,
  `IdLocalidad` int DEFAULT NULL,
  `IdBarrio` int DEFAULT NULL,
  `Calle` varchar(50) DEFAULT NULL,
  `Altura` varchar(10) DEFAULT NULL,
  `Piso` varchar(5) DEFAULT NULL,
  `Dpto` varchar(5) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdDomicilio`),
  UNIQUE KEY `IdDomicilio_UNIQUE` (`IdDomicilio`),
  KEY `IdPais_idx` (`IdPais`),
  KEY `IdProvincia_idx` (`IdProvincia`),
  KEY `IdLocalidad_idx` (`IdLocalidad`),
  KEY `IdBarrio_idx` (`IdBarrio`),
  CONSTRAINT `IdBarrio_Domicilio` FOREIGN KEY (`IdBarrio`) REFERENCES `barrio` (`IdBarrio`),
  CONSTRAINT `IdLocalidad_Domicilio` FOREIGN KEY (`IdLocalidad`) REFERENCES `localidad` (`IdLocalidad`),
  CONSTRAINT `IdPais_Domicilio` FOREIGN KEY (`IdPais`) REFERENCES `pais` (`IdPais`),
  CONSTRAINT `IdProvincia_Domicilio` FOREIGN KEY (`IdProvincia`) REFERENCES `provincia` (`IdProvincia`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entrevistaadmision`
--

DROP TABLE IF EXISTS `entrevistaadmision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrevistaadmision` (
  `IdEntrevistaAdmision` int NOT NULL AUTO_INCREMENT,
  `IdHistoriaClinica` int DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` varchar(10) DEFAULT NULL,
  `IdUsuarioModificacion` varchar(10) DEFAULT NULL,
  `IdUsuarioBaja` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`IdEntrevistaAdmision`),
  KEY `IdHistoriaClinica_idx` (`IdHistoriaClinica`),
  CONSTRAINT `IdHistoriaClinica_EntrevistaAdmision` FOREIGN KEY (`IdHistoriaClinica`) REFERENCES `historiaclinica` (`IdHistoriaClinica`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `especialidad`
--

DROP TABLE IF EXISTS `especialidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `especialidad` (
  `IdEspecialidad` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Codigo` varchar(10) DEFAULT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdEspecialidad`),
  UNIQUE KEY `IdEspecialidad_UNIQUE` (`IdEspecialidad`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `estadoturno`
--

DROP TABLE IF EXISTS `estadoturno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estadoturno` (
  `IdEstadoTurno` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) DEFAULT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdEstadoTurno`),
  UNIQUE KEY `IdEstadoTurno_UNIQUE` (`IdEstadoTurno`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `evolucion`
--

DROP TABLE IF EXISTS `evolucion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evolucion` (
  `IdEvolucion` int NOT NULL AUTO_INCREMENT,
  `IdHistoriaClinica` int DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdEvolucion`),
  KEY `IdHistoriaClinica_idx` (`IdHistoriaClinica`),
  CONSTRAINT `IdHistoriaClinica_Evolucion` FOREIGN KEY (`IdHistoriaClinica`) REFERENCES `historiaclinica` (`IdHistoriaClinica`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `financiador`
--

DROP TABLE IF EXISTS `financiador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financiador` (
  `IdFinanciador` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Telefono` int DEFAULT NULL,
  `E-mail` varchar(50) DEFAULT NULL,
  `Observaciones` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdFinanciador`),
  UNIQUE KEY `IdFinanciador_UNIQUE` (`IdFinanciador`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `historiaclinica`
--

DROP TABLE IF EXISTS `historiaclinica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historiaclinica` (
  `IdHistoriaClinica` int NOT NULL AUTO_INCREMENT,
  `IdPaciente` int NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdHistoriaClinica`),
  UNIQUE KEY `IDHistoriaClinica_UNIQUE` (`IdHistoriaClinica`),
  KEY `IdPaciente_idx` (`IdPaciente`),
  CONSTRAINT `IdPaciente_HistoriaClinica` FOREIGN KEY (`IdPaciente`) REFERENCES `paciente` (`IdPaciente`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `historialreportes`
--

DROP TABLE IF EXISTS `historialreportes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historialreportes` (
  `IdHistorialReportes` int NOT NULL AUTO_INCREMENT,
  `IdTipoReporte` int DEFAULT NULL,
  `IdUsuario` int DEFAULT NULL,
  `LinkReporte` varchar(50) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdHistorialReportes`),
  KEY `IdUsuario_idx` (`IdUsuario`),
  KEY `IdTipoReporte_idx` (`IdTipoReporte`),
  CONSTRAINT `IdTipoReporte_HistorialReportes` FOREIGN KEY (`IdTipoReporte`) REFERENCES `tiporeporte` (`IdTipoReporte`),
  CONSTRAINT `IdUsuario_HistorialReportes` FOREIGN KEY (`IdUsuario`) REFERENCES `usuario` (`IdUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `horariorecurso`
--

DROP TABLE IF EXISTS `horariorecurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horariorecurso` (
  `IdHorarioRecurso` int NOT NULL AUTO_INCREMENT,
  `IdRecurso` int NOT NULL,
  `IdDia` int NOT NULL,
  `HoraDesde` time DEFAULT NULL,
  `HoraHasta` time DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdHorarioRecurso`),
  UNIQUE KEY `IdHorarioRecurso_UNIQUE` (`IdHorarioRecurso`),
  KEY `IdDia_idx` (`IdDia`),
  KEY `IdRecurso_idx` (`IdRecurso`),
  CONSTRAINT `IdDia_HorarioRecurso` FOREIGN KEY (`IdDia`) REFERENCES `dia` (`IdDia`),
  CONSTRAINT `IdRecurso_HorarioRecurso` FOREIGN KEY (`IdRecurso`) REFERENCES `recurso` (`IdRecurso`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `localidad`
--

DROP TABLE IF EXISTS `localidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `localidad` (
  `IdLocalidad` int NOT NULL AUTO_INCREMENT,
  `IdProvincia` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdLocalidad`),
  UNIQUE KEY `IdLocalidad_UNIQUE` (`IdLocalidad`),
  KEY `IdProvincia_idx` (`IdProvincia`),
  CONSTRAINT `IdProvincia_Localidad` FOREIGN KEY (`IdProvincia`) REFERENCES `provincia` (`IdProvincia`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `motivo`
--

DROP TABLE IF EXISTS `motivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `motivo` (
  `IdMotivo` int NOT NULL AUTO_INCREMENT,
  `NombreMotivo` varchar(45) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdMotivo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `paciente`
--

DROP TABLE IF EXISTS `paciente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `paciente` (
  `IdPaciente` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Genero` varchar(15) DEFAULT NULL,
  `IdTipoDocumento` int NOT NULL,
  `NumeroDocumento` int NOT NULL,
  `FechaNacimiento` date DEFAULT NULL,
  `IdDomicilio` int NOT NULL,
  `IdTutoria` int NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdPaciente`),
  UNIQUE KEY `IdPaciente_UNIQUE` (`IdPaciente`),
  KEY `IdTipoDocumento_idx` (`IdTipoDocumento`),
  KEY `IdTutoria_idx` (`IdTutoria`),
  KEY `IdDomicilio_idx` (`IdDomicilio`),
  CONSTRAINT `IdDomicilio_Paciente` FOREIGN KEY (`IdDomicilio`) REFERENCES `domicilio` (`IdDomicilio`),
  CONSTRAINT `IdTipoDocumento_Paciente` FOREIGN KEY (`IdTipoDocumento`) REFERENCES `tipodocumento` (`IdTipoDocumento`),
  CONSTRAINT `IdTutoria_Paciente` FOREIGN KEY (`IdTutoria`) REFERENCES `tutoria` (`IdTutoria`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pais`
--

DROP TABLE IF EXISTS `pais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pais` (
  `IdPais` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdPais`),
  UNIQUE KEY `IdPais_UNIQUE` (`IdPais`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `preguntaadmision`
--

DROP TABLE IF EXISTS `preguntaadmision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `preguntaadmision` (
  `IdPreguntaAdmision` int NOT NULL AUTO_INCREMENT,
  `DescripcionPregunta` varchar(500) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdPreguntaAdmision`),
  UNIQUE KEY `IdPreguntaAdmision_UNIQUE` (`IdPreguntaAdmision`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `privilegio`
--

DROP TABLE IF EXISTS `privilegio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `privilegio` (
  `IdPrivilegio` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdPrivilegio`),
  UNIQUE KEY `IdPrivilegio_UNIQUE` (`IdPrivilegio`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `profesional`
--

DROP TABLE IF EXISTS `profesional`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profesional` (
  `IdProfesional` int NOT NULL AUTO_INCREMENT,
  `IdRecurso` int NOT NULL,
  `IdEspecialidad` int NOT NULL,
  `Matricula` varchar(15) NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdProfesional`),
  UNIQUE KEY `IdProfesional_UNIQUE` (`IdProfesional`),
  KEY `IdRecurso_idx` (`IdRecurso`),
  KEY `IdEspecialidad_idx` (`IdEspecialidad`),
  CONSTRAINT `IdEspecialidad_Profesional` FOREIGN KEY (`IdEspecialidad`) REFERENCES `especialidad` (`IdEspecialidad`),
  CONSTRAINT `IdRecurso_Profesional` FOREIGN KEY (`IdRecurso`) REFERENCES `recurso` (`IdRecurso`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `provincia`
--

DROP TABLE IF EXISTS `provincia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `provincia` (
  `IdProvincia` int NOT NULL AUTO_INCREMENT,
  `IdPais` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdProvincia`),
  UNIQUE KEY `IdProvincia_UNIQUE` (`IdProvincia`),
  KEY `IdPais_idx` (`IdPais`),
  CONSTRAINT `IdPais_Provincia` FOREIGN KEY (`IdPais`) REFERENCES `pais` (`IdPais`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `recurso`
--

DROP TABLE IF EXISTS `recurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recurso` (
  `IdRecurso` int NOT NULL AUTO_INCREMENT,
  `IdTipoRecurso` int NOT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Apellido` varchar(50) DEFAULT NULL,
  `IdTipoDocumento` int NOT NULL,
  `NumeroDocumento` int DEFAULT NULL,
  `Genero` varchar(15) DEFAULT NULL,
  `FechaNacimiento` datetime DEFAULT NULL,
  `Edad` int DEFAULT NULL,
  `Cuil` int DEFAULT NULL,
  `IdDomicilio` int DEFAULT NULL,
  `TelefonoCelular` varchar(15) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Legajo` varchar(10) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdRecurso`),
  UNIQUE KEY `IdRecurso_UNIQUE` (`IdRecurso`) /*!80000 INVISIBLE */,
  KEY `IdTipoDocumento_idx` (`IdTipoDocumento`),
  KEY `IdDomicilio_idx` (`IdDomicilio`),
  KEY `IdTipoRecurso_idx` (`IdTipoRecurso`) /*!80000 INVISIBLE */,
  CONSTRAINT `IdDomicilio_Recurso` FOREIGN KEY (`IdDomicilio`) REFERENCES `domicilio` (`IdDomicilio`),
  CONSTRAINT `IdTipoDocumento_Recurso` FOREIGN KEY (`IdTipoDocumento`) REFERENCES `tipodocumento` (`IdTipoDocumento`),
  CONSTRAINT `IdTipoRecurso_Recurso` FOREIGN KEY (`IdTipoRecurso`) REFERENCES `tiporecurso` (`IdTipoRecurso`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `IdRol` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdRol`),
  UNIQUE KEY `IdRol_UNIQUE` (`IdRol`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rolprivilegio`
--

DROP TABLE IF EXISTS `rolprivilegio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rolprivilegio` (
  `IdRolPrivilegio` int NOT NULL AUTO_INCREMENT,
  `IdRol` int NOT NULL,
  `IdPrivilegio` int NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  PRIMARY KEY (`IdRolPrivilegio`),
  UNIQUE KEY `IdRolPrivilegio(10)_UNIQUE` (`IdRolPrivilegio`),
  KEY `IdRol_idx` (`IdRol`),
  KEY `IdPrivilegio_idx` (`IdPrivilegio`),
  CONSTRAINT `IdPrivilegio_RolPrivilegio` FOREIGN KEY (`IdPrivilegio`) REFERENCES `privilegio` (`IdPrivilegio`),
  CONSTRAINT `IdRol_RolPrivilegio` FOREIGN KEY (`IdRol`) REFERENCES `rol` (`IdRol`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipodocumento`
--

DROP TABLE IF EXISTS `tipodocumento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipodocumento` (
  `IdTipoDocumento` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTipoDocumento`),
  UNIQUE KEY `IdTipoDocumento_UNIQUE` (`IdTipoDocumento`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipopatologia`
--

DROP TABLE IF EXISTS `tipopatologia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipopatologia` (
  `IdTipoPatologia` int NOT NULL AUTO_INCREMENT,
  `IdEspecialidad` int DEFAULT NULL,
  `Nombre` varchar(50) DEFAULT NULL,
  `Descripción` varchar(100) DEFAULT NULL,
  `FechaAlta` varchar(45) DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTipoPatologia`),
  KEY `IdEspecialidad_idx` (`IdEspecialidad`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tiporecurso`
--

DROP TABLE IF EXISTS `tiporecurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiporecurso` (
  `IdTipoRecurso` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTipoRecurso`),
  UNIQUE KEY `IdTipoRecurso_UNIQUE` (`IdTipoRecurso`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tiporeporte`
--

DROP TABLE IF EXISTS `tiporeporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiporeporte` (
  `IdTipoReporte` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) DEFAULT NULL,
  `Descripcion` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTipoReporte`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tipoturno`
--

DROP TABLE IF EXISTS `tipoturno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipoturno` (
  `IdTipoTurno` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Detalle` varchar(100) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTipoTurno`),
  UNIQUE KEY `IdTipoTurno_UNIQUE` (`IdTipoTurno`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `turno`
--

DROP TABLE IF EXISTS `turno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `turno` (
  `IdTurno` int NOT NULL AUTO_INCREMENT,
  `IdTipoTurno` int NOT NULL,
  `IdEspecialidad` int NOT NULL,
  `IdProfesional` int DEFAULT NULL,
  `IdPaciente` int NOT NULL,
  `FechaTurno` date NOT NULL,
  `HoraDesde` time NOT NULL,
  `HoraHasta` time DEFAULT NULL,
  `IdEstadoTurno` int NOT NULL,
  `FechaAsignado` datetime DEFAULT NULL,
  `FechaReceptado` datetime DEFAULT NULL,
  `FechaReasignado` datetime DEFAULT NULL,
  `FechaAnulado` datetime DEFAULT NULL,
  `FechaInicioAtencion` datetime DEFAULT NULL,
  `FechaFinalAtencion` datetime DEFAULT NULL,
  `IdMotivoAnulado` int DEFAULT NULL,
  `IdUsuarioAsignado` int DEFAULT NULL,
  `IdUsuarioReceptado` int DEFAULT NULL,
  `IdUsuarioReasignado` int DEFAULT NULL,
  `IdUsuarioAnulado` int DEFAULT NULL,
  `IdUsuarioInicioAtencion` int DEFAULT NULL,
  `IdUsuarioFinalAtencion` int DEFAULT NULL,
  `TurnoReasignado` tinyint DEFAULT NULL,
  `IdTurnoOriginal` int DEFAULT NULL,
  `IdTurnoReasignado` int DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTurno`),
  UNIQUE KEY `IdTurno_UNIQUE` (`IdTurno`),
  KEY `IdTipoTurno_idx` (`IdTipoTurno`),
  KEY `IdEstadoTurno_idx` (`IdEstadoTurno`),
  KEY `IdEspecialidad_idx` (`IdEspecialidad`),
  KEY `IdPaciente_idx` (`IdPaciente`),
  KEY `IdMotivoAnulado_idx` (`IdMotivoAnulado`),
  CONSTRAINT `IdEspecialidad_Turno` FOREIGN KEY (`IdEspecialidad`) REFERENCES `especialidad` (`IdEspecialidad`),
  CONSTRAINT `IdEstadoTurno_Turno` FOREIGN KEY (`IdEstadoTurno`) REFERENCES `estadoturno` (`IdEstadoTurno`),
  CONSTRAINT `IdMotivoAnulado_Turno` FOREIGN KEY (`IdMotivoAnulado`) REFERENCES `motivo` (`IdMotivo`),
  CONSTRAINT `IdPaciente_Turno` FOREIGN KEY (`IdPaciente`) REFERENCES `paciente` (`IdPaciente`),
  CONSTRAINT `IdTipoTurno_Turno` FOREIGN KEY (`IdTipoTurno`) REFERENCES `tipoturno` (`IdTipoTurno`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tutoria`
--

DROP TABLE IF EXISTS `tutoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tutoria` (
  `IdTutoria` int NOT NULL AUTO_INCREMENT,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Ocupacion` varchar(50) DEFAULT NULL,
  `TelefonoFijo` varchar(15) DEFAULT NULL,
  `TelefonoCelular` varchar(15) DEFAULT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdTutoria`),
  UNIQUE KEY `IdTutoria_UNIQUE` (`IdTutoria`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `IdUsuario` int NOT NULL AUTO_INCREMENT,
  `IdRecurso` int NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Contraseña` varchar(20) NOT NULL,
  `IdRol` int NOT NULL,
  `FechaAlta` datetime DEFAULT NULL,
  `FechaModificacion` datetime DEFAULT NULL,
  `FechaBaja` datetime DEFAULT NULL,
  `IdUsuarioAlta` int DEFAULT NULL,
  `IdUsuarioModificacion` int DEFAULT NULL,
  `IdUsuarioBaja` int DEFAULT NULL,
  PRIMARY KEY (`IdUsuario`),
  UNIQUE KEY `IdUsuario_UNIQUE` (`IdUsuario`),
  KEY `IdRecurso_idx` (`IdRecurso`),
  KEY `IdRol_idx` (`IdRol`),
  CONSTRAINT `IdRecursos_Usuario` FOREIGN KEY (`IdRecurso`) REFERENCES `recurso` (`IdRecurso`),
  CONSTRAINT `IdRol_Usuario` FOREIGN KEY (`IdRol`) REFERENCES `rol` (`IdRol`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-11 20:09:08
