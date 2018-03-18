import pandas as pd, numpy as np
from pandas import *
#
import statsmodels.formula.api as sm
from statsmodels.stats.stattools import (jarque_bera, omni_normtest, durbin_watson)


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
from dash_utils._main_settings import *
from dash_utils.dash_lib_viz_menus import *
from dash_utils.dash_lib_viz_charts_RP import *



#####

# SIM_OUT_PATH = SIM_OUT_PATH_JESS
SIM_OUT_PATH = SIM_OUT_PATH_JEPLUS
SIM_JOBS = 8    #72
#
NORTH = [0,45,90,135,180,225,270,315]
N_angle_dict = {0:'N',45:'NE',90:'E',135:'SE',180:'S',225:'SW',270:'W',315:'NW'}
#
UNITS = ['P1201' ,'P1202','P1203', 'P1204A', 'P2301','P2302','P2303','P2304']
FLOORS = ['MF']
WEATHER_FILES = ['GTWDSY1']
ROOMS = ['KL', 'BD1']
#

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
import random
r = lambda: random.randint(0,255)
# d_color = {}
# keys = range(len(UNITS))
# for i in keys:
#     f = UNITS[i]
#     d_color[f] = '#%02X%02X%02X' % (r(),r(),r())
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

#####
df_ep_rp_allunits = pd.DataFrame()

for U in UNITS:
    sep = '-'*30
    print('\n{}\nUNIT: {}  |  SimJobs:{}\n'.format(sep,U,SIM_JOBS))
    for W in WEATHER_FILES:
        for F in FLOORS:
            #
            U_F_W = '{}_{}_{}'.format(U, F, W)
            U_F_W_SIMS = '{}_{}'.format(U_F_W, SIM_JOBS)

            # RUNPERIOD RESULTS
            SIMRES_DB_EP_RP = os.path.join(SIM_OUT_PATH, U, U_F_W_SIMS, '{}_RP.sqlite.csv'.format(U_F_W_SIMS))
            SQLITE_DB_IES_RP = os.path.join(MAIN_FOLDER, '2_SIMRES/IES/', '{}_RP.sqlite'.format(U_F_W))
            df_sji = query_sqlite_sji(
                db=SIMRES_DB_EP_RP,
                table='SimJobIndex',
                )
            # print('# Querying databases (RP):\n\t{}\n\t{}\n'.format(SIMRES_DB_EP_RP, SQLITE_DB_IES_RP) )

            df_ep_rp = query_sqlite_simres_rp(
                db=SIMRES_DB_EP_RP,
                table=U_F_W_SIMS,
                )
            #
            df_ep_rp_allunits = pd.concat([df_ep_rp_allunits, df_ep_rp], axis=0)
#
df_ep_rp_allunits['@unit'] = [i.split('_')[1] for i in df_ep_rp_allunits.index]
print(df_ep_rp_allunits.shape)


#####


# DASH APP
app = dash.Dash()
app.config.supress_callback_exceptions = True
# CSS
external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css"]
[app.css.append_css({"external_url": css}) for css in external_css]
if 'DYNO' in os.environ:
    app.scripts.append_script({'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'})


##########
# ROASST App
app.layout = html.Div(
    [
        html.Div([
            html.H4('ROASST App 3 - UNIT COMPARISON (RunPeriod)'),
            ],
            style={
                'background-color': '#F3F3F3',
                'font-family': 'overpass',
                'width': '98%',
                'margin': '0 0 0 0', 'padding': '20', 'padding-top': '10', 'padding-bottom': '0',
            },
            ),

        html.Div([
            dash_create_menu_unit(UNITS=UNITS, menu_type='dropdown'),
            dash_create_menu_floor(df=df_sji),
            dash_create_menu_vnt(df=df_sji),
            dash_create_menu_window_width(df=df_sji),
            dash_create_menu_glazing(df=df_sji),
            ],
        className='row',
        style={
            # 'background-color': '#F3F3F3',
            'font-family': 'overpass',
            'width': '90%',
            'margin': '0 0 0 0', 'padding': '10', 'padding-top': '10', 'padding-bottom': '0',
        },
        ),

        html.Hr(),

        html.Div([
            # html.Label('OVERHEATING RISK FOR BEDROOM1 (TM52_C1)'),
            html.Div([
                dcc.Graph(
                    style={'height': '700px'},
                    id='chart_bar_runperiod',
                    figure=plotly.tools.make_subplots(
                        rows=3, cols=3,
                        shared_xaxes=False, shared_yaxes=False,
                        horizontal_spacing=0.1,
                        vertical_spacing=0.15,
                        subplot_titles=('NW','N','NE','W','PLANS','E','SW','S','SE')
                        ),
                ),
            ],  className='row', style={'padding': '10 10 10 10'},
            ),
        ]),    
        
    ],
    style={
        # 'background-color': '#F3F3F3',
        'font-family': 'overpass',
        'width': '100%',
        'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
    },
)

