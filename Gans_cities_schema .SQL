-- Drop the database if it already exists
DROP DATABASE IF EXISTS gans ;

-- Create the database
CREATE DATABASE gans;

-- Use the database
USE gans;

-- Create the 'cities' table

CREATE TABLE cities (
    city_id INT AUTO_INCREMENT, -- Automatically generated ID for each author
    city_name VARCHAR(100) NOT NULL, -- Name of the author
    country_name VARCHAR (100) NOT NULL,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6)
    PRIMARY KEY (city_id) -- Primary key to uniquely identify each author
);

-- Create the 'weather_forecast' table
CREATE TABLE weather_forecast (
    forecast_id INT PRIMARY KEY AUTO_INCREMENT,
    city_id INT NOT NULL,
    forecast_time DATETIME NOT NULL,
    temperature DECIMAL(5, 2),
    feels_like DECIMAL (5, 2),
    humidity INT,
    outlook VARCHAR(100),
    wind_speed_m_s DECIMAL (5, 2),
    rain_prob DECIMAL(5, 2),
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);


CREATE TABLE airports(
    icao CHAR(4) PRIMARY KEY,
    `name` VARCHAR(80),
    `active` BOOL DEFAULT 1,
    city_id INT,
    FOREIGN KEY (city_id) REFERENCES cities(city_id)
);

CREATE TABLE flights(
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    arrive_icao CHAR(4),
    depart_icao CHAR(4),
    depart_airport VARCHAR(80),
    depart_country CHAR(2),
    arrive_time_scheduled DATETIME,
    arrive_time_revised DATETIME,
    flight_number VARCHAR(32),
    aircraft VARCHAR(128),
    FOREIGN KEY (arrive_icao) REFERENCES airports(icao)
);

# run after populating airports
UPDATE airports
SET `active` = 0
WHERE icao = 'EDDT';
