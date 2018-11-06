import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
import json

# import base64
# def encode_image(image_file):
#     encoded = base64.b64encode(open(image_file, 'rb').read())
#     return 'data:image/png;base64,{}'.format(encoded.decode())

df = pd.read_csv('for_dash.csv')
df_table = df.drop(['text','lat','long'], axis = 1)
df_table.rename(columns = {'price':'Цена', 'bedrooms':'Кол.комнат', 'bathrooms':'Кол.ванных', 'sqft_living':'Общая площадь',
                            'floors':'Кол.этажей', 'waterfront':'Вид на воду', 'view':'Общий вид', 'condition':'Общие условия',
                            'sqft_above':'Жилая площадь', 'sqft_basement':'Подвальная площадь', 'yr_built':'Год постойки', 'yr_renovated':'Год перестойки'},
                        inplace = True)
access_token = 'pk.eyJ1IjoiYW15YXJkIiwiYSI6ImNqbm02dzVtMjA1dDYzdnF4MW81cTR5Y3EifQ.HaYUoMAJtBABe18u0mBn5w'


app = dash.Dash()

app.layout = html.Div([

    # Header
    html.Div([
        html.H1('Choose Years', style={'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black'}),
        html.Div([
            dcc.RangeSlider(id = 'year--slider', min = df['yr_built'].min(), max = df['yr_built'].max(),
                            value = [df['yr_built'].min(), df['yr_built'].max()],
                            marks = {str(year): str(year) for year in df['yr_built'].unique() if year%5==0 }),

        ], style = {'width':'90%', 'margin-left':'5%','padding':'0px 0px 20px 0px'}),

    # Left sidebar
    html.Div([
        # floors radio buttons
        html.H4('Выберите количество этажей:', style =  {'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black'}),
        html.Div([
            dcc.RadioItems(id='floor',
                        options = [{'label': i, 'value':i} for i in df['floors'].unique()],
                        value=1,
                        labelStyle={'display': 'inline-block', 'padding':'0px 2px 3px 2px'})
        ], style = {'margin-left':'25%'}),

        # Count of rooms
        html.H4('Выберите количество комнат:', style =  {'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black', 'borderTop':'1px solid grey'}),
        html.Div([
            dcc.RadioItems(id='rooms',
                        options = [{'label': i, 'value':i} for i in sorted(df['bedrooms'].unique())],
                        value=3,
                        labelStyle={'display': 'inline-block', 'padding':'0px 2px 3px 2px'})
        ]),

        # view of water
        html.H4('Вид на речку:', style =  {'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black', 'borderTop':'1px solid grey'}),
        html.Div([
            dcc.RadioItems(id='waterfronts',
                        options = [{'label': i, 'value':i} for i in df['waterfront'].unique()],
                        value='Нет',
                        labelStyle={'display': 'inline-block', 'padding':'0px 2px 3px 2px'})
        ], style = {'margin-left':'30%'}),

        # price
        html.H4('Цена:', style =  {'textAlign':'center', 'padding':'15px 0px 0px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black', 'borderTop':'1px solid grey'}),
        html.Div([
            dcc.RangeSlider(id = 'price--slider', min = df['price'].min(), max = df['price'].max(),
                            value = [df['price'].min(), df['price'].max()],
                            marks = {str(df['price'].min()): str(df['price'].min()),
                                    str(3000000):str(3000000), str(5500000):str(5500000),
                                    str(df['price'].max()): str(df['price'].max()) })
        ], style = {'width':'80%', 'margin-left':'10%','padding':'0px 0px 20px 0px'})
    ], style = {'width':'20%', 'box-shadow':'2px 2px 4px black', 'float':'left', 'margin':'1% 0% 0% 0%', 'border-radius':'10px', 'backgroundColor':'lightgrey'}),

    # Map
    html.Div([
        dcc.Graph(id = 'map-box')
    ], style = {'width':'60%', 'float':'left', 'border':'1px solid black', 'margin':'1% 0% 0% 1%', 'border-radius':'10px', 'box-shadow':'2px 2px 4px black'}),

    # Hover box
    html.Div([
        html.H3('Общая информация', style={'textAlign':'center', 'padding':'7px 0px 3px 0px', 'color':'white', 'text-shadow':'3px 3px 5px black', 'border-bottom':'1px solid grey'}),
        html.Div([
            html.Pre(id = 'hover-data')
        ], style = {'margin-left':'10px'}),
        # html.Div([
        #     html.Img(id = 'img_hover', src = 'children', height = 100, width = 225)
        # ], style = {'margin-top':'7px','width':'100%'})
    ], style = {'width':'18%', 'height':'400px', 'float':'right', 'border':'1px solid black', 'margin':'1% 0% 0% 0%', 'border-radius':'10px', 'box-shadow':'2px 2px 4px black', 'backgroundColor':'lightgrey'}),

    # Table
    html.Div([dt.DataTable(id = 'table',
                rows = df_table.to_dict('records'),
                columns = df_table.columns,
                row_selectable = True,
                filterable = True,
                sortable = True,
                selected_row_indices = [])
                ], style = {'float':'left', 'width':'100%'})

    ], style = {'backgroundColor':'lightgrey', 'border-radius':'10px', 'box-shadow':'2px 2px 4px black'})
])


