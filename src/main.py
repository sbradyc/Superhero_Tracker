#!/usr/bin/env python

from colorama import Fore
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
import query_helper
import time

app = Flask(__name__)
CONFIG = {
    "host":     "classmysql.engr.oregonstate.edu",
    "user":     "username",
    "password": "password",
    "database": "username"
}
conn = mysql.connector.connect(**CONFIG)
cursor = conn.cursor(dictionary=True)


def connect_to_db():
    global conn
    global cursor

    # try to connect to the database, but give up after 5 attempts
    for _ in range(5):
        try:
            conn = mysql.connector.connect(**CONFIG)
            cursor = conn.cursor(dictionary=True)
            print("Connected to database")
            return
        except:
            print("Failed to connect to database. Trying again")

    time.sleep(1)


def query_fetch(query: str, params: tuple = ()):
    # try to execute the query, but give up after 5 attempts
    for _ in range(5):
        try:
            cursor.execute(query, params)
            data = cursor.fetchall()
            print("Fetched data")
            return data
        except:
            connect_to_db()
            print("Failed to fetch data, trying again")

        time.sleep(1)

    # try one last time
    cursor.execute(query, params)
    data = cursor.fetchall()
    print("Failed to fetch data")
    return data


def query_commit(query: str, params: tuple = ()) -> None:
    # try to execute the query, but give up after 5 attempts
    for _ in range(5):
        try:
            cursor.execute(query, params)
            conn.commit()
            print("Committed changes")
            return
        except:
            connect_to_db()
            print("Failed to commit changes, trying again")

        time.sleep(2)

    # try one last time
    cursor.execute(query, params)
    conn.commit()
    print("Failed to commit changes")


