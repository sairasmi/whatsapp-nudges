-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 07, 2023 at 10:34 PM
-- Server version: 10.4.19-MariaDB
-- PHP Version: 8.0.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `whatsapp_nudge`
--

-- --------------------------------------------------------

--
-- Table structure for table `cron_job_log`
--

CREATE TABLE `cron_job_log` (
  `id` int(11) NOT NULL,
  `job_type` varchar(20) NOT NULL,
  `job_status` varchar(20) NOT NULL,
  `job_description` varchar(255) DEFAULT NULL,
  `job_completed_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `message_history`
--

CREATE TABLE `message_history` (
  `id` int(11) NOT NULL,
  `vendor_username` varchar(10) DEFAULT NULL,
  `fetch_date` date DEFAULT NULL,
  `mobile` varchar(10) NOT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `promt_topic` varchar(255) DEFAULT NULL,
  `first_promt_responses` varchar(255) DEFAULT NULL,
  `second_promt_responses` varchar(255) DEFAULT NULL,
  `third_promt_responses` varchar(255) DEFAULT NULL,
  `rating` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `request_about` varchar(255) DEFAULT NULL,
  `request_type` varchar(255) DEFAULT NULL,
  `feedback` varchar(255) DEFAULT NULL,
  `orig_message_created_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `message_log`
--

CREATE TABLE `message_log` (
  `id` int(11) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `nudge` varchar(255) NOT NULL,
  `status` varchar(20) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `sent_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `nudges`
--

CREATE TABLE `nudges` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `nudge_identifier` varchar(255) NOT NULL,
  `isActive` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `nudges`
--

INSERT INTO `nudges` (`id`, `name`, `nudge_identifier`, `isActive`, `created_at`, `updated_at`) VALUES
(1, 'BTT Meeting', 'BTT Meeting', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(2, 'Monthly Review Meeting: Block to GP', 'Monthly Review Meeting: Block to GP', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(3, 'Monthly Review Meeting: District to Block', 'Monthly Review Meeting: District to Block', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(4, 'Pest Incidence', 'Pest Incidence', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(5, 'Scheme Target Setting: Block to GP', 'Scheme Target Setting: Block to GP', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(6, 'Scheme Target Setting: District to Block', 'Scheme Target Setting: District to Block', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(7, 'Weather disruptions', 'Weather disruptions', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56'),
(8, 'Crop Coverage Report', 'Crop Coverage Report', 1, '2023-05-08 00:19:56', '2023-05-08 00:19:56');

-- --------------------------------------------------------

--
-- Table structure for table `t_block_wise_official_contact_info`
--

CREATE TABLE `t_block_wise_official_contact_info` (
  `int_id` bigint(20) UNSIGNED NOT NULL,
  `vch_username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vch_official_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vch_phone_no` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vch_Block` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `vch_District` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `en_department` enum('DSC&WD','HORTICULTURE','AGRICULTURE','AHD','FARD','LI','Cooperation','FISHERIES','AH&VS','OPELIP','OLM','ICARDA','ICRISAT','IRRI','NRRI','WASSAN','CIWA','CTRAN','OUAT','MSSRF') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `vch_designation` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `t_block_wise_official_contact_info`
--

INSERT INTO `t_block_wise_official_contact_info` (`int_id`, `vch_username`, `vch_official_name`, `vch_phone_no`, `vch_Block`, `vch_District`, `en_department`, `vch_designation`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'abanikanta.patra', 'Sri Abani Kanta Patra', '9460163334', 'Khairaput', 'Malkangiri', 'DSC&WD', 'ASCO', '2024-04-23 05:40:00', '2024-04-23 05:40:00', NULL),
(2, 'abanikanta.patra', 'Sri Abani Kanta Patra', '9460163334', 'Mathili', 'Malkangiri', 'DSC&WD', 'ASCO', '2024-04-23 05:40:00', '2024-04-23 05:40:00', NULL),
(3, 'abhijit.pradhan', 'Abhijit Pradhan', '9460163334', 'Jagannathprasad', 'Ganjam', 'AGRICULTURE', 'AAO', '2024-04-23 05:40:00', '2024-04-23 05:40:00', NULL),
(4, 'abhimanyu.swain', 'Abhimanyu Swain', '9460163334', 'Pottangi', 'Koraput', 'AGRICULTURE', 'AAO', '2024-04-23 05:40:00', '2024-04-23 05:40:00', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cron_job_log`
--
ALTER TABLE `cron_job_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_cron_job_log_id` (`id`);

--
-- Indexes for table `message_history`
--
ALTER TABLE `message_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_message_history_id` (`id`);

--
-- Indexes for table `message_log`
--
ALTER TABLE `message_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_message_log_id` (`id`);

--
-- Indexes for table `nudges`
--
ALTER TABLE `nudges`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_nudges_id` (`id`);

--
-- Indexes for table `t_block_wise_official_contact_info`
--
ALTER TABLE `t_block_wise_official_contact_info`
  ADD PRIMARY KEY (`int_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cron_job_log`
--
ALTER TABLE `cron_job_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `message_history`
--
ALTER TABLE `message_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `message_log`
--
ALTER TABLE `message_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nudges`
--
ALTER TABLE `nudges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
