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
NORTH = [0, 45, 90, 135]  # ,180,225,270,315]
N_angle_dict = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}

#####
bar_width = 15
bar_gap = 0;
bar_group_gap = 0;
bar_mode = 'group'
#
colors_dict = {
    'HG_OSJE': 'rgba(255, 0, 0, 0.8)',
    'HG_IES': 'rgba(255, 0, 0, 0.6)',
    'HG_DSB': 'rgba(255, 0, 0, 0.45)',
    'HG_DSBJE': 'rgba(255, 0, 0, 0.45)',
    #
    'HL_OSJE': 'rgba(120, 163, 206, 0.8)',
    'HL_IES': 'rgba(120, 163, 206, 0.6)',
    'HL_DSB': 'rgba(120, 163, 206, 0.45)',
    'HL_DSBJE': 'rgba(120, 163, 206, 0.45)',
    #
    'VNT_OSJE': 'rgba(120, 163, 206, 0.8)',
    'VNT_IES': 'rgba(120, 163, 206, 0.6)',
    'VNT_DSB': 'rgba(120, 163, 206, 0.45)',
    'VNT_DSBJE': 'rgba(120, 163, 206, 0.45)',
    #
    'OH_OSJE': 'rgba(0, 0, 0, 0.8)',
    'OH_IES': 'rgba(0, 0, 0, 0.6)',
    'OH_DSB': 'rgba(0, 0, 0, 0.45)',
    'OH_DSBJE': 'rgba(0, 0, 0, 0.45)',
}
#####


# I need to query one database with simulation results to populate the menus
D = DWELLINGS[0]
SIM_TOOL, SIM_JOBS, RVX = 'JESS', 24, 'EMS_HR_RP'
table = 'TEMPLATE_SJI'
df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table), app.db_conn)
#

#
input_menus = html.Div(
    className='row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size': 13,
    },
    children=[
        dash_create_menu_dwelling(menu_id='D_input(p1)',
                              width='two', menu_type='radio', DWELLINGS=DWELLINGS),
        dash_create_menu_weather(menu_id=['W1_input(p1)', 'W2_input(p1)'], widths=['one', 'one'],
                                 WEATHER_FILES=WEATHER_FILES),
        dash_create_menu_floor(menu_id='F_input(p1)', col=Fcol,
                               width='one', df=df_sji),
        # dash_create_menu_north(menu_id='N_input(p1)',  width='one',
        #     df=df_sji,),
        dash_create_menu_vnt(menu_id=['VNT_KL_input(p1)', 'VNT_B_input(p1)'],
                             cols=[vBcol, vKLcol], width='two', df=df_sji),
        dash_create_menu_window_width(menu_id=['WW_KL_input(p1)', 'WW_B_input(p1)'],
                                      cols=[wwBcol, wwKLcol], width='one', df=df_sji),
        dash_create_menu_glazing(menu_id='G_input(p1)', col=Gcol,
                                 width='one', df=df_sji),
        dash_create_menu_textinput(
            menu_id=[
                'trace_group_1_input(p1)',
                'trace_group_2_input(p1)',
                'trace_group_3_input(p1)',
            ],
            width='one'),

        # dash_create_menu_rooms(menu_id='R_input(p1)', width='one', ROOMS=ROOMS),
        # dash_create_menu_daterange(width='one'),
    ],
)
#
chart1 = html.Div(
    children=[
        dcc.Graph(
            id='chart_bar_runperiod',
            figure={},
            style={'height': '700px'},
        ),
    ],
)

#####

page_1_layout = html.Div(
    className='row',
    style={
        # 'background-color': '#F3F3F3',
        'font-family': 'overpass',  # 'font-size':11,
        'height': '1000px', 'width': '100%',  # 'max-width': '1800',
        'margin': '20 0 0 0', 'padding': '0 0 0 0',
    },
    children=[
        page_title,
        input_menus,
        html.Hr(),
        chart1,
    ],
)


#####
# CALLBACK TO POPULATE MENUS
@app.callback(
    Output('VNT_KL_input(p1)', 'options'),
    [Input('D_input(p1)', 'value'), Input('F_input(p1)', 'value')]
)
def set_vnt_KL_options(D_value, F_value):
    #
    D = D_value
    F = F_value
    D_F = '{}_{}'.format(D_value, F_value)
    table = 'OSJE_{}_{}_SJI'.format(D, SIM_JOBS)
    df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table), app.db_conn)

    #
    VNT_KL_list = df_sji[vKLcol].unique()
    VNT_KL_options = [{'label': '{}'.format(int(1000 * x)), 'value': x} for x in VNT_KL_list]
    return VNT_KL_options


