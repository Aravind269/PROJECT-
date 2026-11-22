-- =====================================================================
-- Community Renewable Energy Awareness and Management Portal
-- Database Schema for MySQL 5.7+ / MySQL 8.0+ / MariaDB
-- =====================================================================

CREATE DATABASE IF NOT EXISTS `community_renewable_energy` 
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `community_renewable_energy`;

-- 1. Users Table
DROP TABLE IF EXISTS `post_comments`;
DROP TABLE IF EXISTS `community_posts`;
DROP TABLE IF EXISTS `saved_calculations`;
DROP TABLE IF EXISTS `feedback_messages`;
DROP TABLE IF EXISTS `projects`;
DROP TABLE IF EXISTS `energy_tips`;
DROP TABLE IF EXISTS `educational_articles`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `role` VARCHAR(20) DEFAULT 'member',
  `bio` TEXT NULL,
  `location` VARCHAR(100) DEFAULT 'Green Valley Community',
  `energy_interest` VARCHAR(100) DEFAULT 'Rooftop Solar & Energy Efficiency',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Renewable Energy Projects Table
CREATE TABLE `projects` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(150) NOT NULL,
  `slug` VARCHAR(150) NOT NULL UNIQUE,
  `category` VARCHAR(50) NOT NULL,
  `description` TEXT NOT NULL,
  `location` VARCHAR(120) NOT NULL,
  `capacity` VARCHAR(60) NOT NULL,
  `annual_generation` DOUBLE DEFAULT 0.0,
  `co2_saved_annual` DOUBLE DEFAULT 0.0,
  `participants_count` INT DEFAULT 0,
  `status` VARCHAR(30) DEFAULT 'Active',
  `budget` DOUBLE DEFAULT 0.0,
  `installation_guide` TEXT NULL,
  `image_url` VARCHAR(255) NULL,
  `created_by_id` INT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_projects_creator` FOREIGN KEY (`created_by_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Community Posts Table
CREATE TABLE `community_posts` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `category` VARCHAR(50) DEFAULT 'Solar Experience',
  `content` TEXT NOT NULL,
  `upvotes` INT DEFAULT 0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_posts_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Post Comments Table
