import os
from urllib import parse


DATABASE_SCHEME = """
CREATE TABLE table_name1
(
 -- Your columns
);

CREATE TABLE table_name2
(
 -- Your columns
);
"""


def get_connection():
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn


def create_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(DATABASE_SCHEME)


def import_to_table_from_csv(table_name, path_to_csv, delimeter=';'):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"COPY {table_name} FROM '{path_to_csv}' WITH DELIMITER '{delimeter}' CSV HEADER;")
