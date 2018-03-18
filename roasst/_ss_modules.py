import pandas as pd
import os
import sqlite3

from roasst.config import DATA_FOLDER_PATH


df_acr_large = pd.read_csv(DATA_FOLDER_PATH + '/df_acr_small.csv')
df_acr_large = pd.read_csv(DATA_FOLDER_PATH + '/df_acr_large.csv')


def get_db_ep_rp(db_name, db_folder):
    DB = os.path.join(DATA_FOLDER_PATH, db_folder, '{}_RP.sqlite'.format(db_name))

#

def query_sqlite_sji(db_name, db_folder, table):
    db = os.path.join(DATA_FOLDER_PATH, db_folder, '{}_RP.sqlite'.format(db_name))
    sqlite_con = sqlite3.connect(db)
    df = pd.read_sql_query('SELECT * FROM {}'.format(table), sqlite_con)
    return df
#
def query_sqlite_simres_rp(db_name, db_folder, table):
    db = os.path.join(DATA_FOLDER_PATH, db_folder, '{}_RP.sqlite'.format(db_name))
    sqlite_con = sqlite3.connect(db)
    df = pd.read_sql_query('SELECT * FROM {}'.format(table),sqlite_con)
    #
    df.set_index('job_id',inplace=True)
    return df
#
def query_sqlite_simres_hr(db_name, db_folder, table):
    db = os.path.join(DATA_FOLDER_PATH, db_folder, '{}_HR.sqlite'.format(db_name))
    sqlite_con = sqlite3.connect(db)
    df = pd.read_sql_query(
        'SELECT * FROM {}'.format(table),
        sqlite_con,
        )
    #
    df.set_index('datetime',inplace=True)
    return df
#
def query_sqlite_simres_hr_job_id(db_name, db_folder, table, job_id):
    db = os.path.join(DATA_FOLDER_PATH, db_folder, '{}_HR.sqlite'.format(db_name))
    sqlite_con = sqlite3.connect(db)
    query = "SELECT * FROM {} WHERE job_id='{}'".format(table, job_id)
    print(query)
    df = pd.read_sql_query(query, sqlite_con)
    #
    df.set_index('datetime',inplace=True)
    return df


def process_sji(df):
    cols_old = list(df)
    cols_new = []
    for col in cols_old:
        cols_new.append(col.replace('@@','@')[:-1] if '@@' in col else col)
    df.columns = cols_new
    
    df['@floor'] = df['ModelFile'].str.rsplit('_',2).str[1]
    df['@dwelling'] = df['ModelFile'].str.rsplit('_',2).str[0].str.split('/').str[1]
    df['@weather'] = df['WeatherFile'].str.split('.').str[0]

    df.drop(['#','ModelFile','WeatherFile'], axis=1, inplace=True)
    [ df.drop(col, axis=1, inplace=True) for col in list(df) if 'script' in col ]
    df.rename(columns={'Job_ID':'job_id'}, inplace=True)
    df.columns = df.columns.str.replace('_m3s', '(m3/s)')
    return df



