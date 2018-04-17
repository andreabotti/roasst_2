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

table = 'TEMPLATE_SJI'
df_sji = pd.read_sql_query(
    'SELECT * FROM {}'.format(table),
    app.db_conn,
    )
#

TABLES = []
q = app.db_conn.execute('SHOW TABLES')
for (table_name,) in q.fetchall():
        TABLES.append(table_name)
TABLES_HR = [T for T in TABLES if '_HR' in T]

#


input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_table_1field(
            tables=TABLES_HR,
            multi=True,
            menu_id='input_T1_p110',
            width='two',
            ),
        # dash_create_menu_table_3fields(
        #     tables=TABLES_HR,
        #     multi=False,
        #     menu_id=['input_T1_p110','input_T2_p110','input_T3_p110'],
        #     width='two',
        #     ),

        dash_create_menu_weather(
            menu_id=['input_W1_p110','input_W2_p110'],
            widths=['one','one'], WEATHER_FILES=WEATHER_FILES,
            ),
        dash_create_menu_floor(menu_id='input_F_p110', col=Fcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_north(menu_id='input_N_p110', col=Ncol,
            width='one', df=df_sji,
            ),
        dash_create_menu_vnt(menu_id=['input_VNT_KL_p110','input_VNT_B_p110'],
            cols=[vBcol,vKLcol], width='two', df=df_sji,
            ),
        dash_create_menu_window_width(menu_id=['input_WW_KL_p110','input_WW_B_p110'],
            cols=[wwBcol,wwKLcol], width='one', df=df_sji,
            ),
        dash_create_menu_glazing(menu_id='input_G_p110', col=Gcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_rooms(menu_id='input_R_p110', width='one', ROOMS=ROOMS),
        dash_create_menu_datepickerrange(menu_id='input_date_p110', width='one'),
        ],
    )

#
chart1 = html.Div(
    children=[
        dcc.Graph(
            id='p110_hr_LineChart',
            figure={},
            style={'height': '680px'},
            ),
        ],
)

#####

p110_layout = html.Div(
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
        # html.Hr(),
        chart1,
        ],
    )

#####

@app.callback(
    Output('input_VNT_KL_p110', 'options'),
    [
    Input('input_T1_p110', 'value'),
    # Input('input_T2_p110', 'value'),
    # Input('input_T3_p110', 'value'),
    ]
)
def set_vnt_KL_options(T_value):
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    for D_SWSJ_HR in T_value:
        try:
            D  = D_SWSJ_HR.split('_')[0]
            SW = D_SWSJ_HR.split('_')[1].split('JE')[0]
            SJ = D_SWSJ_HR.split('_')[1].split('JE')[1]
            #
            table = '{}_SJI'.format(D_SWSJ_HR.rsplit('_',1)[0])
            df_sji = pd.read_sql_query(
                'SELECT * FROM {};'.format(table),
                app.db_conn,
                )
            #
            VNT_KL_list = df_sji[vKLcol].unique()
            VNT_KL_options = [{'label': '{}'.format(x), 'value': x} for x in VNT_KL_list ]
            return VNT_KL_options
        except:
            return [{'label': '{}'.format(x), 'value': x} for x in ['none'] ]

@app.callback(
    Output('input_VNT_KL_p110', 'value'),
    [Input('input_VNT_KL_p110', 'options')]
)
def set_vnt_KL_value(available_options):
    return available_options[0]['value'] 

#

@app.callback(
    Output('input_VNT_B_p110', 'options'),
    [
    Input('input_T1_p110', 'value'),
    # Input('input_T2_p110', 'value'),
    # Input('input_T3_p110', 'value'),
    ]
)
def set_vnt_B_options(T_value):
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    for D_SWSJ_HR in T_value:
        try:
            D  = D_SWSJ_HR.split('_')[0]
            SW = D_SWSJ_HR.split('_')[1].split('JE')[0]
            SJ = D_SWSJ_HR.split('_')[1].split('JE')[1]
            #
            table = '{}_SJI'.format(D_SWSJ_HR.rsplit('_',1)[0])
            df_sji = pd.read_sql_query(
                'SELECT * FROM {};'.format(table),
                app.db_conn,
                )
            #
            VNT_B_list = df_sji[vBcol].unique()
            VNT_B_options = [{'label': '{}'.format(x), 'value': x} for x in VNT_B_list ]
            return VNT_B_options
        except:
            return [{'label': '{}'.format(x), 'value': x} for x in ['none'] ]

