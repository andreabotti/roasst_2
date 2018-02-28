import esoreader
import os
import pandas as pd, numpy as np
from pandas import *

import sqlite3



#####

def eso2df(dd, data, var, var_key,col_name,log):
    df = pd.DataFrame()
    
    for i in range(0,10,1):
        frequency, key, variable = dd.find_variable(var)[i]

        if (key == var_key) and (frequency == 'Hourly'):
            # print('- f: {} | key: {} | v: {}'.format(frequency,key,variable) )
            idx = dd.index[frequency, key, variable]
            time_series = data[idx]
            if log==True:
                print('    extracting from ESO file\t\t  Var:{},     Freq: {},     Key:{},     Lenght of time-series: {}'.format(variable, frequency, key, len(time_series)) )
            else:
                'Do nothing'
            
            rng = pd.date_range('1989-05-01', periods=153*24, freq='H')
            df = pd.DataFrame(data = time_series, index=rng, columns=[col_name], dtype=None, copy=False)        
            df.index.rename('datetime', inplace=True)
            return df
        else:
            'Do nothing'


#####

def extract_from_eso(dd, data, var, var_key,col_name,log):
    df = pd.DataFrame()
    
    for i in range(0,10,1):
        frequency, key, variable = dd.find_variable(var)[i]
        
        if (key == var_key) and (frequency == 'Hourly'):
            idx = dd.index[frequency, key, variable]
            time_series = data[idx]
            if log==True:
                print('    Extracting from ESO file\t\t  Var:{},     Freq: {},     Key:{},     Lenght of time-series: {}'.format(variable, frequency, key, len(time_series)) )
            else:
                'Do nothing'
            
            rng = pd.date_range('2017-05-01', periods=153*24, freq='H')
            df = pd.DataFrame(data = time_series, index=rng, columns=[col_name], dtype=None, copy=False)        
            df.index.rename('datetime', inplace=True)
            return df
        else:
            'Do nothing'



#####

#####

#####



def tm52_from_eso(path, zone, log):
    
    # method 2: without Pandas
    dd,data = esoreader.read(path)
    df_hr = extract_from_eso(dd, data, 'Zone Operative Temperature', zone+'_ZONE', zone, log)
    df_ext_hr = extract_from_eso(dd, data, 'Site Outdoor Air Drybulb Temperature', 'Environment', 'ODT', log)

    #####
    # Applies function that adds columns Trm, Tmax, Tmin calculated on column 'ODT'
    df52_hr = return_TM52_hr_TrmTmaxTmin(df_ext_hr, tm52_range=3, days=7)
    df = pd.concat([df_hr, df_ext_hr, df52_hr],axis=1).round(2)

    # Re-orders columns
    cols = list(df)                                 # get a list of columns
    cols.insert(10, cols.pop(cols.index(zone)) )    # move the column to head of list using index, pop and insert
    df = df.ix[:, cols]                             # use ix to reorder


    ## Applies function for TM52 calculations
    df_tm52_hr = return_TM52_hourly(df, col_name=zone)             #(intermediate - hourly)
    #
    df_tm52_dd = return_TM52_daily(df_tm52_hr, var_name=zone)      #(daily)
    df_tm52_dd.columns = df_tm52_dd.columns.droplevel(1)
    #
    df_tm52_rp = return_TM52_runperiod(df_tm52_dd, var_name=zone)  #(runperiod)
    df_tm52_rp.index.rename('datetime', inplace=True)
    df_tm52_rp.columns = df_tm52_rp.columns.droplevel(1)

    return df_tm52_hr, df_tm52_dd, df_tm52_rp


def tm59_from_eso(path, zone, log):
    
    dd,data = esoreader.read(path)
    df_hr = extract_from_eso(dd, data, 'Zone Operative Temperature', zone+'_ZONE', zone, log)
    df_ext_hr = extract_from_eso(dd, data, 'Site Outdoor Air Drybulb Temperature', 'Environment', 'ODT', log)

    #####
    # Applies function that adds columns Trm, Tmax, Tmin calculated on column 'ODT'
    df52_hr = return_TM52_hr_TrmTmaxTmin(df_ext_hr, tm52_range=3, days=7)
    df = pd.concat([df_hr, df_ext_hr, df52_hr],axis=1).round(2)

    # Re-orders columns
    cols = list(df)                                 # get a list of columns
    cols.insert(10, cols.pop(cols.index(zone)) )    # move the column to head of list using index, pop and insert
    df = df.ix[:, cols]                             # use ix to reorder


    # Applies function for TM59 calculations
    df_tm59_hr = return_TM59_hourly(df, col_name=zone)                 #intermediate - hourly
    #
    df_tm59_dd = return_TM59_daily(df_tm59_hr, var_name=zone)          #daily
    df_tm59_dd.columns = df_tm59_dd.columns.droplevel(1)
    #
    df_tm59_rp = return_TM59_runperiod(df_tm59_dd, var_name=zone)      #runperiod
    df_tm59_rp.index.rename('datetime', inplace=True)
    df_tm59_rp.columns = df_tm59_rp.columns.droplevel(1)

    return df_tm59_hr, df_tm59_dd, df_tm59_rp



