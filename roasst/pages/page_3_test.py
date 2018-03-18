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
from modules import *
from menus import *
from page_title import page_title
from charts_RP import *



#####
sim_choice, SIM_JOBS = 'JEPLUS', 8    #72

#
if sim_choice == 'JEPLUS':
    SIM_OUT_PATH = SIM_OUT_PATH_JEPLUS
if sim_choice == 'JESS':
    SIM_OUT_PATH = SIM_OUT_PATH_JESS


#
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

def assign_trace_fill_outline(U, R):
    if R=='BD1' or R=='BS1':
            col1 = '@vnt_B(m3/s)'
            col2 = '@vnt_B(l/s)'
            trace_fill = 'rgba(0,0,0,0)'
            trace_outline = d_color[U]
    else:
        col1 = '@vnt_{}(m3/s)'.format(R)
        col2 = '@vnt_{}(l/s)'.format(R)
        trace_fill = d_color[U]
        trace_outline = 'rgba(0,0,0,0)'

    return trace_fill, trace_outline




# I need to query one database with simulation results to populate the menus
D = 'P1201'
SIM_TOOL, SIM_JOBS, RVX = 'JESS', 864, 'EMS_RP'
sqlite_con = sqlite3.connect(
    os.path.join(
        DATA_FOLDER_PATH,
        'ALL_{}_RP.sqlite'.format(SIM_JOBS),
        )
    )
table = '{}_{}_SJI'.format(D, SIM_JOBS)
df_sji = pd.read_sql_query('SELECT * FROM {}'.format(table),sqlite_con)



#####
#
input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_unit(menu_id='D_input(p1)',
            width='two', menu_type='radio', DWELLINGS=DWELLINGS),
        dash_create_menu_weather(menu_id=['W1_input(p1)','W2_input(p1)'], width='one',
            WEATHER_FILES=WEATHER_FILES),
        dash_create_menu_floor(menu_id='F_input(p1)', col=Fcol,
            width='one', df=df_sji),
        # dash_create_menu_north(menu_id='N_input(p1)',  width='one',
        #     df=df_sji,),
        dash_create_menu_vnt(menu_id=['VNT_KL_input(p1)','VNT_B_input(p1)'],
            cols=[vBcol,vKLcol], width='two', df=df_sji),
        dash_create_menu_window_width(menu_id=['WW_KL_input(p1)','WW_B_input(p1)'],
            cols=[wwBcol,wwKLcol], width='one', df=df_sji),
        dash_create_menu_glazing(menu_id='G_input(p1)', col=Gcol,
            width='one', df=df_sji),
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




    html.Hr(),

    html.Div([
        # html.Label('OVERHEATING RISK FOR BEDROOM1 (TM52_C1)'),
        html.Div([
            dcc.Graph(
                style={'height': '700px'},
                id='chart_bars_KL',
                figure=plotly.tools.make_subplots(
                    rows=3, cols=3,
                    shared_xaxes=False, shared_yaxes=False,
                    horizontal_spacing=0.1,
                    vertical_spacing=0.15,
                    subplot_titles=('NW','N','NE','W','PLANS','E','SW','S','SE')
                    ),
            ),
        ], className='six columns', style={'padding': '10 10 10 10'},
        ),
        html.Div([
            dcc.Graph(
                style={'height': '700px'},
                id='chart_bars_BD1',
                figure=plotly.tools.make_subplots(
                    rows=3, cols=3,
                    shared_xaxes=False, shared_yaxes=False,
                    horizontal_spacing=0.1,
                    vertical_spacing=0.15,
                    subplot_titles=('NW','N','NE','W','PLANS','E','SW','S','SE')
                    ),
            ),
        ], className='six columns', style={'padding': '10 10 10 10'},
        ),
    ], className='row',
    # style={'padding': '10 10 10 10'},
    ),    
    
],
style={
    # 'background-color': '#F3F3F3',
    'font-family': 'overpass',
    'width': '100%',
    'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
},
)



#####


@app.callback(
    Output('chart_bars_KL', 'figure'),
    [
    Input('U_input', 'value'),
    Input('W1_input', 'value'), Input('W2_input', 'value'),
    Input('F_input', 'value'),
    Input('VNT_B_input', 'value'), Input('VNT_KL_input', 'value'),
    Input('WW_B_input', 'value'), Input('WW_KL_input', 'value'), Input('G_input', 'value'),
    Input('crit_input', 'value'),
    ])

def update_chart_bar_runperiod_KL(
    U_value, W1_value, W2_value, F_value,
    VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value, G_value, crit_value):
    
    R = 'KL'

    import time
    start_time = time.time()

    bar_subplots_rp_multiroom = plotly.tools.make_subplots(
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
            range=[0,15.2], dtick=5, ticksuffix='%',
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
    U_value = [U_value] if type(U_value).__name__ == 'str' else U_value    
    W_value = '{}{}'.format(W1_value, W2_value)
    print(W_value)

    df = df_ep_rp_allunits
    df = df[ df['@weather']==W_value ]

    for N in NORTH:
        df_N = df[ df['@north']==N ]
        
        #####
        pos = dict_subplot_pos[N]
        row,col= [ int(x) for x in pos.split(',') ]
        # print(row, col)
        #####
    
        df_U = pd.DataFrame()
        for U in U_value:
            # print(U)
            sel = df_N[ df_N['@unit']==U ]
            df_U = pd.concat([df_U, sel], axis=0)

            x = sel['{}_{}'.format(R, crit_value)]*100
            y = sel['@unit']
            trace_name = '{}|{}'.format(U,R)
            # x = trace_name
            trace_fill, trace_outline = assign_trace_fill_outline(U=U, R=R)
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


#####


@app.callback(
    Output('chart_bars_BD1', 'figure'),
    [
    Input('U_input', 'value'),
    Input('W1_input', 'value'), Input('W2_input', 'value'),
    Input('F_input', 'value'),
    Input('VNT_B_input', 'value'), Input('VNT_KL_input', 'value'),
    Input('WW_B_input', 'value'), Input('WW_KL_input', 'value'), Input('G_input', 'value'),
    Input('crit_input', 'value')
    ])

def update_chart_bar_runperiod_BD1(
    U_value, W1_value, W2_value, F_value,
    VNT_B_value, VNT_KL_value, WW_B_value, WW_KL_value, G_value, crit_value):
    
    R = 'BD1'
    
    import time
    start_time = time.time()

    bar_subplots_rp_multiroom = plotly.tools.make_subplots(
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
            range=[0,15.2], dtick=5, ticksuffix='%',
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
    U_value = [U_value] if type(U_value).__name__ == 'str' else U_value    
    W_value = '{}{}'.format(W1_value, W2_value)
    print(W_value)

    df = df_ep_rp_allunits
    df = df[ df['@weather']==W_value ]
   

    for N in NORTH:
        df_N = df[ df['@north']==N ]
        # print(df_N.shape)
        # print(df_N['@north'])

        #####
        pos = dict_subplot_pos[N]
        row,col= [ int(x) for x in pos.split(',') ]
        # print(row, col)
        #####


        #
    
        df_U = pd.DataFrame()
        for U in U_value:
            sel = df_N[ df_N['@unit']==U ]
            df_U = pd.concat([df_U, sel], axis=0)

            x = sel['{}_{}'.format(R, crit_value)]*100
            y = sel['@unit']
            trace_name = '{}|{}'.format(U,R)
            # x = trace_name
            trace_fill, trace_outline = assign_trace_fill_outline(U=U, R=R)
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




port = 300
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


