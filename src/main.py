#!/usr/bin/env python

from colorama import Fore
from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
import query_helper

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
    print(Fore.GREEN + "[+] Successfully connected to database")

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
        data = []  # cursor.fetchall()
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
        data = []  # cursor.fetchall()
        return render_template("countries.html", data=data)

    @app.route("/heroes")
    def heroes():
        return render_template("heroes.html")

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
        data = []  # cursor.fetchall()
        return render_template("missions.html", data=data)

    @app.route("/powers")
    def powers():
        return render_template("powers.html")

    @app.route("/villains")
    def villains():
        return render_template("villains.html")

    @app.route("/cities-add", methods=['GET', 'POST'])
    def cities_add():
        if request.method == "GET":
            return render_template("cities-add.html")
        else:
            city_name = request.form.get("city_name")
            country_name = request.form.get("country_name")
            country_id = query_helper.get_country_id(conn,
                                                     cursor,
                                                     country_name)
            query: str = f"""
            INSERT INTO Cities (city_name, country_id)
            VALUES ({city_name}, {country_id});
            """
            cursor.execute(query)
            conn.commit()
            return redirect(url_for("cities"))

    @app.route("/countries-add", methods=['GET', 'POST'])
    def countries_add():
        return render_template("countries-add.html")

    @app.route("/heroes-add", methods=['GET', 'POST'])
    def heroes_add():
        return render_template("heroes-add.html")

    @app.route("/missions-add", methods=['GET', 'POST'])
    def missions_add():
        return render_template("missions-add.html")

    @app.route("/powers-add", methods=['GET', 'POST'])
    def powers_add():
        return render_template("powers-add.html")

    @app.route("/villains-add", methods=['GET', 'POST'])
    def villains_add():
        return render_template("villains-add.html")

    @app.route("/cities-update/<id>", methods=['GET', 'POST'])
    def cities_update(id: int):
        return render_template("cities-update.html")

    @app.route("/countries-update/<id>", methods=['GET', 'POST'])
    def countries_update(id: int):
        return render_template("countries-update.html")

    @app.route("/heroes-update/<id>", methods=['GET', 'POST'])
    def heroes_update(id: int):
        return render_template("heroes-update.html")

    @app.route("/missions-update/<id>", methods=['GET', 'POST'])
    def missions_update(id: int):
        return render_template("missions-update.html")

    @app.route("/powers-update/<id>", methods=['GET', 'POST'])
    def powers_update(id: int):
        return render_template("powers-update.html")

    @app.route("/villains-update/<id>", methods=['GET', 'POST'])
    def villains_update(id: int):
        return render_template("villains-update.html")

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
        # query: str = f"""
        # DELETE FROM Heores
        # WHERE hero_id = {id};
        # """
        # cursor.execute(query)
        # conn.commit()
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
        # query: str = f"""
        # DELETE FROM Powers
        # WHERE power_id = {id};
        # """
        # cursor.execute(query)
        # conn.commit()
        return render_template("powers.html")

    @app.route("/villains-delete/<id>")
    def villains_delete(id: int):
        # query: str = f"""
        # DELETE FROM Villains
        # WHERE villain_id = {id};
        # """
        # cursor.execute(query)
        # conn.commit()
        return redirect(url_for("villains"))

except (mysql.connector.Error,
        mysql.connector.ProgrammingError,
        ValueError) as e:
    print(Fore.RED + f"[-] Error connecting to or using cursor with MySQL {e}")
    if "cursor" in globals() and cursor is not None:
        cursor.close()
        print(Fore.YELLOW + "[~] MySQL cursor closed")
    if conn.is_connected():
        conn.close()
        print(Fore.YELLOW + "[~] MySQL connection closed")
    print(Fore.YELLOW + "[~] Program Exiting...")