@app.callback(
    Output('input_VNT_B_p110', 'value'),
    [Input('input_VNT_B_p110', 'options')]
)
#
def set_vnt_B_value(available_options):
    return available_options[0]['value']


#


@app.callback(
    Output('p110_hr_LineChart', 'figure'),
    [
        Input('input_T1_p110', 'value'),
        # Input('input_T2_p110', 'value'),
        # Input('input_T3_p110', 'value'),
        Input('input_W1_p110', 'value'), Input('input_W2_p110', 'value'),
        Input('input_F_p110', 'value'), Input('input_N_p110', 'value'),
        Input('input_VNT_B_p110', 'value'), Input('input_VNT_KL_p110', 'value'),
        Input('input_WW_B_p110', 'value'), Input('input_WW_KL_p110', 'value'),
        Input('input_G_p110', 'value'), Input('input_R_p110', 'value'),
        Input('input_date_p110', 'start_date'), Input('input_date_p110', 'end_date'),
    ]
    )
def update_chart_scatter_p110(
    # T1_value,
    # T2_value,
    # T3_value,
    T_value,
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
    dict_line = {1:'', 2:'dot', 3:'dash', 4:'dashdot'}
    i = 0
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    # for D_SWSJ_HR in [T1_value, T2_value, T3_value]:
    for D_SWSJ_HR in T_value:
        print(D_SWSJ_HR)
        i=i+1

        try:
            D  = D_SWSJ_HR.split('_')[0]
            SWSJ = D_SWSJ_HR.split('_')[1]
            # SW = D_SWSJ_HR.split('_')[1].split('JE')[0]
            # SJ = D_SWSJ_HR.split('_')[1].split('JE')[1]

    #
            # df_hr = pd.DataFrame()
            if 'OSJE' in SWSJ:

                table = D_SWSJ_HR
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
                df_hr['datetime'] = pd.to_datetime(df_hr['datetime'])
                df_hr.set_index('datetime', inplace=True)
                df_hr.sort_index(axis=0, inplace=True)
                df_hr = df_hr[start_date:end_date]
                print(df_hr.shape)

                traces_hr += dash_HR_add_traces_EXT(
                    df=df_hr,
                    group='EXT',
                    linewidth=1.5,
                    )    
                traces_hr += dash_HR_add_traces(
                    df=df_hr,
                    group=SWSJ,
                    room=room,
                    linewidth=1.2,
                    dash_style=dict_line[i],
                    )
    #

            else:

                table = D_SWSJ_HR
                df_hr = pd.read_sql_query(
                    con = app.db_conn,
                    sql = """SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}' AND `{Ncol}` = '{N}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    """.format(table=table,
                        Wcol=Wcol, W=W_value, Fcol=Fcol,F=F_value, Ncol=Ncol,N=N_value,
                        wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                        Gcol=Gcol, G=G_value,
                        ),
                    )
#
                df_hr['datetime'] = pd.to_datetime(df_hr['datetime'])
                df_hr.set_index('datetime', inplace=True)
                df_hr.sort_index(axis=0, inplace=True)
                df_hr = df_hr[start_date:end_date]
                print(df_hr.shape)
                
                traces_hr += dash_HR_add_traces(
                    df=df_hr,
                    group=SWSJ,
                    room=room,
                    linewidth=1.2,
                    dash_style=dict_line[i],
                    )
        except:
            print('Data not available')

        print('\n\t{0:.3f} seconds'.format(time.time()-start_time) )



    #####
    layout_hr = create_layout_EP_IES_HR(D_value=D, F_value=F, room=room)
    fig_hr = go.Figure(
        data=traces_hr,
        layout=layout_hr,
        )
    return fig_hr


