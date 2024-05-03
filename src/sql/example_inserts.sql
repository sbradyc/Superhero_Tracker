USE SuperTrackerDB;

/* Insert example data into tables */
INSERT INTO Countries (country_name, country_code)
VALUES
('United States of America', 'USA'),
('United Kingdom', 'GB'),
('Wakanda', 'WKD');

INSERT INTO Cities (country_id, city_name)
VALUES
(1, 'New York'),
(2, 'London'),
(3, 'Birnin Zana'),
(1, 'Chicago');  /* Along with the first row, shows that one Country can have multiple Cities */

INSERT INTO Heroes (city_id, pseudonym, first_name, last_name)
VALUES
(1, 'Spider Man', 'Peter', 'Parker'),
(2, 'Union Jack', 'Joseph', 'Chapman'),
(3, 'Black Panther', 'T''Challa', NULL),
(1, 'Power Man', 'Luke', 'Cage');  /* Along with the first row, shows that one City can have multiple Heroes */

INSERT INTO Villains (last_known_loc, pseudonym, first_name, last_name)
VALUES
(1, 'Doctor Octopus', 'Otto', 'Octavius'),
(2, 'Mr. Sinister', 'Nathaniel', 'Essex'),
(3, 'Killmonger', 'Erik', 'Killmonger'),
(1, 'Kingpin', 'Wilson', 'Fisk');  /* Along with the first row, shows that one City can have multiple Villains*/

INSERT INTO Missions (hero_id, villain_id, mission_codename, description)
VALUES
(1, 1, 'Ink Pen', 'Doctor Octopus is on a rampage through the city stealing industrial electrical fuses.'),
(2, 2, 'Kulling', 'Mr. Sinister has been attacking various underground ruins and stealing precious magical artifacts to give to Apocalypse.'),
(3, 3, 'Hunting Season', 'Killmonger is preparing an attack on Wakanda by stealing military technology from SHIELD.'),
(1, 2, 'Red Wolf', 'One of Mr. Sinister''s clones has been seen breaking into numerous research labs throughout the city.'); /* Along with the first and second rows, shows that one City can have multiple Missions, one Hero can have multiple Missions, and one Villain can be involved in multiple Missions */

INSERT INTO Powers (name, description)
VALUES
('Super Strength', 'Strength beyond what is physically possible for a human.'),
('Enhanced Agility', 'Agility beyond what is physically possible for a human.'),
('Cloning', 'The ability to create duplicates of oneself.');

INSERT INTO HeroPowers (power_id, hero_id)
VALUES
(1, 1),
(2, 1),  /* Along with the first row, shows that one Hero can have multiple Powers */
(2, 2),
(2, 3);  /* Along with the second and third rows, shows that one Power can be possessed by multiple heroes */

INSERT INTO VillainPowers (power_id, villain_id)
VALUES
(1, 1),
(3, 2),
(1, 3),  /* Along with the first row, shows that one Power can be possessed by multiple Villains */
(2, 3);  /* Along with the third row, shows that one Villain can have multiple Powers */

INSERT INTO MissionCities (mission_id, city_id)
VALUES
(4, 1), /* Show that a mission can span multiple cities */
(4, 2),
(1, 1), /* Show that a city can have multipe missions in it */
(2, 1);

/* Display table contents */
SELECT * FROM Countries;
SELECT * FROM Cities;
SELECT * FROM Heroes;
SELECT * FROM Villains;
SELECT * FROM Missions;
SELECT * FROM Powers;
SELECT * FROM HeroPowers;
SELECT * FROM VillainPowers;
SELECT * FROM MissionCities;
