#
import os
import pandas as pd, numpy as np
from pandas import *
# import datetime as dt
import dash_table_experiments
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

input_menus = html.Div(
    # className='row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size': 12,
    },
    children=[
        dash_create_menu_table_1field(
            tables=TABLES_RP, multi=True,
            menu_id='input_T1_P252',
            width='row', height='300px'
            ),
        html.Hr(
            style={'margin': '0 0 0 0'},
            ),
        dash_create_menu_weather(
            menu_id=['input_W1_P252','input_W2_P252'],
            width='row', WEATHER_FILES=WEATHER_FILES,
            ),
        html.Hr(
            style={'margin': '0 0 0 0'},
            ),
        dash_create_menu_floor(
            menu_id='input_F_P252', col=Fcol,
            width='row', df=df_sji,
            ),
        dash_create_menu_vnt(df=df_sji,
            menu_id=['input_VNT_KL_P252','input_VNT_B_P252'],
            cols=[vBcol,vKLcol],
            width='row', 
            ),
        html.Hr(
            style={'margin': '0 0 0 0'},
            ),
        dash_create_menu_window_width(df=df_sji,
            menu_id=['input_WW_KL_P252','input_WW_B_P252'],
            cols=[wwBcol,wwKLcol],
            width='row',
            ),
        html.Hr(
            style={'margin': '0 0 0 0'},
            ),
        dash_create_menu_glazing(df=df_sji,
            menu_id='input_G_P252', col=Gcol,
            width='row', 
            ),
        html.Hr(
            style={'margin': '0 0 0 0'},
            ),
        dash_create_menu_OH_criterion(
            menu_id='input_crit_P252',
            width='row',
            ),
    ],
)

#
col_sel = [
    Dcol,
    Wcol,
    Ncol,
    Fcol,
    # vBcol, vKLcol,
    wwBcol, wwKLcol,
    'KL_TM59_Ca','BD1_TM59_Ca', #'BD1_TM59_Cb',
    # 'KL_HA26p','BD1_HA26p',
    ]
#
P252_table = html.Div(
    # className='row',
    # style={
    #     'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
    #     'font-size':11,
    #     'font-family': 'overpass',
    #     },
    children = [
        dash_table_experiments.DataTable(
            id='P252_dyn_table',
            # min_height=600,
            # rows=[{}],
            rows=df_sji.to_dict('records'),
            # selected_row_indices=[],
            # columns=col_sel,
            # row_selectable=True,
            # filterable=True,
            # sortable=True,
            # header_row_height=35,
            # row_update=True,
            ),
        ],
    )
#
P252_chart = html.Div(
    className='row',
    children=[
        dcc.Graph(
            id='P252_RP_BarChart_KL',
            style={'height': '350px',})
        ])

#

P252_layout = html.Div(
    className='row',
    style={
        # 'font-family': 'overpass',  # 'font-size':11,
        'height': '100%',    # '1000px',
        'width': '100%',    # 'max-width': '1800',
        'margin': '0 0 0 0', 'padding': '0 0 0 0',
        },

    children = [
        html.Div(
            className='two columns',
            style={
                'background-color': '#F3F3F3',
                'font-family': 'overpass',  # 'font-size':11,
                # 'height': '1000px', 'width': '100%',    # 'max-width': '1800',
                'margin': '0 0 0 0', 'padding': '0 0 0 0',
                },
            children = [ input_menus ],
            ),
        #
        html.Div(
            className='ten columns',
            children = [
                html.H5('TABLE'),
                # P252_table,
                html.H5('CHARTS'),
                P252_chart,
                ],
            ),
        ]
    )

#

# @app.callback(
#     Output('P252_dyn_table', 'selected_row_indices'),
#     [Input('P252_RP_BarChart_KL', 'clickData')],
#     [State('P252_dyn_table', 'selected_row_indices')])
# #
# def update_selected_row_indices(clickData, selected_row_indices):
#     if clickData:
#         for point in clickData['points']:
#             if point['pointNumber'] in selected_row_indices:
#                 selected_row_indices.remove(point['pointNumber'])
#             else:
#                 selected_row_indices.append(point['pointNumber'])
#     return selected_row_indices


#


