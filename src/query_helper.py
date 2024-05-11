import mysql.connector

CURSOR_OBJ = mysql.connector.cursor_cext.CMySQLCursorDict
NO_CITY_NAME: str = "You must input a city name."


def get_country_id(cursor: CURSOR_OBJ,
                   country_name: str) -> int:
    query: str = f"""
    SELECT country_id
    FROM Countries
    WHERE country_name = '{country_name}';
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    country_entry: dict[str, int] = cursor.fetchall()[0]
    return country_entry.get("country_id", -1)


def get_cities_data(cursor: CURSOR_OBJ) -> list[dict]:
    query: str = """
    SELECT
        city_id,
        city_name
    FROM Cities;
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    return cursor.fetchall()


def get_heroes_data(cursor: CURSOR_OBJ) -> list[dict]:
    query: str = """
    SELECT
        hero_id,
        pseudonym
    FROM Heroes;
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    return cursor.fetchall()


def get_villains_data(cursor: CURSOR_OBJ) -> list[dict]:
    query: str = """
    SELECT
        villain_id,
        pseudonym
    FROM Villains;
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    return cursor.fetchall()


def get_country_name(cursor: CURSOR_OBJ, country_id: int):
    query = f"""
    SELECT country_name
    FROM Countries
    WHERE country_id = {country_id};
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    entry = cursor.fetchall()[0]
    return entry["country_name"]


def get_mission(cursor: CURSOR_OBJ, id: int) -> str:
    query: str = f"""
    SELECT
        mission_id,
        hero_id,
        villain_id,
        city_id,
        mission_codename,
        description
    FROM Missions
    WHERE mission_id = {id};
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    return cursor.fetchall()[0]


def get_city(cursor: CURSOR_OBJ, id: int) -> str:
    query: str = f"""
    SELECT
        city_id,
        country_id,
        city_name
    FROM Cities
    WHERE city_id = {id};
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    return cursor.fetchall()[0]


def get_country(cursor: CURSOR_OBJ, id: int):
    query: str = f"""
    SELECT
        country_id,
        country_name,
        country_code
    FROM Countries
    WHERE country_id = {id};
    """
    try:
        cursor.execute(query)
    except mysql.connector.errors.ProgrammingError:
        return -1
    return cursor.fetchall()[0]
