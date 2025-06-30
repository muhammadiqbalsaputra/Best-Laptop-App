-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 30, 2025 at 07:16 PM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `spk_laptop`
--

-- --------------------------------------------------------

--
-- Table structure for table `alternatif`
--

CREATE TABLE `alternatif` (
  `id` int NOT NULL,
  `nama` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `alternatif`
--

INSERT INTO `alternatif` (`id`, `nama`) VALUES
(1, 'Acer Swift 3'),
(2, 'Asus Vivobook 15'),
(3, 'Lenovo IdeaPad Slim 5'),
(4, 'Lenovo Ideapad Gaming 3');

-- --------------------------------------------------------

--
-- Table structure for table `kriteria`
--

CREATE TABLE `kriteria` (
  `id` int NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `bobot` int DEFAULT NULL,
  `jenis` enum('benefit','cost') NOT NULL DEFAULT 'benefit'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `kriteria`
--

INSERT INTO `kriteria` (`id`, `nama`, `bobot`, `jenis`) VALUES
(1, 'Processor', 5, 'benefit'),
(2, 'Penyimpanan', 4, 'benefit'),
(3, 'Jenis_Penyimpanan', 3, 'benefit'),
(4, 'Tahun_Rilis', 2, 'benefit'),
(5, 'Harga', 5, 'cost'),
(6, 'Daya_Tahan', 3, 'benefit'),
(7, 'Ukuran_Layar', 3, 'benefit'),
(8, 'Berat', 4, 'cost'),
(9, 'Fitur_Tambahan', 4, 'benefit'),
(10, 'tampilan', 1, 'benefit');

-- --------------------------------------------------------

--
-- Table structure for table `skor`
--

CREATE TABLE `skor` (
  `alternatif_id` int NOT NULL,
  `kriteria_id` int NOT NULL,
  `nilai` decimal(10,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `skor`
--

INSERT INTO `skor` (`alternatif_id`, `kriteria_id`, `nilai`) VALUES
(1, 1, '8.0000'),
(1, 2, '512.0000'),
(1, 3, '3.0000'),
(1, 4, '2023.0000'),
(1, 5, '2.0000'),
(1, 6, '14.0000'),
(1, 7, '1.2000'),
(1, 8, '3.0000'),
(1, 9, '2.0000'),
(1, 10, '2.0000'),
(2, 1, '7.0000'),
(2, 2, '256.0000'),
(2, 3, '2.0000'),
(2, 4, '2022.0000'),
(2, 5, '3.0000'),
(2, 6, '15.6000'),
(2, 7, '1.7000'),
(2, 8, '2.0000'),
(2, 9, '2.0000'),
(2, 10, '2.0000'),
(3, 1, '9.0000'),
(3, 2, '1024.0000'),
(3, 3, '3.0000'),
(3, 4, '2024.0000'),
(3, 5, '2.0000'),
(3, 6, '14.0000'),
(3, 7, '1.4000'),
(3, 8, '3.0000'),
(3, 9, '2.0000'),
(3, 10, '2.0000'),
(4, 1, '8.0000'),
(4, 2, '1024.0000'),
(4, 3, '3.0000'),
(4, 4, '2024.0000'),
(4, 5, '3.0000'),
(4, 6, '8.0000'),
(4, 7, '14.0000'),
(4, 8, '2.0000'),
(4, 9, '3.0000'),
(4, 10, '2.0000');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alternatif`
--
ALTER TABLE `alternatif`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kriteria`
--
ALTER TABLE `kriteria`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `skor`
--
ALTER TABLE `skor`
  ADD PRIMARY KEY (`alternatif_id`,`kriteria_id`),
  ADD KEY `kriteria_id` (`kriteria_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alternatif`
--
ALTER TABLE `alternatif`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `kriteria`
--
ALTER TABLE `kriteria`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `skor`
--
ALTER TABLE `skor`
  ADD CONSTRAINT `skor_ibfk_1` FOREIGN KEY (`alternatif_id`) REFERENCES `alternatif` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `skor_ibfk_2` FOREIGN KEY (`kriteria_id`) REFERENCES `kriteria` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
