import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from roasst import urls
from roasst.app import app

from roasst.pages import page_1_layout, page_2_layout, page_3_layout, p110_layout

#


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Home', href='/'),
    dcc.Link('Page 1', href=urls.page_1),
    dcc.Link('Page 2', href=urls.page_2),
    dcc.Link('Page 3', href=urls.page_3),
    dcc.Link('Page 100 HR', href=urls.p110),
    html.Br(),
    html.Div(id='page-content'),
    # html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
])

index_page = html.Div(
    html.H5('INDEX PAGE'),
    )


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == urls.page_1:
        return page_1_layout
    
    elif pathname == urls.p110:
        return p110_layout
    
    elif pathname == urls.page_2:
        return page_2_layout
    
    elif pathname == urls.page_3:
        return page_3_layout
    
    else:
        return index_page