#####

bar_subplots_rp_multiroom = plotly.tools.make_subplots(
rows=3, cols=3,
shared_xaxes=False, shared_yaxes=False,
horizontal_spacing=0.1,
vertical_spacing=0.15,
subplot_titles=('NW','N','NE','W','PLANS','E','SW','S','SE')
)

#####

@app.callback(
    Output('chart_bar_runperiod', 'figure'),
    [
    Input('U_input', 'value'), Input('F_input', 'value'),
    Input('VNT_B_input', 'value'), Input('VNT_KL_input', 'value'),
    Input('WW_B_input', 'value'), Input('WW_KL_input', 'value'),
    Input('G_input', 'value')
    ])


def update_chart_bar_runperiod(U_value, F_value, VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value, G_value):
    
    import time
    start_time = time.time()

    N_angle_dict = {0:'N',45:'NE',90:'E',135:'SE',180:'S',225:'SW',270:'W',315:'NW'}
    #    
    df = df_ep_rp_allunits
    
    # print(df.shape)
    R = ROOMS[0]


    # print(U_value, type(U_value)
    U = [U_value] if type(U_value).__name__ == 'str' else U_value
    print(U)
    
    df_U = pd.DataFrame()
    for U in U_value:
        sel = df[ df['@unit']==U ]
        df_U = pd.concat([df_U, sel], axis=0)
    print(df_U.shape)

    for N in NORTH:
        df_N = df_U[ df_U['@north']==N ]
        print(df_N.shape)
        # print(df_N['@north'])

        #####
        pos = dict_subplot_pos[N]
        row,col= [ int(x) for x in pos.split(',') ]
        # print(row, col)
        #####

        # if R=='BD1' or R=='BS1':
        #         col1 = '@vnt_B(m3/s)'
        #         col2 = '@vnt_B(l/s)'
        #         trace_fill = 'rgba(0,0,0,0)'
        #         trace_outline = d_color[U]
        # else:
        #     col1 = '@vnt_{}(m3/s)'.format(R)
        #     col2 = '@vnt_{}(l/s)'.format(R)
        #     trace_fill = d_color[U]
        #     trace_outline = 'rgba(0,0,0,0)'

        #
        y1 = df_N['{}_HA26p'.format(R)]*100
        y2 = df_N['{}_TM59_Ca'.format(R)]*100
        x = df_N['@unit']
        trace_name = '{}|{}'.format(U,R)
        x = trace_name
        trace_bar = go.Bar(
            x=x,
            y=y1,
            xaxis='x{}'.format(row),
            yaxis='y{}'.format(col),
            # width=bar_width,
            # marker=dict(
            #     color=trace_fill,
            #     line=dict(color=trace_outline, width=1.5),
            #     ),
            name=R,
            text='<b>{}</b>'.format(R),
            textfont=dict(
                size=10,
                color='rgba(0,0,0,0.6)'),
            textposition='auto',
            legendgroup='{}'.format(trace_name),
            )
        bar_subplots_rp_multiroom.append_trace(trace_bar, row=row, col=col)
        print('N:{}, trace:{}, value:{}'.format(N,trace_name,y1) )


    for i in range(1,10):
        bar_subplots_rp_multiroom['layout']['yaxis{}'.format(i)].update(
            range=[0,20], dtick=5, ticksuffix='%',
            )

    return bar_subplots_rp_multiroom

    # print(df1['@vnt_B(m3/s)'][:3])

    # if R=='BD1' or R=='BS1':
    #     col1 = '@vnt_B(m3/s)'
    #     col2 = '@vnt_B(l/s)'
    #     trace_fill = 'rgba(0,0,0,0)'
    #     trace_outline = d_color[U]

    # else:
    #     col1 = '@vnt_{}(m3/s)'.format(R)
    #     col2 = '@vnt_{}(l/s)'.format(R)
    #     trace_fill = d_color[U]
    #     trace_outline = 'rgba(0,0,0,0)'


    # df1[col2] = (df1[col1]*1000).astype(int)
    # vnt_list = df1[col2].unique()




port = 3001
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



bar_width = 1



#             df1[col2] = (df1[col1]*1000).astype(int)
#             vnt_list = df1[col2].unique()

#             #####

#             y1 = round(df1['{}_HA26p'.format(R)][0]*100, 1)
#             y2 = round(df1['{}_TM59_Ca'.format(R)][0]*100, 1)
#             x = df1['@unit'][0]

