import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()

df= pd.read_csv('for_dash.csv')
df.rename(columns = {'inj':'Injured'}, inplace = True)
df['New_region'] = df['Region'].replace({'Western Europe':'europe', 'Southeast Asia':'asia', 'South Asia':'asia', 'South America':'south america',
                                    'Sub-Saharan Africa':'africa','Eastern Europe':'europe', 'Middle East & North Africa':'asia',
                                    'Central Asia':'asia', 'East Asia':'asia','North America':'north america', 'Australasia & Oceania':'asia',
                                    'Central America & Caribbean':'north america'})
regions = df['New_region'].unique()

app.layout = html.Div([
    # Header
    html.Div([
        html.H1(children = 'Choose the Region and the Years', style={'textAlign':'center', 'padding-top':'10px'}),
        html.Div([dcc.Dropdown(id = 'region_dropdown',
                options=[{'label': i, 'value': i} for i in regions],
                value='europe'),

                dcc.RadioItems(id = 'radio-buttons',
                options=[{'label': i, 'value': i} for i in ['Injured', 'Killed', 'Wounded']],
                value='Injured',
                labelStyle={'display': 'inline-block', 'padding':'10px 0px 10px 10px'})
                ], style = {'float':'left', 'width':'20%', 'display':'inline-block'}),
        html.Div([dcc.RangeSlider(id = 'year--slider', min = df['Year'].min()-1, max = df['Year'].max()+1,
                          value = [df['Year'].min(), df['Year'].max()],
                          #value = 1984,
                          marks = {str(year): str(year) for year in df['Year'].unique() if year%2==0 })
                ], style = {'float':'right', 'width':'75%', 'margin-top':'15px'})
        ], style={'borderBottom': 'thin lightgrey solid', 'backgroundColor': 'rgb(250, 250, 250)','padding': '10px 5px 70px 5px'}),

    #Here will be my plots
    html.Div([
        dcc.Graph(id='maps')
    ], style = {'border':'1px solid black'})
])


# Main Plots
@app.callback(dash.dependencies.Output('maps','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('radio-buttons','value'),
             dash.dependencies.Input('year--slider', 'value')])

def update_graph(region, variable, year_value):
    dff = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    dff = dff[dff['New_region']==region]

    we = dff.pivot_table(index = ['city', 'latitude','longitude'], values =[variable], aggfunc=sum).reset_index()

    ##### Prepare data
    def map_data(map, variable):
        text_full=[]
        for i in range(len(map)):
            text = '{}<br>{}: {}'.format(map.loc[i,'city'], variable, map.loc[i,variable].astype(int).round())
            text_full.append(text)
        map['text'] = text_full

        map = map[map[variable].notna()]

        def get_size(x):
            if x <=10: return 2*1.5
            elif (x >11) & (x <=25): return 3*1.5
            elif (x >26) & (x<=50): return 4*1.5
            elif (x >51) & (x<=100): return 8
            elif (x >101) & (x<=250): return 10
            elif (x >251) & (x<=500): return 12
            else: return 14

        map['size'] = map[variable].apply(lambda x: get_size(x))
        return map

    # def for margin
    # def get_margin(variable):
    #     if variable =='europe': return go.Margin(l=50,t=75)
    #     else: continue

    we = map_data(we, variable)

    trace = dict(
           type = 'scattergeo',
           showlegend = False,
           name = variable,
           lon = we['longitude'],
           lat = we['latitude'],
           text = we['text'],
           mode = 'markers',
           hoverinfo = 'text+name',
           marker = dict(
               size = we['size'],
               opacity = 0.95,
               color = 'rgb(240, 140, 45)',
               line = dict(width = 0.5, color = 'black'))
           )

    layout = dict(
         title = 'Terrorist Attacks by Latitude/Longitude {}'.format(variable),
         width = 800, height = 1000, hovermode = 'closest',
         paper_bgcolor='black', font=dict(color = 'white'),
         margin=go.Margin(l=50,t=75),
         geo = dict(
             projection = dict(type = 'mercator'),
             scope = region,
             showland = True,
             landcolor = 'lightgrey',
             subunitwidth = 1,
             subunitcolor = 'black',
             countrywidth = 1,
             countrycolor = 'black',
             showlakes = True,
             lakecolor = 'lightblue',
             bgcolor = 'grey',
         ))

    return dict(data = [trace], layout = layout)



if __name__ == '__main__':
    app.run_server(debug = True)