@app.callback(
    Output('VNT_KL_input(p1)', 'value'),
    [Input('VNT_KL_input(p1)', 'options')]
)
def set_vnt_KL_value(available_options):
    return available_options[0]['value']


#
@app.callback(
    Output('VNT_B_input(p1)', 'options'),
    [Input('D_input(p1)', 'value'), Input('F_input(p1)', 'value')]
)
def set_vnt_B_options(D_value, F_value):
    #
    D = D_value
    F = F_value
    D_F = '{}_{}'.format(D_value, F_value)
    table = 'OSJE_{}_{}_SJI'.format(D, SIM_JOBS)
    df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table), app.db_conn)

    #
    VNT_B_list = df_sji[vBcol].unique()
    VNT_B_options = [{'label': '{}'.format(int(1000 * x)), 'value': x} for x in VNT_B_list]
    return VNT_B_options


@app.callback(
    Output('VNT_B_input(p1)', 'value'),
    [Input('VNT_B_input(p1)', 'options')]
)
def set_vnt_B_value(available_options):
    return available_options[0]['value']


#####

# CALLBACK TO UPDATE CHART
@app.callback(
    Output('chart_bar_runperiod', 'figure'),
    [
        Input('D_input(p1)', 'value'),
        Input('W1_input(p1)', 'value'), Input('W2_input(p1)', 'value'),
        Input('F_input(p1)', 'value'),
        Input('VNT_B_input(p1)', 'value'), Input('VNT_KL_input(p1)', 'value'),
        Input('WW_B_input(p1)', 'value'), Input('WW_KL_input(p1)', 'value'),
        Input('G_input(p1)', 'value'),
        Input('trace_group_1_input(p1)', 'value'),
        Input('trace_group_2_input(p1)', 'value'),
        Input('trace_group_3_input(p1)', 'value'),

    ])