#             #
#             trace_name = '{}|{}'.format(U,R)
#             x = trace_name

#             trace_bar = go.Bar(
#                 x=U,
#                 y=y1,
#                 xaxis='x{}'.format(row),
#                 yaxis='y{}'.format(col),
#                 # width=bar_width,
#                 marker=dict(
#                     color=trace_fill,
#                     line=dict(color=trace_outline, width=1.5),
#                     ),
#                 name=R,
#                 text='<b>{}</b>'.format(R),
#                 textfont=dict(
#                     size=10,
#                     color='rgba(0,0,0,0.6)'),
#                 textposition='auto',
#                 legendgroup='{}'.format(trace_name),
#                 )
#             bar_subplots_rp_oneroom.append_trace(trace_bar, row=row, col=col)

#             #####

#             trace_bar_shading = go.Bar(
#                 x=R,
#                 y=y1,
#                 xaxis='x{}'.format(row),
#                 yaxis='y{}'.format(col),
#                 width=0.1,
#                 marker=dict(
#                     color=trace_fill,
#                     line=dict(color=trace_outline, width=1.5),
#                     ),
#                 name=U,
#                 text='<b>{}</b>'.format(U),
#                 textfont=dict(
#                     size=10,
#                     color='rgba(0,0,0,0.6)'),
#                 textposition='auto',
#                 legendgroup='{}'.format(trace_name),
#                 )

#             bar_subplots_rp_multiroom.append_trace(trace_bar_shading, row=row, col=col)

#             #####

#             trace_scatter = go.Scatter(
#                 x= U,
#                 y=y1,
#                 xaxis='x{}'.format(row),
#                 yaxis='y{}'.format(col),
#                 # orientation='h',
#                 # width=bar_width,
#                 mode='markers+text',
#                 marker=dict(
#                     size=27,
#                     color=trace_fill,
#                     line=dict(color=trace_outline, width=2),
#                     ),
#                 name=R,
#                 text='<b>{}</b>'.format(R),
#                 textfont=dict(
#                     size=10,
#                     color='rgba(0,0,0,0.6)'),
#                 textposition='auto',
#                 legendgroup='{}'.format(trace_name),
#                 )
#             scatter_subplots_rp_multiroom.append_trace(trace_scatter, row=row, col=col)


#     #####
#     for i in range(1,10):
#         bar_subplots_rp_oneroom['layout']['yaxis{}'.format(i)].update(
#             # title=r'% Yearly HRS>26C',
#             range=[0,20], dtick=5, ticksuffix='%',
#             )
#         bar_subplots_rp_oneroom['layout']['yaxis{}'.format(i)].update(
#             # title=r'% Yearly HRS>26C',
#             range=[0,20], dtick=5, ticksuffix='%',
#             )

    
#     # bar_subplots_rp_oneroom['layout'].update(barmode='group')
#     bar_subplots_rp_oneroom['layout'].update(showlegend=False)
#     bar_subplots_rp_oneroom['layout'].update(
#         title='Overheating metrics for all units | <i>room</i> <b>{}</b>'.format(R),
#         )
#     bar_subplots_rp_oneroom_file = 'AllUnits_Room_{}_Summary'.format(R)
#     # bar_subplots_rp_oneroom_url = py.plot(bar_multi_rp, filename=bar_subplots_rp_oneroom_file, auto_open=False)
#     # print(bar_subplots_rp_oneroom_url)

# #
# for i in range(1,10):
#     bar_subplots_rp_multiroom['layout']['yaxis{}'.format(i)].update(
#         range=[0,20], dtick=5, ticksuffix='%',
#         )

# bar_subplots_rp_multiroom['layout'].update(
#     barmode='group',
#     bargroupgap=0.25,
#     bargap=0,
#     )
# bar_subplots_rp_multiroom['layout'].update(showlegend=False)
# bar_subplots_rp_multiroom['layout'].update(
#         title='Overheating metrics for shading options - unit:{}'.format(UNITS[0]),
#         )



# #####

# for i in range(1,10):
#     scatter_subplots_rp_multiroom['layout']['yaxis{}'.format(i)].update(
#         # title=r'% Yearly HRS>26C',
#         range=[0,20], dtick=5, ticksuffix='%',
#         )
#     scatter_subplots_rp_multiroom['layout']['xaxis{}'.format(i)].update(
#         showgrid=False,
#         )

# scatter_subplots_rp_multiroom['layout'].update(showlegend=False)
# scatter_subplots_rp_multiroom['layout'].update(
#     title='Overheating metrics for shading options - unit:{}'.format(UNITS[0]),
#     )
# #
# # scatter_subplots_rp_multiroom_filename = 'AllUnits_Summary'


