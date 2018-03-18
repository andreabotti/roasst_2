import os, sys
import pandas as pd, numpy as np
from pandas import *
import datetime as dt

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
# import dash_table_experiments as dt
import webbrowser

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
SIM_TOOL, SIM_JOBS, RVX = 'JESS', 864, 'EMS_RP'

#####

DWELLINGS = ['P1201','P1202','P1203', 'P1204A', 'P2301','P2302','P2303','P2304']
FLOORS = ['MF']
WEATHER_FILES = ['GTWDSY1','LHRDSY1', 'LWCDSY1']
ROOMS = ['KL', 'BD1']
#
D = DWELLINGS[0]
F = FLOORS[0]
W = WEATHER_FILES[0]



#####

#
input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_unit(menu_id='D_input(p4)', width='three',
            menu_type='dropdown', DWELLINGS=DWELLINGS),
        dash_create_menu_weather(menu_id=['W1_input(p4)','W2_input(p4)'], widths=['three','two'],
            WEATHER_FILES=WEATHER_FILES),
        # dash_create_menu_floor(menu_id='F_input(p1)', col=Fcol,
        #     width='one', df=df_sji),
        # dash_create_menu_north(menu_id='N_input(p1)',  width='one',
        #     df=df_sji,),
        # dash_create_menu_vnt(menu_id=['VNT_KL_input(p1)','VNT_B_input(p1)'],
        #     cols=[vBcol,vKLcol], width='two', df=df_sji),
        # dash_create_menu_window_width(menu_id=['WW_KL_input(p1)','WW_B_input(p1)'],
        #     cols=[wwBcol,wwKLcol], width='one', df=df_sji),
        # dash_create_menu_glazing(menu_id='G_input(p1)', col=Gcol,
        #     width='one', df=df_sji),
        # dash_create_menu_rooms(menu_id='R_input(p1)', width='one', ROOMS=ROOMS),
        # dash_create_menu_daterange(width='one'),
        ],
    )

#
# Ncol = '@north'
# Wcol = '@weather'
# Fcol = '@floor'
# wwBcol = '@wwidth_B'
# wwKLcol = '@wwidth_KL'
# vBcol = '@vnt_B_m3s'
# vKLcol = '@vnt_KL_m3s'
# Ocol = '@c_opaque'
# Gcol = '@c_glazing'
col_sel = [
    Dcol, Wcol, Ncol,Fcol,vBcol, vKLcol, wwBcol, wwKLcol,
    'KL_TM59_Ca','BD1_TM59_Ca', 'BD1_TM59_Cb',
    # 'KL_HA26p','BD1_HA26p',
    ]

datatable = html.Div(
    className='row',
    style={
    'margin': '0 0 0 0', 'padding': '0', 'padding-top': '10', 'padding-bottom': '0',
    'font-size':11,
    'font-family': 'overpass',
    },
    children = [
    dt.DataTable(
        id='dynamic_table',
        min_height=600,
        rows=[{}],
        selected_row_indices=[],
        columns=col_sel,  # optional - sets the order of columns
        filterable=True,
        row_selectable=True,
        # sortable=True,
        # header_row_height=35,
        # row_update=True,
        ),
    ],
)

#
chart1 = html.Div(
    children=[
    dcc.Graph(
        id='chart_RP_KL',
        style={'height': '380px',})
    ],
)
chart2 = html.Div(
    children=[
    dcc.Graph(
        id='chart_RP_BD1',
        style={'height': '380px'})
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
        html.Div(
            className='seven columns',
            style={'margin': '0 0 0 0', 'padding': '20',},
            children=[
                input_menus,
                html.H5('DataTable'),
                datatable,
                ]
            ),
        html.Div(
            className='five columns',
            style={'margin': '0 0 0 0', 'padding': '20'},
            children=[
                html.H5('Chart KL'),
                chart1,
                html.Hr(),
                html.H5('Chart BD1'),
                chart2,
                ]
            ),
        ],
)

#####

layout = go.Layout(
    # autosize=False, width=500, height=500,
    showlegend=False,
    margin=go.Margin(l=100, r=20, b=40, t=40, pad=4),
    #
    yaxis=dict(
        autorange = 'reversed',
        tickfont=dict(
                size=10,
                # family='Courier New, monospace',
                # color='#7f7f7f',
                )
            ),
    #
    xaxis1=dict(
        tickfont=dict(size=11),
        domain=[0,0.45],
        range=[0,0.2],
        # dtick=2,
        showgrid=True,
        title=r'HA26C (%)',
        ),
    xaxis2=dict(
        tickfont=dict(size=11),
        domain=[0.55,1],
        range=[0,0.2],
        # dtick=2,
        showgrid=True,
        title=r'TM59 Ca (%)',
        ),

    )

#####

@app.callback(
    Output('dynamic_table', 'rows'),
    [
    Input('D_input(p4)', 'value'),
    Input('W1_input(p4)', 'value'), Input('W2_input(p4)', 'value'),
    ])

def update_table(D_value, W1_value, W2_value):
    df_table = pd.DataFrame()

    import time
    start_time = time.time()
    #
    D_value = [D_value] if type(D_value).__name__ == 'str' else D_value
    W_value = '{}{}'.format(W1_value, W2_value)
    #

    conn = sqlite_connector( file='ALL_{}_RP.sqlite'.format(SIM_JOBS) )
    for D in D_value:
        table = '{}_{}_RP'.format(D, SIM_JOBS)
        df = pd.read_sql_query(
            con = conn,
            sql = """SELECT * FROM {table};""".format(table=table),
            )
        df_table = pd.concat([df_table, df], axis=0)
    #
    df_table = df_table[ df_table['@weather'] == W_value ]
    print(W_value)
    
    return df_table.to_dict('records')


#####

@app.callback(
    Output('dynamic_table', 'selected_row_indices'),
    [Input('chart_RP_KL', 'clickData')],
    [State('dynamic_table', 'selected_row_indices')])

def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


#####

@app.callback(
    Output('chart_RP_KL', 'figure'), 
    [Input('dynamic_table', 'rows'), Input('dynamic_table', 'selected_row_indices')])

def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    data = go.Data([])
    marker = {'color': ['#0074D9'] * len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    print(dff)
    y = dff['@dwelling'] + '_N' + dff['@north'].astype(str)

    data.append(
        go.Bar(
            x=dff['KL_HA26p'],
            y=y,
            xaxis='x1',
            orientation='h',
            marker=marker,
            ),
        )
    data.append(
        go.Bar(
            x=dff['KL_TM59_Ca'],
            y=y,
            xaxis='x2',
            orientation='h',
            marker=marker,
            ),
        )

    figure = go.Figure(
        data=data,
        layout=layout,
    )
    return figure

#
@app.callback(
    Output('chart_RP_BD1', 'figure'), 
    [Input('dynamic_table', 'rows'), Input('dynamic_table', 'selected_row_indices')])

def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    data = go.Data([])
    marker = {'color': ['#0074D9'] * len(dff)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    
    y = dff['@dwelling'] + '_N' + dff['@north'].astype(str)

    data.append(
        go.Bar(
            x=dff['BD1_HA26p'],
            y=y,
            xaxis='x1',
            orientation='h',
            marker=marker,
            ),
        )
    data.append(
        go.Bar(
            x=dff['BD1_TM59_Ca'],
            y=y,
            xaxis='x2',
            orientation='h',
            marker=marker,
            ),
        )

    figure = go.Figure(
        data=data,
        layout=layout,
    )
    return figure



#####

port = 400
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
