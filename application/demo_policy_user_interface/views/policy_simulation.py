import json
import warnings
from datetime import datetime

import dash
import dash_table
import pandas
# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output, State, ALL

from application.demo_policy_user_interface.server import app

warnings.filterwarnings("ignore")
from nano_data_platform import data_platform_helper

from application.demo_policy_user_interface import app_database_driver
POLICY_PAYOUT_SIMULATION_DB = app_database_driver.POLICY_PAYOUT_SIMULATION_DB
POLICY_DB = app_database_driver.POLICY_DB
SIMULATION_RESULT_DATASTORE = app_database_driver.SIMULATION_RESULT_DATASTORE

##
ENDPOINT = "/policy-simulation"
pb_log_out = dcc.Location(id='pb_log_out', refresh=True)
pb_policy_monitoring = dcc.Location(id='pb_policy_monitoring', refresh=True)
pb_policy_building = dcc.Location(id='pb_policy_building', refresh=True)
pb_policy_analysis = dcc.Location(id='pb_policy_analysis', refresh=True)

pb_home_screen = dcc.Location(id='pb_home_screen', refresh=True)
pb_analysis_result_screen = dcc.Location(id='pb_analysis_result_screen', refresh=True)

header = html.Header(children=html.H2('Policy Builder'))

home_screen = html.Div(className="two columns", children=[html.Div("Home Screen"),
                                                          html.Button(id='home-screen-button',
                                                                      children='Go to Home Screen',
                                                                      n_clicks=0)])

analysis_screen = html.Div(className="two columns", children=[html.Div("Go to Analysis Result"),
                                                              html.Button(id='analysis-screen-button',
                                                                          children='Go to Analysis Result',
                                                                          n_clicks=0)])

log_out = html.Div(className="two columns",
                   children=[html.Div("Log Out"), html.Button(id='back-button', children='Click '
                                                                                         'to Log '
                                                                                         'Out', n_clicks=0)])
policy_parameter_elems = list()
POLICY_ID_INPUT = dcc.Input(id="policy-id", type="number", min=1, step=1,
                            style={'display': 'inline-block', 'margin-right': 20})
POLICY_ID_NAME = html.Form([html.H6("Policy ID", style={'display': 'inline-grid', 'margin-right': 20}), POLICY_ID_INPUT
                               ,
                            html.H6("Policy Name", style={'display': 'inline-grid', 'margin-right': 20}),
                            dcc.Input(id="policy-name", type="text")])
policy_parameter_elems.append(POLICY_ID_NAME)
POLICY_TYPE = html.Form([html.H6("Policy Type", style={
    'display': 'inline-grid', 'height': '50%', 'width': '15%', 'font-size': "75%"
}), dcc.Dropdown(id="policy-type", options=["Earthquake Multi Layer - Multi Location"], style={
    'margin-right': 20, 'display': 'inline-grid', 'height': '50%', 'width': '80%', 'font-size': "80%"
})])
policy_parameter_elems.append(POLICY_TYPE)
POLICY_LIMIT = html.Form([html.H6("Limit", style={'display': 'inline-grid', 'margin-right': 20}),
                          dcc.Input(id="policy-limit", type="number", min=0,
                                    style={'display': 'inline-block', 'margin-right': 20}),
                          html.H6("Currency", style={'display': 'inline-grid', 'margin-right': 20}),
                          dcc.Dropdown(id="policy-currency", options=["EUR", "USD", "GBP", "CHF", "CNY"], style={
                              'display': 'inline-grid', 'height': '50%', 'width': '50%', 'font-size': "80%"
                          })])
policy_parameter_elems.append(POLICY_LIMIT)
POLICY_INCEPTION_EXPIRY = html.Form([html.H6("Inception", style={'display': 'inline-grid', 'margin-right': 20}),
                                     dcc.DatePickerSingle(id="policy-inception",
                                                          style={'display': 'inline-grid', 'margin-right': 20}),
                                     html.H6("Expiry", style={'display': 'inline-grid', 'margin-right': 20}),
                                     dcc.DatePickerSingle(id="policy-expiry", style={
                                         'display': 'inline-grid', 'margin-right': 20
                                     })])
