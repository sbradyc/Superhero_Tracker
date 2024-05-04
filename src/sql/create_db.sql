CREATE DATABASE IF NOT EXISTS SuperTrackerDB;
USE SuperTrackerDB;

START TRANSACTION;

/* For import errors */
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

/* The next queries create the tables. */
CREATE OR REPLACE TABLE Countries (
    country_id INT NOT NULL AUTO_INCREMENT,
    country_name VARCHAR(50),
    country_code VARCHAR(3),
    PRIMARY KEY (country_id)
);

CREATE OR REPLACE TABLE Cities (
    city_id INT NOT NULL AUTO_INCREMENT,
    country_id INT NOT NULL,
    city_name VARCHAR(50),
    PRIMARY KEY (city_id),
    FOREIGN KEY (country_id) REFERENCES Countries(country_id) ON DELETE CASCADE
    /* If the country is gone then the city is most likely gone with it */
);

CREATE OR REPLACE TABLE Heroes (
    hero_id INT NOT NULL AUTO_INCREMENT,
    city_id INT NOT NULL,
    pseudonym VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NULL,
    last_name VARCHAR(50) NULL,
    PRIMARY KEY (hero_id),
    FOREIGN KEY (city_id) REFERENCES Cities(city_id)
);

CREATE OR REPLACE TABLE Villains (
    villain_id INT NOT NULL AUTO_INCREMENT,
    last_known_loc INT NOT NULL,
    pseudonym VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NULL,
    last_name VARCHAR(50) NULL,
    PRIMARY KEY (villain_id),
    FOREIGN KEY (last_known_loc) REFERENCES Cities(city_id)
);

CREATE OR REPLACE TABLE Missions (
    mission_id INT NOT NULL AUTO_INCREMENT,
    hero_id INT NOT NULL,
    villain_id INT NOT NULL,
    city_id INT NOT NULL,
    mission_codename VARCHAR(20) NOT NULL,
    description TEXT(1000) NOT NULL,
    PRIMARY KEY (mission_id),
    FOREIGN KEY (hero_id) REFERENCES Heroes(hero_id),
    FOREIGN KEY (villain_id) REFERENCES Villains(villain_id) ON DELETE CASCADE,
    FOREIGN KEY (city_id) REFERENCES Cities(city_id) ON DELETE CASCADE
    /* If the villain is deleted, delete the mission too since there is no more danger. */
);

CREATE OR REPLACE TABLE Powers (
    power_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NULL,
    description TEXT(1000) NULL,
    PRIMARY KEY (power_id)
);

CREATE OR REPLACE TABLE HeroPowers (
    hero_power_id INT NOT NULL AUTO_INCREMENT,
    hero_id INT NOT NULL,
    power_id INT NOT NULL,
    PRIMARY KEY (hero_power_id),
    FOREIGN KEY (hero_id) REFERENCES Heroes(hero_id) ON DELETE CASCADE, /* If the hero is deleted, delete the entry associated too. */
    FOREIGN KEY (power_id) REFERENCES Powers(power_id) ON DELETE CASCADE
);

CREATE OR REPLACE TABLE VillainPowers (
    villain_power_id INT NOT NULL AUTO_INCREMENT,
    villain_id INT NOT NULL,
    power_id INT NOT NULL,
    PRIMARY KEY (villain_power_id),
    FOREIGN KEY (villain_id) REFERENCES Villains(villain_id) ON DELETE CASCADE, /* If the villain is deleted, delete the entry associated too. */
    FOREIGN KEY (power_id) REFERENCES Powers(power_id) ON DELETE CASCADE
);

SHOW TABLES;

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
