import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools

def General_info():
    df = pd.read_csv('for_dash.csv')

    def map():
        full_trace = []
        for i in df['inj-group'].unique():
            map=df[df['inj-group']==i]
            #map=df[(df['inj-group']==i)&(df['Year']==2001)]
            trace = dict(
                       type = 'scattergeo',
                       locationmode = 'world',
                       showlegend = True,
                       #sort = True,
                       name = str(i),
                       lon = map['longitude'],
                       lat = map['latitude'],
                       text = map['text'],
                       mode = 'markers',
                       hoverinfo = 'text',
                       marker = dict(opacity = 0.8, size=3)
                       )
            full_trace.append(trace)
        layout = dict(
                 title = 'Terrorists Acts by Latitude/Longitude',
                 showlegend = True, hovermode = 'closest', font = dict(color='white'),
                 height = 1000, width = 990, paper_bgcolor = 'black',
                 margin=go.Margin(l=50,t=75),
                 legend = dict(
                     x = 0.15, y = 1,
                     orientation = 'h',
                     bgcolor = 'grey', bordercolor = 'white', borderwidth=2, font = dict(color='white')),
                 annotations = [dict(x=0.5, y=1.022, showarrow=False, text = 'Groups by Injured', font = dict(color='black', size = 16),
                                borderwidth = 2, bordercolor= 'white', bgcolor = 'white')],
                 geo = dict(projection = dict(type = 'orthographic'), # mercator
                     #domain = dict(x = [ -0.2, 1], y = [ 0, 1 ]),
                     #height = 1300, width = 990,
                     scope = 'world',
                     showland = True,
                     landcolor = 'rgb(250, 250, 250)',
                     subunitwidth = 1,
                     subunitcolor = 'rgb(217, 217, 217)',

                     showcountries = True,
                     bgcolor = 'grey',

                     countrywidth = 1,
                     countrycolor = 'rgb(217, 217, 217)',
                     showlakes = True,
                     lakecolor = 'rgb(255, 255, 255)')
                 )

        #figure = dict(data = full_trace, layout = layout)
        return full_trace, layout
    map_trace, map_layout = map()


    def bar_plot():
        pivot = df.pivot_table(index = 'city', values = ['Killed','Wounded'], aggfunc=sum).reset_index()
        pivot['sum'] = pivot['Killed']+pivot['Wounded']
        pivot.sort_values('sum', ascending=False, inplace = True)
        pivot.drop(pivot.index[1], inplace = True)
        pivot = pivot.head(10)

        trace1= go.Bar(y=pivot['city'], x = pivot.Killed, name = 'Killed', orientation='h', text = pivot.Killed,
                       textposition = 'outside',
                       hoverinfo = '{}: {}'.format(pivot['city'], pivot['Killed']))
        trace2= go.Bar(y=pivot['city'], x = pivot.Wounded, name = 'Wounded', orientation='h', text = pivot.Wounded,
                       textposition = 'outside',
                       hoverinfo = '{}: {}'.format(pivot['city'], pivot['Wounded']))
        layout=go.Layout(title = 'Top 10 dangerous cities for live', barmode = 'group', hovermode = 'closest',
                         yaxis=dict(autorange='reversed'), paper_bgcolor= 'black', plot_bgcolor = 'grey',
                         xaxis = dict(range = [0, pivot['Wounded'].max()*1.1]),
                         font = dict(color = 'white'), height = 500,
                         margin = go.Margin(l=100),
                         legend = dict(bgcolor = 'black', bordercolor = 'white', borderwidth=2, x= 0.85, y = 0.05))

        return [trace1,trace2], layout
    bar_trace, bar_layout = bar_plot()


    def dynamic():
        year = df['Year'].value_counts().reset_index().sort_values('index')
        year.rename(columns = {'Year':'count','index':'year'}, inplace = True)

        trace = go.Bar(x=year['year'], y= year['count'].values,# mode = 'line',
                           marker = dict(color = year['count']))

        layout = dict(xaxis=dict(tickangle = 270, autotick = False),
                      annotations = [dict(text = 'Year: {}<br>Amount of injured: {}'.format(year.loc[year['count']==year['count'].max(),'year'][0], year['count'].max()),
                                          x= year.loc[year['count']==year['count'].max(),'year'][0],y=year['count'].max(),ax=-120,ay=20,
                                         align = 'left', arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='red', bordercolor='white', borderwidth=2,
                                         bgcolor='black', font = dict(color = 'white'))],
                     title = 'Dynamic of Terrorists act by Year', paper_bgcolor= 'black', plot_bgcolor = 'grey',
                     font = dict(color = 'white'), height = 500)
        return [trace], layout
    dynamic_trace, dynamic_layout = dynamic()


    general_plots = html.Div(style={'width':'1800', 'height':'1000', 'background':'black'}, children = [
        # div for title
        html.H1(children = 'SOME GENERAL INFORMATION', style={'textAlign':'center', 'color':'white', 'padding-top':'50'}),


        # Map Div
        html.Div(style = {'width':'49%', 'height':'100%', 'float':'left'}, children =[
            #html.H2(children = 'Terrorists Acts by Latitude/Longitude', style={'textAlign':'center','border':'1px solid red'}),
            dcc.Graph(id = 'world_map', figure = {'data':map_trace, 'layout':map_layout})
        ]),

        # Bar plot for city
        html.Div(style = {'width':'49%', 'height':'50%',  'float':'right'}, children =
            dcc.Graph(id = 'city_bar', figure = {'data':bar_trace, 'layout':bar_layout})
        ),

        # Dynamic of acts
        html.Div(style = {'width':'49%', 'height':'50%', 'float':'right'}, children =
            dcc.Graph(id = 'dynamic_act', figure = {'data':dynamic_trace, 'layout':dynamic_layout})
        )

    ])

    return general_plots
general = General_info()

app = dash.Dash()
app.layout = general

if __name__=='__main__':
    app.run_server(debug = True)
