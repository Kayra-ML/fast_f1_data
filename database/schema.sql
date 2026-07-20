-- F1 Veri Ambarı Şema Dosyası (Race ve Practice Ayrılmış)

CREATE TABLE IF NOT EXISTS circuits (
    circuit_id VARCHAR(50) PRIMARY KEY,
    circuit_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    country VARCHAR(50),
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6)
);

CREATE TABLE IF NOT EXISTS constructors (
    constructor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    nationality VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS drivers (
    driver_id VARCHAR(50) PRIMARY KEY,
    permanent_number INT,
    code VARCHAR(5),
    given_name VARCHAR(100),
    family_name VARCHAR(100),
    date_of_birth DATE,
    nationality VARCHAR(50)
);


-- ===============================
-- 2024 ORTAK TABLOLARI
-- ===============================

CREATE TABLE IF NOT EXISTS races_2024 (
    season INT,
    round INT,
    race_name VARCHAR(100),
    circuit_id VARCHAR(50),
    date DATE,
    time TIME,
    url VARCHAR(255),
    PRIMARY KEY (season, round)
);

CREATE TABLE IF NOT EXISTS sessions_2024 (
    session_key INT PRIMARY KEY,
    session_name VARCHAR(50),
    date_start TIMESTAMP,
    date_end TIMESTAMP,
    gmt_offset TIME,
    session_type VARCHAR(20),
    meeting_key INT,
    location VARCHAR(100),
    country_key INT,
    country_code VARCHAR(5),
    country_name VARCHAR(50),
    circuit_key INT,
    circuit_short_name VARCHAR(100),
    year INT
);

CREATE TABLE IF NOT EXISTS race_results_2024 (
    session_key INT,
    meeting_key INT,
    driver_number INT,
    position INT,
    number_of_laps INT,
    dnf BOOLEAN,
    dns BOOLEAN,
    dsq BOOLEAN,
    duration VARCHAR(50),
    gap_to_leader VARCHAR(50),
    PRIMARY KEY (session_key, driver_number)
);

CREATE TABLE IF NOT EXISTS qualifying_results_2024 (
    season INT,
    round INT,
    driver_id VARCHAR(50),
    constructor_id VARCHAR(50),
    position INT,
    q1 VARCHAR(20),
    q2 VARCHAR(20),
    q3 VARCHAR(20),
    PRIMARY KEY (season, round, driver_id)
);

-- ===============================
-- 2024 RACE TABLOLARI
-- ===============================

CREATE TABLE IF NOT EXISTS pit_stops_race_2024 (
    session_key INT,
    meeting_key INT,
    driver_number INT,
    lap_number INT,
    pit_duration DECIMAL(10, 3),
    lane_duration DECIMAL(10, 3),
    stop_duration DECIMAL(10, 3),
    date TIMESTAMP,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS laps_race_2024 (
    session_key INT,
    driver_number INT,
    lap_number INT,
    lap_duration DECIMAL(10, 3),
    sector_1 DECIMAL(10, 3),
    sector_2 DECIMAL(10, 3),
    sector_3 DECIMAL(10, 3),
    is_pit_out_lap BOOLEAN,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS car_data_race_2024 (
    session_key INT,
    driver_number INT,
    date TIMESTAMP,
    rpm DECIMAL(10, 2),
    speed DECIMAL(10, 2),
    n_gear DECIMAL(10, 2),
    throttle DECIMAL(10, 2),
    brake DECIMAL(10, 2),
    drs DECIMAL(10, 2),
    PRIMARY KEY (session_key, driver_number, date)
);

CREATE TABLE IF NOT EXISTS weather_race_2024 (
    session_key INT,
    date TIMESTAMP,
    air_temperature DECIMAL(5, 2),
    track_temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    pressure DECIMAL(7, 2),
    wind_speed DECIMAL(5, 2),
    wind_direction INT,
    rainfall BOOLEAN,
    PRIMARY KEY (session_key, date)
);

-- ===============================
-- 2024 PRACTICE TABLOLARI
-- ===============================

CREATE TABLE IF NOT EXISTS pit_stops_practice_2024 (
    session_key INT,
    meeting_key INT,
    driver_number INT,
    lap_number INT,
    pit_duration DECIMAL(10, 3),
    lane_duration DECIMAL(10, 3),
    stop_duration DECIMAL(10, 3),
    date TIMESTAMP,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS laps_practice_2024 (
    session_key INT,
    driver_number INT,
    lap_number INT,
    lap_duration DECIMAL(10, 3),
    sector_1 DECIMAL(10, 3),
    sector_2 DECIMAL(10, 3),
    sector_3 DECIMAL(10, 3),
    is_pit_out_lap BOOLEAN,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS car_data_practice_2024 (
    session_key INT,
    driver_number INT,
    date TIMESTAMP,
    rpm DECIMAL(10, 2),
    speed DECIMAL(10, 2),
    n_gear DECIMAL(10, 2),
    throttle DECIMAL(10, 2),
    brake DECIMAL(10, 2),
    drs DECIMAL(10, 2),
    PRIMARY KEY (session_key, driver_number, date)
);

CREATE TABLE IF NOT EXISTS weather_practice_2024 (
    session_key INT,
    date TIMESTAMP,
    air_temperature DECIMAL(5, 2),
    track_temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    pressure DECIMAL(7, 2),
    wind_speed DECIMAL(5, 2),
    wind_direction INT,
    rainfall BOOLEAN,
    PRIMARY KEY (session_key, date)
);


-- ===============================
-- 2025 ORTAK TABLOLARI
-- ===============================

CREATE TABLE IF NOT EXISTS races_2025 (
    season INT,
    round INT,
    race_name VARCHAR(100),
    circuit_id VARCHAR(50),
    date DATE,
    time TIME,
    url VARCHAR(255),
    PRIMARY KEY (season, round)
);

CREATE TABLE IF NOT EXISTS sessions_2025 (
    session_key INT PRIMARY KEY,
    session_name VARCHAR(50),
    date_start TIMESTAMP,
    date_end TIMESTAMP,
    gmt_offset TIME,
    session_type VARCHAR(20),
    meeting_key INT,
    location VARCHAR(100),
    country_key INT,
    country_code VARCHAR(5),
    country_name VARCHAR(50),
    circuit_key INT,
    circuit_short_name VARCHAR(100),
    year INT
);

CREATE TABLE IF NOT EXISTS race_results_2025 (
    session_key INT,
    meeting_key INT,
    driver_number INT,
    position INT,
    number_of_laps INT,
    dnf BOOLEAN,
    dns BOOLEAN,
    dsq BOOLEAN,
    duration VARCHAR(50),
    gap_to_leader VARCHAR(50),
    PRIMARY KEY (session_key, driver_number)
);

CREATE TABLE IF NOT EXISTS qualifying_results_2025 (
    season INT,
    round INT,
    driver_id VARCHAR(50),
    constructor_id VARCHAR(50),
    position INT,
    q1 VARCHAR(20),
    q2 VARCHAR(20),
    q3 VARCHAR(20),
    PRIMARY KEY (season, round, driver_id)
);

-- ===============================
-- 2025 RACE TABLOLARI
-- ===============================

CREATE TABLE IF NOT EXISTS pit_stops_race_2025 (
    session_key INT,
    meeting_key INT,
    driver_number INT,
    lap_number INT,
    pit_duration DECIMAL(10, 3),
    lane_duration DECIMAL(10, 3),
    stop_duration DECIMAL(10, 3),
    date TIMESTAMP,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS laps_race_2025 (
    session_key INT,
    driver_number INT,
    lap_number INT,
    lap_duration DECIMAL(10, 3),
    sector_1 DECIMAL(10, 3),
    sector_2 DECIMAL(10, 3),
    sector_3 DECIMAL(10, 3),
    is_pit_out_lap BOOLEAN,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS car_data_race_2025 (
    session_key INT,
    driver_number INT,
    date TIMESTAMP,
    rpm DECIMAL(10, 2),
    speed DECIMAL(10, 2),
    n_gear DECIMAL(10, 2),
    throttle DECIMAL(10, 2),
    brake DECIMAL(10, 2),
    drs DECIMAL(10, 2),
    PRIMARY KEY (session_key, driver_number, date)
);

CREATE TABLE IF NOT EXISTS weather_race_2025 (
    session_key INT,
    date TIMESTAMP,
    air_temperature DECIMAL(5, 2),
    track_temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    pressure DECIMAL(7, 2),
    wind_speed DECIMAL(5, 2),
    wind_direction INT,
    rainfall BOOLEAN,
    PRIMARY KEY (session_key, date)
);

-- ===============================
-- 2025 PRACTICE TABLOLARI
-- ===============================

CREATE TABLE IF NOT EXISTS pit_stops_practice_2025 (
    session_key INT,
    meeting_key INT,
    driver_number INT,
    lap_number INT,
    pit_duration DECIMAL(10, 3),
    lane_duration DECIMAL(10, 3),
    stop_duration DECIMAL(10, 3),
    date TIMESTAMP,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS laps_practice_2025 (
    session_key INT,
    driver_number INT,
    lap_number INT,
    lap_duration DECIMAL(10, 3),
    sector_1 DECIMAL(10, 3),
    sector_2 DECIMAL(10, 3),
    sector_3 DECIMAL(10, 3),
    is_pit_out_lap BOOLEAN,
    PRIMARY KEY (session_key, driver_number, lap_number)
);

CREATE TABLE IF NOT EXISTS car_data_practice_2025 (
    session_key INT,
    driver_number INT,
    date TIMESTAMP,
    rpm DECIMAL(10, 2),
    speed DECIMAL(10, 2),
    n_gear DECIMAL(10, 2),
    throttle DECIMAL(10, 2),
    brake DECIMAL(10, 2),
    drs DECIMAL(10, 2),
    PRIMARY KEY (session_key, driver_number, date)
);

CREATE TABLE IF NOT EXISTS weather_practice_2025 (
    session_key INT,
    date TIMESTAMP,
    air_temperature DECIMAL(5, 2),
    track_temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    pressure DECIMAL(7, 2),
    wind_speed DECIMAL(5, 2),
    wind_direction INT,
    rainfall BOOLEAN,
    PRIMARY KEY (session_key, date)
);

