import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from roasst import urls
from roasst.app import app

from roasst.pages import page_1_layout, page_2_layout, page_3_layout, p110_layout, p220_layout

#

url_page_1 = '/page_1'
url_page_2 = '/page_2'
url_page_3 = '/page_3'
url_p110 = '/p110'
url_p220 = '/p220'

#

link_margin = '20px'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Home', href='/', style={'margin': link_margin}),
    dcc.Link('Page 1', href=url_page_1, style={'margin': link_margin}),
    dcc.Link('Page 2', href=url_page_2, style={'margin': link_margin}),
    dcc.Link('Page 3', href=url_page_3, style={'margin': link_margin}),
    dcc.Link('Hourly', href=url_p110, style={'margin': link_margin}),
    dcc.Link('RunPeriod', href=url_p220, style={'margin': link_margin}),
    html.Hr(),
    # html.Br(),
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
    elif pathname == url_p110:
        return p110_layout
    elif pathname == url_p220:
        return p220_layout
    else:
        return index_page