policy_parameter_elems.append(POLICY_INCEPTION_EXPIRY)

PROTECTION_LAYERS = html.Div(
    [html.H6("Protection Layers", style={'display': 'inline-grid', 'margin-right': 20}),
     html.Button("Add Layer", id="add-protection-layer-button", n_clicks=0),
     html.Div(id='protection-layer-container', children=[]), ])

policy_parameter_elems.append(PROTECTION_LAYERS)

ASSET_LOCATIONS = html.Div([html.H6("Asset Locations", style={'display': 'inline-grid', 'margin-right': 20}),
                            html.Button("Add Location", id="add-asset-location-button", n_clicks=0),
                            html.Div(id='asset-location-container', children=[]), ])

policy_parameter_elems.append(ASSET_LOCATIONS)
OVERWRITE = html.Form([html.H6("OVERWRITE POLICY", style={
    'display': 'inline-grid', 'height': '50%', 'width': '40%', 'font-size': "60%"
}), dcc.Dropdown(id="overwrite-metadata", options=["NO", "YES"], style={
    'margin-right': 20, 'display': 'inline-grid', 'height': '50%', 'width': '50%', 'font-size': "80%"
})])
policy_parameter_elems.append(OVERWRITE)

VALIDATE = html.Div(className="two columns", children=[
    html.H5("VALIDATE POLICY", style={'display': 'inline-grid', 'margin-right': 20, 'font-size': "100%"}),
    html.Button(id="validate-policy-button", children="Click to Validate", n_clicks=0,
                style={'display': 'inline-grid', 'margin-right': 20, 'height': '100%', 'width': '50%',
                       'font-size': "100%"}),
    html.Div(id="validation-message", style={'display': 'inline-grid', 'margin-right': 20})])

policy_parameter_elems.append(VALIDATE)


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


# Create callbacks
@app.callback(Output('validation-message', 'children'),
              [Input('validate-policy-button', 'n_clicks'),
               State("policy-id", "value"), State("policy-name", "value"),
               State("policy-type", "value"), State("policy-limit", "value"), State("policy-currency", "value"),
               State("policy-inception", "date"), State("policy-expiry", "date"),
               State({
                   "type": "layer-parameters", "index": ALL
               }, "children"), State({
                  "type": "location-parameters", "index": ALL
              }, "children"), State("overwrite-metadata", "value")

               ])
def validate_policy(n_clicks, policy_id, policy_name, policy_type, policy_limit, currency, inception, expiry,
                    elem_layers, elem_locations, overwrite_metadata):
    print("policy-analysis-button", policy_id, policy_name, policy_type, policy_limit, inception, expiry, elem_layers,
          elem_locations)

    layers = parse_layers(elem_layers)
    locations = parse_locations(elem_locations)
    overwrite = overwrite_metadata == "YES"

    if n_clicks > 0:
        param_to_check = [policy_id, policy_name, policy_type, policy_limit, inception, expiry]
        if None in param_to_check:
            return f'''Enter missing parameters'''
        if len(layers) == 0:
            return f'''Enter at least 1 layer'''
        if len(locations) == 0:
            return f'''Enter at least 1 location'''

        policy_parameters = dict()
        policy_parameters["policy_id"] = policy_id
        policy_parameters["name"] = policy_name
        policy_parameters["type"] = policy_type
        policy_parameters["limit"] = policy_limit
        policy_parameters["currency"] = currency
        policy_parameters["inception"] = inception
        policy_parameters["expiry"] = expiry
        policy_parameters["protection_layers"] = layers
        policy_parameters["asset_locations"] = locations
        print(policy_parameters)
        if POLICY_DB.get(str(policy_id)) and not overwrite:
            print(POLICY_DB.get(str(policy_id)))
            return f'''The policy ID {policy_id} already saved. Please change the policy ID to ensure the uniqueness.'''
        POLICY_DB.set(str(policy_id), policy_parameters)
        POLICY_DB.dump()
        return "Validated"


### ADD LAYERS