try:
    @app.route("/")
    def main():
        message = "Welcome Shield Agent"
        return render_template("index.html",
                               message=message)

    @app.route("/cities")
    def cities():
        query: str = """
        SELECT
            Cities.city_id AS id,
            Cities.city_name AS city,
            Countries.country_name AS country
        FROM Cities
        INNER JOIN Countries ON Countries.country_id = Cities.country_id;
        """
        data = query_fetch(query)
        return render_template("cities.html", data=data)

    @app.route("/countries")
    def countries():
        query: str = """
        SELECT
            Countries.country_id AS id,
            Countries.country_name AS country,
            Countries.country_code AS code
        FROM Countries;
        """
        data = query_fetch(query)
        return render_template("countries.html", data=data)

    @app.route("/heroes")
    def heroes():
        query: str = """
        SELECT
            Heroes.hero_id AS id,
            Heroes.pseudonym,
            Heroes.first_name,
            Heroes.last_name,
            Cities.city_name AS city,
            GROUP_CONCAT(Powers.name SEPARATOR ', ') AS powers
        FROM Heroes
        LEFT JOIN Cities ON Cities.city_id = Heroes.city_id
        INNER JOIN HeroPowers ON HeroPowers.hero_id = Heroes.hero_id
        INNER JOIN Powers ON Powers.power_id = HeroPowers.power_id
        GROUP BY Heroes.hero_id, Heroes.pseudonym, Heroes.first_name,
            Heroes.last_name, Cities.city_name
        ORDER BY Heroes.pseudonym;
        """
        data = query_fetch(query)
        for row in data:
            row["powers"] = row["powers"].split(", ")

        return render_template(
            "people.html",
            data=data,
            people_type_singular="hero",
            people_type_plural="heroes",
            city_type="City"
        )

    @app.route("/missions")
    def missions():
        query: str = """
        SELECT
            Missions.mission_id AS id,
            Missions.mission_codename AS mission_name,
            Heroes.pseudonym AS hero_name,
            Villains.pseudonym AS villain_name,
            Cities.city_name AS city,
            Missions.description AS description
        FROM Missions
        LEFT JOIN Heroes ON Heroes.hero_id = Missions.hero_id
        LEFT JOIN Villains ON Villains.villain_id = Missions.villain_id
        INNER JOIN Cities ON Cities.city_id = Missions.city_id
        ORDER BY Missions.mission_codename;
        """
        data = query_fetch(query)
        return render_template("missions.html", data=data)

    @app.route("/powers")
    def powers():
        query: str = """
        SELECT
            power_id AS id,
            name,
            description
        FROM Powers;
        """
        data = query_fetch(query)
        return render_template("powers.html",
                               data=data)

    @app.route("/villains")
    def villains():
        query: str = """
        SELECT
            Villains.villain_id AS id,
            Villains.pseudonym,
            Villains.first_name,
            Villains.last_name,
            Cities.city_name AS city,
            GROUP_CONCAT(Powers.name SEPARATOR ', ') AS powers
        FROM Villains
        LEFT JOIN Cities ON Cities.city_id = Villains.last_known_loc
        INNER JOIN VillainPowers ON VillainPowers.villain_id = Villains.villain_id
        INNER JOIN Powers ON Powers.power_id = VillainPowers.power_id
        GROUP BY Villains.villain_id, Villains.pseudonym, Villains.first_name, Villains.last_name, Cities.city_name;
        """
        data = query_fetch(query)
        for row in data:
            row["powers"] = row["powers"].split(", ")

        return render_template(
            "people.html",
            data=data,
            people_type_singular="villain",
            people_type_plural="villains",
            city_type="Last Known Location"
        )

    @app.route("/cities-add", methods=['GET', 'POST'])
    def cities_add():
        if request.method == "GET":
            query = """
            SELECT
                country_id,
                country_name
            FROM Countries
            """
            countries = query_fetch(query)
            return render_template("cities-add.html",
                                   countries=countries)
        else:
            city_name: str = request.form.get("city_name")
            country_id: str = request.form.get("country_id")
            if not city_name:
                return render_template("cities-add.html",
                                       message=query_helper.NO_CITY_NAME)
            query: str = """
            INSERT INTO Cities (city_name, country_id)
            VALUES (%s, %s);
            """
            params = (city_name, country_id)
            query_commit(query, params)
            return redirect(url_for("cities"))

    @app.route("/countries-add", methods=['GET', 'POST'])
    def countries_add():
        if request.method == "GET":
            return render_template("countries-add.html")
        else:
            country_name: str = request.form.get("country_name")
            country_code: str = request.form.get("country_code")
            query: str = """
            INSERT INTO Countries (country_name, country_code)
            VALUES (%s, %s);
            """
            params = (country_name, country_code)
            query_commit(query, params)
            return redirect(url_for("countries"))

    @app.route("/heroes-add", methods=['GET', 'POST'])
    def heroes_add():
        if request.method == "GET":
            # get cities
            cities = query_helper.get_cities_data(cursor)

            # get powers
            query = """
            SELECT
                power_id,
                name
            FROM Powers
            ORDER BY name ASC;
            """
            powers = query_fetch(query)

            return render_template(
                "people-add.html",
                people_type_singular="hero",
                people_type_plural="heroes",
                cities=cities,
                city_type="city",
                powers=powers
            )
        else:
            # create Hero entry
            # NULLED items have the value of an empty string,
            #   and must be set to None for MySQL to recognize them as NULL
            pseudonym = request.form.get("pseudonym")
            first_name = request.form.get("first_name")
            if first_name == "":
                first_name = None
            last_name = request.form.get("last_name")
            if last_name == "":
                last_name = None
            city_id = request.form.get("city_id")
            if city_id == "":
                city_id = None
            query = """
            INSERT INTO Heroes (
                pseudonym,
                first_name,
                last_name,
                city_id
            )
            VALUES (%s, %s, %s, %s);
            """
            params = (pseudonym, first_name, last_name, city_id)
            query_commit(query, params)

            # create HeroPower entries
            query = "SELECT LAST_INSERT_ID();"
            hero_id = query_fetch(query)[0]["LAST_INSERT_ID()"]
            for name, _ in request.form.items():
                prefix = name[:9]
                if prefix == "power_id:":  # if power checkbox was selected
                    power_id = name[9:]
                    query = """
                    INSERT INTO HeroPowers (
                        hero_id,
                        power_id
                    )
                    VALUES (%s, %s);
                    """
                    params = (hero_id, power_id)
                    query_commit(query, params)

            return redirect(url_for("heroes"))

    @app.route("/missions-add", methods=['GET', 'POST'])
    def missions_add():
        if request.method == "GET":
            heroes: list[dict] = query_helper.get_heroes_data(cursor)
            villains: list[dict] = query_helper.get_villains_data(cursor)
            cities: list[dict] = query_helper.get_cities_data(cursor)
            return render_template("missions-add.html",
                                   heroes=heroes,
                                   villains=villains,
                                   cities=cities)
        else:
            # create Missions entry
            # NULLED items have the value of an empty string,
            #   and must be set to None for MySQL to recognize them as NULL
            mission_codename: str = request.form.get("mission_name")
            hero_id: str = request.form.get("hero_id")
            if hero_id == "":
                hero_id = None
            villain_id: str = request.form.get("villain_id")
            if villain_id == "":
                villain_id = None
            city_id: int = int(request.form.get("city_id"))
            description: str = request.form.get("description")
            query: str = """
            INSERT INTO Missions (
                mission_codename,
                hero_id,
                villain_id,
                city_id,
                description
            )
            VALUES (%s, %s, %s, %s, %s);
            """
            params = (mission_codename, hero_id, villain_id, city_id, description)
            query_commit(query, params)
            return redirect(url_for("missions"))

    @app.route("/powers-add", methods=['GET', 'POST'])
    def powers_add():
        if request.method == "GET":
            return render_template("powers-add.html")
        else:
            power_name = request.form.get("name")
            power_description = request.form.get("description")
            query = """
            INSERT INTO Powers (
                name,
                description)
            VALUES (%s, %s);
            """
            params = (power_name, power_description)
            query_commit(query, params)
            return redirect(url_for("powers"))

    @app.route("/villains-add", methods=['GET', 'POST'])
    def villains_add():
        if request.method == "GET":
            # get cities
            cities = query_helper.get_cities_data(cursor)

            # get powers
            query = """
            SELECT
                power_id,
                name
            FROM Powers
            ORDER BY name ASC;
            """
            powers = query_fetch(query)

            return render_template(
                "people-add.html",
                people_type_singular="villain",
                people_type_plural="villains",
                cities=cities,
                city_type="last known location",
                powers=powers
            )
        else:
            # create Villain entry
            # NULLED items have the value of an empty string,
            #   and must be set to None for MySQL to recognize them as NULL
            pseudonym = request.form.get("pseudonym")
            first_name = request.form.get("first_name")
            if first_name == "":
                first_name = None
            last_name = request.form.get("last_name")
            if last_name == "":
                last_name = None
            last_known_loc = request.form.get("city_id")
            if last_known_loc == "":
                last_known_loc = None
            query = """
            INSERT INTO Villains (
                pseudonym,
                first_name,
                last_name,
                last_known_loc
            )
            VALUES (%s, %s, %s, %s);
            """
            params = (pseudonym, first_name, last_name, last_known_loc)
            query_commit(query, params)

            # create VillainPower entries
            query = "SELECT LAST_INSERT_ID();"
            villain_id = query_fetch(query)[0]["LAST_INSERT_ID()"]
            for name, _ in request.form.items():
                prefix = name[:9]
                if prefix == "power_id:":  # if power checkbox was selected
                    power_id = name[9:]
                    query = f"""
                    INSERT INTO VillainPowers (
                        villain_id,
                        power_id
                    )
                    VALUES (%s, %s);
                    """
                    params = (villain_id, power_id)
                    query_commit(query, params)

            return redirect(url_for("villains"))

    @app.route("/cities-update/<id>", methods=['GET', 'POST'])
    def cities_update(id: int):
        if request.method == "GET":
            defaults: dict = query_helper.get_city(cursor, id)
            query = """
            SELECT
                country_id,
                country_name
            FROM Countries
            """
            countries = query_fetch(query)
            print(defaults)
            return render_template("cities-update.html",
                                   defaults=defaults,
                                   countries=countries)
        else:
            city_name: str = request.form.get("city_name")
            country_id: str = request.form.get("country_id")
            if not city_name:
                return render_template("cities-add.html",
                                       message=query_helper.NO_CITY_NAME)
            if country_id == -1:
                return render_template("cities-update.html",
                                       message=query_helper.NO_COUNTRY_NAME,
                                       defaults=defaults,
                                       countries=countries)
            query: str = """
            UPDATE Cities
            SET
                city_name = %s,
                country_id = %s
            WHERE city_id = %s;
            """
            params = (city_name, country_id, id)
            query_commit(query, params)
            return redirect(url_for("cities"))

    @app.route("/countries-update/<id>", methods=['GET', 'POST'])
    def countries_update(id: int):
        if request.method == "GET":
            country: dict = query_helper.get_country(cursor, id)
            return render_template("countries-update.html",
                                   country=country)
        else:
            country_name: str = request.form.get("country_name")
            country_code: str = request.form.get("country_code")
            query: str = """
            UPDATE Countries
            SET
                country_name = %s,
                country_code = %s
            WHERE country_id = %s;
            """
            params = (country_name, country_code, id)
            query_commit(query, params)
            return redirect(url_for("countries"))

    @app.route("/heroes-update/<id>", methods=['GET', 'POST'])
    def heroes_update(id: int):
        if request.method == "GET":
            # get hero
            query = f"""
            SELECT
                hero_id AS id,
                pseudonym,
                first_name,
                last_name,
                city_id
            FROM Heroes
            WHERE hero_id = {id};
            """
            hero = query_fetch(query)[0]
            if hero["first_name"] is None:
                hero["first_name"] = ""
            if hero["last_name"] is None:
                hero["last_name"] = ""

            # get IDs of hero's powers
            query = f"""
            SELECT power_id
            FROM HeroPowers
            WHERE hero_id = {id};
            """
            hero_powers = query_fetch(query)
            hero["power_ids"] = [item["power_id"] for item in hero_powers]

            # get cities
            cities = query_helper.get_cities_data(cursor)

            # get all powers
            query = """
            SELECT
                power_id,
                name
            FROM Powers
            ORDER BY name ASC;
            """
            powers = query_fetch(query)

            return render_template(
                "people-update.html",
                person=hero,
                person_type_singular="hero",
                person_type_plural="heroes",
                cities=cities,
                city_type="city",
                powers=powers
            )
        else:
            # update Heroes table
            # NULLED items have the value of an empty string,
            #   and must be set to None for MySQL to recognize them as NULL
            pseudonym = request.form.get("pseudonym")
            first_name = request.form.get("first_name")
            if first_name == "":
                first_name = None
            last_name = request.form.get("last_name")
            if last_name == "":
                last_name = None
            city_id = request.form.get("city_id")
            if city_id == "":
                city_id = None
            query = """
            UPDATE Heroes
            SET
                pseudonym = %s,
                first_name = %s,
                last_name = %s,
                city_id = %s
            WHERE hero_id = %s;
            """
            params = (pseudonym, first_name, last_name, city_id, id)
            query_commit(query, params)

            # now update HeroPowers entries
            # get list of powers that Hero already has
            query = """
            SELECT power_id
            FROM HeroPowers
            WHERE hero_id = %s;
            """
            params = (id,)
            old_powers = [item["power_id"] for item in query_fetch(query, params)]

            # get list of user-selected powers (may include powers that Hero already has)
            new_powers = []
            for name, _ in request.form.items():
                prefix = name[:9]
                if prefix == "power_id:":  # if power checkbox was selected
                    power_id = int(name[9:])
                    new_powers.append(power_id)

            # get list of powers that were deselected
            deselected_powers = [power_id for power_id in old_powers if power_id not in new_powers]

            # now remove any pre-existing powers from new powers
            new_powers = [power_id for power_id in new_powers if power_id not in old_powers]

            # replace power_id of any deslected HeroPowers with newly selected one,
            # or insert new HeroPower if no deselected ones remain
            for new_power_id in new_powers:
                if len(deselected_powers) > 0:
                    query = """
                    UPDATE HeroPowers
                    SET
                        power_id = %s
                    WHERE hero_id = %s AND power_id = %s;
                    """
                    params = (new_power_id, id, deselected_powers.pop())  # pop power_id to indicate that it has been replaced
                else:
                    query = """
                    INSERT INTO HeroPowers (
                        hero_id,
                        power_id
                    )
                    VALUES (
                        %s,
                        %s
                    );
                    """
                    params = (id, new_power_id)
                query_commit(query, params)

            # delete remaining deselected HeroPowers
            for deselected_power_id in deselected_powers:
                query = """
                DELETE FROM HeroPowers
                WHERE hero_id = %s AND power_id = %s;
                """
                params = (id, deselected_power_id)
                query_commit(query, params)

            return redirect(url_for("heroes"))

    @app.route("/missions-update/<id>", methods=['GET', 'POST'])
    def missions_update(id: int):
        if request.method == "GET":
            mission = query_helper.get_mission(cursor, id)
            heroes: list[dict] = query_helper.get_heroes_data(cursor)
            villains: list[dict] = query_helper.get_villains_data(cursor)
            cities: list[dict] = query_helper.get_cities_data(cursor)
            return render_template("missions-update.html",
                                   defaults=mission,
                                   heroes=heroes,
                                   villains=villains,
                                   cities=cities)
        else:
            # update Missions table
            # NULLED items have the value of an empty string,
            #   and must be set to None for MySQL to recognize them as NULL
            mission_codename: str = request.form.get("mission_name")
            hero_id: str = request.form.get("hero_id")
            if hero_id == "":
                hero_id = None
            villain_id: str = request.form.get("villain_id")
            if villain_id == "":
                villain_id = None
            city_id: int = int(request.form.get("city_id"))
            description: str = request.form.get("description")
            query: str = """
            UPDATE Missions
            SET
                hero_id = %s,
                villain_id = %s,
                city_id = %s,
                mission_codename = %s,
                description = %s
            WHERE mission_id = %s;
            """
            params = (hero_id, villain_id, city_id, mission_codename, description, id)
            query_commit(query, params)
            return redirect(url_for("missions"))

    @app.route("/powers-update/<id>", methods=['GET', 'POST'])
    def powers_update(id: int):
        if request.method == "GET":
            query = f"""
            SELECT
                power_id,
                name,
                description
            FROM Powers
            WHERE power_id = {id};
            """
            power = query_fetch(query)[0]

            return render_template(
                "powers-update.html",
                power=power
            )
        else:
            power_name = request.form.get("name")
            power_description = request.form.get("description")
            query = """
            UPDATE Powers
            SET
                name = %s,
                description = %s
            WHERE power_id = %s;
            """
            params = (power_name, power_description, id)
            query_commit(query, params)

            return redirect(url_for("powers"))

    @app.route("/villains-update/<id>", methods=['GET', 'POST'])
    def villains_update(id: int):
        if request.method == "GET":
            # get villain
            query = f"""
            SELECT
                villain_id AS id,
                pseudonym,
                first_name,
                last_name,
                last_known_loc AS city_id
            FROM Villains
            WHERE villain_id = {id};
            """
            villain = query_fetch(query)[0]
            if villain["first_name"] is None:
                villain["first_name"] = ""
            if villain["last_name"] is None:
                villain["last_name"] = ""

            # get IDs of villain's powers
            query = f"""
            SELECT power_id
            FROM VillainPowers
            WHERE villain_id = {id};
            """
            villain_powers = query_fetch(query)
            villain["power_ids"] = [item["power_id"] for item in villain_powers]

            # get cities
            cities = query_helper.get_cities_data(cursor)

            # get all powers
            query = """
            SELECT
                power_id,
                name
            FROM Powers
            ORDER BY name ASC;
            """
            powers = query_fetch(query)

            return render_template(
                "people-update.html",
                person=villain,
                person_type_singular="villain",
                person_type_plural="villains",
                cities=cities,
                city_type="city",
                powers=powers
            )
        else:
            # update Villains table
            pseudonym = request.form.get("pseudonym")
            first_name = request.form.get("first_name")
            if first_name == "":
                first_name = None
            last_name = request.form.get("last_name")
            if last_name == "":
                last_name = None
            last_known_loc = request.form.get("city_id")
            if last_known_loc == "":
                last_known_loc = None
            query = """
            UPDATE Villains
            SET
                pseudonym = %s,
                first_name = %s,
                last_name = %s,
                last_known_loc = %s
            WHERE villain_id = %s;
            """
            params = (pseudonym, first_name, last_name, last_known_loc, id)
            query_commit(query, params)

            # now update VillainPowers entries
            # get list of powers that Villain already has
            query = """
            SELECT power_id
            FROM VillainPowers
            WHERE villain_id = %s;
            """
            params = (id,)
            old_powers = [item["power_id"] for item in query_fetch(query, params)]

            # get list of user-selected powers (may include powers that Villain already has)
            new_powers = []
            for name, _ in request.form.items():
                prefix = name[:9]
                if prefix == "power_id:":  # if power checkbox was selected
                    power_id = int(name[9:])
                    new_powers.append(power_id)

            # get list of powers that were deselected
            deselected_powers = [power_id for power_id in old_powers if power_id not in new_powers]

            # now remove any pre-existing powers from new powers
            new_powers = [power_id for power_id in new_powers if power_id not in old_powers]

            # replace power_id of any deslected VillainPowers with newly selected one,
            # or insert new VillainPower if no deselected ones remain
            for new_power_id in new_powers:
                if len(deselected_powers) > 0:
                    query = """
                    UPDATE VillainPowers
                    SET
                        power_id = %s
                    WHERE villain_id = %s AND power_id = %s;
                    """
                    params = (new_power_id, id, deselected_powers.pop())  # pop power_id to indicate that it has been replaced
                else:
                    query = """
                    INSERT INTO VillainPowers (
                        villain_id,
                        power_id
                    )
                    VALUES (
                        %s,
                        %s
                    );
                    """
                    params = (id, new_power_id)
                query_commit(query, params)

            # delete remaining deselected VillainPowers
            for deselected_power_id in deselected_powers:
                query = """
                DELETE FROM VillainPowers
                WHERE villain_id = %s AND power_id = %s;
                """
                params = (id, deselected_power_id)
                query_commit(query, params)

            return redirect(url_for("villains"))

    """
    The following routes will do a delete query and then reload
    the page for the user
    """
    @app.route("/cities-delete/<id>")
    def cities_delete(id: int):
        query: str = f"""
        DELETE FROM Cities
        WHERE city_id = {id};
        """
        query_commit(query)
        return redirect(url_for("cities"))

    @app.route("/countries-delete/<id>")
    def countries_delete(id: int):
        query: str = f"""
        DELETE FROM Countries
        WHERE country_id = {id};
        """
        query_commit(query)
        return redirect(url_for("countries"))

    @app.route("/heroes-delete/<id>")
    def heroes_delete(id: int):
        query: str = f"""
        DELETE FROM Heroes
        WHERE hero_id = {id};
        """
        query_commit(query)
        return redirect(url_for("heroes"))

    @app.route("/missions-delete/<id>")
    def missions_delete(id: int):
        query: str = f"""
        DELETE FROM Missions
        WHERE mission_id = {id};
        """
        query_commit(query)
        return redirect(url_for("missions"))

    @app.route("/powers-delete/<id>")
    def powers_delete(id: int):
        query: str = f"""
        DELETE FROM Powers
        WHERE power_id = {id};
        """
        query_commit(query)
        return redirect(url_for("powers"))

    @app.route("/villains-delete/<id>")
    def villains_delete(id: int):
        query: str = f"""
        DELETE FROM Villains
        WHERE villain_id = {id};
        """
        query_commit(query)

        return redirect(url_for("villains"))

except (mysql.connector.Error,
        mysql.connector.ProgrammingError,
        ValueError) as e:
    print(Fore.RED +
          f"[-] Error connecting to or using cursor with MySQL {e}" +
          Fore.RESET)
    if "cursor" in globals() and cursor is not None:
        cursor.close()
        print(Fore.YELLOW + "[~] MySQL cursor closed" + Fore.RESET)
    if "conn" in globals() and conn.is_connected():
        conn.close()
        print(Fore.YELLOW + "[~] MySQL connection closed" + Fore.RESET)
    print(Fore.YELLOW + "[~] Program Exiting..." + Fore.RESET)
    exit(1)

else:
    print(Fore.GREEN + "[+] Server started..." + Fore.RESET)
