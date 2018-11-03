import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import base64
import os

image_filename = os.getcwd()+'/test.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


app = dash.Dash()

tabs_styles = {
    'height': '30px',
    'margin': '5px 0px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'lightgrey',
    'padding': '6px',
    'fontWeight': 'bold',
    'color':'white',
    'text-shadow':'2px 2px 3px black',
    'border-radius':'10px',
    'margin':'0px 10px 0px 10px',
    'box-shadow':'2px 2px 4px black'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color':'black',
    'text-shadow':'2px 2px 3px white',
    'padding': '6px',
    'border-radius':'10px',
    'margin':'0px 10px 0px 10px',
    'box-shadow':'2px 2px 4px grey'
}


df= pd.read_csv('for_dash.csv')
var_type ={'Тип атаки':'AttackType', 'Группировка':'Group', 'Цель атаки':'Target_type', 'Вид оружия ':'Weapon_type'}
# main TABLE for tab1
df_table = df.drop(['latitude', 'inj','longitude','inj-group','text','New_region'], axis = 1)

# table for Terrorist groups Tab2
terr_grouped = df.pivot_table(index = ['Group'], values=['Killed','Wounded','inj'], aggfunc=sum).sort_values('inj', ascending = False).reset_index()
terr_grouped = terr_grouped[terr_grouped['Group'] != 'Unknown']
terr_grouped.drop(columns = 'inj', inplace = True)


app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Choose the Region and Years', style={'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black'}),

        html.Div([
            dcc.Dropdown(id = 'region_dropdown',
            options=[{'label': i, 'value': i} for i in df['Region'].unique()],
            value=df['Region'].unique(),
            multi = True)], style = {'width':'80%','margin-left':'10%'}),

        html.Div([
            dcc.RangeSlider(id = 'year--slider', min = df['Year'].min()-1, max = df['Year'].max()+1,
                          #value = [df['Year'].min(), df['Year'].max()],
                          value = [1970, 1978],
                          marks = {str(year): str(year) for year in df['Year'].unique() if year%2==0 })],
            style = {'width':'90%', "margin-left":'5%', 'margin-top':'10px'}),
    ], style = {'margin':'0px 0px 5px 0px', 'box-shadow':'3px 3px 3px grey', 'border-radius':'25px', 'backgroundColor':'lightgrey', 'padding':'0px 0px 45px 0px'}),


    # Tabs with Graphs
    dcc.Tabs(id='tabs', children = [

        # TAB 1
        dcc.Tab(label = 'World Info', style = tab_style, selected_style=tab_selected_style, children = [
            html.Div([

                # Header
                html.Div([
                    html.H3('Choose the variable', style={'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black'}),
                    html.Div([
                        dcc.RadioItems(id='choose_variable',
                                    options = [{'label': keys, 'value':val} for keys, val in var_type.items()],
                                    value='AttackType',
                                    labelStyle={'display': 'inline-block', 'padding':'10px 0px 10px 10px'}),
                    ], style = {'margin-left':'33%', 'color':'red'})
                ],style = {'margin':'0px 0px 5px 0px', 'box-shadow':'3px 3px 3px grey', 'border-radius':'25px', 'backgroundColor':'lightgrey'}),

                # World maps
                dcc.Graph(id='world_map'),

                # TABLE
                dt.DataTable(id = 'world_table',
                            rows = df_table.to_dict('records'),
                            columns = df_table.columns,
                            row_selectable = True,
                            filterable = True,
                            sortable = True,
                            selected_row_indices = [])
            ])
        ]),

        # TAB 2
        dcc.Tab(label = 'Terrorists Groups', style = tab_style, selected_style=tab_selected_style, children = [
            html.Div([
                    html.Div([dt.DataTable(id = 'terr_table',
                                        rows = terr_grouped.to_dict('records'),
                                        columns = terr_grouped.columns,
                                        row_selectable = True,
                                        filterable = True,
                                        sortable = True,
                                        selected_row_indices = []
                                        )], style = {'border':'1px solid lightgrey', 'box-shadow':'2px 2px 4px black', 'width':'35%', 'float':'left'}),
                    html.Div([dcc.Graph(id = 'top-10')
                ], style = {'border':'1px solid lightgrey', 'box-shadow':'2px 2px 4px black', 'width':'63%', 'height':'480px', 'float':'right'}),
            ]),

            # Dymanic of terror activity
            html.Div([
                html.H3('Dynamic of most 10 Terrorist Groups Activities', style={'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black'}),
                html.Div([
                    dcc.RadioItems(id='killed/wounded',
                                options = [{'label': keys, 'value':val} for keys, val in {'Убитые':'Killed', 'Травмированные':'Wounded'}.items()],
                                value='Killed',
                                labelStyle={'display': 'inline-block', 'padding':'10px 0px 10px 10px'}),
                ], style = {'margin-left':'40%', 'color':'red'}),
                dcc.Graph(id = 'terr_dynamic'),

                # Countries
                html.Div([
                    dcc.Graph(id='countries_terr')
                ], style = {'overflowY': 'scroll', 'height': '350', 'border':'1px solid grey', 'box-shadow':'2px 2px 4px white', 'float':'left', 'width':'47%', 'margin':'1%'}),

                # Countries
                html.Div([
                    dcc.Graph(id='cities_terr')
                ], style = {'overflowY': 'scroll', 'height': '350', 'border':'1px solid grey', 'box-shadow':'2px 2px 4px white', 'float':'left', 'width':'47%', 'margin':'1%'}),
            ], style = {'overflowY': 'scroll', 'border':'1px solid lightgrey', 'margin':'10px 0px 10px 0px', 'box-shadow':'2px 2px 4px black', 'float':'left', 'width':'100%', 'backgroundColor':'lightgrey'}),

            # Bubble chart
            # Bubble right header
            html.Div([
                    html.H2('Choose the variable', style={'textAlign':'center', 'padding':'7px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black'}),
                    dcc.RadioItems(id='bubble-choose',
                                options = [{'label': keys, 'value':val} for keys, val in {'Вид атаки':'AttackType', 'Вид оружия':'Weapon_type', 'Цель нападения':'Target_type'}.items()],
                                value='AttackType',
                                labelStyle={'display': 'inline-block', 'padding':'0px 0px 10px 10px', 'margin-left':'20%'})
                ], style = {'float':'left', 'width':'20%', 'border':'1px solid grey', 'box-shadow':'2px 2px 4px black', 'backgroundColor':'lightgrey'}),

            # Bubble chart
            html.Div([
                dcc.Graph(id = 'bubble-chart')
            ], style = {'border':'1px solid lightgrey', 'box-shadow':'2px 2px 4px black', 'float':'right', 'width':'78%', 'float':'right'}),
        ]),

        # TAB 3
        dcc.Tab(label = 'Some statistic', style = tab_style, selected_style=tab_selected_style, children = [
            html.Div([
                html.H1('It will be soon.')
            ])
        ])
    ], style = tabs_styles)
])




