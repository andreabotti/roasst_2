import os, sys
import pandas as pd, numpy as np
from pandas import *
import datetime as dt
#
import sqlite3


# from ..roasst.app import app
# from ..roasst import urls

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from config import *
from menus import *
from charts_HR import *
from page_title import page_title
from db import *
conn_mysql = roasst_mysql_engine.connect()

#
from modules_test import *
# Replaced by
CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER_PATH = CURRENT_DIR_PATH + '/data'
DATA_FOLDER_PATH = 'D:/Dropbox/EDU_EngD/ROASST/github/roasst_2/roasst/data'
DWELLINGS = ['P2302']




app = dash.Dash()
app.config.supress_callback_exceptions = True
# CSS
external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css",
                ]
[app.css.append_css({"external_url": css}) for css in external_css]
if 'DYNO' in os.environ:
    app.scripts.append_script({'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'})




#####
bar_width = 0.8
bar_gap = 1;
bar_group_gap = 0;
bar_mode = 'group'
#
colors_dict = {
    'HG_IES':'rgba(255, 0, 0, 0.7)', 'HG_EP':'rgba(255, 0, 0, 0.4)',
    'HL_IES':'rgba(120, 163, 206, 0.85)', 'HL_EP':'rgba(120, 163, 206, 0.55)',
    'VNT_IES':'rgba(120, 163, 206, 0.85)', 'VNT_EP':'rgba(120, 163, 206, 0.55)',
    'OH_IES':'rgba(0, 0, 0, 0.8)', 'OH_EP':'rgba(0, 0, 0, 0.55)',
    }

#####

# I need to query one database with simulation results to populate the menus
D = DWELLINGS[0]
SIM_TOOL, SIM_JOBS, RVX = 'JESS', 216, 'EMS_HR_RP'
sqlite_con = sqlite3.connect(
    os.path.join(
        DATA_FOLDER_PATH,
        'ALL_{}_HR.sqlite'.format(SIM_JOBS),
        )
    )
table = '{}_{}_SJI'.format(D, SIM_JOBS)
df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table),sqlite_con)
#


#
input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_unit(menu_id='D_input(p2)',
            width='two', menu_type='radio', DWELLINGS=DWELLINGS),
        dash_create_menu_weather(menu_id=['W1_input(p2)','W2_input(p2)'], widths=['one','one'],
            WEATHER_FILES=WEATHER_FILES),
        dash_create_menu_floor(menu_id='F_input(p2)', col=Fcol,
            width='one', df=df_sji),
        dash_create_menu_north(menu_id='N_input(p2)', col=Ncol,
            width='one', df=df_sji),
        dash_create_menu_vnt(menu_id=['VNT_KL_input(p2)','VNT_B_input(p2)'],
            cols=[vBcol,vKLcol], width='two', df=df_sji),
        dash_create_menu_window_width(menu_id=['WW_KL_input(p2)','WW_B_input(p2)'],
            cols=[wwBcol,wwKLcol], width='one', df=df_sji),
        dash_create_menu_glazing(menu_id='G_input(p2)', col=Gcol,
            width='one', df=df_sji),
        dash_create_menu_rooms(menu_id='R_input(p2)', width='one', ROOMS=ROOMS),
        dash_create_menu_datepickerrange(width='one'),
        ],
    )

#
chart1 = html.Div(
    children=[
        dcc.Graph(
            id='scatter_hr',
            figure={},
            style={'height': '750px'},
            ),
        ],
)

#####

app.layout = html.Div(
    className='row',
    style={
        # 'background-color': '#F3F3F3',
        'font-family': 'overpass',  # 'font-size':11,
        'height': '1000px', 'width': '100%',    # 'max-width': '1800',
        'margin': '20 0 0 0', 'padding': '0 0 0 0',
        },
    children = [
        page_title,
        input_menus,
        html.Hr(),
        chart1,
        ],
    )

#####

@app.callback(
    Output('VNT_KL_input(p2)', 'options'),
    [Input('D_input(p2)', 'value'), Input('F_input(p2)', 'value')]
)
def set_vnt_KL_options(D_value, F_value):
    #
    D = D_value
    F = F_value
    D_F = '{}_{}'.format(D_value, F_value)
    
    df_sji = sqlite_get_sji(
        file='ALL_{}_HR.sqlite'.format(SIM_JOBS),
        table='{}_{}_SJI'.format(D, SIM_JOBS),
        )
    #
    VNT_KL_list = df_sji[vKLcol].unique()
    VNT_KL_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_KL_list ]
    return VNT_KL_options
@app.callback(
    Output('VNT_KL_input(p2)', 'value'),
    [Input('VNT_KL_input(p2)', 'options')]
)
def set_vnt_KL_value(available_options):
    return available_options[0]['value'], 
#
@app.callback(
    Output('VNT_B_input(p2)', 'options'),
    [Input('D_input(p2)', 'value'), Input('F_input(p2)', 'value')]
)
def set_vnt_B_options(D_value, F_value):
    #
    D = D_value
    F = F_value
    D_F = '{}_{}'.format(D_value, F_value)

    df_sji = sqlite_get_sji(
        file='ALL_{}_HR.sqlite'.format(SIM_JOBS),
        table='{}_{}_SJI'.format(D, SIM_JOBS),
        )
    #
    VNT_B_list = df_sji[vBcol].unique()
    VNT_B_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_B_list ]
    return VNT_B_options
@app.callback(
    Output('VNT_B_input(p2)', 'value'),
    [Input('VNT_B_input(p2)', 'options')]
)
def set_vnt_B_value(available_options):
    value = available_options[0]
    return value, 


#####

