import warnings

# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import current_user

from application.demo_policy_user_interface.server import app

warnings.filterwarnings ("ignore")

hs_log_out = dcc.Location (id = 'hs_log_out', refresh = True)
hs_policy_monitoring = dcc.Location (id = 'hs_policy_monitoring', refresh = True)
hs_policy_simulation = dcc.Location (id = 'hs_policy_simulation', refresh = True)
hs_policy_analysis = dcc.Location (id = 'hs_policy_analysis', refresh = True)

header = html.Header ( children = html.H1('Home Screen'))

log_out_element = html.Div (className = "container", children = [html.Div (children = [html.Div (className = "row", children = [
    html.Div (className = "ten columns",
              children = [html.Br (), html.Div ('Log Out'), ]),
    html.Div (className = "two columns", children = [html.Br (), html.Button (id = 'back-button', children = 'Click to Log '
                                                                                                             'Out',
                                                                              n_clicks = 0)])])])])

policy_simulation_element = html.Div (className = "container", children = [html.Div (children = [
    html.Div (className = "row", children = [
        html.Div (className = "ten columns", children = [html.Br (), html.Div ('Policy Simulator'), ]),
        html.Div (className = "ten columns", children = [html.Br (), html.Button (id = 'policy-simulation-button',
                                                                                  children = 'Go to Policy Simulator',
                                                                                  n_clicks = 0)])])])])

layout = html.Div (
    children = [hs_log_out, hs_policy_monitoring,hs_policy_simulation,hs_policy_analysis, header,
                policy_simulation_element,
                log_out_element])


# Create callbacks


@app.callback (Output ('hs_log_out', 'pathname'), [Input ('back-button', 'n_clicks')])
def logout_dashboard (n_clicks) :
    print ("back-button", n_clicks)
    if n_clicks > 0 :
        return '/'

# Create callbacks
@app.callback (Output ('hs_policy_simulation', 'pathname'), [Input ('policy-simulation-button', 'n_clicks')])
def go_to_policy_simulation (n_clicks) :
    print ("policy-simulation-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-simulation'

