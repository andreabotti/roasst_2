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
NORTH = [0, 45, 90, 135, 180, 225, 270, 315]
N_angle_dict = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}
#
SYMBOLS = [
    "circle", "circle-open", "circle-dot", "circle-open-dot",
    "square", "square-open", "square-dot", "square-open-dot",
    "diamond", "diamond-open", "diamond-dot", "diamond-open-dot",
    "cross", "cross-open", "cross-dot", "cross-open-dot", "x", "x-open", "x-dot", "x-open-dot",
    "triangle-up", "triangle-up-open", "triangle-up-dot", "triangle-up-open-dot", "triangle-down",
    "triangle-down-open", "triangle-down-dot", "triangle-down-open-dot", "triangle-left",
    "triangle-left-open", "triangle-right", "triangle-right-open", "triangle-right-dot",
    "triangle-right-open-dot"
]

#

plot_m = [50, 20, 20, 60, 0]  # l=20, r=20, b=20, t=50, pad=0

dict_subplot_pos = {
    315: '1,1',  # NW
    0: '1,2',  # N
    45: '1,3',  # NE
    270: '2,1',  # W
    90: '2,3',  # E
    225: '3,1',  # SW
    180: '3,2',  # S
    135: '3,3',  # SE
}
#


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
    className='eight columns',  # style={'padding': '10 10 10 10'},
    children=[
        dcc.Graph(
            id='RP_POLAR_RP_BarChart_KL', style={'height': '1000px'},
            figure={},
        ),
    ],
)
chart_BD1 = html.Div(
    className='four columns',  # style={'padding': '10 10 10 10'},
    children=[
        dcc.Graph(id='RP_POLAR_RP_BarChart_BD1', style={'height': '800px'}, figure={}, ),
    ],
)
charts = html.Div(
    # className='row',
    # style={
    #     'font-family': 'overpass', 'width': '100%',
    #     'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
    #     },
    children=[
        chart_KL,
        chart_BD1,
    ],
)

#
app.scripts.config.serve_locally = True
input_menus = html.Div(
    # className='row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size': 12,
    },
    children=[
        dash_create_menu_table_1field(
            tables=TABLES_RP, multi=True,
            menu_id='input_T1_RP_POLAR',
            width='row', height='300px'
        ),
        html.Hr(
            style={'margin': '0 0 0 0'},
        ),
        dash_create_menu_weather(
            menu_id=['input_W1_RP_POLAR', 'input_W2_RP_POLAR'],
            width='row', WEATHER_FILES=WEATHER_FILES,
        ),
        html.Hr(
            style={'margin': '0 0 0 0'},
        ),
        dash_create_menu_radio_floor(
            menu_id='input_F_RP_POLAR', col=Fcol,
            width='row', df=df_sji,
        ),
        dash_create_menu_vnt(df=df_sji,
                             menu_id=['input_VNT_KL_RP_POLAR', 'input_VNT_B_RP_POLAR'],
                             cols=[vBcol, vKLcol],
                             width='row',
                             ),
        html.Hr(
            style={'margin': '0 0 0 0'},
        ),
        dash_create_menu_window_width(df=df_sji,
                                      menu_id=['input_WW_KL_RP_POLAR', 'input_WW_B_RP_POLAR'],
                                      cols=[wwBcol, wwKLcol],
                                      width='row',
                                      ),
        html.Hr(
            style={'margin': '0 0 0 0'},
        ),
        dash_create_menu_glazing(df=df_sji,
                                 menu_id='input_G_RP_POLAR', col=Gcol,
                                 width='row',
                                 ),
        html.Hr(
            style={'margin': '0 0 0 0'},
        ),
        dash_create_menu_OH_criterion(
            menu_id='input_crit_RP_POLAR',
            width='row',
        ),
    ],
)

