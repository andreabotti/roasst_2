# DASH
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt




def dash_create_menu_unit(DWELLINGS, menu_type, menu_id, cols):

    # Defines input menus for exploring results
    D_list = [x for x in sorted(DWELLINGS) ]
    D_options = [{'label': x, 'value': x} for x in sorted(DWELLINGS) ]

    # U radio
    html_radio = html.Div([
        html.H6('DWELLING'),
        dcc.RadioItems(
            id=menu_id, options=D_options, value=D_list[0],
            labelStyle={'display': 'inline-block'}
            ), 
        ], className= 'two columns',
        )

    # U dropdown
    html_drowpdown = html.Div([
        html.H6('DWELLING'),
        dcc.Dropdown(
            id='D_input', options=D_options, value=D_list[0],
            multi=True,
            ),
        ],
        className= '{} columns'.format(cols),
        style={'margin-right': '10'},
        )

    if menu_type=='radio':
        return html_radio
    elif menu_type=='dropdown':
        return html_drowpdown
    else:
        print('Wrong menu type selection')

#

def dash_create_menu_weather(WEATHER_FILES, menu_id, cols):
    
    dict_weather = {
        'GTW': 'Gatwick Airport (rural)',
        'LHR': 'Heathrow Airport (semi-urban)',
        'LWC': 'LDN Weather Centre (urban)',
        }
    W1_list = [x[:3] for x in sorted(WEATHER_FILES) ]

    if cols == 'one':  
        W1_options = [{'label': x, 'value': x} for x in W1_list ]
    else:
        W1_options = [{'label': dict_weather[x], 'value': x} for x in W1_list]

        
    #
    W2_list = ['DSY1', 'DSY2', 'DSY3']
    W2_options = [{'label': i, 'value': i} for i in W2_list]
    
    html_wea = html.Div([
        html.Div([
            html.H6('WEATHER'),
            html.Label('LOCATION'),
            dcc.RadioItems(
                id=menu_id[0], options=W1_options, value=W1_list[0],
                ),
            ],
            className= '{} columns'.format(cols),
            ),

        html.Div([
            html.H6('WEATHER'),
            html.Label('DSY'),
            dcc.RadioItems(
                id=menu_id[1], options=W2_options, value=W2_list[0],
                # labelStyle={'display': 'inline-block'}
                ), 
            ],
            className= 'one column',
            style={
            # 'fontSize': 13,
            # 'padding': '5',
            },
            ),
        ])
    
    return html_wea

#


def dash_create_menu_north(df, menu_id, cols):
    NORTH_dict = {0:'N',45:'NE',90:'E',135:'SE',180:'S',225:'SW',270:'W',315:'NW'}
    col = '@north'
    N_list = [x for x in sorted(df[col].unique() ) ]
    N_options = [{'label': '{}'.format(NORTH_dict[x]), 'value': x} for x in sorted(df[col].unique()) ]

    # N slider
    return html.Div([
        html.H6('ORIENTATION'),
        # html.Label('<b>ANGLE FROM NORTH</b>'),
        dcc.RadioItems(
            id=menu_id, options=N_options, value=N_list[0],
            labelStyle={'display': 'inline-block'}
            ), 
        ],
        className= '{} columns'.format(cols),
        )


def dash_create_menu_floor(df, menu_id, cols):
    col = '@floor'
    F_list = [x for x in sorted(df[col].unique() ) ]
    F_options = [{'label': x, 'value': x} for x in sorted(df[col].unique() ) ]

    # F radio
    return html.Div([
        html.H6('FLOOR'),
        dcc.RadioItems(
            id=menu_id, options=F_options, value=F_list[0],
            # labelStyle={'display': 'inline-block'}
            ), 
        ],
        className= '{} columns'.format(cols),
        )

#