#########################################################################
###  TAB - 1
###  MAP
@app.callback(dash.dependencies.Output('world_map','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value'),
             dash.dependencies.Input('choose_variable', 'value')])


def update_graph(region, year_value, variable):

    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]

    dff = df2[df2['Region'].isin(region)]

    we = dff.pivot_table(index = ['Year', 'Region', 'city', variable,'latitude','longitude'], values =['inj','Killed','Wounded'], aggfunc=sum).reset_index()
    ##### Prepare data
    def map_data(map):
        text_full=[]
        for i in range(len(map)):
            text = '{}<br>Year: {}<br>City: {}<br>Killed: {}<br>Wounded: {}'.format(map.loc[i,variable], map.loc[i,'Year'],
                                                                                   map.loc[i,'city'],
                                                                                   map.loc[i,'Killed'].astype(int).round(),
                                                                                   map.loc[i,'Wounded'].astype(int).round())
            text_full.append(text)
        map['text'] = text_full

        map = map[map['inj'].notna()]

        def get_size(x):
            if x <=10: return 2*1.5
            elif (x >11) & (x <=25): return 3*1.5
            elif (x >26) & (x<=50): return 4*1.5
            elif (x >51) & (x<=100): return 8
            elif (x >101) & (x<=250): return 10
            elif (x >251) & (x<=500): return 12
            else: return 14

        map['size'] = map['inj'].apply(lambda x: get_size(x))
        return map


    we = map_data(we)

    full_trace = []
    for i in we[variable].unique():
        maps=we[we[variable]==i]
        trace = dict(
                   type = 'scattergeo',
                   locationmode = 'world',
                   showlegend = True,
                   #sort = True,
                   name = str(i),
                   lon = maps['longitude'],
                   lat = maps['latitude'],
                   text = maps['text'],
                   mode = 'markers',
                   hoverinfo = 'text',
                   marker = dict(opacity = 0.8, size=maps['size'])
                   )
        full_trace.append(trace)

    layout = dict(
             title = 'Terrorists Acts by Latitude/Longitude',
             showlegend = True, hovermode = 'closest', font = dict(color='white'),
             height = 1250, width = 1280, paper_bgcolor = 'black',
             margin=go.Margin(l=50,t=75),
             legend = dict(
                 x = 0.15, y = 1,
                 orientation = 'h',
                 bgcolor = 'grey', bordercolor = 'white', borderwidth=2, font = dict(color='white')),
             geo = dict(projection = dict(type = 'orthographic'),
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

    return dict(data = full_trace, layout = layout)


#############################################################################
###   TAB 1
###   TABLE
@app.callback(dash.dependencies.Output('world_table','rows'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value')])


def update_graph(region, year_value):

    df2 = df_table.loc[(df_table['Year']>=year_value[0])&(df_table['Year']<=year_value[1])]
    dff = df2[df2['Region'].isin(region)]
    rows = dff.to_dict('records')

    return rows


#############################################################################
###   TAB 2
###   TABLE
@app.callback(dash.dependencies.Output('terr_table','rows'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value')])


def update_graph(region, year_value):
    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    df2 = df2[df2['Region'].isin(region)]

    terr_gr2 = df2.pivot_table(index = ['Group'], values=['Killed','Wounded','inj'], aggfunc=sum).sort_values('inj', ascending = False).reset_index()
    terr_gr2 = terr_gr2[terr_gr2['Group'] != 'Unknown']
    terr_gr2.drop(columns = 'inj', inplace = True)

    rows = terr_gr2.to_dict('records')
    return rows


#######################################################################
### TAB 2
### Top 10 terr groups
@app.callback(dash.dependencies.Output('top-10','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value')])

def update_graph(region, year_value):
    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    df2 = df2[df2['Region'].isin(region)]
    df2 = df2[df2['Group'] != 'Unknown']
    top_terr = df2.pivot_table(index = ['Group'], values=['Killed','Wounded','inj'], aggfunc=sum).sort_values('inj', ascending = False).reset_index().head(10)

    bar1 = go.Bar(y=top_terr['Group'], x=top_terr['Killed'].values, orientation = 'h', name = 'Killed')
    bar2 = go.Bar(y=top_terr['Group'], x=top_terr['Wounded'].values, orientation = 'h', name = 'Wounded')
    layout = go.Layout(barmode = 'stack', title = 'Top 10 Terrorists Groups', yaxis = dict(autorange = 'reversed'),
                        margin = go.Margin(l = 400), paper_bgcolor='lightgrey', height = 480)

    return dict(data = [bar1, bar2], layout = layout)


#######################################################################
### TAB 2
### Terrorist Activity
@app.callback(dash.dependencies.Output('terr_dynamic','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value'),
             dash.dependencies.Input('killed/wounded', 'value')])

def update_graph(region, year_value, action):
    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    df2 = df2[df2['Region'].isin(region)]
    df2 = df2[df2['Group'] != 'Unknown']

    # Find top 10 groups for this years
    ten_gr = df2.pivot_table(index = ['Group'], values=[action], aggfunc=sum).sort_values(action, ascending = False).reset_index().head(10)
    ten_gr = ten_gr.Group.values

    # prepare my DataFrame
    ter_df = df2[df2['Group'].isin(ten_gr)]
    gr2 = ter_df.pivot_table(index = ['Group','Year'], values=[action], aggfunc=sum).reset_index()

    # Plot
    full_trace = []
    for i in gr2['Group'].unique():
        ggg = gr2[gr2['Group']==i]
        trace = go.Scatter(dict(x = ggg['Year'],
                                y= ggg[action].values,
                                name = i,
                                mode = 'lines+markers'))
        full_trace.append(trace)

    layout = go.Layout(legend = dict(x=0.01, y= 0.98, bgcolor = 'lightgrey', bordercolor = 'white', borderwidth=2),
                      plot_bgcolor = 'black', paper_bgcolor = 'lightgrey', font = dict(color = 'black'),
                      xaxis = dict(autotick = False, tickangle = 270, dtick = 2),
                      height = 550)

    return dict(data = full_trace, layout=layout)


#######################################################################
### TAB 2
### Bubble chart

@app.callback(dash.dependencies.Output('bubble-chart','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value'),
             dash.dependencies.Input('bubble-choose', 'value')])

def update_graph(region, year_value, action_bubble):
    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    df2 = df2[df2['Region'].isin(region)]
    df2 = df2[df2['Group'] != 'Unknown']

    # prepare df
    pivot = df2.pivot_table(index = action_bubble, values = ['Killed','Wounded'], aggfunc=sum).reset_index()
    pivot['sum'] = pivot['Killed']+pivot['Wounded']
    pivot['perc'] = pivot['sum'].div(pivot['sum'].sum())
    pivot['perc'] = round((pivot['perc']*100),2)

    # size of markers
    def get_size(x):
        if x <=1: return 2
        elif (x >1) & (x<=2.5): return 4
        elif (x >2.5) & (x <=5): return 6
        elif (x >5) & (x<=10): return 8
        elif (x >10) & (x<=26): return 12
        else: return 16
    pivot['size'] =pivot['perc'].apply(lambda x:  get_size(int(x)))

    full_text = []
    for i in range(len(pivot)):
        pivot.loc[i, 'text'] ='{} ({}%)<br>Убитых: {}<br>Раненных: {}'.format(pivot.loc[i, action_bubble], pivot.loc[i,'perc'].astype(str),
                                                                                 pivot.loc[i,'Killed'].astype(int).round(),
                                                                                 pivot.loc[i,'Wounded'].astype(int).round())

    # get name of variable for title
    def get_name(variable):
        if variable == 'Target_type': return 'Target Type'
        elif variable == 'Weapon_type': return 'Weapon Type'
        else : return 'Attack Type'

    #Chart
    full_bubble = []
    for i in pivot[action_bubble].unique():
        reg = pivot[pivot[action_bubble]==i]
        trace = go.Scatter(x=reg['Wounded'], y= reg['Killed'], mode = 'markers', text = reg['text'], textposition = 'bottom center',
                       name = i, hoverinfo = 'text',
                       marker = dict(size = reg['size']*5, opacity = 0.7))
        full_bubble.append(trace)

    layout = go.Layout(title = 'The ration of Killed to Wounded by {}'.format(get_name(action_bubble)),
                      xaxis = dict( title = 'Wounded', type = 'log'),
                      yaxis = dict(title = 'Killed', type = 'log'), #range = pivot['Killed']
                      hovermode = 'closest',
                      paper_bgcolor = 'lightgrey')

    return dict(data = full_bubble, layout = layout)


#######################################################################
### TAB 2
### Counrties Bar chart
@app.callback(dash.dependencies.Output('countries_terr','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value'),
             dash.dependencies.Input('killed/wounded', 'value')])


def update_graph(region, year_value, variable):
    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    df2 = df2[df2['Region'].isin(region)]
    df2 = df2[df2[variable] !=0]

    gr = df2.pivot_table(index = ['Country'], values=[variable], aggfunc=sum).sort_values(variable, ascending = True).reset_index()
    trace = go.Bar(y=gr['Country'], x=gr[variable].values, orientation = 'h', hoverinfo = 'text',
                    textposition='outside', textfont = dict(size = 10, color = 'black'), text =gr[variable].values) #
    layout = go.Layout(title = 'All Countries by {}'.format(variable),
                      height = gr['Country'].nunique()*22, margin = go.Margin(l=200), #height = 3000
                      font = dict(color = 'white'), paper_bgcolor = 'black', plot_bgcolor = 'lightgrey',
                      xaxis = dict(range = [0, gr[variable].max()*1.15]))

    return dict(data = [trace], layout = layout)

#######################################################################
### TAB 2
### Counrties Bar chart
@app.callback(dash.dependencies.Output('cities_terr','figure'),
             [dash.dependencies.Input('region_dropdown','value'),
             dash.dependencies.Input('year--slider', 'value'),
             dash.dependencies.Input('killed/wounded', 'value')])


def update_graph(region, year_value, variable):
    df2 = df.loc[(df['Year']>=year_value[0])&(df['Year']<=year_value[1])]
    df2 = df2[df2['Region'].isin(region)]
    df2 = df2[df2[variable] !=0]

    gr = df2.pivot_table(index = ['city'], values=[variable], aggfunc=sum).sort_values(variable, ascending = True).reset_index()
    trace = go.Bar(y=gr['city'], x=gr[variable].values, orientation = 'h', hoverinfo = 'text',
                    textposition='outside', textfont = dict(size = 10, color = 'black'), text =gr[variable].values) #
    layout = go.Layout(title = 'All Cities by {}'.format(variable),
                      height = gr['city'].nunique()*18, margin = go.Margin(l=200),
                      font = dict(color = 'white'), paper_bgcolor = 'black', plot_bgcolor = 'lightgrey',
                      xaxis = dict(range = [0, gr[variable].max()*1.15]))

    return dict(data = [trace], layout = layout)


if __name__=='__main__':
    app.run_server(debug = True)
