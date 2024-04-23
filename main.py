#!/usr/bin/env python

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main():
    message = "Welcome Shield Agent"
    return render_template("index.html",
                           message=message)
