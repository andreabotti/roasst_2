import os

import dash
import plotly
from sqlalchemy import create_engine

# from roasst.config import PLOTLY_USERNAME, PLOTLY_API_KEY
PLOTLY_USERNAME = 'a.botti'
PLOTLY_API_KEY = 'MpDq2yINla4zb0TUd7qo'

plotly.tools.set_credentials_file(username=PLOTLY_USERNAME, api_key=PLOTLY_API_KEY)


def get_db_connection(use_local_db=False):
    conn = create_engine(os.environ['DATABASE_URL'], echo=True)
    return conn.connect()


def get_app():
    app = dash.Dash(__name__)
    server = app.server
    server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
    app.config.supress_callback_exceptions = True

    external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                    "https://cdn.rawgit.com/plotly/dash-apps-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css",
                    "https://codepen.io/chriddyp/pen/bWLwgP.css"]

    [app.css.append_css({"external_url": css}) for css in external_css]
    if 'DYNO' in os.environ:
        app.scripts.append_script({
            'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'})
    return app


app = get_app()
app.db_conn = get_db_connection()