@app.callback(
    Output('scatter_hr', 'figure'),
    [
        Input('D_input(p2)', 'value'),
        Input('W1_input(p2)', 'value'), Input('W2_input(p2)', 'value'),
        Input('F_input(p2)', 'value'), Input('N_input(p2)', 'value'),
        Input('VNT_B_input(p2)', 'value'), Input('VNT_KL_input(p2)', 'value'),
        Input('WW_B_input(p2)', 'value'), Input('WW_KL_input(p2)', 'value'),
        Input('G_input(p2)', 'value'), Input('R_input(p2)', 'value'),
        Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date'),
        # Input('RangeSlider_month', 'value'),
    ]
    )


def update_chart_scatter_hr(
    D_value, W1_value, W2_value,
    F_value, N_value,
    VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value,
    G_value, room,
    start_date, end_date,
    ):
    traces_hr = []
    import time
    start_time = time.time()
    #
    D = D_value
    F = F_value
    D_F = '{}_{}'.format(D_value, F_value)
    W_value = '{}{}'.format(W1_value, W2_value)
    D_F_W = '{}_{}_{}'.format(D_value, F_value, W_value)
    #
    table = '{}_{}_HR'.format(D, SIM_JOBS)
    conn_sqlite = sqlite_connector( file='ALL_{}_HR.sqlite'.format(SIM_JOBS) )
    df_ep_hr = pd.read_sql_query(
        con = conn_sqlite,
        sql = """SELECT * FROM {table}
            WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
            AND `{Ncol}` = '{N}'
            AND `{vBcol}` = '{VNT_B}' AND `{vKLcol}` = '{VNT_KL}'
            AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
            AND `{Gcol}` = '{G}'
            ;""".format(
                table=table,
                Wcol=Wcol, W=W_value,   Fcol=Fcol, F=F_value, Ncol=Ncol, N=N_value,
                vBcol=vBcol, VNT_B=VNT_B_value, vKLcol=vKLcol, VNT_KL=VNT_KL_value,
                wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                Gcol=Gcol, G=G_value,
                ),
        )
    df_ep_hr['datetime'] = pd.to_datetime(df_ep_hr['datetime'])
    df_ep_hr.set_index('datetime', inplace=True)
    df_ep_hr.sort_index(axis=0, inplace=True)
    #    
    df_ep_hr = df_ep_hr[start_date:end_date]
    print(df_ep_hr.shape)
    #
    traces_hr = dash_HR_add_traces_EP(
        df=df_ep_hr,
        group='ROASST',
        room=room,
        linewidth=1.5,
        )

    traces_hr += dash_HR_add_traces_EXT(
        df=df_ep_hr,
        group='EXT',
        linewidth=1.5,
        )    

    # print(df_ep_hr['TM59_Tmax'][:5])

#####

    # DBS - HOURLY SIMRES
    try:
        # SQLite (superseded)
        # file = 'DSB/DSB_{}_HR.sqlite'.format(D)
        # conn_sqlite = sqlite_connector(file=file)
        table = 'DSBYZ_{}_HR'.format(D)
        df_dsb_hr = pd.read_sql_query(
            con = conn_mysql,
            sql = """SELECT * FROM {table}
            WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}' AND `{Ncol}` = '{N}'
            """.format(
                table=table,
                Wcol=Wcol, W=W_value, Fcol=Fcol,F=F_value, Ncol=Ncol,N=N_value,
                )
            )
        df_dsb_hr['datetime'] = pd.to_datetime(df_dsb_hr['datetime'])
        df_dsb_hr.set_index('datetime', inplace=True)
        #
        df_dsb_hr = df_dsb_hr[start_date:end_date]
        #
        traces_hr += dash_HR_add_traces(
            df=df_dsb_hr,
            group='DSBYZ',
            room=room,
            linewidth=1.2,
            dash_style='dashdot'
            )
    except:
        'Do nothing'
    print('\n\t{0:.3f} seconds'.format(time.time()-start_time) )

#####
    # IES - HOURLY SIMRES    
    D_F_W_N = '{}_{}_{}_{}'.format(D_value, F_value, W_value, N_value)
    try:
        # SQLite (superseded)
        # file = 'IES/IES_{}_HR.sqlite'.format(D)
        # conn_sqlite = sqlite_connector(file=file)
        #
        table = 'IES_{}_HR'.format(D)
        df_ies_hr = pd.read_sql_query(
            con = conn_mysql,
            sql = """SELECT * FROM {table}
            WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}' AND `{Ncol}` = '{N}'
            """.format(
                table=table,
                Wcol=Wcol, W=W_value, Fcol=Fcol,F=F_value, Ncol=Ncol,N=N_value,
                )
            )
        df_ies_hr['datetime'] = pd.to_datetime(df_ies_hr['datetime'])
        df_ies_hr.set_index('datetime', inplace=True)
        df_ies_hr = df_ies_hr[start_date:end_date]
        #
        traces_hr += dash_HR_add_traces(
            df=df_ies_hr,
            group='IES',
            room=room,
            linewidth=1.2,
            dash_style='dot',
            )
    except:
        'Do nothing'
    print('\n\t{0:.3f} seconds'.format(time.time()-start_time) )


    #####
    layout_hr = create_layout_EP_IES_HR(D_value=D_value, F_value=F_value, room=room)
    fig_hr = go.Figure(
        data=traces_hr,
        layout=layout_hr,
        )
    return fig_hr





port = 200
#
print('Dash on port: {}'.format(port))
dash_url = "http://127.0.0.1:{}/".format(port)

#
import webbrowser  
webbrowser.open(
    dash_url,
    new=1,
    autoraise=True)


if __name__ == '__main__':
    app.run_server(
        port=port,
        debug=False)