#
RP_POLAR_layout = html.Div(
    className='row',
    style={
        # 'font-family': 'overpass',  # 'font-size':11,
        'height': '100%',  # '1000px',
        'width': '100%',  # 'max-width': '1800',
        'margin': '0 0 0 0', 'padding': '0 0 0 0',
    },

    children=[
        html.Div(
            className='two columns',
            style={
                'background-color': '#F3F3F3',
                # 'font-size': 11,
                'font-family': 'overpass',  # 'font-size':11,
                # 'height': '1000px', 'width': '100%',    # 'max-width': '1800',
                'margin': '0 0 0 0', 'padding': '0 0 0 0',
            },
            children=[input_menus],
        ),
        html.Div(
            className='ten columns',
            children=[
                html.H5('CHARTS'),
                charts,
            ],
        ),
    ]
)


def polar_factory(domain_x, domain_y):
    return dict(
        domain=dict(
            x=domain_x,
            y=domain_y,
        ),
        angularaxis=dict(
            tickwidth=3,
            tickcolor="#DDDDDD",
            linewidth=3,
            linecolor="#DDDDDD",
            rotation=90,
            direction="clockwise",
        ),
        radialaxis=dict(
            range=[0, 18],
            dtick=3,
            showline=True,
            linewidth=0,
            linecolor="#E7E7E7",
            tickwidth=0,
            gridwidth=2,
            gridcolor="#ECECEC",
            layer="below traces",
        )
    )


@app.callback(
    Output('RP_POLAR_RP_BarChart_KL', 'figure'),
    [
        Input('input_T1_RP_POLAR', 'value'),
        Input('input_W1_RP_POLAR', 'value'), Input('input_W2_RP_POLAR', 'value'),
        Input('input_F_RP_POLAR', 'value'),
        Input('input_VNT_B_RP_POLAR', 'value'), Input('input_VNT_KL_RP_POLAR', 'value'),
        Input('input_WW_B_RP_POLAR', 'value'), Input('input_WW_KL_RP_POLAR', 'value'),
        Input('input_G_RP_POLAR', 'value'),
        Input('input_crit_RP_POLAR', 'value'),
    ])
