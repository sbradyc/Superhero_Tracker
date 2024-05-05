import mysql.connector

CURSOR_OBJ = mysql.connector.cursor_cext.CMySQLCursorDict
NO_COUNTRY_NAME: str = "No country by that name"


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


def get_cities_id(cursor: CURSOR_OBJ) -> list[dict]:
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


def get_heroes_id(cursor: CURSOR_OBJ) -> list[dict]:
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


def get_villains_id(cursor: CURSOR_OBJ) -> list[dict]:
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
