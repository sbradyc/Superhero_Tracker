USE SuperTrackerDB;

/* SELECT for Countries Table */
SELECT
    country_name AS Country,
    country_code AS Code
FROM Countries;

/* SELECT for Cities Table */
SELECT
    city_name AS City,
    Countries.country_name AS Country
FROM Cities
INNER JOIN Countries ON Countries.country_id = Cities.country_id;

/* SELECT for Heroes Table (Combining Heroes & HeroPowers) */
SELECT
    pseudonym AS Pseudonym,
    first_name AS FName,
    last_name AS LName,
    Cities.city_name AS City,
    GROUP_CONCAT(Powers.name SEPARATOR ', ') AS Powers
FROM Heroes
INNER JOIN Cities ON Cities.city_id = Heroes.city_id
LEFT JOIN HeroPowers ON HeroPowers.hero_id = Heroes.hero_id
LEFT JOIN Powers ON Powers.power_id = HeroPowers.power_id
GROUP BY Heroes.hero_id, Heroes.pseudonym, Heroes.first_name, Heroes.last_name, Cities.city_name;

/* SELECT for Villains Table (Combining Villains & VillainPowers) */
SELECT
    pseudonym AS Pseudonym,
    first_name AS FName,
    last_name AS LName,
    Cities.city_name AS Location,
    GROUP_CONCAT(Powers.name SEPARATOR ', ') AS Powers
FROM Villains
INNER JOIN Cities ON Cities.city_id = Villains.last_known_loc
LEFT JOIN VillainPowers ON VillainPowers.villain_id = Villains.villain_id
LEFT JOIN Powers ON Powers.power_id = VillainPowers.power_id
GROUP BY Villains.villain_id, Villains.pseudonym, Villains.first_name, Villains.last_name, Cities.city_name;

/* SELECT for Missions Table */
SELECT
    Missions.mission_codename AS CODENAME,
    Heroes.pseudonym AS Hero,
    Villains.pseudonym AS Villain,
    Cities.city_name AS City,
    Missions.description AS Description
FROM Missions
INNER JOIN Heroes ON Heroes.hero_id = Missions.hero_id
INNER JOIN Villains ON Villains.villain_id = Missions.villain_id
INNER JOIN Cities ON Cities.city_id = Missions.city_id;

/* SELECT for Powers Table */
SELECT
    name AS Name,
    description AS Description
FROM Powers;

/* Add a Country */
INSERT INTO Countries (country_name, country_code)
VALUES (:country_name, :country_code);

/* Add a City */
INSERT INTO Cities (city_name, country_id)
VALUES (:city_name, :country_id_from_dropdown);

/* Add a Mission */
INSERT INTO Missions (mission_codename, hero_id, villain_id, city_id)
VALUES (:mission_codename, :hero_id_from_dropdown, :villain_id_from_dropdown, city_id_from_dropdown);

/* Add a Power */
INSERT INTO Powers (name, description)
VALUES (:power_name, :power_description);

/* Add a Hero */
INSERT INTO Heroes (pseudonym, first_name, last_name, city_id)
VALUES (:pseudonym, :first_name, :last_name, :city_id_from_dropdown);

/* Add a Villain */
INSERT INTO Villains (pseudonym, first_name, last_name, last_known_loc)
VALUES (:pseudonym, :first_name, :last_name, :city_id_from_dropdown);

/* Add a Power to a Hero (do this for each selected power AFTER Hero entry has been created) */
INSERT INTO HeroPowers (hero_id, power_id)
VALUES (:hero_id, :power_id);

/* Add a Power to a Villain (do this for each selected power AFTER Villain entry has been created) */
INSERT INTO VillainPowers (villain_id, power_id)
VALUES (:villain_id, :power_id);

/* UPDATE entry for Countries with the : character being used to denote the variables that will
   have data from Python
*/
UPDATE Countries
SET
    country_name = :country_name,
    country_code = :country_code
WHERE country_id = :country_id;

/* UPDATE entry for Cities with the : character being used to denote the variables that will
   have data from Python
*/
UPDATE Cities
SET
    city_name = :city_name,
    country_id = (SELECT country_id FROM Countries WHERE country_name = :country_name)
WHERE city_id = :city_id;

/* UPDATE entry for Heroes with the : character being used to denote the variables that will
   have data from Python. Along with this update you will be able to update the powers of that
   hero as well but the update for those will be done with the inserts and delete queries to
   HeroPowers table on the backend.
*/
UPDATE Heroes
SET
    city_id = (SELECT city_id FROM Cities WHERE city_name = :city_name),
    pseudonym = :pseudonym,
    first_name = :first_name,
    last_name = :last_name
WHERE hero_id = :hero_id;

/* UPDATE entry for Villains with the : character being used to denote the variables that will
   have data from Python. Along with this update you will be able to update the powers of that
   villain as well but the update for those will be done with the inserts and delete queries to
   VillainPowers table on the backend.
*/
UPDATE Villains
SET
    last_known_loc = (SELECT city_id FROM Cities WHERE city_name = :city_name),
    pseudonym = :pseudonym,
    first_name = :first_name,
    last_name = :last_name
WHERE villain_id = :villain_id;

/* UPDATE entry for Missions with the : character being used to denote the variables that will
   have data from Python
*/
UPDATE Missions
SET
    hero_id = (SELECT hero_id FROM Heroes WHERE pseudonym = :pseudonym),
    villain_id = (SELECT villain_id FROM Villains WHERE pseudonym = :pseudonym),
    city_id = (SELECT city_id FROM Cities WHERE city_name = :city_name),
    mission_codename = :codename,
    description = :description
WHERE mission_id = :mission_id;

UPDATE Powers
SET
    name = :name,
    description = :description
WHERE power_id = :power_id;

/* Delete a Country */
DELETE FROM Countries
WHERE country_id = :country_id;

/* Delete a City */
DELETE FROM Cities
WHERE city_id = :city_id;

/* Delete a Mission */
DELETE FROM Missions
WHERE mission_id = :mission_id;

/* Delete a Power */
DELETE FROM Powers
WHERE power_id = :power_id;

/* Delete a Hero */
DELETE FROM Heroes
WHERE hero_id = :hero_id;

/* Delete a Villain */
DELETE FROM Villains
WHERE villain_id = :villain_id;

/* Delete a HeroPower */
DELETE FROM HeroPowers
WHERE hero_power_id = :hero_power_id;

/* Delete a VillainPower */
DELETE FROM VillainPowers
WHERE villain_power_id = :villain_power_id;
