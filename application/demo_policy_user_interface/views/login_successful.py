import warnings

# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import current_user

from application.demo_policy_user_interface.server import app

warnings.filterwarnings ("ignore")

hs_log_out = dcc.Location (id = 'hs_log_out', refresh = True)
hs_policy_monitoring = dcc.Location (id = 'hs_policy_monitoring', refresh = True)
hs_policy_building = dcc.Location (id = 'hs_policy_building', refresh = True)
hs_policy_analysis = dcc.Location (id = 'hs_policy_analysis', refresh = True)

header = html.Header ( children = html.H1('Home Screen'))

log_out_element = html.Div (className = "container", children = [html.Div (children = [html.Div (className = "row", children = [
    html.Div (className = "ten columns",
              children = [html.Br (), html.Div ('Log Out'), ]),
    html.Div (className = "two columns", children = [html.Br (), html.Button (id = 'back-button', children = 'Click to Log '
                                                                                                             'Out',
                                                                              n_clicks = 0)])])])])
policy_monitoring_element = html.Div (className = "container", children = [html.Div (children = [
    html.Div (className = "row", children = [
        html.Div (className = "ten columns", children = [html.Br (), html.Div ('Policy Monitor'), ]),
        html.Div (className = "ten columns", children = [html.Br (), html.Button (id = 'policy-monitoring-button',
                                                                                  children = 'Go to Policy Monitor',
                                                                                  n_clicks = 0)])])])])

policy_building_element = html.Div (className = "container", children = [html.Div (children = [
    html.Div (className = "row", children = [
        html.Div (className = "ten columns", children = [html.Br (), html.Div ('Policy Builder'), ]),
        html.Div (className = "ten columns", children = [html.Br (), html.Button (id = 'policy-building-button',
                                                                                  children = 'Go to Policy Builder',
                                                                                  n_clicks = 0)])])])])
policy_analysis_element = html.Div (className = "container", children = [html.Div (children = [
    html.Div (className = "row", children = [
        html.Div (className = "ten columns", children = [html.Br (), html.Div ('Policy Analyzer'), ]),
        html.Div (className = "ten columns", children = [html.Br (), html.Button (id = 'policy-analysis-button',
                                                                                  children = 'Go to Policy Analyzer',
                                                                                  n_clicks = 0)])])])])
layout = html.Div (
    children = [hs_log_out, hs_policy_monitoring,hs_policy_building,hs_policy_analysis, header, policy_monitoring_element, policy_building_element, policy_analysis_element, log_out_element])


# Create callbacks


@app.callback (Output ('hs_log_out', 'pathname'), [Input ('back-button', 'n_clicks')])
def logout_dashboard (n_clicks) :
    print ("back-button", n_clicks)
    if n_clicks > 0 :
        return '/'


# Create callbacks
@app.callback (Output ('hs_policy_monitoring', 'pathname'), [Input ('policy-monitoring-button', 'n_clicks')])
def go_to_policy_monitoring (n_clicks) :
    print ("policy-monitoring-button", n_clicks)
    if n_clicks > 0 :
        print("Resu")
        return '/policy-monitoring'


# Create callbacks
@app.callback (Output ('hs_policy_building', 'pathname'), [Input ('policy-building-button', 'n_clicks')])
def go_to_policy_building (n_clicks) :
    print ("policy-building-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-building'


# Create callbacks
@app.callback (Output ('hs_policy_analysis', 'pathname'), [Input ('policy-analysis-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks) :
    print ("policy-analysis-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-analysis'
