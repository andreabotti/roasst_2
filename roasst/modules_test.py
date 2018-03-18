import pandas as pd
import os
import sqlite3

# from roasst.config import DATA_FOLDER_PATH
from config import DATA_FOLDER_PATH



def sqlite_connector(file):
    con = sqlite3.connect(
        os.path.join(DATA_FOLDER_PATH, file)
        )
    return con

def sqlite_get_sji(file, table):
    sqlite_con = sqlite3.connect(
        os.path.join(DATA_FOLDER_PATH, file)
        )
    df = pd.read_sql_query('SELECT * FROM {}'.format(table),sqlite_con)
    
    return df

def sqlite_get_simres_HR(file, table):
    sqlite_con = sqlite3.connect(
        os.path.join(DATA_FOLDER_PATH, file)
        )
    df = pd.read_sql_query('SELECT * FROM {}'.format(table),sqlite_con)
    
    return df