import os, sys
import pandas as pd, numpy as np
from pandas import *
#


# PLOTLY
import plotly
from plotly import tools
plotly.tools.set_credentials_file(username='a.botti', api_key='MpDq2yINla4zb0TUd7qo')
import plotly.plotly as py, plotly.graph_objs as go
# DASH
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

# ROASST
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from config import *
from menus import *
from page_title import page_title
from charts_HR import *
from charts_RP import *
from app import *




#####
bar_width = 0.8
bar_gap = 1
bar_group_gap = 0
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
D = 'P1201'
SIM_JOBS = 24

table = 'OSJE_{}_{}_SJI'.format(D, SIM_JOBS)
df_sji = pd.read_sql_query(
    'SELECT * FROM {}'.format(table),
    app.db_conn,
    )
print(df_sji[:2])

#####

dashapp = dash.Dash()
dashapp.config.supress_callback_exceptions = True
# CSS
external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-apps-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css",
                "https://codepen.io/chriddyp/pen/bWLwgP.css"]
[dashapp.css.append_css({"external_url": css}) for css in external_css]
if 'DYNO' in os.environ:
    dashapp.scripts.append_script({'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'})


#
TABLES = []
q = app.db_conn.execute('SHOW TABLES')
for (table_name,) in q.fetchall():
        TABLES.append(table_name)
print(TABLES)

#



input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_table(
            tables=TABLES,
            menu_id=['input_T1_p100','input_T2_p100','input_T3_p100'],
            width='two',
            ),
        # dash_create_menu_dwelling_textinput(
        #     menu_id=[
        #         'input_SW_D_SJ_1_p100',
        #         'input_SW_D_SJ_2_p100',
        #         'input_SW_D_SJ_3_p100',
        #     ],
        #     width='two'),
        # dash_create_menu_dwelling(
        #     menu_id='input_D_p100',
        #     width='one', menu_type='radio', DWELLINGS=DWELLINGS,
        #     ),
        dash_create_menu_weather(
            menu_id=['input_W1_p100','input_W2_p100'],
            widths=['one','one'], WEATHER_FILES=WEATHER_FILES,
            ),
        dash_create_menu_floor(menu_id='input_F_p100', col=Fcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_north(menu_id='input_N_p100', col=Ncol,
            width='one', df=df_sji,
            ),
        dash_create_menu_vnt(menu_id=['input_VNT_KL_p100','input_VNT_B_p100'],
            cols=[vBcol,vKLcol], width='two', df=df_sji,
            ),
        dash_create_menu_window_width(menu_id=['WW_KL_input_p100','WW_B_input_p100'],
            cols=[wwBcol,wwKLcol], width='one', df=df_sji,
            ),
        dash_create_menu_glazing(menu_id='input_G_p100', col=Gcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_rooms(menu_id='R_input_p100', width='one', ROOMS=ROOMS),
        dash_create_menu_datepickerrange(width='one'),
        ],
    )

#
chart_HR_scatter = html.Div(
    children=[
        dcc.Graph(
            id='100_hr_LineChart',
            figure={},
            style={'height': '680px'},
            ),
        ],
)

#####

dashapp.layout = html.Div(
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
        chart_HR_scatter,
        ],
    )


@dashapp.callback(
    Output('100_hr_LineChart', 'figure'),
        [
        Input('input_T1_p100', 'value'),
        Input('input_T2_p100', 'value'),
        Input('input_T3_p100', 'value'),
        Input('input_W1_p100', 'value'), Input('input_W2_p100', 'value'),
        Input('input_F_p100', 'value'), Input('input_N_p100', 'value'),
        Input('input_VNT_B_p100', 'value'), Input('input_VNT_KL_p100', 'value'),
        Input('WW_B_input_p100', 'value'), Input('WW_KL_input_p100', 'value'),
        Input('input_G_p100', 'value'), Input('R_input_p100', 'value'),
        Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date'),
        ]
    )


def update_chart_scatter_hr(
    T1_value, T2_value, T3_value,
    W1_value, W2_value,
    F_value, N_value,
    VNT_B_value, VNT_KL_value,
    WW_B_value, WW_KL_value,
    G_value, room,
    start_date, end_date,
    ):
    traces_hr = []
    
    import time
    start_time = time.time()
#
    F = F_value
    W_value = '{}{}'.format(W1_value, W2_value)

