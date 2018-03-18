import os
from urllib import parse


from sqlalchemy import create_engine

# roasst_mysql_engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}?charset=utf8".format(
#     host='jea.ensims.com',
#     user="andreab",
#     pw="abotti",
#     db="ROASST")
# )
roasst_mysql_engine = create_engine(
    "mysql+pymysql://{user}:{pw}@{host}/{db}".format(
        host='localhost:8000',
        user="root",
        pw="r04sst",
        db="roasst"),
    echo=True,
    )
# roasst_mysql_engine = create_engine(
#     "mysql+mysqlconnector://{user}:{pw}@{host}/{db}".format(
#         host='jea.ensims.com',
#         user="andreab",
#         pw="abotti",
#         db="ROASST"),
#     echo=True
#     )





# Older

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

