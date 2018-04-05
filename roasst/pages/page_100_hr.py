import pandas as pd, numpy as np
from pandas import *
import datetime as dt


from roasst.app import app
from roasst import urls
from ..config import *
from ..menus import *
from roasst.pages.charts_HR import *
from roasst.pages.page_title import page_title



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
SIM_TOOL, SIM_JOBS, RVX = 'JESS', 24, 'EMS_HR_RP'
SHOW_IES = False

table = 'OSJE_{}_{}_SJI'.format(D, SIM_JOBS)
df_sji = pd.read_sql_query(
    'SELECT * FROM {}'.format(table),
    app.db_conn,
    )
#


input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_textinput(
            menu_id=[
                'input_SW_D_SJ_1_p100',
                'input_SW_D_SJ_2_p100',
                'input_SW_D_SJ_3_p100',
            ],
            width='two'),
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
        dash_create_menu_glazing(menu_id='G_input_p100', col=Gcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_rooms(menu_id='R_input_p100', width='one', ROOMS=ROOMS),
        dash_create_menu_datepickerrange(width='one'),
        ],
    )

#
chart1 = html.Div(
    children=[
        dcc.Graph(
            id='scatter_hr',
            figure={},
            style={'height': '680px'},
            ),
        ],
)

#####

page_100_hr_layout = html.Div(
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
    Output('input_VNT_KL_p100', 'options'),
    [Input('input_SW_D_SJ_1_p100', 'value')]
)
def set_vnt_KL_options(SW_D_SJ_1_p100_value):
    #
    SW = SW_D_SJ_1_p100_value.split('_')[0]
    D  = SW_D_SJ_1_p100_value.split('_')[1]
    SJ = SW_D_SJ_1_p100_value.split('_')[2]
    #
    table = '{}_SJI'.format(SW_D_SJ_1_p100_value)
    df_sji = pd.read_sql_query(
        'SELECT * FROM {};'.format(table),
        app.db_conn,
        )
    #
    VNT_KL_list = df_sji[vKLcol].unique()
    VNT_KL_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_KL_list ]
    return VNT_KL_options
@app.callback(
    Output('input_VNT_KL_p100', 'value'),
    [Input('input_VNT_KL_p100', 'options')]
)
def set_vnt_KL_value(available_options):
    return available_options[0]['value'] 


#


@app.callback(
    Output('input_VNT_B_p100', 'options'),
    [Input('input_SW_D_SJ_1_p100', 'value')]
)
def set_vnt_B_options(SW_D_SJ_1_p100_value):
    #
    SW = SW_D_SJ_1_p100_value.split('_')[0]
    D  = SW_D_SJ_1_p100_value.split('_')[1]
    SJ = SW_D_SJ_1_p100_value.split('_')[2]
    #
    table = '{}_SJI'.format(SW_D_SJ_1_p100_value)
    df_sji = pd.read_sql_query(
        'SELECT * FROM {};'.format(table),
        app.db_conn,
        )
    #
    VNT_B_list = df_sji[vBcol].unique()
    VNT_B_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_B_list ]
    return VNT_B_options
#
@app.callback(
    Output('input_VNT_B_p100', 'value'),
    [Input('input_VNT_B_p100', 'options')]
)
#
def set_vnt_B_value(available_options):
    return available_options[0]['value']


#


@app.callback(
    Output('scatter_hr_100', 'figure'),
    [
        Input('input_SW_D_SJ_1_p100', 'value'),
        Input('input_SW_D_SJ_2_p100', 'value'),
        Input('input_SW_D_SJ_3_p100', 'value'),
        Input('input_W1_p100', 'value'), Input('input_W2_p100', 'value'),
        Input('input_F_p100', 'value'), Input('input_N_p100', 'value'),
        Input('input_VNT_B_p100', 'value'), Input('input_VNT_KL_p100', 'value'),
        Input('WW_B_input_p100', 'value'), Input('WW_KL_input_p100', 'value'),
        Input('G_input_p100', 'value'), Input('R_input_p100', 'value'),
        Input('date_picker_range', 'start_date'), Input('date_picker_range', 'end_date'),
    ]
    )
def update_chart_scatter_hr_100(
    SW_D_SJ_1,
    SW_D_SJ_2,
    SW_D_SJ_3,
    W1_value, W2_value,
    F_value, N_value,
    VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value,
    G_value, room,
    start_date, end_date,
    ):
    traces_hr = []
    import time
    start_time = time.time()
    #

    dict_line = {1:'dot', 2:'dash', 3:'dashdot'}
    i = 0

#
    for SW_D_SJ in [SW_D_SJ_1, SW_D_SJ_2, SW_D_SJ_3]:
        i=i+1

        SW = SW_D_SJ.split('_')[0]
        D  = SW_D_SJ.split('_')[1]
        SJ = SW_D_SJ.split('_')[2]
        #
        F = F_value

#

        if SW == 'OSJE':

            try:
                table = '{}_HR'.format(SW_D_SJ)
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
            except:
                print('{} not available'.format(table))
#               
        if SW == 'DSBJE':
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
        if SW == 'DSB' or SW == 'IES':
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

        df_hr['datetime'] = pd.to_datetime(df_hr['datetime'])
        df_hr.set_index('datetime', inplace=True)
        df_hr.sort_index(axis=0, inplace=True)
        df_hr = df_hr[start_date:end_date]
        print(df_hr.shape)
        
        traces_hr += dash_HR_add_traces(
            df=df_hr,
            group=S,
            room=room,
            linewidth=1.2,
            dash_style=dict_line[i],
            )

        print('\n\t{0:.3f} seconds'.format(time.time()-start_time) )



    #####
    layout_hr = create_layout_EP_IES_HR(D_value=D_value, F_value=F_value, room=room)
    fig_hr = go.Figure(
        data=traces_hr,
        layout=layout_hr,
        )
    return fig_hr