# @app.callback(
#     dcc.Output('P252_dyn_table', 'rows'),
#     [
#         dcc.Input('input_T1_P252', 'value'),
#         dcc.Input('input_W1_P252', 'value'), dcc.Input('input_W2_P252', 'value'),
#     ],
#     )

# def update_table(T_value, W1_value, W2_value):

#     import time
#     start_time = time.time()
#     #
    
#     T_value = [T_value] if type(T_value).__name__ == 'str' else T_value
#     W_value = '{}{}'.format(W1_value, W2_value)
    
#     #

#     df_table = pd.DataFrame()
#     for T in T_value:
#         D  = T.split('_')[0]
#         SWSJ = T.split('_')[1]
#         table = T

#         print(table)
#         if 'OSJE' in T:
#             df_rp = pd.read_sql_query(
#                 con=app.db_conn,
#                 sql="""SELECT * FROM {table}
#                     WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
#                     AND `{vBcol}` = '{VNT_B}' AND `{vKLcol}` = '{VNT_KL}'
#                     AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
#                     AND `{Gcol}` = '{G}'
#                     ;""".format(
#                     table=table,
#                     Wcol=Wcol, W=W_value,
#                     Fcol=Fcol, F=F_value,
#                     vBcol=vBcol, VNT_B=VNT_B_value, vKLcol=vKLcol, VNT_KL=VNT_KL_value,
#                     wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
#                     Gcol=Gcol, G=G_value,
#                 ),
#             )
#             df_table = pd.concat([df_table, df_rp], axis=0)
#             df_table = df_table[ df_table['@weather'] == W_value ]
#         #
#         elif 'DSBJE' in T:
#             df_rp = pd.read_sql_query(
#                 con=app.db_conn,
#                 sql="""SELECT * FROM {table}
#                     WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
#                     AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
#                     AND `{Gcol}` = '{G}'
#                     ;""".format(
#                     table=table,
#                     Wcol=Wcol, W=W_value,
#                     Fcol=Fcol, F=F_value,
#                     wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
#                     Gcol=Gcol, G=G_value,
#                 ),
#             )
#             df_table = pd.concat([df_table, df_rp], axis=0)
#             df_table = df_table[ df_table['@weather'] == W_value ]
    
#     return df_table.to_dict('records')

# #


# #

# P252_RP_BarChart_KL_layout = go.Layout(
#     # autosize=False, width=500, height=500,
#     showlegend=False,
#     margin=go.Margin(l=100, r=20, b=40, t=40, pad=4),
#     #
#     yaxis=dict(
#         autorange = 'reversed',
#         tickfont=dict(
#                 size=10,
#                 # family='Courier New, monospace',
#                 # color='#7f7f7f',
#                 )
#             ),
#     #
#     xaxis1=dict(
#         tickfont=dict(size=11),
#         domain=[0,0.45],
#         range=[0,0.2],
#         # dtick=2,
#         showgrid=True,
#         title=r'HA26C (%)',
#         ),
#     xaxis2=dict(
#         tickfont=dict(size=11),
#         domain=[0.55,1],
#         range=[0,0.2],
#         # dtick=2,
#         showgrid=True,
#         title=r'TM59 Ca (%)',
#         ),

#     )

# @app.callback(
#     Output('P252_RP_BarChart_KL', 'figure'), 
#     [Input('P252_dyn_table', 'rows'), Input('P252_dyn_table', 'selected_row_indices')])

# def update_figure(rows, selected_row_indices):
#     dff = pd.DataFrame(rows)
#     data = go.Data([])
#     marker = {'color': ['#0074D9'] * len(dff)}
#     for i in (selected_row_indices or []):
#         marker['color'][i] = '#FF851B'
#     print(dff)
#     y = dff['@dwelling'] + '_N' + dff['@north'].astype(str)

#     data.append(
#         go.Bar(
#             x=dff['KL_HA26c'],
#             y=y,
#             xaxis='x1',
#             orientation='h',
#             marker=marker,
#             ),
#         )
#     data.append(
#         go.Bar(
#             x=dff['KL_TM59_Ca'],
#             y=y,
#             xaxis='x2',
#             orientation='h',
#             marker=marker,
#             ),
#         )

#     figure = go.Figure(
#         data=data,
#         layout=P252_RP_BarChart_KL_layout,
#     )
#     return figure