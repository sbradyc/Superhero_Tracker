#!/usr/bin/env python

from colorama import Fore
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
# import query_helper

app = Flask(__name__)
CONFIG = {
    "host":     "mysql.engr.oregonstate.edu",
    "user":     "username",
    "password": "password",
    "database": "cs340_username"
}

try:
    conn = mysql.connector.connect(**CONFIG)
    cursor = conn.cursor(dictionary=True)
    print(Fore.GREEN + "[+] Successfully connected to database" + Fore.RESET)

    @app.route("/")
    def main():
        message = "Welcome Shield Agent"
        return render_template("index.html",
                               message=message)

    @app.route("/cities")
    def cities():
        # query: str = """
        # SELECT
        #     Cities.city_id AS id,
        #     Cities.city_name AS city,
        #     Countries.country_name AS country
        # FROM Cities
        # INNER JOIN Countries ON Countries.country_id = Cities.country_id;
        # """
        # cursor.execute(query)
        data = [{"id": 1, "city": "New York", "country": "United States of America"}]  # cursor.fetchall()
        return render_template("cities.html", data=data)

    @app.route("/countries")
    def countries():
        # query: str = """
        # SELECT
        #     Countries.country_id AS id,
        #     Countries.country_name AS country,
        #     Countries.country_code AS code
        # FROM Countries;
        # """
        # cursor.execute(query)
        data = [{"id": 1, "country": "United States of America", "code": "USA"}]  # cursor.fetchall()
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
        INNER JOIN Cities ON Cities.city_id = Heroes.city_id
        INNER JOIN HeroPowers ON HeroPowers.hero_id = Heroes.hero_id
        INNER JOIN Powers ON Powers.power_id = HeroPowers.power_id
        GROUP BY Heroes.hero_id, Heroes.pseudonym, Heroes.first_name, Heroes.last_name, Cities.city_name
        ORDER BY Heroes.pseudonym;
        """
        cursor.execute(query)
        data = cursor.fetchall()
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
        # query: str = """
        # SELECT
        #     Missions.mission_id AS id,
        #     Missions.mission_codename AS mission_name,
        #     Heroes.pseudonym AS hero_name,
        #     Villains.pseudonym AS villain_name,
        #     Cities.city_name AS city,
        #     Missions.description AS description
        # FROM Missions
        # INNER JOIN Heroes ON Heroes.hero_id = Missions.hero_id
        # INNER JOIN Villains ON Villains.villain_id = Missions.villain_id
        # INNER JOIN Cities ON Cities.city_id = Missions.city_id;
        # """
        # cursor.execute(query)
        data = [{"id": 1, "mission_name": "Ink Pen", "hero_name": "Spider Man", "villain_name": "Doc Oc", "city": "New York", "description": "Doc Oc is stealing fuses from major power stations in New York"}]  # cursor.fetchall()
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
        cursor.execute(query)
        data = cursor.fetchall()
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
        INNER JOIN Cities ON Cities.city_id = Villains.last_known_loc
        INNER JOIN VillainPowers ON VillainPowers.villain_id = Villains.villain_id
        INNER JOIN Powers ON Powers.power_id = VillainPowers.power_id
        GROUP BY Villains.villain_id, Villains.pseudonym, Villains.first_name, Villains.last_name, Cities.city_name;
        """
        cursor.execute(query)
        data = cursor.fetchall()
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
            # query = f"""
            # SELECT
            #     country_id,
            #     country_name
            # FROM Countries
            # """
            # cursor.execute(query)
            countries = [{"country_id": 1, "country_name": "United States of America"}]  # cursor.fetchall()
            return render_template("cities-add.html",
                                   countries=countries)
        else:
            # city_name: str = request.form.get("city_name")
            # country_id: str = request.form.get("country_id")
            # if not city_name:
            #     return render_template("cities-add.html",
            #                            message=query_helper.NO_CITY_NAME)
            # query: str = f"""
            # INSERT INTO Cities (city_name, country_id)
            # VALUES ({city_name}, {country_id});
            # """
            # cursor.execute(query)
            # conn.commit()
            return redirect(url_for("cities"))

    @app.route("/countries-add", methods=['GET', 'POST'])
    def countries_add():
        if request.method == "GET":
            return render_template("countries-add.html")
        else:
            # country_name: str = request.form.get("country_name")
            # country_code: str = request.form.get("country_code")
            # query: str = f"""
            # INSERT INTO Countries (country_name, country_code)
            # VALUES ({country_name}, {country_code});
            # """
            # cursor.execute(query)
            # conn.commit()
            return redirect(url_for("countries"))

    @app.route("/heroes-add", methods=['GET', 'POST'])
    def heroes_add():
        if request.method == "GET":
            # get cities
            query = """
            SELECT
                city_id,
                city_name
            FROM Cities
            ORDER BY city_name ASC;
            """
            cursor.execute(query)
            cities = cursor.fetchall()

            # get powers
            query = """
            SELECT
                power_id,
                name
            FROM Powers
            ORDER BY name ASC;
            """
            cursor.execute(query)
            powers = cursor.fetchall()

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
            pseudonym = request.form.get("pseudonym")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            city_id = request.form.get("city_id")
            query = f"""
            INSERT INTO Heroes (
                pseudonym,
                first_name,
                last_name,
                city_id
            )
            VALUES (
                "{pseudonym}",
                "{first_name}",
                "{last_name}",
                {city_id}
            );
            """
            cursor.execute(query)
            conn.commit()

            # create HeroPower entries
            query = "SELECT LAST_INSERT_ID();"
            cursor.execute(query)
            hero_id = cursor.fetchall()[0]["LAST_INSERT_ID()"]
            for name, _ in request.form.items():
                prefix = name[:9]
                if prefix == "power_id:":  # if power checkbox was selected
                    power_id = name[9:] 
                    query = f"""
                    INSERT INTO HeroPowers (
                        hero_id,
                        power_id
                    )
                    VALUES (
                        {hero_id},
                        {power_id}
                    );
                    """
                    cursor.execute(query)
                    conn.commit()

            return redirect(url_for("heroes"))

    @app.route("/missions-add", methods=['GET', 'POST'])
    def missions_add():
        if request.method == "GET":
            heroes: list[dict] = []  # query_helper.get_heroes_data(cursor)
            villains: list[dict] = []  # query_helper.get_villains_data(cursor)
            cities: list[dict] = []  # query_helper.get_cities_data(cursor)
            return render_template("missions-add.html",
                                   heroes=heroes,
                                   villains=villains,
                                   cities=cities)
        else:
            # mission_name: str = request.form.get("mission_name")
            # hero_id: int = int(request.form.get("hero_id"))
            # villain_id: int = int(request.form.get("villain_id"))
            # city_id: int = int(request.form.get("city_id"))
            # description: str = request.form.get("description")
            # query: str = f"""
            # INSERT INTO Missions (
            #     mission_codename,
            #     hero_id,
            #     villain_id,
            #     city_id,
            #     description)
            # VALUES ('{mission_name}',
            #          {hero_id},
            #          {villain_id},
            #          {city_id},
            #          '{description}');
            # """
            # cursor.execute(query)
            # conn.commit()
            return redirect(url_for("missions"))

    @app.route("/powers-add", methods=['GET', 'POST'])
    def powers_add():
        if request.method == "GET":
            return render_template("powers-add.html")
        else:
            power_name = request.form.get("name")
            power_description = request.form.get("description")
            query = f"""
            INSERT INTO Powers (
                name,
                description)
            VALUES (
                '{power_name}',
                '{power_description}'
            );
            """
            cursor.execute(query)
            conn.commit()
            return redirect(url_for("powers"))

    @app.route("/villains-add", methods=['GET', 'POST'])
    def villains_add():
        if request.method == "GET":
            # get cities
            query = """
            SELECT
                city_id,
                city_name
            FROM Cities
            ORDER BY city_name ASC;
            """
            cursor.execute(query)
            cities = cursor.fetchall()

            # get powers
            query = """
            SELECT
                power_id,
                name
            FROM Powers
            ORDER BY name ASC;
            """
            cursor.execute(query)
            powers = cursor.fetchall()

            return render_template(
                "people-add.html",
                people_type_singular="villain",
                people_type_plural="villains",
                cities=cities,
                city_type="last known location",
                powers=powers
            )
        else:
            # create Hero entry
            pseudonym = request.form.get("pseudonym")
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            city_id = request.form.get("city_id")
            query = f"""
            INSERT INTO Villains (
                pseudonym,
                first_name,
                last_name,
                last_known_loc
            )
            VALUES (
                "{pseudonym}",
                "{first_name}",
                "{last_name}",
                {city_id}
            );
            """
            cursor.execute(query)
            conn.commit()

            # create HeroPower entries
            query = "SELECT LAST_INSERT_ID();"
            cursor.execute(query)
            villain_id = cursor.fetchall()[0]["LAST_INSERT_ID()"]
            for name, _ in request.form.items():
                prefix = name[:9]
                if prefix == "power_id:":  # if power checkbox was selected
                    power_id = name[9:] 
                    query = f"""
                    INSERT INTO VillainPowers (
                        villain_id,
                        power_id
                    )
                    VALUES (
                        {villain_id},
                        {power_id}
                    );
                    """
                    cursor.execute(query)
                    conn.commit()

            return redirect(url_for("villains"))

    @app.route("/cities-update/<id>", methods=['GET', 'POST'])
    def cities_update(id: int):
        # defaults: dict = query_helper.get_city(cursor, id) UPDATE THIS QUERY TO GET country_name
        # query = f"""
        # SELECT
        #     country_id,
        #     country_name
        # FROM Countries
        # """
        # cursor.execute(query)
        # countries = cursor.fetchall()
        if request.method == "GET":
            countries = [{"country_id": 1, "country_name": "United States of America"}]  # cursor.fetchall()
            return render_template("cities-update.html",
                                   defaults={"city_id": 1,
                                             "city_name": "example",
                                             "country_name": "United States of America"},
                                   countries=countries)
        else:
            # city_name: str = request.form.get("city_name")
            # country_id: str = request.form.get("country_id")
            # if not city_name:
            #     return render_template("cities-add.html",
            #                            message=query_helper.NO_CITY_NAME)
            # if country_id == -1:
            #     return render_template("cities-update.html",
            #                            message=query_helper.NO_COUNTRY_NAME,
            #                            defaults=defaults,
            #                            countries=countries)
            # query: str = f"""
            # UPDATE Cities
            # SET
            #     city_name = '{city_name}',
            #     country_id = {country_id}
            # WHERE city_id = {id};
            # """
            # cursor.execute(query)
            # conn.commit()
            print(request.form.get("country_id"))
            return redirect(url_for("cities"))

    @app.route("/countries-update/<id>", methods=['GET', 'POST'])
    def countries_update(id: int):
        if request.method == "GET":
            # country: dict = query_helper.get_country(cursor, id)
            return render_template("countries-update.html",
                                   country={"country_name": "example",
                                            "country_code": "example"})
        else:
            # country_name: str = request.form.get("country_name")
            # country_code: str = request.form.get("country_code")
            # query: str = f"""
            # UPDATE Countries
            # SET
            #     country_name = '{country_name}',
            #     country_code = '{country_code}'
            # WHERE country_id = {id};
            # """
            # cursor.execute(query)
            # conn.commit()
            return redirect(url_for("countries"))

    @app.route("/heroes-update/<id>", methods=['GET', 'POST'])
    def heroes_update(id: int):
        data = {"id": 1, "pseudonym": "Spider-man", "first_name": "Peter", "last_name": "Parker", "city": "New York", "powers": ["Super Strength", "Enhanced Agility"]}
        return render_template(
            "people-update.html",
            person=data,
            people_type_singular="hero",
            people_type_plural="heroes",
            city_type="city"
        )

    @app.route("/missions-update/<id>", methods=['GET', 'POST'])
    def missions_update(id: int):
        if request.method == "GET":
            mission = []  # query_helper.get_mission(cursor, id)
            heroes: list[dict] = []  # query_helper.get_heroes_data(cursor)
            villains: list[dict] = []  # query_helper.get_villains_data(cursor)
            cities: list[dict] = []  # query_helper.get_cities_data(cursor)
            data = {"id": 1, "mission_codename": "Ink Pen", "hero_name": "Spider Man", "villain_name": "Doc Oc", "city": "New York", "description": "Doc Oc is stealing fuses from major power stations in New York"}
            return render_template("missions-update.html",
                                   defaults=data,  # mission,
                                   heroes=heroes,
                                   villains=villains,
                                   cities=cities)
        else:
            # mission_name: str = request.form.get("mission_name")
            # hero_id: int = int(request.form.get("hero_id"))
            # villain_id: int = int(request.form.get("villain_id"))
            # city_id: int = int(request.form.get("city_id"))
            # description: str = request.form.get("description")
            # query: str = f"""
            # UPDATE Missions
            # SET
            #     hero_id = {hero_id},
            #     villain_id = {villain_id},
            #     city_id = {city_id},
            #     mission_codename = '{mission_name}',
            #     description = '{description}'
            # WHERE mission_id = {id};
            # """
            # cursor.execute(query)
            # conn.commit()
            return redirect(url_for("missions"))

    @app.route("/powers-update/<id>", methods=['GET', 'POST'])
    def powers_update(id: int):
        if request.method == "GET":
            query = f"""
            SELECT
                name,
                description
            FROM Powers
            WHERE power_id = {id};
            """
            cursor.execute(query)
            power = cursor.fetchall()[0]

            return render_template(
                "powers-update.html",
                power=power
            )
        else:
            power_name = request.form.get("name")
            power_description = request.form.get("description")
            query = f"""
            UPDATE Powers
            SET
                name = '{power_name}',
                description = '{power_description}'
            WHERE power_id = {id};
            """
            cursor.execute(query)
            conn.commit()

            return redirect(url_for("powers"))

    @app.route("/villains-update/<id>", methods=['GET', 'POST'])
    def villains_update(id: int):
        data = {"id": 1, "pseudonym": "Doctor Octopus", "first_name": "Otto", "last_name": "Octavius", "city": "New York", "powers": ["Cybernetic Tentacles"]}
        return render_template(
            "people-update.html",
            person=data,
            people_type_singular="villain",
            people_type_plural="villains",
            city_type="last known location"
        )

    """
    The following routes will do a delete query and then reload
    the page for the user
    """
    @app.route("/cities-delete/<id>")
    def cities_delete(id: int):
        # query: str = f"""
        # DELETE FROM Cities
        # WHERE city_id = {id};
        # """
        # cursor.execute(query)
        # conn.commit()
        return redirect(url_for("cities"))

    @app.route("/countries-delete/<id>")
    def countries_delete(id: int):
        # query: str = f"""
        # DELETE FROM Countries
        # WHERE country_id = {id};
        # """
        # cursor.execute(query)
        # conn.commit()
        return redirect(url_for("countries"))

    @app.route("/heroes-delete/<id>")
    def heroes_delete(id: int):
        query: str = f"""
        DELETE FROM Heroes
        WHERE hero_id = {id};
        """
        cursor.execute(query)
        conn.commit()

        return redirect(url_for("heroes"))

    @app.route("/missions-delete/<id>")
    def missions_delete(id: int):
        # query: str = f"""
        # DELETE FROM Missions
        # WHERE mission_id = {id};
        # """
        # cursor.execute(query)
        # conn.commit()
        return redirect(url_for("missions"))

    @app.route("/powers-delete/<id>")
    def powers_delete(id: int):
        query: str = f"""
        DELETE FROM Powers
        WHERE power_id = {id};
        """
        cursor.execute(query)
        conn.commit()
        return redirect(url_for("powers"))

    @app.route("/villains-delete/<id>")
    def villains_delete(id: int):
        query: str = f"""
        DELETE FROM Villains
        WHERE villain_id = {id};
        """
        cursor.execute(query)
        conn.commit()

        return redirect(url_for("villains"))

except (mysql.connector.Error,
        mysql.connector.ProgrammingError,
        ValueError) as e:
    print(Fore.RED +
          f"[-] Error connecting to or using cursor with MySQL {e}" +
          Fore.RESET)
    # if "cursor" in globals() and cursor is not None:
    #     cursor.close()
    #     print(Fore.YELLOW + "[~] MySQL cursor closed" + Fore.RESET)
    # if "conn" in globals() and conn.is_connected():
    #     conn.close()
    #     print(Fore.YELLOW + "[~] MySQL connection closed" + Fore.RESET)
    print(Fore.YELLOW + "[~] Program Exiting..." + Fore.RESET)
    exit(1)

else:
    print(Fore.GREEN + "[+] Server started..." + Fore.RESET)
