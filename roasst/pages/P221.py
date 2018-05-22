#
import os
import pandas as pd, numpy as np
from pandas import *
import datetime as dt
import json

from roasst.app import app
from roasst.config import *
from roasst.menus import *
from roasst.pages.charts_RP import *
from roasst.pages.page_title import page_title


#####
NORTH = [0,45,90,135,180,225,270,315]
N_angle_dict = {0:'N',45:'NE',90:'E',135:'SE',180:'S',225:'SW',270:'W',315:'NW'}
#
UNITS = ['P1201' ,'P1202','P1203', 'P1204A', 'P2301','P2302','P2303','P2304']
FLOORS = ['MF']
WEATHER_FILES = ['GTWDSY1','LHRDSY1', 'LWCDSY1']
ROOMS = ['KL', 'BD1']
#

plot_m = [50,20,20,60,0]    # l=20, r=20, b=20, t=50, pad=0

dict_subplot_pos = {
    315:'1,1',   # NW
    0:'1,2',    # N
    45:'1,3',   # NE
    270:'2,1',  # W
    90:'2,3',  # E
    225:'3,1', # SW
    180:'3,2',  # S
    135:'3,3', # SE
}
# COLOR DICTIONARY
d_color = {
    'P1201':'#328674', 'P1201$B1':'#5E976E', 'P1201$B2':'#75a3a3',
    'P1202':'#5E976E',
    'P1203':'#FAA222',
    'P1204A':'#D17C20',
    'P2301':'#D5661A',
    'P2302':'#75a3a3',
    'P2303':'#712D19',
    'P2304':'#863D52',
    }
# print(d_color)

def assign_trace_fill_outline(D, R):
    if R=='BD1' or R=='BS1':
            col1 = '@vnt_B(m3/s)'
            col2 = '@vnt_B(l/s)'
            trace_fill = 'rgba(0,0,0,0)'
            trace_outline = d_color[D]
    else:
        col1 = '@vnt_{}(m3/s)'.format(R)
        col2 = '@vnt_{}(l/s)'.format(R)
        trace_fill = d_color[D]
        trace_outline = 'rgba(0,0,0,0)'

    return trace_fill, trace_outline

DEFAULT_COLORSCALE = ["#2a4858", "#265465", "#1e6172", "#106e7c", "#007b84", \
    "#00898a", "#00968e", "#19a390", "#31b08f", "#4abd8c", "#64c988", \
    "#80d482", "#9cdf7c", "#bae976", "#d9f271", "#fafa6e"]

# I need to query one database with simulation results to populate the menus
D = 'P1201'
SIM_JOBS = 24
platform = 'DSBJE'
#
table = 'TEMPLATE_SJI'
df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table), app.db_conn)

#

TABLES = []
q = app.db_conn.execute('SHOW TABLES')
for (table_name,) in q.fetchall():
        TABLES.append(table_name)
TABLES_RP = [T for T in TABLES if '_RP' in T]

#

chart_KL = html.Div(
    className='six columns',#    style={'padding': '10 10 10 10'},
    children=[
        dcc.Graph(id='P221_RP_BarChart_KL',   style={'height': '650px'},  figure={},),
        ],
    )
chart_BD1 = html.Div(
    className='six columns',#    style={'padding': '10 10 10 10'},
    children=[
        dcc.Graph(id='P221_RP_BarChart_BD1',  style={'height': '650px'},  figure={},),
        ],
    )
charts = html.Div(
    className='row',
    style={
        'font-family': 'overpass', 'width': '100%',
        'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
        },
    children=[
        chart_KL,
        chart_BD1,
        ],
    )

#
app.scripts.config.serve_locally = True
input_menus = html.Div(
    className='row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size': 12,
    },
    children=[
        dash_create_menu_table_1field(
            tables=TABLES_RP, multi=True,
            menu_id='input_T1_P221',
            width='four', height='',
            ),
        dash_create_menu_weather(
            menu_id=['input_W1_P221','input_W2_P221'],
            width='one', WEATHER_FILES=WEATHER_FILES,
            ),
        dash_create_menu_radio_floor(
            menu_id='input_F_P221', col=Fcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_vnt(menu_id=['input_VNT_KL_P221','input_VNT_B_P221'],
            cols=[vBcol,vKLcol], width='two', df=df_sji,
            ),
        dash_create_menu_window_width(menu_id=['input_WW_KL_P221','input_WW_B_P221'],
            cols=[wwBcol,wwKLcol], width='one', df=df_sji,
            ),
        dash_create_menu_glazing(menu_id='input_G_P221', col=Gcol,
            width='one', df=df_sji,
            ),
        dash_create_menu_OH_criterion(
            menu_id='input_crit_P221', width='one',
            ),
        # dash_create_menu_colorscales(
        #     width='two',
        #     menu_id='input_colorscale_P221',
        #     # swatches=len(DEFAULT_COLORSCALE),
        #     swatches=7,
        #     # colorscale=DEFAULT_COLORSCALE,
        #     ),
    ],
)

