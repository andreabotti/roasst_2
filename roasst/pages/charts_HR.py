# other libraries
import matplotlib.pyplot as plt
plt.rcdefaults()
import seaborn as sns
import cufflinks as cf
from pandas import *

# PLOTLY
import plotly
plotly.tools.set_credentials_file(username='a.botti', api_key='MpDq2yINla4zb0TUd7qo')
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools

# DASH
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt




def dash_HR_add_traces(df, group, room, linewidth, dash_style):

    # PLOTTING
    x = df.index
    #            
    y1a = df[room+'_OT']
    y2a = df[room+'_HG_SOLAR(W)']
    y3a = df[room+'_HG_PPL(W)']
    y4a = df[room+'_HL_VNT(W)']
    y5a = df[room+'_VNT(ach)']
#####

    trace1a = go.Scatter(
        x = x,
        y = y1a,
        yaxis='y3',
        name='TEMP ({})'.format(group),
        line = dict(
            color = 'rgb(0,0,0)',
            width = linewidth,
            dash = dash_style,
            ),
        legendgroup=group,
        )
#####
    trace2a = go.Scatter(
        x = x,
        y = y2a,
        yaxis='y2',
        name='SOLAR ({})'.format(group),
        line = dict(
            color = 'rgb(232,166,40)',
            width = linewidth,
            dash = dash_style,
            ),
        legendgroup=group,
        )
#####
    trace3a = go.Scatter(
        x = x,
        y = y3a,
        yaxis='y2',
        name='PEOPLE ({})'.format(group),
        line = dict(
            color = 'rgb(57, 88, 39)',
            width = linewidth,
            dash = dash_style,
            ),
        legendgroup=group,
        )
#####
    trace4a = go.Scatter(
        x = x,
        y = y4a,
        yaxis='y2',
        name='VNT ({})'.format(group),
        line = dict(
            color = 'rgb(12, 122, 166)',
            width = linewidth,
            dash = dash_style,
            ),
        legendgroup=group,
        )
#####
    trace5a = go.Scatter(
        x = x,
        y = y5a,
        yaxis='y1',
        name='VNT ({})'.format(group),
        line = dict(
            color = 'rgb(44, 179, 175)',
            width = linewidth,
            dash = dash_style,
            ),
        legendgroup=group,
        )

    traces_hr = [trace5a, trace2a, trace3a, trace4a, trace1a]
    return traces_hr

#####



def dash_HR_add_traces_EXT(df, group, linewidth):

    # PLOTTING
    x = df.index
    y_Tmax = df['TM59_Tmax']
    y0 = df['ODT']

    trace_Tmax = go.Scatter(
        x = x,
        y = y_Tmax,
        yaxis='y3',
        name='Tmax',
        line = dict(
            color = 'rgba(178,34,34,0.4)',
            width = linewidth,
            # dash = 'dash',
            ),
        legendgroup=group,
        )
    #####
    trace0 = go.Scatter(
        x = x,
        y = y0,
        yaxis='y3',
        name='EXT TEMP',
        line = dict(
            color = 'rgb(200,200,200)',
            width = linewidth,
            # dash = 'dot'
            ),
        legendgroup=group,
        )

    traces_hr = [ trace0, trace_Tmax ]
    return traces_hr


#####


def dash_HR_add_traces_EP(df, group, room, linewidth):

    # PLOTTING
    x = df.index
    y0 = df['ODT']
    y1b = df[room+'_OT']
    y2b = df[room+'_HG_SOLAR(W)']
    y3b = df[room+'_HG_PPL(W)']
    y4b = df[room+'_HL_VNT(W)']
    y5b = df[room+'_VNT(ach)']
    #

#####   
    trace1b = go.Scatter(
        x = x,
        y = y1b,
        yaxis='y3',
        name='TEMP (EP)',
        line = dict(
            color = 'rgb(0,0,0)',
            width = linewidth,
            # dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace2b = go.Scatter(
        x = x,
        y = y2b,
        yaxis='y2',
        name='SOLAR (EP)',
        line = dict(
            color = 'rgb(232,166,40)',
            width = linewidth,
            # dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace3b = go.Scatter(
        x = x,
        y = y3b,
        yaxis='y2',
        name='PEOPLE (EP)',
        line = dict(
            color = 'rgb(57, 88, 39)',
            width = linewidth,
            # dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace4b = go.Scatter(
        x = x,
        y = -y4b,
        yaxis='y2',
        name='VNT (EP)',
        line = dict(
            color = 'rgb(12, 122, 166)',
            width = linewidth,
            # dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace5b = go.Scatter(
        x = x,
        y = y5b,
        yaxis='y1',
        name='VNT (EP)',
        line = dict(
            color = 'rgb(44, 179, 175)',
            width = linewidth,
            # dash = dash_style,
            ),
        legendgroup='ep',
        )


    traces_hr = [
        trace5b,
        trace2b, trace3b, trace4b,
        trace1b,
        ]
    return traces_hr



#####

def create_layout_EP_IES_HR(D_value, F_value, room):
    
    layout_hr = go.Layout(
        title='EP-IES comparison for<br>' \
        '<i>unit</i>: <b>{}</b> | <i>floor</i>: <b>{}</b> |  <i>room</i>: <b>{}</b>'.format(D_value,F_value,room),
        yaxis1=dict(
            domain=[0, 0.12], range=[0,8], dtick=2, showgrid=False,
            #
            title='<b>NAT. VENT.<br>(ACH)</b>',
            titlefont=dict(
                family='Calibri Light,sans-serif',
                size=15,
                color='grey'
                ),
            showticklabels=True,
            tickfont=dict(
                family='Calibri,sans-serif',
                size=11,
                color='grey'
                ),
            ),
        #
        yaxis2=dict(
            domain=[0.18, 0.55], range=[-600,800], dtick=200, showgrid=True,
            ticksuffix='W',
            #
            title='<b>HEAT GAINS / LOSSES</b>',
            titlefont=dict(
                family='Calibri Light,sans-serif',
                size=15,
                color='grey'
                ),
            showticklabels=True,
            tickfont=dict(
                family='Calibri,sans-serif',
                size=11,
                color='grey'
                ),
            ),
        #
        yaxis3=dict(
            domain=[0.62,1], range=[20,34], dtick=2, showgrid=True,
            ticksuffix='°C',
            #
            title='<b>TEMPERATURE</b>',
            titlefont=dict(
                family='Calibri Light,sans-serif',
                size=15,
                color='grey'
                ),
            showticklabels=True,
            tickfont=dict(
                family='Calibri,sans-serif',
                size=11,
                color='grey'
                ),
        ),
    )

    return layout_hr
