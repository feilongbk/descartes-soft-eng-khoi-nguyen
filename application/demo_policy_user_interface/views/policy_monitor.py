import warnings

# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import current_user

from application.demo_policy_user_interface.server import app

warnings.filterwarnings ("ignore")

ENDPOINT = "/policy-monitoring"

pm_log_out = dcc.Location (id = 'pm_log_out', refresh = True)
pm_policy_monitoring = dcc.Location (id = 'pm_policy_monitoring', refresh = True)
pm_policy_building = dcc.Location (id = 'pm_policy_building', refresh = True)
pm_policy_analysis = dcc.Location (id = 'pm_policy_analysis', refresh = True)
pm_home_screen = dcc.Location (id = 'pm_home_screen', refresh = True)

header = html.Header (children = html.H2 ('Policy Monitor'))

go_to_other_pages = html.Div (className = "row", children = [html.Div ("Other Interfaces"),
                                                             html.Button (id = 'policy-building-button',
                                                                          children = 'Go to Policy Builder',
                                                                          n_clicks = 0),html.Br (),
                                                             html.Button (id = 'policy-analysis-button',
                                                                          children = 'Go to Policy Analyzer',
                                                                          n_clicks = 0), html.Br (),

                                                             ])

page_content = html.Div ("Page Content")

home_screen = html.Div (className = "row", children = [html.Div ("Home Screen"),html.Button (id = 'home-screen-button',
                                                                          children = 'Go to Home Screen',
                                                                          n_clicks = 0)])
log_out = html.Div (className = "row", children = [html.Div ("Log Out"),html.Button (id = 'back-button', children = 'Click '
                                                                                                         'to Log '
                                                                                                         'Out',
                                                                          n_clicks = 0)])

layout = html.Div (
    children = [pm_log_out,pm_home_screen, pm_policy_monitoring,pm_policy_building, pm_policy_analysis, header, page_content, go_to_other_pages, home_screen, log_out])

@app.callback (Output ('pm_log_out', 'pathname'), [Input ('back-button', 'n_clicks')])
def logout_dashboard (n_clicks) :
    print ("back-button", n_clicks)
    if n_clicks > 0 :
        return '/'


# Create callbacks
@app.callback (Output ('pm_policy_monitoring', 'pathname'), [Input ('policy-monitoring-button', 'n_clicks')])
def go_to_policy_monitoring (n_clicks) :
    print ("policy-monitoring-button", n_clicks)
    if n_clicks > 0 :
        print("Resu")
        return '/policy-monitoring'


# Create callbacks
@app.callback (Output ('pm_policy_building', 'pathname'), [Input ('policy-building-button', 'n_clicks')])
def go_to_policy_building (n_clicks) :
    print ("policy-building-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-building'


# Create callbacks
@app.callback (Output ('pm_policy_analysis', 'pathname'), [Input ('policy-analysis-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks) :
    print ("policy-analysis-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-analysis'

# Create callbacks
@app.callback (Output ('pm_home_screen', 'pathname'), [Input ('home-screen-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks) :
    if n_clicks > 0 :
        return '/success'