CREATE TABLE `post_comments` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `post_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_comments_post` FOREIGN KEY (`post_id`) REFERENCES `community_posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_comments_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Saved Energy Calculations Table
CREATE TABLE `saved_calculations` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT NULL,
  `monthly_bill` DOUBLE NOT NULL,
  `monthly_kwh` DOUBLE NOT NULL,
  `tariff_rate` DOUBLE DEFAULT 0.15,
  `roof_area_sqft` DOUBLE DEFAULT 500.0,
  `sunlight_hours` DOUBLE DEFAULT 5.0,
  `recommended_kw` DOUBLE NOT NULL,
  `monthly_savings` DOUBLE NOT NULL,
  `annual_savings` DOUBLE NOT NULL,
  `co2_reduction_tons` DOUBLE NOT NULL,
  `trees_equivalent` INT DEFAULT 0,
  `payback_years` DOUBLE DEFAULT 0.0,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_calc_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Contact and Feedback Table
CREATE TABLE `feedback_messages` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `subject` VARCHAR(150) NOT NULL,
  `category` VARCHAR(50) DEFAULT 'General Feedback',
  `message` TEXT NOT NULL,
  `status` VARCHAR(20) DEFAULT 'New',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Energy Saving Tips Table
CREATE TABLE `energy_tips` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(150) NOT NULL,
  `category` VARCHAR(50) NOT NULL,
  `description` TEXT NOT NULL,
  `potential_savings_kwh` INT DEFAULT 50,
  `difficulty` VARCHAR(20) DEFAULT 'Easy',
  `icon` VARCHAR(50) DEFAULT 'bi-lightbulb'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Educational Articles Table
CREATE TABLE `educational_articles` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(200) NOT NULL,
  `slug` VARCHAR(200) NOT NULL UNIQUE,
  `category` VARCHAR(50) NOT NULL,
  `summary` TEXT NOT NULL,
  `content` TEXT NOT NULL,
  `read_time` VARCHAR(20) DEFAULT '5 min read',
  `icon` VARCHAR(50) DEFAULT 'bi-journal-text',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================================
-- Seed Initial Data
-- =====================================================================

-- Demo Users (Password: admin123 and green123)
-- Hash generated using scrypt (compatible with Werkzeug)
INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `role`, `bio`, `location`, `energy_interest`) VALUES
(1, 'Elena Vance', 'elena@greenportal.org', 'scrypt:32768:8:1$7CqU2qL$f2c2539fbe54c5e88863f82cb3aaef2eb82dbe0b7f8ba1686a6358ad7a13d80eb8092bbfa7dfc4da17e0b571168f182c40c3c6f4df201e7492c6ea003ff5888d', 'admin', 'Environmental engineer and coordinator of the Community Solar Cooperative.', 'Portland, OR', 'Microgrids & Solar Photovoltaics'),
(2, 'Marcus Chen', 'marcus@cleanenergy.org', 'scrypt:32768:8:1$7CqU2qL$f2c2539fbe54c5e88863f82cb3aaef2eb82dbe0b7f8ba1686a6358ad7a13d80eb8092bbfa7dfc4da17e0b571168f182c40c3c6f4df201e7492c6ea003ff5888d', 'member', 'Homeowner with an 8.4 kW rooftop solar and battery storage setup since 2023.', 'Denver, CO', 'Rooftop Solar & Home Battery Storage'),
(3, 'Sophia Rodriguez', 'sophia@ecocommunity.net', 'scrypt:32768:8:1$7CqU2qL$f2c2539fbe54c5e88863f82cb3aaef2eb82dbe0b7f8ba1686a6358ad7a13d80eb8092bbfa7dfc4da17e0b571168f182c40c3c6f4df201e7492c6ea003ff5888d', 'member', 'Permaculture advocate and clean energy enthusiast working on biomass digestors.', 'Austin, TX', 'Biomass & Organic Waste Energy');

-- Projects
INSERT INTO `projects` (`id`, `title`, `slug`, `category`, `description`, `location`, `capacity`, `annual_generation`, `co2_saved_annual`, `participants_count`, `status`, `budget`, `installation_guide`, `image_url`, `created_by_id`) VALUES
(1, 'Sunny Heights Community Solar Farm', 'sunny-heights-community-solar-farm', 'Solar', 'A joint neighborhood solar garden installed on unused municipal land, allowing 180 apartment residents and homeowners without suitable roofs to subscribe and offset their electric bills.', 'Oakridge District, Portland, OR', '450 kW', 680.0, 480.0, 185, 'Active', 520000.0, '1. Site feasibility assessment; 2. Community subscriber onboarding; 3. Tier-1 monocrystalline bifacial panel mounting; 4. Grid interconnect with net metering; 5. Cloud inverter monitoring.', 'solar_farm.svg', 1),
(2, 'Prairie Breeze Cooperative Wind Project', 'prairie-breeze-cooperative-wind-project', 'Wind', 'Community-owned dual 850 kW wind turbines powering agricultural processing, community centers, and local schools with 100% clean kinetic wind energy.', 'Meadow Valley County, CO', '1.7 MW', 4200.0, 2940.0, 310, 'Active', 2100000.0, '1. Wind resource LiDAR measurement over 12 months; 2. Environmental and avian impact clearance; 3. Foundation concrete pouring and tower erection; 4. Grid synchronization and supervisory SCADA control.', 'wind_project.svg', 1),
(3, 'Clear Creek Micro-Hydro Generation Station', 'clear-creek-micro-hydro-generation-station', 'Hydro', 'Low-impact run-of-river micro-hydro electric installation providing steady, non-intermittent baseline power to 75 mountain valley households without damming the creek.', 'Cascade Foothills, WA', '120 kW', 850.0, 595.0, 75, 'Active', 280000.0, '1. Intake screen installation with fish-friendly diversion; 2. Penstock pipe laying along terrain slope; 3. Pelton impulse turbine and induction generator setup; 4. Automated flow control valve system.', 'hydro_project.svg', 1),
(4, 'GreenFields Agricultural Biomass & Biogas Unit', 'greenfields-agricultural-biomass-biogas-unit', 'Biomass', 'Anaerobic digester facility converting farm organic matter, crop residues, and animal manure into clean biogas for electricity generation and nutrient-rich biofertilizer.', 'Central Valley Agro-District, CA', '350 kW', 2100.0, 1470.0, 92, 'Active', 750000.0, '1. Anaerobic digester tank sealing and heating loops; 2. Biogas collection dome and sulfur removal scrubber; 3. Combined Heat and Power (CHP) engine integration; 4. High-grade organic biofertilizer separator.', 'biomass_project.svg', 2),
(5, 'Sunset Ridge Community Rooftop Microgrid', 'sunset-ridge-community-rooftop-microgrid', 'Solar', 'An interconnected network of 45 residential rooftops equipped with smart hybrid inverters and localized LFP battery storage for community resilience during blackouts.', 'Sunset Ridge, Austin, TX', '225 kW', 340.0, 238.0, 45, 'Planning', 390000.0, '1. Structural roof inspections and electrical upgrades; 2. Standardized 5kW solar + 10kWh battery kits; 3. Smart gateway for peer-to-peer virtual power plant coordination.', 'microgrid_project.svg', 3);

-- Community Posts
INSERT INTO `community_posts` (`id`, `user_id`, `title`, `category`, `content`, `upvotes`) VALUES
(1, 2, 'My First Year with an 8.4 kW Rooftop Solar System: Real Numbers and Tips', 'Solar Experience', 'We installed 21 monocrystalline panels with microinverters last spring. Over 12 months, our electricity bill dropped from an average of $215/month to just the $14 grid connection fee! We produced 11,200 kWh and even accumulated $180 in net metering credits during summer. For anyone considering it: make sure to trim overhanging branches and opt for microinverters if you have partial morning shade.', 24),
(2, 3, 'How our neighborhood organized a collective bulk-purchasing program', 'Policy & Subsidy', 'By bundling 28 households together, we negotiated a 22% discount with a certified local solar installer! We also leveraged the 30% clean energy tax credit and local municipal rebates. The whole process took 4 months from informational meetings to first panel energization. Happy to share our RFP template with anyone interested!', 19),
(3, 1, 'Understanding Net Metering vs Time-of-Use (TOU) Rates in 2026', 'Energy Tips', 'Utility rate structures are evolving rapidly. With Time-of-Use rates, electricity is most expensive between 4 PM and 9 PM. If you pair your solar panels with a modest 5-10 kWh battery, you can discharge battery power during peak hours and sell excess solar during high-rate intervals, drastically increasing your annual financial savings.', 15);

-- Post Comments
INSERT INTO `post_comments` (`id`, `post_id`, `user_id`, `content`) VALUES
(1, 1, 3, 'Incredible results Marcus! How did the snow in winter affect your generation in Colorado?'),
(2, 1, 2, 'Thanks Sophia! The panels are installed at a 35-degree tilt, so snow usually slides off within 24-48 hours once the sun peeks out. Losses were less than 5% over winter!'),
(3, 2, 1, 'Collective purchasing is the gold standard for accelerating community renewable adoption. Great work!');

-- Energy Saving Tips
INSERT INTO `energy_tips` (`id`, `title`, `category`, `description`, `potential_savings_kwh`, `difficulty`, `icon`) VALUES
(1, 'Switch to High-Efficiency LED Lighting', 'Lighting', 'Replace remaining incandescent and halogen bulbs with ENERGY STAR certified LEDs. They use 75% less energy and last up to 25 times longer.', 45, 'Easy', 'bi-lightbulb'),
(2, 'Install a Smart Programmable Thermostat', 'Heating & Cooling', 'Automate temperature setbacks when sleeping or away from home. Adjusting 7-10 degrees for 8 hours daily can save up to 10% on annual HVAC costs.', 120, 'Moderate', 'bi-thermometer-half'),
(3, 'Eliminate Phantom Energy Drain', 'Appliances', 'Use smart power strips that cut power to TVs, gaming consoles, and desktop peripherals when in standby mode, which often accounts for 5-10% of household electricity.', 35, 'Easy', 'bi-plug'),
(4, 'Optimize Refrigerator and Freezer Temperatures', 'Kitchen & Appliances', 'Keep refrigerator between 35°F and 38°F (1.7°C to 3.3°C) and freezer at 0°F (-18°C). Regularly vacuum condenser coils behind or underneath to maintain compressor efficiency.', 25, 'Easy', 'bi-snow'),
(5, 'Wash Laundry in Cold Water', 'Appliances', 'About 75% to 90% of energy used by your washing machine goes toward heating the water. Cold water detergents clean modern fabrics equally well while saving substantial electricity.', 40, 'Easy', 'bi-droplet-half'),
(6, 'Seal Air Leaks Around Windows and Doors', 'Home', 'Apply weatherstripping and silicone caulk around drafty window frames, exterior doors, and attic hatches to keep conditioned air inside.', 95, 'Moderate', 'bi-house-heart');

-- Educational Articles
INSERT INTO `educational_articles` (`id`, `title`, `slug`, `category`, `summary`, `content`, `read_time`, `icon`) VALUES
(1, 'The Complete Guide to Solar Photovoltaic Systems', 'complete-guide-to-solar-pv', 'Solar', 'Discover how solar semiconductor cells convert sunlight directly into clean, carbon-free electricity for homes and businesses.', 'Solar photovoltaic (PV) technology harnesses solar irradiance through semiconductor silicon cells. When sunlight strikes the cell, photons energize electrons, generating a Direct Current (DC). An inverter then converts this DC into standard Alternating Current (AC) for household appliances.\n\nKey Advantages:\n- Zero operational emissions and air pollutants.\n- Abundant, inexhaustible resource across all inhabited continents.\n- Minimal moving parts resulting in 25 to 30-year operational lifespans.\n- Modular scalability from 1 kW residential setups to 500 MW utility arrays.\n\nChallenges & Solutions:\n- Intermittency: Solved through advanced lithium iron phosphate (LFP) energy storage and smart grid interconnections.\n- Upfront capital expense: Substantially reduced by government incentives, solar tax credits, and community group buys.', '6 min read', 'bi-sun-fill'),
(2, 'Harnessing the Wind: From Gentle Breezes to Community Turbines', 'harnessing-the-wind-turbines', 'Wind', 'Learn how aerodynamic turbine blades convert kinetic wind energy into mechanical and electrical power.', 'Wind power utilizes aerodynamic lift principles similar to aircraft wings. Moving air passes over curved turbine blades, creating lift and driving a central rotor connected through a gearbox to a high-efficiency generator.\n\nAdvantages:\n- Exceptional energy return on investment (EROI).\n- Compact land footprint; farming and cattle grazing continue right beneath the towers.\n- Very low lifecycle carbon footprint (under 11 grams of CO2 equivalent per kWh generated).\n\nConsiderations:\n- Site-dependent wind resource requirements requiring average speeds above 4.5 m/s.\n- Siting assessments required to protect local bird and bat migration corridors.', '5 min read', 'bi-wind'),
(3, 'Micro-Hydro and Run-of-River Power for Mountain Communities', 'micro-hydro-run-of-river', 'Hydro', 'How flowing streams deliver steady, baseline renewable electricity without ecological disturbance or large reservoirs.', 'Micro-hydro systems harness the kinetic and gravitational potential energy of falling water. Unlike mega-dams that flood valleys, run-of-river installations divert a fraction of a stream through a sloped penstock to spin a Pelton or Turgo turbine, returning the water immediately downstream unharmed.\n\nAdvantages:\n- High reliability factor (often 70% to 90% capacity factor, running 24/7 day and night).\n- Extremely high energy density compared to solar or wind on equivalent footprint.\n- Decades-long service life with basic preventive maintenance.', '4 min read', 'bi-water'),
(4, 'Biomass and Biogas: Transforming Organic Waste into Circular Energy', 'biomass-and-biogas-circular-energy', 'Biomass', 'Explore the role of agricultural residues, food waste, and organic matter in closing the carbon loop and providing renewable baseload energy.', 'Biomass energy captures energy stored in chemical bonds of organic materials. Through anaerobic digestion or gasification, organic matter such as crop husks, livestock manure, and municipality food scrap is broken down by microorganisms into methane-rich biogas, which fuels clean combustion engines.\n\nAdvantages:\n- Diverts methane-emitting organic waste from municipal landfills.\n- Produces high-value organic biofertilizer as a by-product.\n- Provides controllable, on-demand dispatchable renewable power.', '5 min read', 'bi-tree-fill');

-- Feedback / Contact Sample
INSERT INTO `feedback_messages` (`name`, `email`, `subject`, `category`, `message`, `status`) VALUES
('David Miller', 'david.m@example.com', 'Inquiry regarding Community Solar Subscription', 'Inquiry', 'Hello! Our family lives in an apartment building in the Oakridge district. How can we enroll in the Sunny Heights Community Solar Farm to receive clean power credits on our monthly utility bill?', 'New');