def dash_create_menu_vnt(df, menu_id, cols):

    col = '@vnt_B(m3/s)'
    VNT_B_list = [x for x in sorted(df[col].unique() ) ]
    VNT_B_list = [0.03, 0.04, 0.05]
    VNT_B_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_B_list ]
    #
    col = '@vnt_KL(m3/s)'
    VNT_KL_list = [round(x,2) for x in sorted(df[col].unique() ) ]
    VNT_KL_list = [0.03, 0.04, 0.05] + [0.16, 0.17, 0.18]
    VNT_KL_options = [{'label': '{}'.format(int(1000*x)), 'value': x} for x in VNT_KL_list ]

    # VNT radio
    return html.Div(
        className= '{} columns'.format(cols),
        children=[
            html.H6('VENTILATION'),
            html.Label('KL'),
            dcc.RadioItems(
                id=menu_id[0], options=VNT_KL_options, value=VNT_KL_list[0],
                labelStyle={'display': 'inline-block'}
                ),

            html.Label('B'),
            dcc.RadioItems(
                id=menu_id[1], options=VNT_B_options, value=VNT_B_list[0],
                labelStyle={'display': 'inline-block'}
                ),
            html.Label('max rates in l/s)'),
            ],
        )

#

def dash_create_menu_window_width(df, menu_id, cols):
    col = '@wwidth_B'
    WW_B_list = [x for x in sorted(df[col].unique() ) ]
    WW_B_options = [{'label': x, 'value': x} for x in sorted(df[col].unique() ) ]
    col = '@wwidth_KL'
    WW_KL_list = [x for x in sorted(df[col].unique() ) ]
    WW_KL_options = [{'label': x, 'value': x} for x in sorted(df[col].unique() ) ]

    # WWIDTH radio
    return html.Div([
        html.H6('WWidth'),
        html.Div([
            html.Label('KL'),
            dcc.RadioItems(
                id=menu_id[0], options=WW_KL_options, value=1,  #WW_KL_list[0],
                labelStyle={'display': 'inline-block'}
                ),
            ], # className= 'two columns',
            ),
        #
        html.Div([
            html.Label('BD'),
            dcc.RadioItems(
                id=menu_id[1], options=WW_B_options, value=1, #WW_B_list[0],
                labelStyle={'display': 'inline-block'}
                ),
            ], # className= 'one column',
            ),
    ],
    className= '{} columns'.format(cols),
    )

#

def dash_create_menu_glazing(df, menu_id, cols):
    #
    col = '@c_glazed'
    G_list = [x for x in sorted(df[col].unique() ) ]
    G_options = [{'label': x, 'value': x} for x in sorted(df[col].unique() ) ]

    # GLAZING G-VALUE
    return html.Div([
    html.H6('GLAZING'),
    html.Label('G-VALUE'),
        dcc.RadioItems(
            id=menu_id, options=G_options, value=G_list[0],
            # labelStyle={'display': 'inline-block'}
            ),
        ],
        className= '{} columns'.format(cols),
        )

#

def dash_create_menu_rooms(ROOMS, menu_id, cols):
    #
    ROOM_list = [x for x in ROOMS ]
    ROOM_options = [{'label': x, 'value': x} for x in ROOMS ]

    return html.Div(
        className= '{} columns'.format(cols),
        children = [
            html.H6('ROOM'),
                dcc.RadioItems(
                    id=menu_id, options=ROOM_options, value=ROOM_list[0],
                    labelStyle={'display': 'inline-block'}
                    ),
            ],
        )

#

def dash_create_menu_daterange(cols):
    month_list = [5,6,7,8,9]
    month_options = {5:'MAY',6:'JUN', 7:'JUL',8:'AUG',9:'SEP'}

    return html.Div(
        className= '{} columns'.format(cols),
        children = [
            html.H6('Choose Date Range'),
            dcc.RangeSlider(
                id = 'RangeSlider_month',
                updatemode = 'mouseup', #don't let it update till mouse released
                min = min(month_list),
                max = max(month_list),
                value = [min(month_list), max(month_list)],
                marks=month_options,
                # marks=pd.date_range(start='1989-5-1',end='1989-9-30',freq='D'),
                ),
            ],
    )

#


def dash_create_menu_OH_metric():
    metrics = ['HA26p','TM59_Ca']
    crit_list = [x for x in metrics]
    crit_options = [{'label': x, 'value': x} for x in metrics]

    # OH radio
    return html.Div(
        className = '{} columns'.format(cols),
        children = [
            html.H6('OH Criterion'),
            dcc.RadioItems(
                id='crit_input', options=crit_options, value=crit_list[0],
                # labelStyle={'display': 'inline-block'}
                ), 
            ],
        )
