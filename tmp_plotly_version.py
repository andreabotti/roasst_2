import plotly
print(plotly.__version__)
import plotly.offline as off
#
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

import pandas as pd

# off.init_notebook_mode()


#
# COLUMN NAMES
Dcol = '@dwelling'; Ncol = '@north'; Wcol = '@weather'; Fcol = '@floor'
wwBcol = '@wwidth_B'; wwKLcol = '@wwidth_KL'
vBcol = '@vnt_B_ls'; vKLcol = '@vnt_KL_ls'
Ocol = '@c_opaque'; Gcol = '@c_glazing'
#
W_value='GTWDSY1'; F_value='MF'; WW_B_value,WW_KL_value=1,1; G_value='DSB'

#
import os
from sqlalchemy import create_engine
def get_db_connection(use_local_db=False):
    conn = create_engine(
        os.environ['DATABASE_URL'],
        echo=True,
        )
    return conn.connect()
db_conn = get_db_connection()
#
table = 'P1201do_DSBJE24_RP'
df_rp = pd.read_sql_query(
    con=db_conn,
    sql="""SELECT * FROM {table}
        WHERE `{Wcol}` = '{W}' AND `{Fcol}` = '{F}'
        AND `{wwBcol}` = '{WW_B}' AND `{wwKLcol}` = '{WW_KL}'
        AND `{Gcol}` = '{G}'
        ;""".format(
        table=table,
        Wcol=Wcol, W=W_value,
        Fcol=Fcol, F=F_value,
        wwBcol=wwBcol, WW_B=WW_B_value, wwKLcol=wwKLcol, WW_KL=WW_KL_value,
        Gcol=Gcol, G=G_value,
    ),
)
print('df_rp: {}'.format(df_rp.shape))


#
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/hobbs-pearson-trials.csv")
df = df_rp

#
NORTH = [0,45,90,135,180,225,270,315]
R = 'KL'
crit = 'TM59_Ca'
#
data = []
for N in NORTH:
    df_N = df_rp[ df_rp['@north']==N ]
    
    col = '{}_{}'.format(R, crit)
    r = df_N.iloc[0][col]
    theta = N
    print(theta, r)

    trace = go.Scatterpolar(
        r = r,
        theta = theta,
        mode = "markers",
        name = col,
        marker = dict(
            color = "rgb(27,158,119)",
            size = 12,
            # line = dict(
            #     color = "white"
            #     ),
            # opacity = 0.7
            ),
        cliponaxis = False,
        )
    data.append(trace)

print(data[3])
    
layout = go.Layout(
    title = "test plot",
    font = dict(
      size = 15
    ),
    showlegend = True,
    polar = dict(
      bgcolor = "rgb(223, 223, 223)",
      angularaxis = dict(
        tickwidth = 2,
        linewidth = 3,
        layer = "below traces",
        rotation=90,
        ),
      radialaxis = dict(
        range=[0,20],
        side = "counterclockwise",
        showline = True,
        linewidth = 2,
        tickwidth = 2,
        gridcolor = "white",
        gridwidth = 2,
      )
    ),
    paper_bgcolor = "rgb(223, 223, 223)"
)

fig = go.Figure(data=data, layout=layout)
url = py.iplot(fig, filename='test_plot', validate = False)
print(url)