import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from roasst import urls
from roasst.app import app

from roasst.pages import *

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Navigate to "/"', href='/'),
    html.Br(),
    html.Div(id='page-content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
])

index_page = html.Div([
    dcc.Link('Dash app 1', href=urls.page_1),
    html.Br(),
    dcc.Link('Dash app 2', href=urls.page_2),
])


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == urls.page_1:
        return page_1_layout
    elif pathname == urls.page_2:
        return page_2_layout          #page_2_layout
    else:
        return index_page
