-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 14, 2024 at 01:02 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sigma_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) DEFAULT NULL,
  `harga` int(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`id`, `nama`, `harga`) VALUES
(1, 'Nasi Goreng Spesial', 25000),
(2, 'Soto Betawi', 30000),
(3, 'Ayam Penyet Sambal Matah', 28000),
(4, 'Gado-Gado', 22000),
(5, 'Sate Ayam', 35000),
(6, 'Mie Goreng Jawa', 20000),
(7, 'Ikan Bakar Rica-Rica', 50000),
(8, 'Rendang Daging Sapi', 55000),
(9, 'Bakso Komplit', 27000),
(10, 'Nasi Uduk', 18000),
(11, 'Tahu Gejrot', 15000),
(12, 'Sop Buntut', 45000),
(13, 'Nasi Campur Bali', 40000),
(14, 'Sate Lilit Bali', 38000),
(15, 'Pecel Lele', 25000),
(16, 'Soto Ayam', 25000),
(17, 'Ayam Taliwang', 40000),
(18, 'Gudeg Jogja', 32000),
(19, 'Coto Makassar', 35000),
(20, 'Rawon Surabaya', 33000);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `client_ip` varchar(45) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `total_harga` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `client_ip`, `nama`, `quantity`, `total_harga`) VALUES
(1, '192.168.110.214', 'Nasi Goreng Spesial', 3, 75000.00),
(2, '192.168.110.214', 'Soto Betawi', 2, 60000.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
