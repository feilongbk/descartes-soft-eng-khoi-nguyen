import warnings

# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output

from application.demo_policy_user_interface.server import app

warnings.filterwarnings("ignore")
from nano_data_platform import data_platform_helper

POLICY_DB = data_platform_helper.get_data_platform_pickle_db_connection(db_name="POLICY_METADATA.db", auto_dump=True)
## WE USE POLICY IT AS METADATA STORE
POLICY_PAYOUT_SIMULATION_DB = data_platform_helper.get_data_platform_pickle_db_connection(
    db_name="POLICY_PAYOUT_SIMULATION.db", auto_dump=True)
SIMULATION_RESULT_DATASTORE = "SIMULATION_RESULT"
##
ENDPOINT = "/analysis-result"
ar_log_out = dcc.Location(id='ar_log_out', refresh=True)

ar_policy_analysis = dcc.Location(id='ar_policy_analysis', refresh=True)

ar_home_screen = dcc.Location(id='ar_home_screen', refresh=True)
ar_policy_builder_screen = dcc.Location(id='ar_policy_builder_screen', refresh=True)

header = html.Header(children=html.H2('Analysis Result'))

home_screen = html.Div(className="two columns", children=[html.Div("Home Screen"),
                                                          html.Button(id='home-screen-button',
                                                                      children='Go to Home Screen',
                                                                      n_clicks=0)])

analysis_screen = html.Div(className="two columns", children=[html.Div("Policy Builder"),
                                                              html.Button(id='policy-screen-button',
                                                                          children='Go to Policy Builder',
                                                                          n_clicks=0)])

log_out = html.Div(className="two columns",
                   children=[html.Div("Log Out"), html.Button(id='back-button', children='Click '
                                                                                         'to Log '
                                                                                         'Out', n_clicks=0)])
policy_parameter_elems = list()
POLICY_ID_INPUT = dcc.Input(id="policy-id", type="number", min=1, step=1,
                            style={'display': 'inline-block', 'margin-right': 20})

display_elements = list()
DISPLAY = html.Div(className="two columns", children=[
    html.H5("DISPLAY ANALYSIS RESULT", style={'display': 'inline-grid', 'margin-right': 20, 'font-size': "100%"}),
    html.Button(id="display-policy-button", children="Click to Display", n_clicks=0,
                style={'display': 'inline-grid', 'margin-right': 20, 'height': '100%', 'width': '50%',
                       'font-size': "100%"})
])
display_elements.append(DISPLAY)
display_elements.append(
    html.Div(id="simulation-message", style={'display': 'inline-grid', 'margin-right': 20}))

POLICY_ID_NAME = html.Form(
    [html.H6("Policy ID", style={'display': 'inline-grid', 'margin-right': 20}), POLICY_ID_INPUT])

policy_parameter_elems.append(POLICY_ID_NAME)


def parse_layers(elem_layers):
    result = list()
    for elem_layer in elem_layers:
        layer_data = dict()
        for child in elem_layer:
            if "max-radius" in str(child):
                layer_data["max_radius"] = child['props']["value"]
            if "payout-ratio" in str(child):
                layer_data["payout_ratio"] = child['props']["value"]
            if "min-magnitude" in str(child):
                layer_data["min_magnitude"] = child['props']["value"]
        result.append(layer_data)
    return result


def parse_locations(elem_locations):
    result = list()
    for elem_location in elem_locations:
        location_data = dict()
        for child in elem_location:
            if "latitude" in str(child):
                location_data["latitude"] = child['props']["value"]
            if "longitude" in str(child):
                location_data["longitude"] = child['props']["value"]
        result.append(location_data)
    return result


#### VISULAIZATION / STATS

page_content_header = html.Div("Enter Policy ID to visualize Analysis")

page_content = html.Div(className="row", children=[page_content_header, html.Div(className="row",
                                                                                 children=
                                                                                 policy_parameter_elems + display_elements)])

layout = html.Div(
    children=[ar_log_out, ar_home_screen, ar_policy_builder_screen, header,
              page_content, html.Br(), analysis_screen, home_screen, log_out])


@app.callback(Output('ar_log_out', 'pathname'), [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    print("back-button", n_clicks)
    if n_clicks > 0:
        return '/'


# Create callbacks
@app.callback(Output('ar_home_screen', 'pathname'), [Input('home-screen-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks):
    if n_clicks > 0:
        return '/success'

# Create callbacks
@app.callback(Output('ar_policy_builder_screen', 'pathname'), [Input('policy-screen-button', 'n_clicks')])
def go_to_policy_simulation(n_clicks):
    if n_clicks > 0:
        return "/policy-simulation"