def update_RP_POLAR_Polar_RP_KL(
        T_value,
        W1_value, W2_value,
        F_value,
        VNT_B_value, VNT_KL_value,
        WW_B_value, WW_KL_value,
        G_value,
        crit_value,
):
    import time
    start_time = time.time()

    #
    R = 'KL'
    RP_POLAR_chart_data = []
    RP_POLAR_chart_layout = go.Layout(
        font=dict(
            family='Calibri,sans-serif',
            size=12,
            color='grey',
        ),
        showlegend=True,
    )

    N_angle_dict = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}
    #    
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #
    width = 1 / len(T_value)
    spacing = 0.02
    cum_width = 0

    for i, T in enumerate(T_value, start=1):
        domain_x = [round(cum_width + spacing, 2), round(cum_width + width, 2)]
        domain_y = [0, 1]
        cum_width += width + spacing
        polar_id = "polar%i" % i
        RP_POLAR_chart_layout[polar_id] = polar_factory(domain_x, domain_y)

        D = T.split('_')[0]
        SWSJ = T.split('_')[1]
        table = T
        print(table)
        if 'IES' in T:
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value,
                    Fcol=Fcol, F=F_value,
                ),
            )

        elif 'OSJE' in T:
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
                    WHERE `{Wcol}` = '{W}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        print('df_rp: {}'.format(df_rp.shape))

        df_rp_GF = df_rp[df_rp['@floor'] == 'GF']
        df_rp_MF = df_rp[df_rp['@floor'] == 'MF']
        df_rp_TF = df_rp[df_rp['@floor'] == 'TF']

        col = '{}_{}'.format(R, crit_value)
        # import random
        # marker_symbol = random.choice(SYMBOLS)
        marker_symbol = 'circle'
        marker_size = 15
        color_scales = cl.scales['12']['qual']['Paired']
        marker_color = DICT_COLOR[D.split('do')[0]] if 'do' in D else DICT_COLOR[D]

        # GF
        radius = df_rp_GF[col]
        theta = df_rp_GF['@north']
        trace_GF = go.Scatterpolar(
            r=radius, theta=theta, mode='markers',
            name=D,
            marker=dict(
                # line=dict(width=2, color = marker_color),
                color=marker_color,
                size=marker_size,
                opacity=0.5,
                symbol=marker_symbol,
            ),
            legendgroup=D,
            cliponaxis=False,
            subplot=polar_id,
        )
        RP_POLAR_chart_data.append(trace_GF)

        # MF
        radius = df_rp_MF[col]
        theta = df_rp_MF['@north']
        trace_MF = go.Scatterpolar(
            r=radius, theta=theta,
            mode='markers',
            name=D,
            marker=dict(
                # line=dict(width=2, color = marker_color),
                color=marker_color,
                size=marker_size,
                opacity=0.7,
                symbol=marker_symbol,
            ),
            legendgroup=D,
            cliponaxis=False,
            subplot=polar_id,
        )
        RP_POLAR_chart_data.append(trace_MF)

        # MF
        radius = df_rp_TF[col]
        theta = df_rp_TF['@north']
        trace_TF = go.Scatterpolar(
            r=radius, theta=theta,
            mode='markers',
            # fill = 'toself',
            name=D,
            marker=dict(
                # line=dict(width=2, color = marker_color),
                color=marker_color,
                size=marker_size,
                opacity=0.7,
                symbol=marker_symbol,
            ),
            legendgroup=D,
            cliponaxis=False,
            subplot=polar_id,
        )
        RP_POLAR_chart_data.append(trace_TF)

    #

    RP_POLAR_chart = go.Figure(
        data=RP_POLAR_chart_data,
        layout=RP_POLAR_chart_layout)
    return RP_POLAR_chart


#


@app.callback(
    Output('RP_POLAR_RP_BarChart_BD1', 'figure'),
    [
        Input('input_T1_RP_POLAR', 'value'),
        Input('input_W1_RP_POLAR', 'value'), Input('input_W2_RP_POLAR', 'value'),
        Input('input_F_RP_POLAR', 'value'),
        Input('input_VNT_B_RP_POLAR', 'value'), Input('input_VNT_KL_RP_POLAR', 'value'),
        Input('input_WW_B_RP_POLAR', 'value'), Input('input_WW_KL_RP_POLAR', 'value'),
        Input('input_G_RP_POLAR', 'value'),
        Input('input_crit_RP_POLAR', 'value'),
    ])
def update_RP_POLAR_RP_BarChart_BD1(
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
        subplot_titles=('NW', 'N', 'NE', 'W', 'PLANS', 'E', 'SW', 'S', 'SE')
    )
    bar_subplots_rp_multiroom['layout'].update(showlegend=False)
    bar_subplots_rp_multiroom['layout'].update(
        margin=go.Margin(l=plot_m[0], r=plot_m[1], b=plot_m[2], t=plot_m[3], pad=plot_m[4]))
    #
    for i in range(1, 10):
        bar_subplots_rp_multiroom['layout']['xaxis{}'.format(i)].update(
            range=[0, 20], dtick=5, ticksuffix='%',
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

    N_angle_dict = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}
    #    
    T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #

    df_D = pd.DataFrame()
    for T in T_value:
        D = T.split('_')[0]
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
            df_N = df_rp[df_rp['@north'] == N]

            pos = dict_subplot_pos[N]
            row, col = [int(x) for x in pos.split(',')]

            if 'HA' in crit_value:
                crit = crit_value.split('_')[0]
            else:
                crit = crit_value
            #
            x = df_N['{}_{}'.format(R, crit)]
            y = df_N['@dwelling']
            trace_name = '{}|{}'.format(D, R)
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
