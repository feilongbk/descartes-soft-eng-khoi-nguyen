import warnings

# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import current_user

from application.demo_policy_user_interface.server import app

warnings.filterwarnings ("ignore")

ENDPOINT = "/policy-building"
pb_log_out = dcc.Location (id = 'pb_log_out', refresh = True)
pb_policy_monitoring = dcc.Location (id = 'pb_policy_monitoring', refresh = True)
pb_policy_building = dcc.Location (id = 'pb_policy_building', refresh = True)
pb_policy_analysis = dcc.Location (id = 'pb_policy_analysis', refresh = True)
pb_home_screen = dcc.Location (id = 'pb_home_screen', refresh = True)

header = html.Header (children = html.H2 ('Policy Builder'))

go_to_other_pages = html.Div (className = "row", children = [html.Div ("Other Interfaces"),
                                                             html.Button (id = 'policy-monitoring-button',
                                                                          children = 'Go to Policy Monitoring',
                                                                          n_clicks = 0),html.Br (),
                                                             html.Button (id = 'policy-analysis-button',
                                                                          children = 'Go to Policy Analyzer',
                                                                          n_clicks = 0)])
home_screen = html.Div (className = "two columns", children = [html.Div ("Home Screen"),html.Button (id = 'home-screen-button',
                                                                          children = 'Go to Home Screen',
                                                                          n_clicks = 0)])
log_out = html.Div (className = "two columns", children = [html.Div ("Log Out"),html.Button (id = 'back-button', children = 'Click '
                                                                                                         'to Log '
                                                                                                         'Out',
                                                                          n_clicks = 0)])
policy_parameter_elems = list()

POLICY_ID = html.Div (className = "row", children = [html.H6 ("Policy ID",style={'display':'inline-block','margin-right':20}),dcc.Input(id="policy-id",type = "number",min =1,step = 1,style={'display':'inline-block','margin-right':20})])
policy_parameter_elems.append(POLICY_ID)
POLICY_NAME = html.Div (className = "row", children = [html.H6 ("Policy Name",style={'display':'inline-block','margin-right':20}),dcc.Input(id="policy-name",type = "text")])
policy_parameter_elems.append(POLICY_NAME)
POLICY_TYPE= html.Div (className = "row", children = [html.H6 ("Policy Type",style={'display':'inline-block','margin-right':20}),dcc.Dropdown(id="policy-type",options = ["Earthquake Multi Layer - Multi Location"])])
policy_parameter_elems.append(POLICY_TYPE)
POLICY_LIMIT = html.Div (className = "row", children = [html.H6 ("Limit",style={'display':'inline-block','margin-right':20}),dcc.Input(id="policy-limit",type = "number",min =0,style={'display':'inline-block','margin-right':20})])
policy_parameter_elems.append(POLICY_LIMIT)
POLICY_INCEPTION = html.Div (className = "row", children = [html.H6 ("Inception",style={'display':'inline-block','margin-right':20}),dcc.DatePickerSingle(id="policy-inception",style={'display':'inline-block','margin-right':20})])
policy_parameter_elems.append(POLICY_INCEPTION)
POLICY_EXPIRY = html.Div (className = "row", children = [html.H6 ("Expiry",style={'display':'inline-block','margin-right':20}),dcc.DatePickerSingle(id="policy-expiry",style={'display':'inline-block','margin-right':20})])
policy_parameter_elems.append(POLICY_EXPIRY)


page_content_header =  html.Div ("Enter Policy Terms And Conditions")

page_content = html.Div (className = "row", children = [page_content_header,html.Div (className = "row",children =  policy_parameter_elems)])





layout = html.Div (
    children = [pb_log_out,pb_home_screen, pb_policy_monitoring,pb_policy_building, pb_policy_analysis, header, page_content, go_to_other_pages,home_screen, log_out])










@app.callback (Output ('pb_log_out', 'pathname'), [Input ('back-button', 'n_clicks')])
def logout_dashboard (n_clicks) :
    print ("back-button", n_clicks)
    if n_clicks > 0 :
        return '/'


# Create callbacks
@app.callback (Output ('pb_policy_monitoring', 'pathname'), [Input ('policy-monitoring-button', 'n_clicks')])
def go_to_policy_monitoring (n_clicks) :
    print ("policy-monitoring-button", n_clicks)
    if n_clicks > 0 :
        print("Resu")
        return '/policy-monitoring'


# Create callbacks
@app.callback (Output ('pb_policy_building', 'pathname'), [Input ('policy-building-button', 'n_clicks')])
def go_to_policy_building (n_clicks) :
    print ("policy-building-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-building'


# Create callbacks
@app.callback (Output ('pb_policy_analysis', 'pathname'), [Input ('policy-analysis-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks) :
    print ("policy-analysis-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-analysis'

# Create callbacks
@app.callback (Output ('pb_home_screen', 'pathname'), [Input ('home-screen-button', 'n_clicks')])
def go_to_policy_analysis(n_clicks) :
    print ("policy-analysis-button", n_clicks)
    if n_clicks > 0 :
        return '/success'