# Map block
@app.callback(dash.dependencies.Output('map-box', 'figure'),
            [dash.dependencies.Input('year--slider', 'value'),
            dash.dependencies.Input('floor', 'value'),
            Input('rooms', 'value'),
            Input('waterfronts','value'),
            Input('price--slider', 'value')])

def update_graph(year_value, floor_numb, rooms_numb, water_view, money):
    df2 = df.loc[(df['yr_built']>=year_value[0])&(df['yr_built']<=year_value[1])&(df['floors']==floor_numb)&(df['bedrooms']==rooms_numb)&\
                (df['waterfront'] == water_view)&(df['price']>=money[0])&(df['price']<=money[1])]

    trace = go.Scattermapbox(lat= df2['lat'], lon=df2['long'],
        mode='markers', marker=dict(size=4),
        text=df2['text'], hoverinfo = 'text')

    layout = go.Layout(autosize=True, hovermode='closest',
                    mapbox=dict(accesstoken=access_token, bearing=0,
                            center=dict(lat=47.5112,lon=-122.257),
                            pitch=0, zoom=10))
    return dict(data = [trace], layout = layout)


# TABLE
@app.callback(dash.dependencies.Output('table', 'rows'),
            [dash.dependencies.Input('year--slider', 'value'),
            dash.dependencies.Input('floor', 'value'),
            Input('rooms', 'value'),
            Input('waterfronts','value'),
            Input('price--slider', 'value')])

def update_graph(year_value, floor_numb, rooms_numb, water_view, money):
    dff = df_table.loc[(df_table['Год постойки']>=year_value[0])&(df_table['Год постойки']<=year_value[1])&\
                (df_table['Кол.этажей']==floor_numb)&(df_table['Кол.комнат']==rooms_numb)&\
                (df_table['Вид на воду'] == water_view)&(df_table['Цена']>=money[0])&(df_table['Цена']<=money[1])]
    rows = dff.to_dict('records')
    return rows


# hover info
@app.callback(dash.dependencies.Output('hover-data', 'children'),
            [dash.dependencies.Input('map-box', 'hoverData')])

def display_click_data(hoverData):
    lan = hoverData['points'][0]['lat']
    long = hoverData['points'][0]['lon']
    df3 = df[(df['lat']==lan)&(df['long']==long)]

    return 'Год експлуатации: {} \nЦена: {}\nКоличество этажей: {}\nКоличество комнат: {}\nКоличество ванных комнат: {}\nОбщая площадь: {}\nЖилая площадь: {}\nПодвальная площадь: {}\nВид на реку: {}\nОбщий вид: {} из 4\nОбщая оценка: {} из 5'\
            .format(df3['yr_built'].values[0], df3['price'].values[0], df3['floors'].values[0], df3['bedrooms'].values[0], df3['bathrooms'].values[0],
                    df3['sqft_living'].values[0], df3['sqft_above'].values[0], df3['sqft_basement'].values[0],
                    df3['waterfront'].values[0], df3['view'].values[0], df3['condition'].values[0])
    #return json.dumps(hoverData, indent = 2)


# # image
# @app.callback(dash.dependencies.Output('img_hover', 'src'),
#             [dash.dependencies.Input('map-box', 'hoverData')])
#
# def callback_image(hoverData):
#     return encode_image('loading.png')



if __name__ == '__main__':
    app.run_server(debug = True)
