-- This file contains all the code required to create & seed the database tables.


-- Switches to the plants database.

USE plants;


-- Drop all Tables

DROP TABLE IF EXISTS measurement;
DROP TABLE IF EXISTS botanist_assignment;
DROP TABLE IF EXISTS plant_error;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS origin;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS error;
DROP TABLE IF EXISTS botanist;


-- Create Tables

CREATE TABLE "botanist" (
    botanist_id SMALLINT IDENTITY(1,1),
    botanist_name VARCHAR(50) NOT NULL,
    botanist_email VARCHAR(40) NOT NULL UNIQUE,
    botanist_phone VARCHAR(25) NOT NULL UNIQUE,
    PRIMARY KEY (botanist_id)
);
GO

CREATE TABLE "error" (
    error_id SMALLINT IDENTITY(1,1),
    error_name VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (error_id)
);
GO

CREATE TABLE "country" (
    country_id SMALLINT IDENTITY(1,1),
    country_name VARCHAR(60) NOT NULL UNIQUE,
    PRIMARY KEY (country_id)
);
GO


-- `city_name` is UNIQUE to making seeding the data easier.
-- If this needs to change, the seeding script will as well.
CREATE TABLE "city" (
    city_id SMALLINT IDENTITY(1,1),
    city_name VARCHAR(200) NOT NULL UNIQUE,
    country_id SMALLINT NOT NULL,
    PRIMARY KEY (city_id),
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);
GO

CREATE TABLE "origin" (
    origin_id SMALLINT IDENTITY(1,1),
    origin_latitude FLOAT NOT NULL,
    origin_longitude FLOAT NOT NULL,
    city_id SMALLINT NOT NULL,
    PRIMARY KEY (origin_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);
GO

CREATE TABLE "plant" (
    plant_id SMALLINT IDENTITY(1,1),
    botanist_id SMALLINT NOT NULL,
    origin_id SMALLINT NOT NULL,
    plant_name VARCHAR(100) NOT NULL,
    scientific_name VARCHAR(100),
    PRIMARY KEY (plant_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    FOREIGN KEY (origin_id) REFERENCES origin(origin_id)
);
GO

CREATE TABLE "plant_error" (
    plant_error_id SMALLINT IDENTITY(1,1),
    plant_id SMALLINT NOT NULL,
    error_id SMALLINT NOT NULL,
    received_at DATETIME NOT NULL,
    PRIMARY KEY (plant_error_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);
GO

CREATE TABLE "botanist_assignment" (
    assignment_id SMALLINT IDENTITY(1,1),
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (botanist_id) REFERENCES botanist(botanist_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);
GO

CREATE TABLE "measurement" (
    measurement_id SMALLINT IDENTITY(1,1),
    plant_id SMALLINT NOT NULL,
    temperature FLOAT NOT NULL,
    soil_moisture FLOAT NOT NULL,
    last_watered DATETIME NOT NULL,
    [at] DATETIME NOT NULL,
    PRIMARY KEY (measurement_id),
    FOREIGN KEY (plant_id) REFERENCES plant(plant_id)
);
GO
