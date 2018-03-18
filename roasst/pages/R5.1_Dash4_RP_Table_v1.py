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
PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dash_utils._main_settings import *
from dash_utils.dash_lib_viz_menus import *
from dash_utils.dash_lib_viz_charts_HR import *



#####
sim_choice, SIM_JOBS = 'JEPLUS', 8    #72

#
if sim_choice == 'JEPLUS':
    SIM_OUT_PATH = SIM_OUT_PATH_JEPLUS
if sim_choice == 'JESS':
    SIM_OUT_PATH = SIM_OUT_PATH_JESS

#####

UNITS = ['P1201','P1202','P1203', 'P1204A', 'P2301','P2302','P2303','P2304']
FLOORS = ['MF']
WEATHER_FILES = ['GTWDSY1','LHRDSY1', 'LWCDSY1']
ROOMS = ['KL', 'BD1']
#
U = UNITS[0]
F = FLOORS[0]
W = WEATHER_FILES[0]


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
            df_ep_rp['@weather'] = W
            df_ep_rp_allunits = pd.concat([df_ep_rp_allunits, df_ep_rp], axis=0)

#
df_ep_rp_allunits['@unit'] = [i.split('_')[1] for i in df_ep_rp_allunits.index]
df_ep_rp_allunits['@dwelling'] = [ x.split('_')[1] for x in df_ep_rp_allunits.index ]


#####

#
page_title = html.Div([
    html.H4('ROASST App 2 - RunPeriod Results'),
    ],
    className = 'row',
    style={
        'background-color': '#F3F3F3',
        'font-family': 'overpass',
        'width': '98%',
        'margin': '0 0 0 0', 'padding': '20', 'padding-top': '10', 'padding-bottom': '0',
    },
)
#
input_menus = html.Div(
    className = 'row',
    style={
        'margin': '0 0 0 0', 'padding': '10',
        'font-size':13,
        },
    children=[
        dash_create_menu_unit(UNITS=UNITS, menu_type='dropdown', cols='five'),
        dash_create_menu_weather(WEATHER_FILES=WEATHER_FILES, cols='three'),
        ],
)
#
col_sel = ['@dwelling', '@weather', '@north', '@floor',
'KL_HA26p','BD1_HA26p','KL_TM59_Ca','BD1_TM59_Ca', 'BD1_TM59_Cb']

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
graph1 = html.Div(
    children=[
    dcc.Graph(
        id='chart_RP_KL',
        style={'height': '380px',})
    ],
)
graph2 = html.Div(
    children=[
    dcc.Graph(
        id='chart_RP_BD1',
        style={'height': '380px'})
    ],
)


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
                graph1,
                html.Hr(),
                html.H5('Chart BD1'),
                graph2,
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
    Input('U_input', 'value'),
    Input('W1_input', 'value'), Input('W2_input', 'value'),
    ])

def update_table(U_value, W1_value, W2_value):
    df_table = pd.DataFrame()

    import time
    start_time = time.time()
    #
    U_value = [U_value] if type(U_value).__name__ == 'str' else U_value
    for U in U_value:
        df = df_ep_rp_allunits[ df_ep_rp_allunits['@dwelling'] == U ]
        df_table = pd.concat([df_table, df], axis=0)
    
    #
    W_value = '{}{}'.format(W1_value, W2_value)
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
