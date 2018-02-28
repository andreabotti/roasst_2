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





def dash_HR_add_traces(df_ies_hr, df_ep_hr, room, dash_style):

    # PLOTTING
    x = df_ep_hr.index
    #            
    y0 = df_ep_hr['ODT']
    y1a = df_ies_hr[room+'_OT']
    y1b = df_ep_hr[room+'_OT']
    #
    y2a = df_ies_hr[room+'_HG_SOLAR(W)']
    y2b = df_ep_hr[room+'_HG_SOLAR(W)']
    #
    y3a = df_ies_hr[room+'_HG_PPL(W)']
    y3b = df_ep_hr[room+'_HG_PPL(W)']
    #
    y4a = df_ies_hr[room+'_HL_VNT(W)']
    y4b = df_ep_hr[room+'_HL_VNT(W)']
    #
    y5a = df_ies_hr[room+'_VNT(ach)']
    y5b = df_ep_hr[room+'_VNT(ach)']
    #
    y_Tmax = df_ep_hr['Tmax']
#####
    

    trace_Tmax = go.Scatter(
        x = x,
        y = y_Tmax,
        yaxis='y3',
        name='Tmax',
        line = dict(
            color = 'rgba(178,34,34,0.4)',
            width = 2,
            # dash = 'dash',
            ),
        legendgroup='ext',
        )
    #####
    trace0 = go.Scatter(
        x = x,
        y = y0,
        yaxis='y3',
        name='EXT TEMP',
        line = dict(
            color = 'rgb(200,200,200)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ext',
        )
    trace1a = go.Scatter(
        x = x,
        y = y1a,
        yaxis='y3',
        name='TEMP (IES)',
        line = dict(
            color = 'rgb(0,0,0)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
    trace1b = go.Scatter(
        x = x,
        y = y1b,
        yaxis='y3',
        name='TEMP (EP)',
        line = dict(
            color = 'rgb(0,0,0)',
            width = 2,
            dash = 'dot'
            ),
        legendgroup='ep',
        )
#####
    trace2a = go.Scatter(
        x = x,
        y = y2a,
        yaxis='y2',
        name='SOLAR (IES)',
        line = dict(
            color = 'rgb(232,166,40)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
    trace2b = go.Scatter(
        x = x,
        y = y2b,
        yaxis='y2',
        name='SOLAR (EP)',
        line = dict(
            color = 'rgb(232,166,40)',
            width = 2,
            dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace3a = go.Scatter(
        x = x,
        y = y3a,
        yaxis='y2',
        name='PEOPLE (IES)',
        line = dict(
            color = 'rgb(57, 88, 39)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
    trace3b = go.Scatter(
        x = x,
        y = y3b,
        yaxis='y2',
        name='PEOPLE (EP)',
        line = dict(
            color = 'rgb(57, 88, 39)',
            width = 2,
            dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace4a = go.Scatter(
        x = x,
        y = y4a,
        yaxis='y2',
        name='VNT (IES)',
        line = dict(
            color = 'rgb(12, 122, 166)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
    trace4b = go.Scatter(
        x = x,
        y = -y4b,
        yaxis='y2',
        name='VNT (EP)',
        line = dict(
            color = 'rgb(12, 122, 166)',
            width = 2,
            dash = dash_style,
            ),
        legendgroup='ep',
        )
#####
    trace5a = go.Scatter(
        x = x,
        y = y5a,
        yaxis='y1',
        name='VNT (IES)',
        line = dict(
            color = 'rgb(44, 179, 175)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
    trace5b = go.Scatter(
        x = x,
        y = y5b,
        yaxis='y1',
        name='VNT (EP)',
        line = dict(
            color = 'rgb(44, 179, 175)',
            width = 2,
            dash = dash_style,
            ),
        legendgroup='ep',
        )


    traces_hr = [
    trace5a, trace5b,
    trace2a, trace2b, trace3a, trace3b, trace4a, trace4b,
    trace0, trace1a, trace1b,
    trace_Tmax
    ]

    return traces_hr

#####



def dash_HR_add_traces_IES(df_ies_hr, room, dash_style):

    # PLOTTING
    x = df_ies_hr.index
    #            
    y1a = df_ies_hr[room+'_OT']
    y2a = df_ies_hr[room+'_HG_SOLAR(W)']
    y3a = df_ies_hr[room+'_HG_PPL(W)']
    y4a = df_ies_hr[room+'_HL_VNT(W)']
    y5a = df_ies_hr[room+'_VNT(ach)']
#####

    trace1a = go.Scatter(
        x = x,
        y = y1a,
        yaxis='y3',
        name='TEMP (IES)',
        line = dict(
            color = 'rgb(0,0,0)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
#####
    trace2a = go.Scatter(
        x = x,
        y = y2a,
        yaxis='y2',
        name='SOLAR (IES)',
        line = dict(
            color = 'rgb(232,166,40)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
#####
    trace3a = go.Scatter(
        x = x,
        y = y3a,
        yaxis='y2',
        name='PEOPLE (IES)',
        line = dict(
            color = 'rgb(57, 88, 39)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
#####
    trace4a = go.Scatter(
        x = x,
        y = y4a,
        yaxis='y2',
        name='VNT (IES)',
        line = dict(
            color = 'rgb(12, 122, 166)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )
#####
    trace5a = go.Scatter(
        x = x,
        y = y5a,
        yaxis='y1',
        name='VNT (IES)',
        line = dict(
            color = 'rgb(44, 179, 175)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ies',
        )

    traces_hr = [trace5a, trace2a, trace3a, trace4a, trace1a]
    return traces_hr

#####


def dash_HR_add_traces_EP(df_ep_hr, room, dash_style):

    # PLOTTING
    x = df_ep_hr.index
    y0 = df_ep_hr['ODT']
    y1b = df_ep_hr[room+'_OT']
    y2b = df_ep_hr[room+'_HG_SOLAR(W)']
    y3b = df_ep_hr[room+'_HG_PPL(W)']
    y4b = df_ep_hr[room+'_HL_VNT(W)']
    y5b = df_ep_hr[room+'_VNT(ach)']
    #
    y_Tmax = df_ep_hr['Tmax']
#####   

    trace_Tmax = go.Scatter(
        x = x,
        y = y_Tmax,
        yaxis='y3',
        name='Tmax',
        line = dict(
            color = 'rgba(178,34,34,0.4)',
            width = 2,
            # dash = 'dash',
            ),
        legendgroup='ext',
        )
    #####
    trace0 = go.Scatter(
        x = x,
        y = y0,
        yaxis='y3',
        name='EXT TEMP',
        line = dict(
            color = 'rgb(200,200,200)',
            width = 2,
            # dash = 'dot'
            ),
        legendgroup='ext',
        )
    trace1b = go.Scatter(
        x = x,
        y = y1b,
        yaxis='y3',
        name='TEMP (EP)',
        line = dict(
            color = 'rgb(0,0,0)',
            width = 2,
            dash = 'dot'
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
            width = 2,
            dash = dash_style,
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
            width = 2,
            dash = dash_style,
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
            width = 2,
            dash = dash_style,
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
            width = 2,
            dash = dash_style,
            ),
        legendgroup='ep',
        )


    traces_hr = [
    trace5b,
    trace2b, trace3b, trace4b,
    trace0, trace1b,
    trace_Tmax
    ]
    return traces_hr



#####

def create_layout_EP_IES_HR(D_value, F_value, room):
    
    layout_hr = go.Layout(
        title='EP-IES comparison for<br>' \
        '<i>unit</i>: <b>{}</b> | <i>floor</i>: <b>{}</b> |  <i>room</i>: <b>{}</b>'.format(D_value,F_value,room),
        yaxis1=dict(
            domain=[0, 0.12], range=[0,6], dtick=2, showgrid=False,
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
                size=12,
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
                size=12,
                color='grey'
                ),
            ),
        #
        yaxis3=dict(
            domain=[0.62,1], range=[19.8,32.2], dtick=2, showgrid=True,
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
                size=12,
                color='grey'
                ),
        ),
    )

    return layout_hr
