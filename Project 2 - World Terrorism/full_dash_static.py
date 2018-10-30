import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from sub_dashes.statistical_dash import Statictic
from sub_dashes.general_dash import General_info
from sub_dashes.table_tab import Table_dash

app = dash.Dash()

tabs_styles = {
    'height': '30px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '5px 0px 5px 0px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '5px 0px 5px 0px'
}


app.layout = html.Div([
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-2',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='General Info (Static)',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style, selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Statistical Info (Static)',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style, selected_style=tab_selected_style
            ),
            dcc.Tab(
                label='Dash Table',
                value='tab-3', className='custom-tab',
                selected_className='custom-tab--selected',
                style=tab_style, selected_style=tab_selected_style
            ),
        ]),
    html.Div(id='tabs-content-classes')
])


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return General_info()
    elif tab == 'tab-2':
        return Statictic()
    elif tab == 'tab-3':
        return Table_dash()

if __name__ == '__main__':
    app.run_server(debug=True)
