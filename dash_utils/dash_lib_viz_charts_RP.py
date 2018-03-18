# other libraries
import matplotlib
matplotlib.use('Agg')
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





def dash_fig_multi_RP_add_bars(fig_multi, df_ies, df_ep, N, N_angle_dict, row,
    room, bar_width, outline_width, colors_dict, all_traces):

    df_ies = df_ies.loc[ df_ies['@north'].astype(int) == N ]
    df_ies.set_index('@north', inplace=True)
    engine = 'IES'
    bar_fill = 'rgba(0,0,0,0)' 
    #

    # y = '{} ({})'.format(df_ies.index,N_angle_dict[df_ies.index])
    y = df_ies.index
    # print('y: {}'.format(y))

    #
    x1a = df_ies[room+'_HL_VNT(kWh)']
    name='HL_VNT({})'.format(engine),
    # text = '{}'.format(x1a[0].round(1))
    trace1a = go.Bar(
        x = x1a,
        y = y,
        xaxis='x1',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HL_'+engine], width=outline_width),
            color=bar_fill,
            ),        
        # name=text,
        # text=text,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace1a, row=row, col=1)
    all_traces.append(trace1a)
    # print(trace.name, text)

    #
    x2a = df_ies[room+'_HG_SOLAR(kWh)']
    name='HL_SOLAR({})'.format(engine)
    # text = '{}'.format(x2a[0].round(1))
    trace2a = go.Bar(
        x = x2a,
        y = y,
        xaxis='x2',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HG_'+engine], width=outline_width),
            color=bar_fill,
            ),        
        # name=name,
        # text=text,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace2a, row=row, col=2)
    all_traces.append(trace2a)
    # print(trace.name, text)
    
    #
    x3a = df_ies[room+'_VNT(l/s)']
    name = 'VNT(l/s)({})'.format(engine)
    # text = '{}'.format(x3a[0].round(1))
    trace = go.Bar(
        x = x3a,
        y = y,
        xaxis='x3',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HL_'+engine], width=outline_width),
            color=bar_fill,
            ),
        # name=name,
        # text=text,
        textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=3)
    all_traces.append(trace)
    # print(trace.name, text)

    #
    x4a = df_ies[room+'_VNT(ach)']
    name='VNT(ach)({})'.format(engine),
    # text = '{}'.format(x4a[0].round(1))
    trace = go.Bar(
        x = x4a,
        y = y,
        xaxis='x4',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['VNT_'+engine], width=outline_width),
            color=bar_fill,
            ),
        # name=name,
        # text=text,
        textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)
    # print(trace.name, text)

    x5a = df_ies[room+'_HA26p'] * 100
    name='_HA26p({})'.format(engine),
    trace = go.Bar(
        x = x5a,
        y = y,
        xaxis='x5',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['OH_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        # text='{}'.format(y3a[0].round(1)), textposition='inside',
        # textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=5)
    all_traces.append(trace)

    #
    x6a = df_ies[room+'_TM59_Ca'] * 100
    name = 'TM59_Ca({})'.format(engine),
    # text = '{}'.format(x5a[0].round(1))
    trace = go.Bar(
        x = x6a,
        y = y,
        xaxis='x6',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['OH_'+engine], width=outline_width),
            color=bar_fill,
            ),
        # name=name,
        # text=text,
        textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=6)
    all_traces.append(trace)
    # print(trace.name, text)


