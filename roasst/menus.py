# DASH
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


#

def dash_create_menu_textinput(menu_id, width):
    return html.Div(
        className='{} columns'.format(width),
        style={'fontSize': 12},
        children=[
            html.H6('TRACES'),
            dcc.Input(id=menu_id[0], value='', type='text'),
            dcc.Input(id=menu_id[1], value='', type='text'),
            dcc.Input(id=menu_id[2], value='', type='text'),
        ]
    )

def dash_create_menu_dwelling_textinput(menu_id, width):
    return html.Div(
        className='{} columns'.format(width),
        style={'fontSize': 12},
        children=[
            html.H6('TRACES'),
            dcc.Input(id=menu_id[0], value='P1201_OSJE24_HR', type='text'),
            dcc.Input(id=menu_id[1], value='DSBJE_P1201_24', type='text'),
            dcc.Input(id=menu_id[2], value='DSB_P1201', type='text'),
        ]
    )

#

def dash_create_menu_table_3fields(tables, multi, menu_id, width):
    # Defines input menus for exploring results
    T_list = [x for x in sorted(tables)]
    T_options = [{'label': x, 'value': x} for x in sorted(tables)]

    html_drowpdown = html.Div([
        html.H6('TABLE'),
        dcc.Dropdown(
            id=menu_id[0], options=T_options, value='P1201_OSJE216_HR',
            multi=multi,
        ),
        dcc.Dropdown(
            id=menu_id[1], options=T_options, value=T_list[-1],
            multi=multi,
        ),
        dcc.Dropdown(
            id=menu_id[2], options=T_options, value=T_list[-1],
            multi=multi,
        ),
    ],
        className='{} columns'.format(width),
        style={'margin-right': '10'},
    )

    return html_drowpdown

#

def dash_create_menu_table_1field(tables, multi, menu_id, width):
    # Defines input menus for exploring results
    T_list = [x for x in sorted(tables)]
    T_options = [{'label': x, 'value': x} for x in sorted(tables)]

    html_drowpdown = html.Div([
        html.H6('TABLE'),
        dcc.Dropdown(
            id=menu_id, options=T_options, value='P1201_OSJE216_RP',
            multi=multi,
        ),
    ],
        className='{} columns'.format(width),
        style={'margin-right': '10'},
    )

    return html_drowpdown


#

def dash_create_menu_dwelling(DWELLINGS, menu_type, menu_id, width):
    # Defines input menus for exploring results
    D_list = [x for x in sorted(DWELLINGS)]
    D_options = [{'label': x, 'value': x} for x in sorted(DWELLINGS)]

    # U radio
    html_radio = html.Div([
        html.H6('DWELLING'),
        dcc.RadioItems(
            id=menu_id, options=D_options, value=D_list[0],
            labelStyle={'display': 'inline-block'}
        ),
    ],
        className='{} columns'.format(width),
    )

    # U dropdown
    html_drowpdown = html.Div([
        html.H6('DWELLING'),
        dcc.Dropdown(
            id=menu_id, options=D_options, value=D_list[0],
            multi=True,
        ),
    ],
        className='{} columns'.format(width),
        style={'margin-right': '10'},
    )

    if menu_type == 'radio':
        return html_radio
    elif menu_type == 'dropdown':
        return html_drowpdown
    else:
        print('Wrong menu type selection')


#

def dash_create_menu_weather(WEATHER_FILES, menu_id, widths):
    dict_weather = {
        'GTW': 'Gatwick Airport (rural)',
        'LHR': 'Heathrow Airport (semi-urban)',
        'LWC': 'LDN Weather Centre (urban)',
    }
    W1_list = [x[:3] for x in sorted(WEATHER_FILES)]

    if widths[0] == 'one':
        W1_options = [{'label': x, 'value': x} for x in W1_list]
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
            className='{} columns'.format(widths[0]),
        ),

        html.Div([
            html.H6('WEATHER'),
            html.Label('DSY'),
            dcc.RadioItems(
                id=menu_id[1], options=W2_options, value=W2_list[0],
                # labelStyle={'display': 'inline-block'}
            ),
        ],
            className='{} columns'.format(widths[1]),
            style={
                # 'fontSize': 13,
                # 'padding': '5',
            },
        ),
    ])

    return html_wea


#


def dash_create_menu_north(df, col, menu_id, width):
    NORTH_dict = {0: 'N', 45: 'NE', 90: 'E', 135: 'SE', 180: 'S', 225: 'SW', 270: 'W', 315: 'NW'}
    N_list = [x for x in sorted(df[col].unique())]
    N_options = [{'label': '{}'.format(NORTH_dict[x]), 'value': x} for x in sorted(df[col].unique())]

    # N slider
    return html.Div([
        html.H6('ORIENTATION'),
        # html.Label('<b>ANGLE FROM NORTH</b>'),
        dcc.RadioItems(
            id=menu_id, options=N_options, value=N_list[0],
            labelStyle={'display': 'inline-block'}
        ),
    ],
        className='{} columns'.format(width),
    )


