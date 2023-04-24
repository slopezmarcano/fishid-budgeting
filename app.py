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
@app.callback(Output('tab-content', 'children'),
              Input('tabs', 'value'),
              State('species_count', 'value'),
              State('species_location', 'value'),
              State('species_type', 'value'),
              State('video_count', 'value'),
              State('no_habitats', 'value'),
              State('habitat_type', 'value'),
              State('dev_time', 'value'),
              State('eco_metrics', 'value'),
              State('num_students', 'value'),
              State('num_courses', 'value'),
              State('course_type', 'value'),
              State('access_time', 'value'),
              State('num_clients', 'value'),
              State('service_type', 'value'),
              State('service_time', 'value'),
              prevent_initial_call=True)

def render_tab_content(tab, species_count, species_location, species_type, video_count, no_habitats, habitat_type, dev_time, eco_metrics, num_students, num_courses, course_type, access_time, num_clients, service_type, service_time):
    if tab == 'providers':
        return providers_page
    elif tab == 'educators':
        return educators_page
    elif tab == 'consultants':
        return consultants_page

@app.callback(Output('budget-output', 'children'),
              Input('submit-button', 'n_clicks'),
              State('tabs', 'value'),
              State('species_count', 'value'),
              State('species_location', 'value'),
              State('species_type', '


##-- DEPLOY --##
if __name__=='__main__':
    app.run_server(debug=False)
# %%
