#!/usr/bin/env python

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    message = "Welcome Shield Agent"
    return render_template("index.html",
                           message=message)


@app.route("/cities")
def cities():
    return render_template("cities.html")


@app.route("/countries")
def countries():
    return render_template("countries.html")


@app.route("/heroes")
def heroes():
    return render_template("heroes.html")


@app.route("/missions")
def missions():
    return render_template("missions.html")


@app.route("/powers")
def powers():
    return render_template("powers.html")


@app.route("/villains")
def villains():
    return render_template("villains.html")


@app.route("/cities-add")
def cities_add():
    return render_template("cities-add.html")


@app.route("/countries-add")
def countries_add():
    return render_template("countries-add.html")


@app.route("/heroes-add")
def heroes_add():
    return render_template("heroes-add.html")


@app.route("/missions-add")
def missions_add():
    return render_template("missions-add.html")


@app.route("/powers-add")
def powers_add():
    return render_template("powers-add.html")


@app.route("/villains-add")
def villains_add():
    return render_template("villains-add.html")


@app.route("/cities-update")
def cities_update():
    return render_template("cities-update.html")


@app.route("/countries-update")
def countries_update():
    return render_template("countries-update.html")


@app.route("/heroes-update")
def heroes_update():
    return render_template("heroes-update.html")


@app.route("/missions-update")
def missions_update():
    return render_template("missions-update.html")


@app.route("/powers-update")
def powers_update():
    return render_template("powers-update.html")


@app.route("/villains-update")
def villains_update():
    return render_template("villains-update.html")


# The following may or may not be actually used
@app.route("/cities-delete")
def cities_delete():
    return render_template("cities-delete.html")


@app.route("/countries-delete")
def countries_delete():
    return render_template("countries-delete.html")


@app.route("/heroes-delete")
def heroes_delete():
    return render_template("heroes-delete.html")


@app.route("/missions-delete")
def missions_delete():
    return render_template("missions-delete.html")


@app.route("/powers-delete")
def powers_delete():
    return render_template("powers-delete.html")


@app.route("/villains-delete")
def villains_delete():
    return render_template("villains-delete.html")