#####

#####

#####



def import_simjobindex(file):
    df = pd.read_csv(
        file,
        index_col = 'Job_ID',
        skipinitialspace=True,
        header=0)

    df.index.rename('job_id', inplace=True) 
    return df


#####


# Imports daily results
def import_simres_daily(file):
    df = pd.read_csv(
        file,
        skipinitialspace=True,
        header=0)
    
    datetime_new = []
    for time in df['Date/Time']:
        try:
            time = datetime.strptime(time, '%m/%d  %H:%M:%S')
            time_new = time - timedelta(hours=1)
        except ValueError:
            time_new = datetime.strptime(time.replace('24:', '00:'), '%m/%d  %H:%M:%S')
        datetime_new.append(time_new)
    df['Date/Time'] = datetime_new

    df.set_index(['Job_ID', 'Date/Time'], inplace=True)
    df.index.set_names(['job_id','datetime'], inplace=True)

    return df


#####


# Imports daily results
def import_simres_runperiod(file):
    df = pd.read_csv(
        file,
        skipinitialspace=True,
        header=0)
    
    df.rename(columns = {'Job_ID':'job_id'}, inplace=True)
    df.set_index('job_id', inplace=True)
    return df

#####

def import_allcombinedresults(file):
    df = pd.read_csv(
        file,
        skipinitialspace=True,
        header=0
    )
    df.rename(columns = {'Job_ID':'job_id'}, inplace=True)
    df.set_index('job_id', inplace=True)

    return df

#####

def filter_df(df, p1,v1, p2,v2, p3,v3):    
    for p,v in zip( (p1,p2,p3), (v1,v2,v3) ):
        # print(p,v)
        "Do nothing"

    df = df[ df[p1] == v1 ]
    df = df[ df[p2] == v2 ]
    df = df[ df[p3] == v3 ]
    print(df.shape)

    return df

#####

def add_cols_wfr_wa(df,Area_Win_B, Area_Win_KL, Area_Floor_B, Area_Floor_KL):

    df.loc[:,'@wfr_B']  = (df.loc[:,'@wwr_B'].astype(float) / Area_Floor_B).round(2)
    df.loc[:,'@wfr_KL'] = (df.loc[:,'@wwr_KL'].astype(float) / Area_Floor_KL).round(2)
    df.loc[:,'@wa_B']   = (Area_Win_B * df.loc[:,'@wwr_B'].astype(float) / 100).round(2)
    df.loc[:,'@wa_KL']  = (Area_Win_KL * df.loc[:,'@wwr_KL'].astype(float) / 100).round(2)
    return df



#####

#####

#####



def query_sqlite_sji(db, table):
    # SQLITE
    sqlite_con = sqlite3.connect(db)
    df = pd.read_sql_query(
        'SELECT * FROM {} \
        -- LIMIT 3'
        .format(table),
        sqlite_con
        )
    return df

#####

def query_sqlite_simres_hr(db, table):
    
    # SQLITE
    sqlite_con = sqlite3.connect(db)
    df = pd.read_sql_query(
        'SELECT * FROM {} \
        -- LIMIT 3'
        .format(table),
        sqlite_con
        )
    df.set_index('datetime',inplace=True)
    return df

#####

def query_sqlite_simres_rp(db, table):
    # hashed as u_w_sims used as input
    # u_w_sims = '{}_{}_{}'.format(U, W, jobs)

    # SQLITE
    sqlite_con = sqlite3.connect(db)
    df = pd.read_sql_query(
        'SELECT * FROM {}'.format(table),
        sqlite_con
        )
    df.set_index('job_id',inplace=True)
    
    # df.rename(
    #     columns={value : '{}|{}'.format(U, value)},
    #     inplace=True
    #     )
    # df = df['{}|{}'.format(U, value)]

    return df

#####

def query_sqlite_multiple_dfs_merge_on_value(db, units, weather_files, jobs, value):
    df_all = pd.DataFrame()

    for U in units:
        for W in weather_files:
            u_w_sims = '{}_{}_{}'.format(U, W, jobs)

            # CSV
            # df = pd.read_csv('{}/{}_RP_S.csv'.format(folder, U) )

            # SQLITE
            sqlite_con = sqlite3.connect(db)
            df = pd.read_sql_query(
                'SELECT * FROM {} \
                -- LIMIT 3'
                .format(u_w_sims),
                sqlite_con
                )
            df.set_index('job_id',inplace=True)
            
            df.rename(
                columns={value : '{}|{}'.format(U, value)},
                inplace=True
                )
            df = df['{}|{}'.format(U, value)]

            df_all = pd.concat(
                [df_all, df],
                axis=1,
                ignore_index=False,
                )
    return df_all