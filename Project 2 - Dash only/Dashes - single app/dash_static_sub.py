import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools

import colorlover as cl

YlGnBu = cl.scales['9']['seq']['YlGnBu']
BrBG = cl.scales['9']['seq']['Reds']
PuRd = cl.scales['9']['seq']['PuRd']

colours = [ i for j in [YlGnBu,BrBG, PuRd] for i in j ]

df = pd.read_csv('for_dash.csv')

#############################################################
def sub_plot(pivot, type,x,y, legend, variable):
    colors = ['#e6194b', '#f58231', '#ffe119', '#bfef45', '#3cb44b', '#42d4f4', '#4363d8', '#911eb4', '#f032e6', '#e6beff', '#a9a9a9','blue']
    c = 0
    full_trace = []
    for i in pivot[variable].unique():
        ggg = pivot[pivot[variable]==i]
        trace = go.Scatter(dict(x = ggg['Year'], y= ggg[type].values, name = i, legendgroup = 'group1', showlegend = legend,
                                mode = 'lines+markers', xaxis = x, yaxis = y, marker = dict(color = colors[c])))
        c+=1
        full_trace.append(trace)
    return full_trace
'''
sub_layout = go.Layout(legend = dict(legend_pos, orientation="h", bgcolor = 'grey', bordercolor = 'white',
                   borderwidth=2, font = dict(size=10, color = 'white')), # x = 0.435, y=1
              plot_bgcolor = 'black', paper_bgcolor = 'lightgrey', font = dict(color = 'black'),
              xaxis1 = dict(autotick = False, tickangle = 270, dtick = 2, **dict(domain=[0, 0.41], anchor='y1')),
              xaxis2 = dict(autotick = False, tickangle = 270, dtick = 2, **dict(domain=[0.59, 1], anchor='y2'),autorange='reversed'),
              yaxis1 = dict(**dict(domain=[0,1], anchor='x1'),overlaying='y', side='right'),
              yaxis2 = dict(**dict(domain=[0,1], anchor='x2'))  # , overlaying='y', side='right'
              )
'''

# Killed / Wounded by region
def plots(variable, x_legend_pos):
    by_region = df.pivot_table(index = [variable, 'Year'], values = ['Killed','Wounded'], aggfunc=sum).reset_index()
    killed_by_region_trace = sub_plot(by_region, 'Killed','x1','y1', True, variable)
    wounded_by_region_trace= sub_plot(by_region, 'Wounded','x2','y2', False, variable)

    fig = tools.make_subplots(rows=1, cols=2,
                              specs = [[{},{}]], shared_yaxes=True,
                              subplot_titles = ('Dymanic Killed by {}'.format(variable), 'Dynamic Wounded by {}'.format(variable)))
    for i in range(0,len(df[variable].unique())):
        fig['data'].append(killed_by_region_trace[i])
        fig['data'].append(wounded_by_region_trace[i])

    sub_layout = go.Layout(legend = dict(orientation="h", bgcolor = 'grey', bordercolor = 'white',
                       borderwidth=2, font = dict(size=10, color = 'white'), x=x_legend_pos, y=1), # x = 0.435, y=1
                  plot_bgcolor = 'black', paper_bgcolor = 'grey', font = dict(color = 'white'),
                  xaxis1 = dict(autotick = False, tickangle = 270, dtick = 2, **dict(domain=[0, 0.41], anchor='y1')),
                  xaxis2 = dict(autotick = False, tickangle = 270, dtick = 2, **dict(domain=[0.59, 1], anchor='y2'),autorange='reversed'),
                  yaxis1 = dict(**dict(domain=[0,1], anchor='x1'),overlaying='y', side='right'),
                  yaxis2 = dict(**dict(domain=[0,1], anchor='x2')),  # , overlaying='y', side='right'
                  height = 500)

    fig['layout'].update(sub_layout)
    return fig

region_plots = plots('Region', 0.435)
month_plots = plots('Month', 0.465)

######################################################################################
# Bubble chart
def get_bubble(variable, title):
    pivot = df.pivot_table(index = variable, values = ['Killed','Wounded'], aggfunc=sum).reset_index()
    pivot['sum'] = pivot['Killed']+pivot['Wounded']
    pivot['perc'] = pivot['sum'].div(pivot['sum'].sum())
    pivot['perc'] = round((pivot['perc']*100),2)

    def get_size(x):
        if x <=1: return 2
        elif (x >1) & (x<=2.5): return 4
        elif (x >2.5) & (x <=5): return 6
        elif (x >5) & (x<=10): return 8
        elif (x >10) & (x<=26): return 12
        else: return 16
    pivot_size = pivot['perc'].apply(lambda x:  get_size(int(x)))
    pivot['size'] =pivot['perc'].apply(lambda x:  get_size(int(x)))
    pivot['colors'] = colours[0:len(pivot)]

    full_text = []
    for i in range(len(pivot)):
        text = pivot.loc[i,variable]+' ({}%)<br>Killed: {}<br>Wounded: {}'.format(pivot.loc[i,'perc'].astype(str),
                                                                                 pivot.loc[i,'Killed'].astype(int).round(),
                                                                                 pivot.loc[i,'Wounded'].astype(int).round())
        full_text.append(text)
    pivot['text'] = full_text

    full_bubble = []
    for i in pivot[variable].unique():
        reg = pivot[pivot[variable]==i]
        trace = go.Scatter(x=reg['Wounded'], y= reg['Killed'], mode = 'markers', text = reg['text'], textposition = 'bottom center',
                       name = i, hoverinfo = 'text',
                       marker = dict(size = reg['size']*5, color = reg['colors']))
        full_bubble.append(trace)

    layout = go.Layout(title = 'Ratio Killed to Wounded by {}'.format(title),
                      font = dict(color = 'white'), paper_bgcolor='grey', plot_bgcolor = 'black',
                      xaxis = dict( title = 'Wounded', type = 'log'),
                      yaxis = dict(range = pivot['Killed'], title = 'Killed', type = 'log'),
                      hovermode = 'closest')


    fig = go.Figure(data = full_bubble, layout = layout)

    return fig

# Bubble
buggle = get_bubble('Region', 'Region')
target = get_bubble('Target_type', 'Type of target')
weapon = get_bubble('Weapon_type', 'Type of Weapon')


#########################################################################################
app = dash.Dash()

app.layout = html.Div(style={'height':'1000', 'background':'white', 'width':'1600px'}, children = [
    # title
    html.H1(children = 'My first Dash', style={'textAlign':'center', 'color':'white'}),

    # chart 1 left
    html.Div(style = {'float':'left', 'width':'1600px'}, children = [
        dcc.Graph(id = 'killed_by_region', figure = region_plots)
    ]),

    # chart 2 left
    html.Div(style = {'float':'left', 'width':'1600px'}, children = [
        dcc.Graph(id = 'killed_by_mont', figure = month_plots)
    ]),

    # Bubble chart 1
    html.Div(style = {'float':'left', 'width':'1600px'}, children = [
        dcc.Graph(id = 'bubble-chart', figure = buggle)
    ]),

    # Bubble chart 2
    html.Div(style = {'float':'left', 'width':'1600px'}, children = [
        dcc.Graph(id = 'target_bubble-chart', figure = target)
    ]),

    # Bubble chart 3
    html.Div(style = {'float':'left', 'width':'1600px'}, children = [
        dcc.Graph(id = 'weapon_bubble-chart', figure = weapon)
    ]),
])


if __name__=='__main__':
    app.run_server(debug = True)
