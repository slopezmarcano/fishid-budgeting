# %%
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_daq as daq

#-- LAYOUTS FROM OTHER MODULES--#
import providers
import educators
import consultants


app = dash.Dash(__name__)


# -- APP VERSION --#
app_version ="v1.7"

version = html.Div([
    html.Div(f"SLM - Version: {app_version}",
    style={'text-align': 'right', 'font-size': '12px'})
])

#-- SET THEME --#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

# App layout
app.layout = html.Div([
    html.H1('FishID - AI Solutions for Marine Biodiversity Conservation'),
    dcc.Tabs(id='tabs', value='providers', children=[
        dcc.Tab(label='AI Providers', value='providers'),
        dcc.Tab(label='For Educators', value='educators'),
        dcc.Tab(label='For Consultants', value='consultants'),
    ]),
    html.Div(id='page-content')
])


# Callback to display the layout of the selected tab
@app.callback(Output('page-content', 'children'),
              Input('tabs', 'value'))
def display_page(tab):
    if tab == 'providers':
        return providers.layout
    elif tab == 'educators':
        return educators.layout
    elif tab == 'consultants':
        return consultants.layout


# Callback to calculate and display the budget
@app.callback(Output('budget-output', 'children'),
              Input('calculate-budget', 'n_clicks'),
              [Input('tab', 'value')],
              [Input('species-count', 'value'),
               Input('species-location', 'value'),
               Input('species-type', 'value'),
               Input('video-count', 'value'),
               Input('no-habitats', 'value'),
               Input('habitat-type', 'value'),
               Input('dev-time', 'value'),
               Input('eco-metrics', 'value'),
               # Additional inputs for educators.py and consultants.py
               ])

##-- DEPLOY --##
if __name__=='__main__':
    app.run_server(debug=False)
# %%
