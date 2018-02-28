import pandas as pd, numpy as np
from pandas import *
import datetime as dt

# ROASST
# from dash_utils.dash_lib_sql_query import *
# from dash_utils.dash_lib_viz_menus import *
# from dash_utils.dash_lib_viz_charts_HR import *

# from ..roasst.app import app
# from ..roasst import urls

from config import *
from modules import *
from menus import *
from charts_HR import *
from page_title import page_title




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
df_sji_csv = pd.read_csv( os.path.join(DATA_FOLDER_PATH, str(SIM_JOBS), 'SimJobIndex.csv') )
df_sji_csv = process_sji(df=df_sji_csv)

#
input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_unit(menu_id='D_input(p2)', cols='two', menu_type='radio',
            DWELLINGS=DWELLINGS),
        dash_create_menu_weather(menu_id=['W1_input(p2)','W2_input(p2)'], cols='one',
            WEATHER_FILES=WEATHER_FILES),
        dash_create_menu_floor(menu_id='F_input(p2)', cols='one',
            df=df_sji_csv),
        dash_create_menu_north(menu_id='N_input(p2)',  cols='one',
            df=df_sji_csv,),
        dash_create_menu_vnt(menu_id=['VNT_KL_input(p2)','VNT_B_input(p2)'], cols='two',
            df=df_sji_csv),
        dash_create_menu_window_width(menu_id=['WW_KL_input(p2)','WW_B_input(p2)'], cols='one',
            df=df_sji_csv),
        dash_create_menu_glazing(menu_id='G_input(p2)', cols='one', df=df_sji_csv),
        dash_create_menu_rooms(menu_id='R_input(p2)', cols='one', ROOMS=ROOMS),
        dash_create_menu_daterange(cols='one'),
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
    df_sji = query_sqlite_sji(
        db_folder=str(SIM_JOBS),
        db_name=D_F, table='SimJobIndex',
        )
    #
    VNT_KL_list = df_sji['@vnt_KL(m3/s)'].unique()
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
    df_sji = query_sqlite_sji(
        db_folder=str(SIM_JOBS),
        db_name=D_F, table='SimJobIndex',
        )
    #
    VNT_B_list = df_sji['@vnt_B(m3/s)'].unique()
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
        Input('RangeSlider_month', 'value'), 
    ]
    )


def update_chart_scatter_hr(
    D_value, W1_value, W2_value,
    F_value, N_value,
    VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value,
    G_value, room,
    range_month,
    ):
    
    import time
    start_time = time.time()

    D = D_value
    F = F_value
    D_F = '{}_{}'.format(D_value, F_value)
    W_value = '{}{}'.format(W1_value, W2_value)

    # FILTERING DATA
    df_sji = query_sqlite_sji(
        db_folder=str(SIM_JOBS),
        db_name=D_F, table='SimJobIndex',
        )
    df = df_sji
    # print(df_sji[:3])
    print('{}|{}|{}|{}|{}|{}'.format(W_value, D_value, F_value, N_value, VNT_KL_value, VNT_B_value))
    df_EP_JOB = df[
        (df['@weather'] == W_value) & (df['@floor'] == F_value) & (df['@north'] == N_value) &
        (df['@vnt_B(m3/s)'] == VNT_B_value) & (df['@vnt_KL(m3/s)'] == VNT_KL_value) &
        (df['@wwidth_B'] == WW_B_value) & (df['@wwidth_KL'] == WW_KL_value) & (df['@c_glazed'] == G_value)
    ]
    print(df_EP_JOB.shape)
    EP_JOB_ID = df_EP_JOB.iloc[0]['job_id']
    print(EP_JOB_ID)

    # EPLUS - HOURLY SIMRES
    df_ep_hr = query_sqlite_simres_hr(
        db_folder=str(SIM_JOBS),
        db_name=D_F,
        table=D_F,
        )
    df_ep_hr = df_ep_hr[df_ep_hr['job_id']==EP_JOB_ID]
    df_ep_hr.index = pd.to_datetime(df_ep_hr.index)
    df_ep_hr = df_ep_hr[datetime(1989, range_month[0], 1):datetime(1989,range_month[1],30)]
    #
    traces_hr = dash_HR_add_traces_EP(df_ep_hr=df_ep_hr, room=room, dash_style='dot')

    # IES - HOURLY SIMRES
    try:
        D_F_W = '{}_GTWDSY1'.format(D_F)
        D_F_W_N = '{}_N{}'.format(D_F_W, N_value)
        df_ies_rp = query_sqlite_simres_hr(
            db_folder='IES',
            db_name='IES_'+D_F_W, table=D_F_W_N,
            )
        df_ies_hr.index = pd.to_datetime(df_ies_hr.index)
        df_ies_hr = df_ies_hr[datetime(1989, range_month[0], 1):datetime(1989,range_month[1],30)]
        traces_hr += dash_HR_add_traces_IES(df_ies_hr=df_ies_hr, room=room, dash_style='dot')
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