#
    dict_line = {1:'dot', 2:'dash', 3:'dashdot'}
    i = 0
    for SW_D_SJ in [T1_value, T2_value, T3_value]:
        print(SW_D_SJ)
        i=i+1

        # try:
        SW = SW_D_SJ.split('_')[0]
        D  = SW_D_SJ.split('_')[1]
        SJ = SW_D_SJ.split('_')[2]
        # except:
        #     'Do nothing'

#
        df_hr = pd.DataFrame()
        if SW == 'OSJE':

            # try:
            table = '{}_HR'.format(SW_D_SJ)
            print('reading table: {}'.format(table))
            df_hr = pd.read_sql_query(
                con = app.db_conn,
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
            #
            traces_hr += dash_HR_add_traces_EXT(
                df=df_hr,
                group='EXT',
                linewidth=1.5,
                )    
            # except:
            #     print('{} not available'.format(table))
#               
        elif SW == 'DSBJE':
            try:
                table = '{}_HR'.format(SW_D_SJ)
                df_hr = pd.read_sql_query(
                    con = app.db_conn,
                    sql = """SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}' AND `{Ncol}` = '{N}'
                    """.format(table=table,
                        Wcol=Wcol, W=W_value, Fcol=Fcol,F=F_value, Ncol=Ncol,N=N_value,
                        ),
                    )
            except:
                print('{} not available'.format(table))
#
        elif SW == 'DSB' or SW == 'IES':
            try:
                table = '{}_{}_HR'.format(SW, D)
                df_hr = pd.read_sql_query(
                    con = app.db_conn,
                    sql = """SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}' AND `{Ncol}` = '{N}'
                    """.format(table=table,
                        Wcol=Wcol, W=W_value, Fcol=Fcol,F=F_value, Ncol=Ncol,N=N_value,
                        ),
                    )
            except:
                print('{} not available'.format(table))

#
        print(df_hr[:2])
        df_hr['datetime'] = pd.to_datetime(df_hr['datetime'])
        df_hr.set_index('datetime', inplace=True)
        df_hr.sort_index(axis=0, inplace=True)
        df_hr = df_hr[start_date:end_date]
        print(df_hr.shape)
        
        traces_hr += dash_HR_add_traces(
            df=df_hr,
            group=SW,
            room=room,
            linewidth=1.2,
            dash_style=dict_line[i],
            )

        print('\n\t{0:.3f} seconds'.format(time.time()-start_time) )


    
    layout_hr = create_layout_HR_comparison()
    fig_hr = go.Figure(
        data=traces_hr,
        layout=layout_hr,
        )
    return fig_hr





#####

# @dashapp.callback(
#     Output('input_VNT_KL_p100', 'options'),
#     [Input('input_T1_p100', 'value')]
# )
# def set_vnt_KL_options(T1_value):
#     #
#     SW = T1_value.split('_')[0]
#     D  = T1_value.split('_')[1]
#     SJ = T1_value.split('_')[2]
#     #
#     table = '{}_SJI'.format(T1_value.rsplit('_',1)[0])
#     df_sji = pd.read_sql_query(
#         'SELECT * FROM {};'.format(table),
#         app.db_conn,
#         )
#     #
#     VNT_KL_list = df_sji[vKLcol].unique()
#     VNT_KL_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_KL_list ]
#     return VNT_KL_options
# #
# @dashapp.callback(
#     Output('input_VNT_KL_p100', 'value'),
#     [Input('input_VNT_KL_p100', 'options')]
# )
# def set_vnt_KL_value(available_options):
#     return available_options[0]['value'] 


#


# @dashapp.callback(
#     Output('input_VNT_B_p100', 'options'),
#     [Input('input_T1_p100', 'value')]
# )
# def set_vnt_B_options(T1_value):
#     #
#     SW = T1_value.split('_')[0]
#     D  = T1_value.split('_')[1]
#     SJ = T1_value.split('_')[2]
#     #
#     table = '{}_SJI'.format(T1_value.rsplit('_',1)[0])
#     df_sji = pd.read_sql_query(
#         'SELECT * FROM {};'.format(table),
#         app.db_conn,
#         )
#     #
#     VNT_B_list = df_sji[vBcol].unique()
#     VNT_B_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_B_list ]
#     return VNT_B_options
# #
# @dashapp.callback(
#     Output('input_VNT_B_p100', 'value'),
#     [Input('input_VNT_B_p100', 'options')]
# )
# def set_vnt_B_value(available_options):
#     return available_options[0]['value']


#






port = 1000
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
    dashapp.run_server(
        port=port,
        debug=False)