def update_chart_bar_runperiod(
    D_value, W1_value, W2_value, F_value,
    VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value,
    G_value,
    trace_group_1, trace_group_2, trace_group_3,
    ):

    import time
    start_time = time.time()
    all_traces = []
    #

    N_angle_dict = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}
    fig_multi_rp = plotly.tools.make_subplots(
        rows=len(ROOMS), cols=6,
        shared_xaxes=True, shared_yaxes=True, vertical_spacing=0.1,
    )
    #
    D = D_value;
    F = F_value;
    D_F = '{}_{}'.format(D_value, F_value)
    W_value = '{}{}'.format(W1_value, W2_value)
    #
    # file = 'ALL_{}_RP.sqlite'.format(SIM_JOBS)
    table = 'OSJE_{}_{}_RP'.format(D, SIM_JOBS)
    df_ep_rp = pd.read_sql_query(
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
    print('df_ep_rp: {}'.format(df_ep_rp.shape))

    # Adding traces
    for i in range(0, len(ROOMS), 1):
        row = i + 1
        col = i + 1
        room = ROOMS[i]
        print('\n\ni:{} | room:{} | row:{}'.format(i, room, row))

        for N in NORTH:
            # print(int(N))
            dash_fig_multi_RP_add_bars(
                fig_multi=fig_multi_rp,
                df=df_ep_rp, platform='OSJE',
                N=int(N), N_angle_dict=N_angle_dict, Ncol=Ncol,
                room=room, row=row,
                bar_width=bar_width, outline_width=1.3,
                colors_dict=colors_dict, all_traces=all_traces,
            )

#

    # RUNPERIOD SIMRES
    i = 0
    for trace_group in [trace_group_1, trace_group_2, trace_group_3]:
        i=i+1

        try:
            table = '{}_{}_24_RP'.format(trace_group, D) if 'JE' in trace_group \
                else '{}_{}_RP'.format(trace_group, D)
            
            df_rp = pd.read_sql_query(
                con = app.db_conn,
                sql = """SELECT * FROM {table}
                WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
                """.format(
                    table=table,
                    Wcol=Wcol, W=W_value, Fcol=Fcol,F=F_value,
                    )
                )
            print(table)
            print(df_rp.shape)
            #
            for i in range(0, len(ROOMS), 1):
                row = i + 1
                col = i + 1
                room = ROOMS[i]
                print('\n\ni:{} | room:{} | row:{}'.format(i, room, row))

                for N in NORTH:
                    # print(int(N))
                    dash_fig_multi_RP_add_bars(
                        fig_multi=fig_multi_rp,
                        df=df_rp, platform=trace_group,
                        N=int(N), N_angle_dict=N_angle_dict, Ncol=Ncol,
                        room=room, row=row,
                        bar_width=bar_width, outline_width=1.3,
                        colors_dict=colors_dict, all_traces=all_traces,
                    )
        except:
            print('Could not retrieve table: {}'.format(table))
        #
        print('\n\t{0:.3f} seconds'.format(time.time()-start_time) )




    # try:
    #     table = 'IES_{}_RP'.format(D)
    #     df_ies_rp = pd.read_sql_query(
    #         con=app.db_conn,
    #         sql="""SELECT * FROM {table}
    #             WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
    #             """.format(
    #             table=table,
    #             Wcol=Wcol, W=W_value, Fcol=Fcol, F=F_value,
    #         )
    #     )
    #     print('df_ies_rp: {}'.format(df_ies_rp.shape))
    #     #
    #     for i in range(0, len(ROOMS), 1):
    #         row = i + 1
    #         col = i + 1
    #         room = ROOMS[i]
    #         print('\n\ni:{} | room:{} | row:{}'.format(i, room, row))

    #         for N in NORTH:
    #             # print(int(N))
    #             dash_fig_multi_RP_add_bars(
    #                 fig_multi=fig_multi_rp,
    #                 df=df_ies_rp, platform='IES',
    #                 N=int(N), N_angle_dict=N_angle_dict, Ncol=Ncol,
    #                 room=room, row=row,
    #                 bar_width=bar_width, outline_width=1.3,
    #                 colors_dict=colors_dict, all_traces=all_traces,
    #             )
    #         print('Could not retrieve table: {}'.format(table))
    # except:
    #     'Do nothing'

    # #####

    # try:
    #     table = 'DSB_{}_RP'.format(D)
    #     df_dsb_rp = pd.read_sql_query(
    #         con=app.db_conn,
    #         sql="""SELECT * FROM {table}
    #             WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
    #             """.format(
    #             table=table,
    #             Wcol=Wcol, W=W_value, Fcol=Fcol, F=F_value,
    #         )
    #     )
    #     print('df_dsb_rp: {}'.format(df_dsb_rp.shape))
    #     #
    #     for i in range(0, len(ROOMS), 1):
    #         row = i + 1
    #         col = i + 1
    #         room = ROOMS[i]
    #         print('\ni:{} | room:{} | row:{}'.format(i, room, row))

    #         for N in NORTH:
    #             # print(int(N))
    #             dash_fig_multi_RP_add_bars(
    #                 df=df_dsb_rp, platform='DSB',
    #                 fig_multi=fig_multi_rp,
    #                 N=int(N), N_angle_dict=N_angle_dict, Ncol=Ncol,
    #                 room=room, row=row,
    #                 bar_width=bar_width, outline_width=1.3,
    #                 colors_dict=colors_dict, all_traces=all_traces,
    #             )
    #         print('DSB traces added')
    # except:
    #     print('Could not retrieve table: {}'.format(table))

    #     print('\t\t%s seconds' % (time.time() - start_time))

    #####

    layout_multi_rp = go.Layout(
        yaxis1=dict(
            title='<b>KL</b>', titlefont=dict(size=20),
            dtick=45,
            showgrid=True,
        ),
        yaxis2=dict(
            title='<b>BD1</b>', titlefont=dict(size=20),
            dtick=45,
            showgrid=True,
        ),
        # yaxis3=dict(
        #     title='<b>BS1</b>', titlefont=dict(size=20),
        #     ),
        xaxis1=dict(
            domain=[0, 0.175],
            range=[-2000, 0], dtick=250,
            showgrid=True,
            title='Total Heat Losses (kWh)',
        ),
        xaxis2=dict(
            domain=[0.175, 0.275],
            range=[0, 1000], dtick=250,
            showgrid=True,
            title='Total Heat Gains (kWh)',
        ),
        xaxis3=dict(
            domain=[0.3, 0.425],
            range=[0, 50], dtick=10,
            showgrid=False,
            title='Mean Ventilation (l/s)',
        ),
        xaxis4=dict(
            domain=[0.45, 0.575],
            range=[0, 5], dtick=1,
            showgrid=False,
            title='Mean Ventilation (ach)',
        ),
        xaxis5=dict(
            domain=[0.6, 0.8],
            range=[20, 0], dtick=2,
            showgrid=True,
            title=r'HA26C (%)',
        ),
        xaxis6=dict(
            domain=[0.85, 1],
            range=[30, 0], dtick=2,
            showgrid=True,
            title=r'TM59 Ca (%)',
        ),
        legend=dict(
            font=dict(size=7),
        ),
        #
        barmode=bar_mode,
        bargap=bar_gap,
        bargroupgap=bar_group_gap,
        showlegend=False,
        title='EPLUS-IES COMPARISON<br><i>unit</i>: <b>{}</b> | <i>floor</i>: <b>{}</b>'.format(D, F),
    )
    fig_multi_rp['layout'].update(layout_multi_rp)
    print(len(all_traces))

    return fig_multi_rp
