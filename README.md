# Superhero Tracker

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sbradyc/Superhero_Tracker/mysql.yml?label=MySQL) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sbradyc/Superhero_Tracker/safety.yml?label=Safety) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/sbradyc/Superhero_Tracker/lint.yml?label=Flake8) ![GitHub Issues](https://img.shields.io/github/issues/sbradyc/Superhero_Tracker?label=Issues)



This is Kippen and Sean's CS340 Project.

## Overview

With over 100 Heroes currently active across the world and a considerable number of Villains to match, the Heroes coalition, SHIELD, needs a more robust way of tracking these superhumans to respond to threats against the public in any major Cities. In order to do this, a cutting-edge website that is supported by a powerful database backend will help provide SHIELD agents with the necessary information to help superheroes respond to threats in under 60 seconds. With over 10+ Missions a day, Heroes are needed constantly wherever the fight may be. The database will also contain as much information on Villains (such as Powers) as possible to be retrieved quickly when they need to be dealt with.

## Installation & Usage

1. Make sure you have pipenv installed using `pip install pipenv`.
2. Clone the repo using `git clone https://github.com/sbradyc/Superhero_Tracker.git`.
3. Change your directory to be inside the root of the project `cd Superhero_Tracker`.
4. Install the packages needed and spin up pipenv shell using `pipenv install && pipenv shell`.
5. To run the webserver do `flask --app src/main run`
    - If you want to host the website in production mode then use `gunicorn -w 4 'src.main:app'`

## Developing

For more information about developing Superhero Tracker you can refer to [CONTRIBUTORS.md](https://github.com/sbradyc/Superhero_Tracker/blob/main/CONTRIBUTORS.md)

## Contributors

<p>
    <h4>Kippen Lee</h4>
  <a href="https://github.com/kippenlee">
    <img src="https://skillicons.dev/icons?i=github" />
  </a>
</p>


<p> 
    <h4>Sean Brady</h4>
  <a href="https://github.com/sbradyc">
    <img src="https://skillicons.dev/icons?i=github" />
  </a>
</p>
