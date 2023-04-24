# %%
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_daq as daq



app = dash.Dash(__name__)

column1 = dbc.Col([
    html.Div([
        html.H1('AI Educators'),

        html.Div([
            html.Label('Workshop Format'),
            dcc.RadioItems(
                options=[
                    {'label': 'In-Person', 'value': 'in-person'},
                    {'label': 'Online', 'value': 'online'}
                ],
                value='in-person'
            ),
        ]),

        html.Div([
            html.Label('Workshop Type'),
            dcc.Dropdown(
                options=[
                    {'label': 'Fast Track Workshop (3 days)', 'value': 'fast-track'},
                    {'label': 'Regular Workshop (5 days)', 'value': 'regular'},
                    {'label': 'Extensive Workshop (7 days)', 'value': 'extensive'}
                ],
                value='fast-track'
            ),
        ]),

        html.Div([
            html.Label('Number of Staff/Students'),
            dcc.Input(
                id='num-students',
                type='number',
                value=10
            )
        ]),

        html.Div([
            html.Label('Contact Time After Workshop'),
            dcc.Input(
                id='contact-time',
                type='number',
                value=2
            )
        ])
    ], md=6)
])


column2 = dbc.Col(
    [
        html.H3("Project Investment", className="text-center mt-3"),
        html.H6(id="output", className="text-center text-success")
    ]
    )


#-- APP LAYOUT--#
layout = dbc.Container(
    [
        html.P("This is the page for FishID as AI Providers"), 
        dbc.Row([column1, column2])
    ],
    fluid=True,
    className="dbc",
)


@app.callback(
    Output(component_id='output', component_property='children'),
    [
        State(component_id='num-students', component_property='value'),
        State(component_id='contact-time', component_property='value'),
        State(component_id='workshop-format', component_property='value'),
        State(component_id='workshop-type', component_property='value')
    ]
)
def calculate_cost(num_students, contact_time, workshop_format, workshop_type):
    if workshop_type == 'fast-track':
        cost_per_student = 2500
    elif workshop_type == 'regular':
        cost_per_student = 3500
    else:
        cost_per_student = 4000
    
    if workshop_format == 'online':
        discount = 0.1
    else:
        discount = 0
    
    total_cost = num_students * cost_per_student * (1 - discount)
    
    return f'Total cost: ${total_cost}. Contact time after workshop: {contact_time} weeks.'


if __name__=='__main__':
    app.run_server(debug=False)
# %%