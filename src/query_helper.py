import mysql.connector


def get_country_id(cursor: mysql.connector.cursor_cext.CMySQLCursorDict,
                   country_name: str) -> int:
    query: str = f"""
    SELECT country_id
    FROM Countries
    WHERE country_name = {country_name};
    """
    cursor.execute(query)
    return cursor.fetchall()["country_id"]