@app.callback(Output('protection-layer-container', 'children'),
              [Input('add-protection-layer-button', 'n_clicks'), Input({
                  "type": "remove-protection-layer", "index": ALL
              }, 'n_clicks')], State('protection-layer-container', 'children'))
def add_protection_layer(n_clicks, n_clicks_2, children):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_id, n_clicks, n_clicks_2)

    if n_clicks > 0:
        if triggered_id == 'add-protection-layer-button':
            new_layer = html.Div([html.I("Max Radius (km)", style={
                'display': 'inline-block', 'margin-right': 20, 'margin-left': 20, 'font-size': "50%"
            }), dcc.Input(id=f"layer-{n_clicks}-max-radius", type="number", min=0, style={'width': "10%"}),
                                  html.I("Min Magnitude (Richter)", style={
                                      'display': 'inline-block', 'margin-right': 20, 'margin-left': 20,
                                      'font-size': "50%"
                                  }), dcc.Input(id=f"layer-{n_clicks}-min-magnitude", type="number", min=0,
                                                style={'width': "10%"}), html.I("Payout Ratio (%)", style={
                    'display': 'inline-block', 'margin-right': 20, 'margin-left': 20, 'font-size': "50%"
                }), dcc.Input(id=f"layer-{n_clicks}-payout-ratio", type="number", min=0, max=100.0,
                              style={'width': "10%"}),
                                  html.Button("X", id={'type': 'remove-protection-layer', 'index': n_clicks})],
                                 id={
                                     'type': 'layer-parameters', 'index': n_clicks
                                 })
            children.append(new_layer)
            return children
    print(len(n_clicks_2))
    if len(n_clicks_2) > 0:
        delete_chart = json.loads(triggered_id)["index"]
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]
        return children
    return children


### ADD LOCATIONS
@app.callback(Output('asset-location-container', 'children'),
              [Input('add-asset-location-button', 'n_clicks'), Input({
                  "type": "remove-asset-location", "index": ALL
              }, 'n_clicks')], State('asset-location-container', 'children'))
def add_asset_location(n_clicks, n_clicks_2, children):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    print(triggered_id, n_clicks, n_clicks_2)
    if n_clicks > 0:
        if triggered_id == 'add-asset-location-button':
            new_layer = html.Div([html.I("Latitude (-90,90)", style={
                'display': 'inline-block', 'margin-right': 20, 'margin-left': 20, 'font-size': "50%"
            }), dcc.Input(id=f"asset-location-{n_clicks}-latitude", type="number", min=-90, max=90,
                          style={'width': "10%"}), html.I("Longitude (-180,180)", style={
                'display': 'inline-block', 'margin-right': 20, 'margin-left': 20, 'font-size': "50%"
            }), dcc.Input(id=f"asset-location-{n_clicks}-longitude", type="number", min=-180, max=180,
                          style={'width': "10%"}),
                                  html.Button("X", id={'type': 'remove-asset-location', 'index': n_clicks})],
                                 id={
                                     'type': 'location-parameters', 'index': n_clicks
                                 })
            children.append(new_layer)
            return children
    if len(n_clicks_2) > 0:
        delete_chart = json.loads(triggered_id)["index"]
        children = [chart for chart in children if "'index': " + str(delete_chart) not in str(chart)]
        return children
    return children


#### SIMULATION PARAMETERS

def format_dataframe(df):
    new_df = df.copy()
    new_df.columns = [str(x).upper() for x in new_df.columns]
    for col in new_df.columns:
        if new_df[col].dtype == "object":
            new_df[col] = new_df[col].apply(str)
    columns = [{'name': col, 'id': col} for col in new_df.columns]
    data = new_df.to_dict(orient='records')
    return dash_table.DataTable(columns=columns, data=data)


simulation_parameter_elems = list()

