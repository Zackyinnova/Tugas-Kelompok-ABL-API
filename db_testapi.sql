-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 16, 2026 at 05:54 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_testapi`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `release_date` date DEFAULT NULL,
  `pages` int(11) DEFAULT NULL,
  `cover_image` varchar(255) DEFAULT NULL,
  `abstract` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `title`, `author`, `publisher`, `release_date`, `pages`, `cover_image`, `abstract`, `created_at`) VALUES
(1, 'Think and Grow Rich', 'Napoleon Hill', 'The Ralston Society', '1937-01-01', 320, '../static/img/CoverBuku/think and grow rich.jpg', 'Think and Grow Rich adalah buku pengembangan diri karya Napoleon Hill yang membahas prinsip-prinsip kesuksesan berdasarkan hasil wawancara dan penelitian terhadap para tokoh sukses. Buku ini menekankan pentingnya tujuan yang jelas, keyakinan, ketekunan, pengendalian diri, serta kekuatan pikiran positif untuk mencapai kesuksesan finansial dan pribadi.', '2026-06-16 12:48:22'),
(2, 'Atomic Habits', 'James Clear', 'Avery', '2018-10-16', 320, '../static/img/CoverBuku/atomic habits.jpg', 'Buku tentang bagaimana perubahan kecil yang dilakukan secara konsisten dapat menghasilkan perubahan besar dalam kehidupan.', '2026-06-16 12:54:32'),
(3, 'Edensor', 'Andrea Hirata', 'Bentang Pustaka', '2007-01-01', 294, '../static/img/CoverBuku/edensor.jpg', 'Novel ketiga dari tetralogi Laskar Pelangi yang menceritakan perjalanan Ikal dan Arai menggapai mimpi di Eropa.', '2026-06-16 12:54:32'),
(4, 'Filosofi Teras', 'Henry Manampiring', 'Kompas', '2018-01-01', 346, '../static/img/CoverBuku/filosofi teras.jpg', 'Buku yang memperkenalkan filsafat Stoikisme dan penerapannya dalam kehidupan sehari-hari.', '2026-06-16 12:54:32'),
(5, 'Laskar Pelangi', 'Andrea Hirata', 'Bentang Pustaka', '2005-01-01', 529, '../static/img/CoverBuku/Laskar Pelangi.jpg', 'Novel inspiratif tentang perjuangan anak-anak Belitung dalam memperoleh pendidikan.', '2026-06-16 12:54:32'),
(6, 'Rich Dad Poor Dad', 'Robert T. Kiyosaki', 'Warner Books', '1997-04-01', 336, '../static/img/CoverBuku/rich dad poor dad.jpg', 'Buku keuangan pribadi yang membandingkan pola pikir orang kaya dan orang miskin terhadap uang.', '2026-06-16 12:54:32'),
(7, 'The Psychology of Money', 'Morgan Housel', 'Harriman House', '2020-09-08', 256, '../static/img/CoverBuku/The Psychology of Money.jpg', 'Membahas bagaimana perilaku dan psikologi manusia memengaruhi keputusan keuangan.', '2026-06-16 12:54:32'),
(8, '5 cm', 'Donny Dhirgantoro', 'Grasindo', '2005-01-01', 381, '../static/img/CoverBuku/5cm.jpg', 'Novel tentang persahabatan, mimpi, dan perjalanan mendaki Mahameru.', '2026-06-16 12:54:32'),
(9, 'Berani Tidak Disukai', 'Ichiro Kishimi & Fumitake Koga', 'Gramedia Pustaka Utama', '2019-01-01', 336, '../static/img/CoverBuku/Berani Tidak Disukai.jpg', 'Buku yang membahas psikologi Alfred Adler tentang kebebasan dan kebahagiaan hidup.', '2026-06-16 12:54:32'),
(10, 'The Daily Stoic', 'Ryan Holiday & Stephen Hanselman', 'Portfolio', '2016-10-18', 416, '../static/img/CoverBuku/the daily.jpg', 'Kumpulan refleksi harian berdasarkan ajaran filsafat Stoikisme untuk kehidupan modern.', '2026-06-16 12:54:32');

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(1, 'zacky innova', 'zackyinova1@gmail.com', 'astaga12', '2026-06-14 15:52:08'),
(2, 'jeckaja', 'zackyinova2@gmail.com', 'scrypt:32768:8:1$lQRuOvbJEHsO6Iz6$f596fbf9d266ca738c869d1c23bdaf6893f8e0dd9978855050a0c81793b3ddbc4e6c3e4043fb7224d423056da29121eade045c008c4273ceecd0c98100d07728', '2026-06-16 05:32:34'),
(3, 'zacky innov1', 'zackyinova3@gmail.com', 'scrypt:32768:8:1$r3QkWinMwD53BSR5$2c583aa716ee03b387d1ab86b2e2cfc11576d8d59c5dfb87a14f83d1cd165bf5bea79492864aae500d232c05993ff76bfecc2727b75dbd80a9df149ad26d7372', '2026-06-16 05:46:22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_fav` (`user_id`,`book_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
