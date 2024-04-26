/* Insert example data into tables */
INSERT INTO Countries (country_name, country_code)
VALUES
('United States of America', 'USA'),
('United Kingdom', 'GB'),
('Wakanda', 'WKD');

INSERT INTO Cities (country_id, city_name)
VALUES
(0, 'New York'),
(1, 'London'),
(2, 'Birnin Zana');

INSERT INTO Heroes (city_id, pseudonym, first_name, last_name)
VALUES
(0, 'Spider Man', 'Peter', 'Parker'),
(1, 'Union Jack', 'Joseph', 'Chapman'),
(2, 'Black Panther', 'T''Challa', NULL);

INSERT INTO Villains (last_known_loc, pseudonym, first_name, last_name)
VALUES
(0, 'Doctor Octopus', 'Otto', 'Octavius'),
(1, 'Mr. Sinister', 'Nathaniel', 'Essex'),
(2, 'Killmonger', 'Erik', 'Killmonger');

INSERT INTO Missions (city_id, hero_id, villain_id, mission_codename, description)
VALUES
(0, 0, 0, 'Ink Pen', 'Doctor Octopus is on a rampage through the city stealing industrial electrical fuses.'),
(1, 1, 1, 'Kulling', 'Mr. Sinister has been attacking various underground ruins and stealing precious magical artifacts to give to Apocalypse.'),
(2, 2, 2, 'Hunting Season', 'Killmonger is preparing an attack on Wakanda by stealing military technology from SHIELD.');

INSERT INTO Powers (name, description)
VALUES
('Super Strength', 'Strength beyond what is physically possible for a human.'),
('Enhanced Agility', 'Agility beyond what is physically possible for a human.'),
('Cloning', 'The ability to create duplicates of oneself.');

INSERT INTO HeroPowers (power_id, hero_id)
VALUES
(0, 0),
(1, 0),
(1, 1),
(1, 2);

INSERT INTO VillainPowers (power_id, villain_id)
VALUES
(0, 0),
(2, 1),
(0, 2);