#
P221_layout = html.Div(
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
        charts,
        ],
    )

#

# @app.callback(
#         Output('color_output', 'children'),
#         [Input('input_colorscale_P221', 'colorscale')])
# def display_output(colorscale):
#     return json.dumps(colorscale)

#


#
@app.callback(
    Output('P221_RP_BarChart_KL', 'figure'),
    [
        Input('input_T1_P221', 'value'),
        Input('input_W1_P221', 'value'), Input('input_W2_P221', 'value'),
        Input('input_F_P221', 'value'),
        Input('input_VNT_B_P221', 'value'), Input('input_VNT_KL_P221', 'value'),
        Input('input_WW_B_P221', 'value'), Input('input_WW_KL_P221', 'value'),
        Input('input_G_P221', 'value'),
        Input('input_crit_P221', 'value'),
    ])

def update_P221_RP_BarChart_KL(
    T_value,
    W1_value, W2_value,
    F_value,
    VNT_B_value, VNT_KL_value,
    WW_B_value, WW_KL_value,
    G_value,
    crit_value,
    ):
    
    R = 'KL'

    import time
    start_time = time.time()
    
    bar_subplots_rp_multiroom = tools.make_subplots(
        rows=3, cols=3,
        shared_xaxes=False, shared_yaxes=False,
        horizontal_spacing=0.15,
        vertical_spacing=0.1,
        subplot_titles=('NW','N','NE','W','PLANS','E','SW','S','SE')
        )
    bar_subplots_rp_multiroom['layout'].update(showlegend=False)
    bar_subplots_rp_multiroom['layout'].update(
        margin=go.Margin(l=plot_m[0], r=plot_m[1], b=plot_m[2], t=plot_m[3], pad=plot_m[4]) )
    #
    for i in range(1,10):
        bar_subplots_rp_multiroom['layout']['xaxis{}'.format(i)].update(
            range=[0,20], dtick=5, ticksuffix='%',
            tickfont=dict(
                family='Calibri,sans-serif',
                size=12,
                color='grey'
                ),
            )
        bar_subplots_rp_multiroom['layout']['yaxis{}'.format(i)].update(
            tickfont=dict(
                family='Calibri,sans-serif',
                size=12,
                color='grey'
                ),
            )

    N_angle_dict = {0:'N',45:'NE',90:'E',135:'SE',180:'S',225:'SW',270:'W',315:'NW'}
    #    
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #
    
    df_D = pd.DataFrame()
    for T in T_value:
        D  = T.split('_')[0]
        SWSJ = T.split('_')[1]
        table = T
        print(table)
        if 'OSJE' in T:
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{vBcol}` = '{VNT_B}' AND `{vKLcol}` = '{VNT_KL}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value,
                    Fcol=Fcol, F=F_value,
                    vBcol=vBcol, VNT_B=VNT_B_value, vKLcol=vKLcol, VNT_KL=VNT_KL_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        elif 'DSBJE' in T:
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value,
                    Fcol=Fcol, F=F_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        print('df_rp: {}'.format(df_rp.shape))

        # df_D = pd.concat([df_D, sel], axis=0)

        for N in NORTH:
            df_N = df_rp[ df_rp['@north']==N ]
            
            pos = dict_subplot_pos[N]
            row,col= [ int(x) for x in pos.split(',') ]    

            if 'HA' in crit_value:
                crit = crit_value.split('_')[1]
            else:
                crit = crit_value
            #
            x = df_N['{}_{}'.format(R, crit)]
            y = df_N['@dwelling']
            trace_name = '{}|{}'.format(D,R)
#
            # trace_fill, trace_outline = assign_trace_fill_outline(D=D, R=R)
#
            trace_bar = go.Bar(
                x=x,
                y=y,
                xaxis='x{}'.format(row),
                yaxis='y{}'.format(col),
                orientation='h',
                # width=bar_width,
#
                # marker=dict(
                #     color=trace_fill,
                #     line=dict(color=trace_outline, width=1.5),
                #     ),
#
                name=trace_name,
                text='<b>{}</b>'.format(R),
                textfont=dict(
                    size=10,
                    color='rgba(0,0,0,0.6)'),
                textposition='auto',
                legendgroup='{}'.format(trace_name),
                )
            bar_subplots_rp_multiroom.append_trace(trace_bar, row=row, col=col)
    

    return bar_subplots_rp_multiroom


#


@app.callback(
    Output('P221_RP_BarChart_BD1', 'figure'),
    [
        Input('input_T1_P221', 'value'),
        Input('input_W1_P221', 'value'), Input('input_W2_P221', 'value'),
        Input('input_F_P221', 'value'),
        Input('input_VNT_B_P221', 'value'), Input('input_VNT_KL_P221', 'value'),
        Input('input_WW_B_P221', 'value'), Input('input_WW_KL_P221', 'value'),
        Input('input_G_P221', 'value'),
        Input('input_crit_P221', 'value'),
    ])

def update_P221_RP_BarChart_BD1(
    T_value,
    W1_value, W2_value,
    F_value,
    VNT_B_value, VNT_KL_value,
    WW_B_value, WW_KL_value,
    G_value,
    crit_value,
    ):
    
    R = 'BD1'

    import time
    start_time = time.time()
    
    bar_subplots_rp_multiroom = tools.make_subplots(
        rows=3, cols=3,
        shared_xaxes=False, shared_yaxes=False,
        horizontal_spacing=0.15,
        vertical_spacing=0.1,
        subplot_titles=('NW','N','NE','W','PLANS','E','SW','S','SE')
        )
    bar_subplots_rp_multiroom['layout'].update(showlegend=False)
    bar_subplots_rp_multiroom['layout'].update(
        margin=go.Margin(l=plot_m[0], r=plot_m[1], b=plot_m[2], t=plot_m[3], pad=plot_m[4]) )
    #
    for i in range(1,10):
        bar_subplots_rp_multiroom['layout']['xaxis{}'.format(i)].update(
            range=[0,20], dtick=5, ticksuffix='%',
            tickfont=dict(
                family='Calibri,sans-serif',
                size=12,
                color='grey'
                ),
            )
        bar_subplots_rp_multiroom['layout']['yaxis{}'.format(i)].update(
            tickfont=dict(
                family='Calibri,sans-serif',
                size=12,
                color='grey'
                ),
            )

    N_angle_dict = {0:'N',45:'NE',90:'E',135:'SE',180:'S',225:'SW',270:'W',315:'NW'}
    #    
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #
    
    df_D = pd.DataFrame()
    for T in T_value:
        D  = T.split('_')[0]
        SWSJ = T.split('_')[1]
        table = T
        print(table)
        if 'OSJE' in T:
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{vBcol}` = '{VNT_B}' AND `{vKLcol}` = '{VNT_KL}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value,
                    Fcol=Fcol, F=F_value,
                    vBcol=vBcol, VNT_B=VNT_B_value, vKLcol=vKLcol, VNT_KL=VNT_KL_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        elif 'DSBJE' in T:
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value,
                    Fcol=Fcol, F=F_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        print('df_rp: {}'.format(df_rp.shape))

        # df_D = pd.concat([df_D, sel], axis=0)

        for N in NORTH:
            df_N = df_rp[ df_rp['@north']==N ]
            
            pos = dict_subplot_pos[N]
            row,col= [ int(x) for x in pos.split(',') ]    

            if 'HA' in crit_value:
                crit = crit_value.split('_')[0]
            else:
                crit = crit_value
            #
            x = df_N['{}_{}'.format(R, crit)]
            y = df_N['@dwelling']
            trace_name = '{}|{}'.format(D,R)
#
            # trace_fill, trace_outline = assign_trace_fill_outline(D=D, R=R)
#
            trace_bar = go.Bar(
                x=x,
                y=y,
                xaxis='x{}'.format(row),
                yaxis='y{}'.format(col),
                orientation='h',
                # width=bar_width,
#
                # marker=dict(
                #     color=trace_fill,
                #     line=dict(color=trace_outline, width=1.5),
                #     ),
#
                name=trace_name,
                text='<b>{}</b>'.format(R),
                textfont=dict(
                    size=10,
                    color='rgba(0,0,0,0.6)'),
                textposition='auto',
                legendgroup='{}'.format(trace_name),
                )
            bar_subplots_rp_multiroom.append_trace(trace_bar, row=row, col=col)
    

    return bar_subplots_rp_multiroom
