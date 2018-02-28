import os
import pandas as pd, numpy as np
from pandas import *


# ROASST
# from dash_utils.dash_lib_viz_menus import *
# from dash_utils.dash_lib_viz_charts_RP import *


from roasst.app import app
from roasst import urls
from roasst.config import *



# I need to query one database with simulation results to populate the menus
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
    df.rename(columns={'Job_ID':'job_id'}, inplace=True)
    [ df.drop(col, axis=1, inplace=True) for col in list(df) if 'script' in col ]
    return df



df_sji = pd.read_csv( os.path.join(DATA_FOLDER_PATH, str(SIM_JOBS), 'SimJobIndex.csv') )
df_sji = process_sji(df=df_sji)
print(df_sji[:3])

