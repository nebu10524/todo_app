-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para todo_app
CREATE DATABASE IF NOT EXISTS `todo_app` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `todo_app`;

-- Volcando estructura para tabla todo_app.tareas
CREATE TABLE IF NOT EXISTS `tareas` (
  `id_tarea` varchar(10) NOT NULL,
  `usuario_id` varchar(10) NOT NULL,
  `texto` text NOT NULL,
  `fecha` date DEFAULT curdate(),
  `prioridad` enum('baja','media','alta') DEFAULT 'media',
  `completada` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id_tarea`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla todo_app.tareas: ~0 rows (aproximadamente)
INSERT INTO `tareas` (`id_tarea`, `usuario_id`, `texto`, `fecha`, `prioridad`, `completada`) VALUES
	('TAR001', 'USU001', 'Actualizar informe final del proyecto', '2025-09-01', 'baja', 1);

-- Volcando estructura para tabla todo_app.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id_usuario` varchar(10) NOT NULL,
  `usuario` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla todo_app.usuarios: ~0 rows (aproximadamente)
INSERT INTO `usuarios` (`id_usuario`, `usuario`, `email`, `password`) VALUES
	('USU001', 'Andy Torres', 'andy.torres@example.com', '654321');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
