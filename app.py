# %%
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_daq as daq

# -- APP VERSION --#
app_version ="v1.6.1"

version = html.Div([
    html.Div(f"SLM - Version: {app_version}",
    style={'text-align': 'right', 'font-size': '12px'})
])

#-- APP TITLE --#
#Title of the page
mytitle = dcc.Markdown(children='# The FishID Budget App') #Header or title of the page

#Instructions
instructions = dcc.Markdown('Hi! Welcome to the FishID Budget App. This app will provide a rough estimation of the investment required to develop a FishID model. Please complete the questions and click submit for the app to display the FishID budget. Default values are displayed on the right before user clicks submit')


#-- SET THEME --#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

##-- MAP TO SELECT LOCATION --# #not being displayed in v1.6
# # Create a map figure
data = {"region": ["Pacific Ocean", "Mediterranean Sea", "Caribbean Sea", "Sargasso Sea", 
                    "Atlantic Ocean", "Indian Ocean", "Red Sea"],
        "info": ["Experienced annotators - Yes", "Experienced annotators - Training required", "Experienced annotators - Training required", 
                "Experienced annotators - Training required", "Experienced annotators - Training required", "Experienced annotators - Training required"
                , "Experienced annotators - Training required"]}
df = pd.DataFrame(data)

location_map = px.scatter_mapbox(lat=[-23.256487, 38.535276, 12.881425, 58.367668, 16.540929, -0.843030, 43.022667], lon=[156.497258, 5.010596, -65.007114, -97.144209, -43.749826, 80.256920, 35.703342],
                    hover_name=["Pacific Ocean", "Mediterranean Sea", "Caribbean Sea", "Sargasso Sea", 
                    "Atlantic Ocean", "Indian Ocean", "Red Sea"],
                    #hover_data={"lat": [-23.256487, 38.535276, 12.881425, 58.367668, 16.540929, -0.843030, 43.022667], 
                                #"lon": [156.497258, 5.010596, -65.007114, -97.144209, -43.749826, 80.256920, 35.703342]},
                    text=df["info"],
                    mapbox_style="carto-positron",
                    zoom=2)

# Set the map layout
location_map.update_layout(mapbox_center={"lat": -23.256487, "lon": 157.940743},
                  mapbox_zoom=2)


#-- COMPONENTS --#
#Column1
column1 = dbc.Col (
    [    #species_location_dropdown
        html.Div(
            [dbc.Label("Location where data will/is collected", html_for="map-dropdown", style= {'font-weight' : 'bold'}),
            dcc.Dropdown(id="map-dropdown", options=[{"label": "Pacific Ocean", "value": 0},
                                            {"label": "Mediterranean Sea", "value": 1},
                                            {"label": "Caribbean Sea", "value": 2},
                                            {"label": "Sargasso Sea", "value": 3},
                                            {"label": "Atlantic Ocean", "value": 4},
                                            {"label": "Indian Ocean", "value": 5},
                                            {"label": "Red Sea", "value": 6},
                                            {"label": "Baltic Sea", "value": 7},],value=0),
            #dcc.Graph(id="map", figure=location_map)
             ],
            className="mb-3"
            ),
        #no_species_slider
        html.Div(
            [dbc.Label("# of species to be detected", html_for="slider", style= {'font-weight' : 'bold'}),
            dcc.Slider(id="species-count", min=5, max=80, step=10, value=5),], className="mb-3"),
        
        #species_type_dropdown
        html.Div(
            [dbc.Label("Select the option that best fit the species type", html_for="dropdown", style= {'font-weight' : 'bold'}),
            dcc.Dropdown(id="species-type", options=[{"label": "Commercial", "value": "commercial"},{"label": "Abundant", "value": "abundant"},
            {"label": "Keystone", "value": "keystone"},{"label": "Rare and Non-Abundant", "value": "rare"}],value='commercial'),], className="mb-3"),
        
        #no_videos_slider
        html.Div(
            [dbc.Label("# of hours FishID will process", html_for="slider", style= {'font-weight' : 'bold'}),
            dcc.Slider(id="video-count", min=100, max=1000, step=250, value=100),], className="mb-3"),
        
        #no_of habitats
        html.Div(
            [dbc.Label("# of distinct habitats where the model will be deployed", html_for="slider", style= {'font-weight' : 'bold'}),
            dcc.Slider(id="no-habitats", min=1, max=5, step=1, value=1),], className="mb-3"),

        #habitat types
        html.Div(
            [dbc.Label ("Select the most common habitat in your dataset", html_for="dropdown", style= {'font-weight' : 'bold'}),
            dcc.Dropdown (id = "habitat-type", options=[{"label": "Seagrass", "value": 0},  {"label": "Coral Reef", "value": 1},
                                                            {"label": "Rocky Reef", "value": 2}, {"label": "Kelp Forest", "value": 3}, {"label": "Estuaries", "value": 4},
                                                            {"label": "Deep Sea", "value": 5}, {"label": "Aerial", "value": 6}, {"label": "Unstructured habitat", "value": 7} ], value = 0),], className = "mb-3"),

        #annotation support
        html.Div(
            [dbc.Label("Do you require FishID's annotation support ?"),
            daq.BooleanSwitch(id="anno-switch", on = True, color="#388697",)]),

        #development timeframe
        html.Div(
            [dbc.Label("Timeframe (months) for model development", html_for="slider", style= {'font-weight' : 'bold'}),
            dcc.Slider(id="dev-time", min=2, max=10, step=1, value=3),], className="mb-3"),

        #submit_button   
        html.Div(
            [dbc.Button("Submit", id="submit-button", color="primary", className ="btn-success"),], className="mt-3"),       
    ],
    md=4,
)
#Column2
column2 = dbc.Col(
    [
        html.H3("Project Investment", className="text-center mt-3"),
        html.H6(id="output1", className="text-center text-success"),
        dcc.Graph(id="output2", figure={})
    ]
    )