SIMULATE = html.Div(className="two columns", children=[
    html.H5("RUN SIMULATION", style={'display': 'inline-grid', 'margin-right': 20, 'font-size': "100%"}),
    html.Button(id="simulate-policy-button", children="Click to Simulate", n_clicks=0,
                style={'display': 'inline-grid', 'margin-right': 20, 'height': '100%', 'width': '50%',
                       'font-size': "100%"}), html.Div([html.H6("OVERWRITE SIMULATION", style={
        'display': 'inline-grid', 'height': '50%', 'width': '40%', 'font-size': "60%"
    }), dcc.Dropdown(id="overwrite-simulation", options=["NO", "YES"], style={
        'margin-right': 20, 'display': 'inline-grid', 'height': '50%', 'width': '50%', 'font-size': "80%"
    })])
])
simulation_parameter_elems.append(SIMULATE)
simulation_parameter_elems.append(
    html.Div(id="simulation-message", style={'display': 'inline-grid', 'margin-right': 20}))


@app.callback(Output('simulation-message', 'children'),
              [Input('simulate-policy-button', 'n_clicks'), State("policy-id", "value"),
               State("overwrite-simulation", "value")])
def run_simulation(n_clicks, policy_id, overwrite_simulation):
    print("SIMULATE", n_clicks)
    overwrite_simulation = overwrite_simulation=="YES"
    if n_clicks > 0:
        policy_parameters = POLICY_DB.get(str(policy_id))

        simulation_metadata = dict()
        simulation_metadata["policy_id"] = policy_id
        simulation_metadata["start_time"] = datetime.utcnow().isoformat()
        simulation_metadata["policy_parameters"] = policy_parameters
        simulation_metadata["end_time"] = None
        simulation_metadata["status"] = "PENDING"
        # POLICY_PAYOUT_SIMULATION_DB.set(str(policy_id),simulation_metadata)

        if not policy_parameters:
            return "Create the policy first"
        cloned_policy_parameters = dict(policy_parameters)
        locations = cloned_policy_parameters.pop("asset_locations")
        layers = cloned_policy_parameters.pop("protection_layers")
        layers.sort(key=lambda x: x["payout_ratio"])
        locations.sort(key=lambda x: x["longitude"])
        print(policy_parameters)
        print(layers)
        print(locations)
        children = []
        children.append(format_dataframe(pandas.DataFrame([cloned_policy_parameters])))
        children.append(format_dataframe(pandas.DataFrame(layers)))
        children.append(format_dataframe(pandas.DataFrame(locations)))

        if POLICY_PAYOUT_SIMULATION_DB.get(str(policy_id)) and not overwrite_simulation:
            print("Already exists")
            children.append(html.Br())
            children.append(html.Div(
                f"A simulation result for policy ID {policy_id} already exists. If you want to overwrite it, please specify in OVERWRITE SIMULATION options "
                ))
            return children

        ## SIMULATION ##
        from application.demo_policy_user_interface import utils
        result = utils.simulate_earthquake(policy_parameters, layers, locations)

        POLICY_PAYOUT_SIMULATION_DB.set(str(policy_id), simulation_metadata)

        simulation_metadata["end_time"] = datetime.utcnow().isoformat()
        simulation_metadata["status"] = "SUCCEEDED"

        data_platform_helper.dump_object_to_flat_file(result, str(policy_id), SIMULATION_RESULT_DATASTORE)
        children.append(html.Br())
        children.append(html.Div("Done Simulation. Go to Analysis Result Screen to visualize the details"))
        return children


#### VISULAIZATION / STATS

import plotly.express as px

page_content_header = html.Div("Enter Policy Terms And Conditions")

page_content = html.Div(className="row", children=[page_content_header, html.Div(className="row",
                                                                                 children=
                                                                                 policy_parameter_elems + simulation_parameter_elems)])

layout = html.Div(
    children=[pb_log_out, pb_home_screen, pb_analysis_result_screen, header,
              page_content, html.Br(),analysis_screen, home_screen,  log_out])


@app.callback(Output('pb_log_out', 'pathname'), [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    print("back-button", n_clicks)
    if n_clicks > 0:
        return '/'


# Create callbacks
@app.callback(Output('pb_home_screen', 'pathname'), [Input('home-screen-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks):
    if n_clicks > 0:
        return '/success'


# Create callbacks
@app.callback(Output('pb_analysis_result_screen', 'pathname'), [Input('analysis-screen-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks):
    if n_clicks > 0:
        return '/analysis-result'
