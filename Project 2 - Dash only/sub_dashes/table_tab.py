import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

import plotly.offline as py
import plotly.graph_objs as go
import pandas as pd


def Table_dash():
    df = pd.read_csv('for_dash.csv')
    #df = df[df['Year']==1971]



    table = html.Div([dt.DataTable(
        rows = df.to_dict('records'),
        columns = df.columns,
        row_selectable = True,
        filterable = True,
        sortable = True,
        selected_row_indices = [],
        id = 'data_table'
    )])

    return table

app = dash.Dash()
app.layout = Table_dash()

if __name__ == '__main__':
    app.run_server(debug=True)
