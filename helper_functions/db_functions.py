def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    import sqlite3
    from sqlite3 import Error
    import re

    db_file = re.sub('/', '_', db_file)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def query_db(p_db_conn, p_sql):
    """
    Query the sqlite DB
    Args:
        p_db_conn: The DB connector object
        p_sql: The query to run (str)
    Returns:
        results of the query
    """
    from sqlite3 import Error

    p_rows = ''
    try:
        cursor = p_db_conn.cursor()
        cursor.execute(p_sql)
        p_rows = cursor.fetchall()
    except Error as e:
        print(e)
    return p_rows


def execute_sql(p_db_conn, p_sql):
    """
    Executes some sql
    Args:
        p_db_conn: The DB connector object
        p_sql: The sql to execute (str)
    Returns: Nothing
    """
    from sqlite3 import Error
    try:
        c = p_db_conn.cursor()
        c.execute(p_sql)
        p_db_conn.commit()
    except Error as e:
        print("Had an error while running execute_sql:" + str(e) + '\n This command: ' + str(p_sql) )
