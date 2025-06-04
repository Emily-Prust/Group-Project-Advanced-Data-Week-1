-- This file contains all the code required to create & seed the database tables.

-- Drop all Tables

DROP TABLE IF EXISTS measurement;
DROP TABLE IF EXISTS botanist;
DROP TABLE IF EXISTS botanist_assignment;
DROP TABLE IF EXISTS error;
DROP TABLE IF EXISTS plant_error;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS origin;
DROP TABLE IF EXISTS plant;


-- Create Tables

CREATE TABLE "measurement" (
    measurement_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    temperature FLOAT NOT NULL,
    soil_moisture FLOAT NOT NULL,
    last_watered TIMESTAMP NOT NULL,
    [at] TIMESTAMP NOT NULL,
    PRIMARY KEY (measurement_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE "botanist" (
    botanist_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    botanist_name VARCHAR(50) NOT NULL,
    botanist_email VARCHAR(40) NOT NULL UNIQUE,
    botanist_phone VARCHAR(11) NOT NULL UNIQUE,
    PRIMARY KEY (botanist_id)
);

CREATE TABLE "botanist_assignment" (
    assignment_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE "error" (
    error_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    error_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (error_id)
);

CREATE TABLE "plant_error" (
    plant_error_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    plant_id SMALLINT NOT NULL,
    error_id SMALLINT NOT NULL,
    received_at TIMESTAMP NOT NULL,
    PRIMARY KEY (plant_error_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);

CREATE TABLE "country" (
    country_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    country_name VARCHAR(60) NOT NULL,
    PRIMARY KEY (country_id)
);

CREATE TABLE "city" (
    city_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    city_name VARCHAR(200) NOT NULL,
    country_id SMALLINT NOT NULL,
    PRIMARY KEY (city_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE TABLE "origin" (
    origin_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    origin_latitude FLOAT NOT NULL,
    origin_longitude FLOAT NOT NULL,
    city_id SMALLINT NOT NULL,
    PRIMARY KEY (origin_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);

CREATE TABLE "plant" (
    plant_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    botanist_id SMALLINT NOT NULL,
    origin_id SMALLINT NOT NULL,
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    FOREIGN KEY (origin_id) REFERENCES origin(origin_id)
);

-- Seed data

INSERT INTO botanist (botanist_name, botanist_email, botanist_phone) VALUES
('botanist_name_1', 'botanist_email_1', 'botanist_phone_number_1'),
('botanist_name_2', 'botanist_email_2', 'botanist_phone_number_2');

INSERT INTO origin (origin_latitude, origin_longitude, city_id) VALUES
(0.0, 0.0, 'example_city_id_1'),
(0.0, 0.0, 'example_city_id_2');


INSERT INTO city (city_name, country_id) VALUES
('city_1', 'country_id_1'),
('city_2', 'country_id_2');


INSERT INTO country (country_name) VALUES
('country_1'),
('country_2');