#
import os
import pandas as pd, numpy as np
from pandas import *
import datetime as dt

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




# I need to query one database with simulation results to populate the menus
D = 'P1201'
SIM_JOBS = 24
platform = 'DSBJE'
#
table = 'TEMPLATE_SJI'
df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table), app.db_conn)



#####
chart_KL = html.Div(
    className='six columns',#    style={'padding': '10 10 10 10'},
    children=[
        dcc.Graph(
            id='chart_bars_KL(p3)',
            style={'height': '700px'},
            figure={},
            ),
        ],
    )
chart_BD1 = html.Div(
    className='six columns',#    style={'padding': '10 10 10 10'},
    children=[
        dcc.Graph(
            id='chart_bars_BD1(p3)',
            style={'height': '700px'},
            figure={},
            ),
        ],
    )
charts = html.Div(
    className='row',
    style={
        # 'background-color': '#F3F3F3',
        'font-family': 'overpass',
        'width': '100%',
        'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
        },
    children=[
        chart_KL,
        chart_BD1,
        ],
    )

#

input_menus = html.Div(
    className='row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size': 13,
    },
    children=[
        dash_create_menu_dwelling(
            menu_id='D_input(p3)', width='two',
            menu_type='dropdown', DWELLINGS=DWELLINGS),
        dash_create_menu_weather(
            menu_id=['W1_input(p3)', 'W2_input(p3)'], width='one',
            WEATHER_FILES=WEATHER_FILES),
        dash_create_menu_floor(
            menu_id='F_input(p3)', col=Fcol,
            width='one', df=df_sji),
        # dash_create_menu_north(menu_id='N_input(p3)',  width='one',
        #     df=df_sji,),
        dash_create_menu_vnt(
            menu_id=['VNT_KL_input(p3)', 'VNT_B_input(p3)'],
            cols=[vBcol, vKLcol], width='two', df=df_sji),
        dash_create_menu_window_width(
            menu_id=['WW_KL_input(p3)', 'WW_B_input(p3)'],
            cols=[wwBcol, wwKLcol], width='one', df=df_sji),
        dash_create_menu_glazing(
            menu_id='G_input(p3)', col=Gcol,
            width='one', df=df_sji),
        dash_create_menu_OH_criterion(
            menu_id='crit_input(p3)', width='one',
            )
    ],
)

#

page_3_layout = html.Div(
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
        charts,
        ],
    )


#


@app.callback(
    Output('chart_bars_KL(p3)', 'figure'),
    [
    Input('D_input(p3)', 'value'),
    Input('W1_input(p3)', 'value'), Input('W2_input(p3)', 'value'),
    Input('F_input(p3)', 'value'),
    Input('VNT_B_input(p3)', 'value'), Input('VNT_KL_input(p3)', 'value'),
    Input('WW_B_input(p3)', 'value'), Input('WW_KL_input(p3)', 'value'),
    Input('G_input(p3)', 'value'),
    Input('crit_input(p3)', 'value'),
    ])
def update_chart_bar_runperiod_KL(
    D_value,
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
    print(start_time)
    
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
    D_value = [D_value] if type(D_value).__name__ == 'str' else D_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #
    # table = 'ALL_{}_RP'.format(D, SIM_JOBS)
    print(D_value)

    
    df_D = pd.DataFrame()
    for D in D_value:
        F = F_value;
        D_F = '{}_{}'.format(D, F_value)

        table = '{}_{}_{}_RP'.format(platform,D, SIM_JOBS)
        print(table)
        if platform=='OSJE':
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{vBcol}` = '{VNT_B}' AND `{vKLcol}` = '{VNT_KL}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value, Fcol=Fcol, F=F_value,
                    vBcol=vBcol, VNT_B=VNT_B_value, vKLcol=vKLcol, VNT_KL=VNT_KL_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        elif platform=='DSBJE':
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value, Fcol=Fcol, F=F_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                ),
            )
        print('df_rp: {}'.format(df_rp.shape))

        # df_D = pd.concat([df_D, sel], axis=0)

        for N in NORTH:
            df_N = df_rp[ df_rp['@north']==N ]
            
            pos = dict_subplot_pos[N]
            row,col= [ int(x) for x in pos.split(',') ]    

            x = df_N['{}_{}'.format(R, crit_value)]
            y = df_N['@dwelling']
            trace_name = '{}|{}'.format(D,R)
            # x = trace_name
            trace_fill, trace_outline = assign_trace_fill_outline(D=D, R=R)
            trace_bar = go.Bar(
                x=x,
                y=y,
                xaxis='x{}'.format(row),
                yaxis='y{}'.format(col),
                orientation='h',
                # width=bar_width,
                marker=dict(
                    color=trace_fill,
                    line=dict(color=trace_outline, width=1.5),
                    ),
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
    Output('chart_bars_BD1(p3)', 'figure'),
    [
    Input('D_input(p3)', 'value'),
    Input('W1_input(p3)', 'value'), Input('W2_input(p3)', 'value'),
    Input('F_input(p3)', 'value'),
    Input('VNT_B_input(p3)', 'value'), Input('VNT_KL_input(p3)', 'value'),
    Input('WW_B_input(p3)', 'value'), Input('WW_KL_input(p3)', 'value'),
    Input('G_input(p3)', 'value'),
    Input('crit_input(p3)', 'value'),
    ])
def update_chart_bar_runperiod_BD1(
    D_value,
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
    print(start_time)
    
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
    D_value = [D_value] if type(D_value).__name__ == 'str' else D_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #
    # table = 'ALL_{}_RP'.format(D, SIM_JOBS)
    print(D_value)

    
    df_D = pd.DataFrame()
    for D in D_value:
        F = F_value;
        D_F = '{}_{}'.format(D, F_value)

        table = '{}_{}_{}_RP'.format(platform,D, SIM_JOBS)
        print(table)
        if platform=='OSJE':
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{vBcol}` = '{VNT_B}' AND `{vKLcol}` = '{VNT_KL}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    AND `{Gcol}` = '{G}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value, Fcol=Fcol, F=F_value,
                    vBcol=vBcol, VNT_B=VNT_B_value, vKLcol=vKLcol, VNT_KL=VNT_KL_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                    Gcol=Gcol, G=G_value,
                ),
            )
        elif platform=='DSBJE':
            df_rp = pd.read_sql_query(
                con=app.db_conn,
                sql="""SELECT * FROM {table}
                    WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                    AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
                    ;""".format(
                    table=table,
                    Wcol=Wcol, W=W_value, Fcol=Fcol, F=F_value,
                    wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
                ),
            )
        print('df_rp: {}'.format(df_rp.shape))

        # df_D = pd.concat([df_D, sel], axis=0)

        for N in NORTH:
            df_N = df_rp[ df_rp['@north']==N ]
            
            pos = dict_subplot_pos[N]
            row,col= [ int(x) for x in pos.split(',') ]    

            x = df_N['{}_{}'.format(R, crit_value)]
            y = df_N['@dwelling']
            trace_name = '{}|{}'.format(D,R)
            # x = trace_name
            trace_fill, trace_outline = assign_trace_fill_outline(D=D, R=R)
            trace_bar = go.Bar(
                x=x,
                y=y,
                xaxis='x{}'.format(row),
                yaxis='y{}'.format(col),
                orientation='h',
                # width=bar_width,
                marker=dict(
                    color=trace_fill,
                    line=dict(color=trace_outline, width=1.5),
                    ),
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

