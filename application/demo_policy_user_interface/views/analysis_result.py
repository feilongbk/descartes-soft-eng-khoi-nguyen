import warnings

import dash_table
import pandas
import plotly.io as pio

from application.demo_policy_user_interface import utils

pio.renderers.default = 'browser'
# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output, State

from application.demo_policy_user_interface.server import app

warnings.filterwarnings("ignore")
from nano_data_platform import data_platform_helper

from application.demo_policy_user_interface import app_database_driver
POLICY_PAYOUT_SIMULATION_DB = app_database_driver.POLICY_PAYOUT_SIMULATION_DB
POLICY_DB = app_database_driver.POLICY_DB
SIMULATION_RESULT_DATASTORE = app_database_driver.SIMULATION_RESULT_DATASTORE
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
    html.Div(id="display-message", style={'display': 'inline-grid', 'margin-right': 20}))

POLICY_ID_NAME = html.Form(
    [html.H6("Policy ID", style={'display': 'inline-grid', 'margin-right': 20}), POLICY_ID_INPUT])

policy_parameter_elems.append(POLICY_ID_NAME)


def format_dataframe(df):
    new_df = df.copy()
    new_df.columns = [str(x).upper() for x in new_df.columns]
    for col in new_df.columns:
        if new_df[col].dtype == "object":
            new_df[col] = new_df[col].apply(str)
    columns = [{'name': col, 'id': col} for col in new_df.columns]
    data = new_df.to_dict(orient='records')
    return dash_table.DataTable(columns=columns, data=data)


from plotly import express as px


#### VISULAIZATION / STATS
def display_yearly_payout(payout_object):
    if len(payout_object) == 0:
        return html.Div("No relevant historical events for this policy. All simulated payout is zero")
    return dcc.Graph(figure=px.bar(x=payout_object.index, y=payout_object.values))


def display_payout_histogram(payout_object):
    if len(payout_object) == 0:
        return html.Div("No relevant historical events for this policy. All simulated payout is zero")
    return dcc.Graph(figure=px.histogram(x=payout_object.values, nbins=101, histnorm='probability density'))


def display_burning_cost(payout_object):
    if len(payout_object) == 0:
        burning_cost_series = {start_year: 0.0 for
                               start_year
                               in range(1911, 2022)}
    else:
        burning_cost_series = {start_year: utils.tools.compute_burning_cost(payout_object, start_year, 2021) for start_year
                           in range(1911, 2022)}
    burning_cost_series = pandas.Series(burning_cost_series)
    return dcc.Graph(figure=(px.line(x=burning_cost_series.index, y=burning_cost_series.values)))


## LOAD SIMULATION RESULT
@app.callback(Output('display-message', 'children'),
              [Input('display-policy-button', 'n_clicks'), State("policy-id", "value")])
def run_simulation(n_clicks, policy_id):
    if n_clicks > 0:
        children = list()
        if policy_id is None:
            children.append(html.Div("Please specify Policy ID"))
            return children
        policy_parameters = POLICY_DB.get(str(policy_id))
        if not policy_parameters:
            children.append(html.Div(
                f"There is no metadata found for Policy ID {policy_id}. Please go to Policy Builder to create."))
            return children

        cloned_policy_parameters = dict(policy_parameters)
        locations = cloned_policy_parameters.pop("asset_locations")
        layers = cloned_policy_parameters.pop("protection_layers")
        layers.sort(key=lambda x: x["payout_ratio"])
        locations.sort(key=lambda x: x["longitude"])

        children.append(format_dataframe(pandas.DataFrame([cloned_policy_parameters])))
        children.append(format_dataframe(pandas.DataFrame(layers)))
        children.append(format_dataframe(pandas.DataFrame(locations)))

        policy_simulation_metadata = POLICY_PAYOUT_SIMULATION_DB.get(str(policy_id))
        if not policy_simulation_metadata:
            children.append(
                html.Div(
                    f"There is no simulation data found for Policy ID {policy_id}. Please go to Policy Builder to simulate."))
            return children
        payout_data = data_platform_helper.load_object_to_flat_file(str(policy_id), SIMULATION_RESULT_DATASTORE)
        print(payout_data)

        children.append(html.Div("Historical Payout", style={'display': 'inline-grid',"width":"100%"}))
        children.append(display_yearly_payout(payout_data))
        children.append(html.Div("Payout Histogram", style={'display': 'inline-grid',"width":"100%"}))
        children.append(display_payout_histogram(payout_data))
        children.append(html.Div("Burning cost", style={'display': 'inline-grid',"width":"100%"}))
        children.append(display_burning_cost(payout_data))
        return children

    pass


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