#####

    engine = 'EP'
    df_ep = df_ep.loc[ df_ep['@north'] == N ]
    #
    x1b = - df_ep[room+'_HL_VNT(kWh)']
    name='HL_VNT({})'.format(engine),
    trace = go.Bar(
        x = x1b,
        y = y,
        xaxis='x1',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['HL_'+engine]),
        # name=name,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)
    # print(trace.name, text)

    #
    x2b = df_ep[room+'_HG_SOLAR(kWh)']
    name='HL_SOLAR({})'.format(engine),
    # text = '{}'.format(x2b[0].round(1))
    trace = go.Bar(
        x = x2b,
        y = y,
        xaxis='x2',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['HG_'+engine]),        
        # name=name,
        # text=text,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)
    # print(trace.name, text)

    #
    x3b = df_ep[room+'_VNT(l/s)']
    name='VNT(l/s)({})'.format(engine)
    # text = '{}'.format(x3b[0].round(1))
    # if x3b>x3a:
    #     text_pos = 'outside'
    # else:
    #     text_pos = 'inside'

    trace = go.Bar(
        x = x3b,
        y = y,
        xaxis='x3',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['VNT_'+engine]),
        # name=name,
        # text=text,
        # textposition=text_pos,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=3)
    all_traces.append(trace)
    # print(trace.name, text)

    #
    x4b = df_ep[room+'_VNT(ach)']
    # name='VNT(ach)({})'.format(engine)
    # text = '{}'.format(x4b[0].round(1))
    # if x4b>x4a:
    #     text_pos = 'outside'
    # else:
    #     text_pos = 'inside'

    trace = go.Bar(
        x = x4b,
        y = y,
        xaxis='x4',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['VNT_'+engine]),
        # name=name,
        # text=text,
        # textposition=text_pos,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)
    # print(trace.name, text)


    #
    x5b = df_ep[room+'_HA26p'] * 100
    name='_HA26p({})'.format(engine)
    # text = '{}'.format(x5b[0].round(1))
    text_pos = 'inside'    
    trace = go.Bar(
        x = x5b,
        y = y,
        xaxis='x5',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['OH_'+engine]),
        # name=name,
        # text=text,
        textposition=text_pos,
        textfont=dict(color='rgba(0,0,0,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=5)
    all_traces.append(trace)
    # print(trace.name, text)

    #
    x6b = df_ep[room+'_TM59_Ca'] * 100
    name='TM59_Ca({})'.format(engine)
    # text = '{}'.format(x5b[0].round(1))
    text_pos = 'inside'    
    trace = go.Bar(
        x = x6b,
        y = y,
        xaxis='x6',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['OH_'+engine]),
        # name=name,
        # text=text,
        textposition=text_pos,
        textfont=dict(color='rgba(0,0,0,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=6)
    all_traces.append(trace)
    # print(trace.name, text)



#####










#####

def fig_multi_RP_add_bars(fig_multi, df_ies, df_ep, N, N_angle_dict, row,
    room, bar_width, outline_width, colors_dict, all_traces):

    df_ies = df_ies.loc[ df_ies['@north'] == int(N) ]
    df_ep = df_ep.loc[ df_ep['@north'] == int(N) ]
    # print(df_ies)


    engine = 'IES'
    bar_fill = 'rgba(0,0,0,0)' 
    #
    y1a = df_ies[room+'_HL_VNT(kWh)']
    name='HL_VNT({})'.format(engine),
    trace = go.Bar(
        x = y1a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x1',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HL_'+engine], width=outline_width),
            color=bar_fill,
            ),        
        name=name, text='{}'.format(room), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)
    
    #
    y2a = df_ies[room+'_HG_SOLAR(kWh)']
    name='HL_SOLAR({})'.format(engine),
    trace = go.Bar(
        x = y2a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x2',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HG_'+engine], width=outline_width),
            color=bar_fill,
            ),        
        name=name, text='{}'.format(room), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)

    
    #
    y3a = df_ies[room+'_VNT(l/s)']
    name='VNT(l/s)({})'.format(engine),
    trace = go.Bar(
        x = y3a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x3',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HL_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y3a[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=3)
    all_traces.append(trace)
    
    #
    y4a = df_ies[room+'_VNT(ach)']
    name='VNT(ach)({})'.format(engine),
    trace = go.Bar(
        x = y4a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x4',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['VNT_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y4a[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)

    #
    y5a = df_ies[room+'_TM59_Ca'] * 100
    name='TM59_Ca({})'.format(engine),
    trace = go.Bar(
        x = y5a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x5',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['OH_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y5a[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=5)
    all_traces.append(trace)



#####

    engine = 'EP'
    #
    y1b = - df_ep[room+'_HL_VNT(kWh)']
    name='HL_VNT({})'.format(engine),
    trace = go.Bar(
        x = y1b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x1',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['HL_'+engine]),
        name=name, legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)

    #
    y2b = df_ep[room+'_HG_SOLAR(kWh)']
    name='HL_SOLAR({})'.format(engine),
    trace = go.Bar(
        x = y2b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x2',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['HG_'+engine]),        
        name=name, text='{}'.format(engine), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)

    #
    y3b = df_ep[room+'_VNT(l/s)']
    name='VNT(l/s)({})'.format(engine)
    if y3b[0]>y3a[0]:
        text_pos = 'outside'
    else:
        text_pos = 'inside'

    trace = go.Bar(
        x = y3b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x3',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['VNT_'+engine]),
        name=name,
        text='{}'.format(y3b[0].round(1)),
        textposition=text_pos,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=3)
    all_traces.append(trace)

    #
    y4b = df_ep[room+'_VNT(ach)']
    name='VNT(ach)({})'.format(engine)
    if y4b[0]>y4a[0]:
        text_pos = 'outside'
    else:
        text_pos = 'inside'

    trace = go.Bar(
        x = y4b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x4',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['VNT_'+engine]),
        name=name,
        text='{}'.format(y4b[0].round(1)),
        textposition=text_pos,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)

    #
    y5b = df_ep[room+'_TM59_Ca'] * 100
    name='TM59_Ca({})'.format(engine),
    text_pos = 'inside'    
    trace = go.Bar(
        x = y5b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x5',
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['OH_'+engine]),
        name=name,
        text='{}'.format(y5b[0].round(1)),
        textposition=text_pos,
        textfont=dict(color='rgba(0,0,0,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=5)
    all_traces.append(trace)




#####


def create_update_menu_RP(df_ep, values_list, groups, lenght_true_false, U, F):

    df_ep = df_ep.loc[ df_ep['@vnt_B(l/s)'] == values_list[0] ]
    values_KL = df_ep['@vnt_KL(l/s)'].unique()



    true_set = list(np.ones(lenght_true_false, dtype=bool))
    false_set = list(np.zeros(lenght_true_false, dtype=bool))

    updatemenus = list([dict(active=0,
        buttons=list([
            dict(label = '{}l/s'.format(values_list[0]),
                method = 'update',
                args = [
                {'visible': groups * (true_set+false_set+false_set)},
                {'title': 'EPLUS-IES COMPARISON<br><i>unit</i>: <b>{}</b> | <i>floor</i>: <b>{}</b>'.format(U, F)+
                ' | <i>max.vnt.rate</i>: <b>{}</b>l/s'.format(values_list[0])},
                ]
                ),
            dict(label = '{}l/s'.format(values_list[1]),
                method = 'update',
                args = [
                {'visible': groups * (false_set+true_set+false_set)},
                {'title': 'EPLUS-IES COMPARISON<br><i>unit</i>: <b>{}</b> | <i>floor</i>: <b>{}</b>'.format(U, F)+
                ' | <i>max.vnt.rate</i>: <b>{}</b>l/s'.format(values_list[1])},
                ],
                ),
            dict(label = '{}l/s'.format(values_list[2]),
                method = 'update',
                args = [
                {'visible': groups * (false_set+false_set+true_set)},
                {'title': 'EPLUS-IES COMPARISON<br><i>unit</i>: <b>{}</b> | <i>floor</i>: <b>{}</b>'.format(U, F)+
                ' | <i>max.vnt.rate</i>: <b>{}</b>l/s'.format(values_list[2])},
                ],
                ),
            ]),
        direction = 'down',
        pad = {'r': 10, 't': 10},
        showactive = True,
        x = 0.68,
        xanchor = 'left',
        y = 1.08,
        yanchor = 'top' 
    )])

    return updatemenus


######












#####

def fig_multi_RP_add_traces_EP_IES_SAP(fig_multi, df_ies, df_ep, df_sap, N, N_angle_dict, row,
    room, bar_width, outline_width, colors_dict, all_traces):

    df_ies = df_ies.loc[ df_ies['@north'] == int(N) ]
    df_ep = df_ep.loc[ df_ep['@north'] == int(N) ]
    # print(df_ies)


    engine = 'IES'
    bar_fill = 'rgba(0,0,0,0)' 
    #
    y1a = df_ies[room+'_HG_SOLAR(W)']
    name='HL_SOLAR({})'.format(engine),
    trace = go.Bar(
        x = y1a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(1*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HG_'+engine], width=outline_width),
            color=bar_fill,
            ),        
        name=name, text='{}'.format(room), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)

        
    #
    y2a = df_ies[room+'_VNT(ach)']
    name='VNT(ach)({})'.format(engine),
    trace = go.Bar(
        x = y2a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(2*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['VNT_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y2a[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)


    #
    y3a = df_ies[room+'_HA26p'] * 100
    name='_HA26p({})'.format(engine),
    trace = go.Bar(
        x = y3a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(3*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['OH_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y3a[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=3)
    all_traces.append(trace)


    #
    y4a = df_ies[room+'_TM59_Ca'] * 100
    name='TM59_Ca({})'.format(engine),
    trace = go.Bar(
        x = y4a,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(4*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['OH_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y4a[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)



#####

    engine = 'EP'
    #
    y1b = df_ep[room+'_HG_SOLAR(W)']
    name='HL_SOLAR({})'.format(engine),
    trace = go.Bar(
        x = y1b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(1*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['HG_'+engine]),        
        name=name, text='{}'.format(engine), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)


    #
    y2b = df_ep[room+'_VNT(ach)']
    name='VNT(ach)({})'.format(engine)
    trace = go.Bar(
        x = y2b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(2*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['VNT_'+engine]),
        name=name,
        # text='{}'.format(y2b[0].round(1)),

        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)


    #
    y3b = df_ep[room+'_HA26p'] * 100
    name='HA26p({})'.format(engine),
    trace = go.Bar(
        x = y3b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(3*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['OH_'+engine]),
        name=name,
        # text='{}'.format(y3b[0].round(1)),
        textfont=dict(color='rgba(0,0,0,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=3)
    all_traces.append(trace)

    #
    y4b = df_ep[room+'_TM59_Ca'] * 100
    name='TM59_Ca({})'.format(engine),
    text_pos = 'inside'    
    trace = go.Bar(
        x = y4b,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(4*row),
        yaxis='y{}'.format(row),
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['OH_'+engine]),
        name=name,
        # text='{}'.format(y4b[0].round(1)),
        # textposition=text_pos,
        textfont=dict(color='rgba(0,0,0,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)





def fig_multi_RP_add_traces_EP_IES_SAP_ALL(fig_multi, df_ies, df_ep, df_sap, N, N_angle_dict, row,
    room, bar_width, outline_width, colors_dict, all_traces):


    df_ies = df_ies.loc[ df_ies['@north'] == int(N) ]
    df_ep = df_ep.loc[ df_ep['@north'] == int(N) ]
    row = 3

    ######
    
    engine = 'IES'
    bar_fill = 'rgba(0,0,0,0)' 
    #
    y1a_sum = df_ies['BD1_HG_SOLAR(W)'] + df_ies['KL_HG_SOLAR(W)']
    name='HL_SOLAR({})'.format(engine),
    trace = go.Bar(
        x = y1a_sum,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(1*row),
        yaxis='y3',
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['HG_'+engine], width=outline_width),
            color=bar_fill,
            ),        
        name=name, text='{}'.format(room), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)

        
    #
    y2a_avg = (df_ies['BD1_VNT(ach)']*35.25 + df_ies['BD1_VNT(ach)']*64.76)/149.69

    name='VNT(ach)({})'.format(engine),
    trace = go.Bar(
        x = y2a_avg,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(2*row),
        yaxis='y3',
        orientation='h',
        width=bar_width,
        marker=dict(
            line=dict(color=colors_dict['VNT_'+engine], width=outline_width),
            color=bar_fill,
            ),
        name=name,
        text='{}'.format(y2a_avg[0].round(1)), textposition='inside',
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)



    engine = 'EP'
    #
    y1b_sum = df_ep['BD1_HG_SOLAR(W)'] + df_ep['KL_HG_SOLAR(W)']
    name='HL_SOLAR({})'.format(engine),
    trace = go.Bar(
        x = y1b_sum,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(1*row),
        yaxis='y3',
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['HG_'+engine]),        
        name=name, text='{}'.format(engine), legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)


    #
    y2b_avg = (df_ep['BD1_VNT(ach)']*35.25 + df_ep['BD1_VNT(ach)']*64.76)/149.69
    name='VNT(ach)({})'.format(engine)

    trace = go.Bar(
        x = y2b_avg,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(2*row),
        yaxis='y3',
        orientation='h',
        width=bar_width,
        marker=dict(color=colors_dict['VNT_'+engine]),
        name=name,
        # text='{}'.format(y2b_avg[0].round(1)),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)


#####

    df_sap = df_sap.loc[ df_sap['@north'] == int(N) ]

    
    y1sap = df_sap['Gss_jun']
    name='Gss_jun',
    trace = go.Scatter(
        x = y1sap,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(1*row),
        yaxis='y{}'.format(row),
        marker=dict(
            size=10,
            color='rgba(0,0,0,0.8',
            symbol='circle-open',
        ),      
        name=name,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=1)
    all_traces.append(trace)


    #
    y2sap = df_sap['SAP_P1(ach)']
    name='SAP_P1(ach)',
    trace = go.Scatter(
        x = y2sap,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(2*row),
        yaxis='y{}'.format(row),
        marker=dict(
            size=10,
            color='rgba(0,0,0,0.8',
            symbol='circle-open',
        ),      
        name=name,
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=2)
    all_traces.append(trace)


    #
    y5sap = df_sap['Tt_jun']
    name='Tt_jun',
    trace = go.Scatter(
        x = y5sap,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(4*row),
        yaxis='y{}'.format(row),
        marker=dict(
            size=10,
            color='rgba(0,0,0,0.8',
            symbol='star-open',
            ),
        name=name,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)

    y5sap = df_sap['Tt_jul']
    name='Tt_jul',
    trace = go.Scatter(
        x = y5sap,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(4*row),
        yaxis='y{}'.format(row),
        marker=dict(
            size=10,
            color='rgba(0,0,0,0.8',
            symbol='square-open',
            ),
        name=name,
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)

    y5sap = df_sap['Tt_aug']
    name='Tt_aug',
    trace = go.Scatter(
        x = y5sap,
        y = '{} ({})'.format(N,N_angle_dict[N]),
        xaxis='x{}'.format(4*row),
        yaxis='y{}'.format(row),
        marker=dict(
            size=10,
            color='rgba(0,0,0,0.8',
            symbol='triangle-up-open',
            ),
        name=name,      
        textfont=dict(color='rgba(255,255,255,0.8)'),
        legendgroup='{}'.format(engine),
        )
    fig_multi.append_trace(trace, row=row, col=4)
    all_traces.append(trace)