def dash_create_menu_floor(df, col, menu_id, width):
    F_list = [x for x in sorted(df[col].unique())]
    F_options = [{'label': x, 'value': x} for x in sorted(df[col].unique())]

    # F radio
    return html.Div(
        className='{} columns'.format(width),
        # style={
        #     'margin': '0 0 0 0',
        #     'padding': '0 0 0 0',
        # },
        children=[
            html.H6('FLOOR'),
            dcc.RadioItems(
                id=menu_id, options=F_options, value=F_list[0],
                # labelStyle={'display': 'inline-block'}
            ),
        ],
    )


#

def dash_create_menu_vnt(df, cols, menu_id, width):
    col = '_@vnt_B_m3s'
    VNT_B_list = [x for x in sorted(df[cols[0]].unique())]
    VNT_B_list = [0.03, 0.04, 0.05]
    VNT_B_options = [{'label': '{}'.format(int(1000 * x)), 'value': x} for x in VNT_B_list]
    #
    col = '_@vnt_KL_m3s'
    VNT_KL_list = [round(x, 2) for x in sorted(df[cols[1]].unique())]
    VNT_KL_list = [0.03, 0.04, 0.05] + [0.16, 0.17, 0.18]
    VNT_KL_options = [{'label': '{}'.format(int(1000 * x)), 'value': x} for x in VNT_KL_list]

    # VNT radio
    return html.Div(
        className='{} columns'.format(width),
        style={
            'margin': '10 0 0 0',
            'padding': '0 0 0 0',
        },
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

def dash_create_menu_window_width(df, cols, menu_id, width):
    WW_B_list = [x for x in sorted(df[cols[0]].unique())]
    WW_B_options = [{'label': x, 'value': x} for x in sorted(df[cols[0]].unique())]

    WW_KL_list = [x for x in sorted(df[cols[1]].unique())]
    WW_KL_options = [{'label': x, 'value': x} for x in sorted(df[cols[1]].unique())]

    # WWIDTH radio
    return html.Div([
        html.H6('WWidth'),
        html.Div([
            html.Label('KL'),
            dcc.RadioItems(
                id=menu_id[0], options=WW_KL_options, value=1,  # WW_KL_list[0],
                labelStyle={'display': 'inline-block'}
            ),
        ],  # className= 'two columns',
        ),
        #
        html.Div([
            html.Label('BD'),
            dcc.RadioItems(
                id=menu_id[1], options=WW_B_options, value=1,  # WW_B_list[0],
                labelStyle={'display': 'inline-block'}
            ),
        ],  # className= 'one column',
        ),
    ],
        className='{} columns'.format(width),
    )


#

def dash_create_menu_glazing(df, col, menu_id, width):
    G_list = [x for x in sorted(df[col].unique())]
    G_options = [{'label': x, 'value': x} for x in sorted(df[col].unique())]

    # GLAZING G-VALUE
    return html.Div([
        html.H6('GLAZING'),
        html.Label('G-VALUE'),
        dcc.RadioItems(
            id=menu_id, options=G_options, value=G_list[0],
            # labelStyle={'display': 'inline-block'}
        ),
    ],
        className='{} columns'.format(width),
    )


#

def dash_create_menu_rooms(ROOMS, menu_id, width):
    #
    ROOM_list = [x for x in ROOMS]
    ROOM_options = [{'label': x, 'value': x} for x in ROOMS]

    return html.Div(
        className='{} columns'.format(width),
        children=[
            html.H6('ROOM'),
            dcc.RadioItems(
                id=menu_id, options=ROOM_options, value=ROOM_list[0],
                labelStyle={'display': 'inline-block'}
            ),
        ],
    )


#
from datetime import datetime as dt


def dash_create_menu_month(width):
    month_list = [5, 6, 7, 8, 9]
    month_options = {5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AUG', 9: 'SEP'}

    return html.Div(
        className='{} columns'.format(width),
        children=[
            html.H6('Choose Date Range'),
            dcc.RangeSlider(
                id='RangeSlider_month',
                updatemode='mouseup',  # don't let it update till mouse released
                min=min(month_list),
                max=max(month_list),
                value=[min(month_list), max(month_list)],
                marks=month_options,
                # marks=pd.date_range(start='1989-5-1',end='1989-9-30',freq='D'),
            ),
        ],
    )


def dash_create_menu_datepickerrange(menu_id, width):
    return html.Div(
        className='{} columns'.format(width),
        style={'fontSize': 12},
        children=[
            html.H6('DATE'),
            dcc.DatePickerRange(
                id=menu_id,
                start_date=dt(1989, 5, 1),
                end_date_placeholder_text='Select a date',
                display_format='MMM, DD',
                day_size=30,
                # with_portal=True,
                # calendar_orientation='vertical',
            )
        ]
    )


#


def dash_create_menu_OH_criterion(menu_id, width):
    metrics = ['HA26p', 'TM59_Ca']
    crit_list = [x for x in metrics]
    crit_options = [{'label': x, 'value': x} for x in metrics]

    # OH radio
    return html.Div(
        className='{} columns'.format(width),
        children=[
            html.H6('OH Criterion'),
            dcc.RadioItems(
                id=menu_id, options=crit_options, value=crit_list[1],
                # labelStyle={'display': 'inline-block'}
            ),
        ],
    )