#-- APP LAYOUT--#
app.layout = dbc.Container(
    [
        html.Img(src=app.get_asset_url('FishID_Logo_V7_SL.jpg'), width="100px", height="100px"),
        mytitle,
        instructions, 
        dbc.Row([column1, column2]),
        version
    ],
    fluid=True,
    className="dbc",
)

## -- CALLBACK --##
@app.callback(
    [
        dash.dependencies.Output("output1", "children"),
        dash.dependencies.Output("output2", "figure"),
    ],
    [   dash.dependencies.Input("anno-switch", "on"),
        dash.dependencies.Input("submit-button", "n_clicks")],
    [
        dash.dependencies.State("species-count", "value"),
        dash.dependencies.State("map-dropdown", "value"),
        dash.dependencies.State("species-type", "value"),
        dash.dependencies.State("video-count", "value"),
        dash.dependencies.State("no-habitats", "value"),
        dash.dependencies.State("habitat-type", "value"),
        dash.dependencies.State("dev-time", "value"),
    ],
)


def budget_calculation(on, n_clicks, species_count, species_location, species_type, video_count, no_habitats, habitat_type, dev_time):
    
    if on: 
        if species_location == 0 and (species_type == 'commercial' or species_type =='abundant') and habitat_type == 0 and dev_time ==2: #easy-case scenario but with short dev time
            annos = 500 #for each species commercial species where there is a lot of data
            dev_cost = 18000 #lower dev time = higher cost . 2 RA for 2 months

            species_cost = species_count * annos * no_habitats
            video_cost = video_count * 50 #processing cost 
            total_cost = species_cost + video_cost + dev_cost
        else:
            annos = 3000 #for each species for species outside FID region
            habitat = 5000 #challening habitats fee
            dev_cost = 6000 * dev_time #standard fee for each month of development
            
            species_cost = species_count * annos + habitat * no_habitats
            video_cost = video_count * 50 #processing cost 
            total_cost = species_cost + video_cost + dev_cost 
    else:
        #no habitat fee
        #cost of species extremely reduced
        annos = 100
        dev_cost = 4000 * dev_time #standard fee for each month of development - lower support tier

        species_cost = species_count * annos * no_habitats
        video_cost = video_count * 50 #processing cost 
        total_cost = species_cost + video_cost + dev_cost
    return (
    f'The initial cost of the project is AU ${total_cost}',
    generate_linegraph(total_cost),
    )


def generate_linegraph(total_cost):
    sample_period = range(1, 8)
    output_value = [max(total_cost * (1- 0.3 * (i)), 1000) for i in range(7)]
    line_graph = px.line(x=sample_period, y=output_value, labels={'x': 'Sampling Period', 'y': 'Processing and Model Investment in AU$'})
    line_graph.update_layout(
        title={'text': "30 percent cost reduction for each sampling period", 'font': {'size': 14}},
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        font=dict(family='Courier New, monospace', size=12, color='black')
    )
    return (line_graph)



##-- DEPLOY --##
if __name__=='__main__':
    app.run_server(debug=False)
# %%
