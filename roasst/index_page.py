import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dtt

from roasst import urls
from roasst.app import app

from roasst.pages import page_1_layout, page_2_layout, page_3_layout
from roasst.pages import P111_layout, P112_layout, P221_layout, P222_layout, P252_layout 

#

url_page_1 = '/page_1'
url_page_2 = '/page_2'
url_page_3 = '/page_3'
url_P111 = '/P111'
url_P112 = '/P112'
url_P221 = '/P221'
url_P222 = '/P222'
url_P252 = '/P252'

#

link_margin = '20px'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Home', href='/', style={'margin': link_margin}),
    # dcc.Link('Page 1', href=url_page_1, style={'margin': link_margin}),
    # dcc.Link('Page 2', href=url_page_2, style={'margin': link_margin}),
    # dcc.Link('Page 3', href=url_page_3, style={'margin': link_margin}),
    dcc.Link('Hourly_H', href=url_P111, style={'margin': link_margin}),
    dcc.Link('Hourly_V', href=url_P112, style={'margin': link_margin}),
    dcc.Link('RP_orientations_H', href=url_P221, style={'margin': link_margin}),
    dcc.Link('RP_orientations_V', href=url_P222, style={'margin': link_margin}),
    dcc.Link('RP_table_filter', href=url_P252, style={'margin': link_margin}),
    html.Br(),
    html.Hr(
        style={'margin': '0 0 0 0'},
        ),
    html.Div(id='page-content'),
])

index_page = html.Div(
    html.H5('INDEX PAGE'),
    )


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == url_page_1:
        return page_1_layout        
    elif pathname == url_page_2:
        return page_2_layout
    elif pathname == url_page_3:
        return page_3_layout
    #
    elif pathname == url_P111:
        return P111_layout
    elif pathname == url_P112:
        return P112_layout
    #
    elif pathname == url_P221:
        return P221_layout
    elif pathname == url_P222:
        return P222_layout
    elif pathname == url_P252:
        return P252_layout
    #
    else:
        return index_page

