import json
import warnings

import dash
# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output, State, ALL

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
                                                                          n_clicks = 0), html.Br (),
                                                             html.Button (id = 'policy-analysis-button',
                                                                          children = 'Go to Policy Analyzer',
                                                                          n_clicks = 0)])
home_screen = html.Div (className = "two columns", children = [html.Div ("Home Screen"),
                                                               html.Button (id = 'home-screen-button',
                                                                            children = 'Go to Home Screen',
                                                                            n_clicks = 0)])
log_out = html.Div (className = "two columns",
                    children = [html.Div ("Log Out"), html.Button (id = 'back-button', children = 'Click '
                                                                                                  'to Log '
                                                                                                  'Out', n_clicks = 0)])
policy_parameter_elems = list ()

POLICY_ID_NAME = html.Form ([html.H6 ("Policy ID", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                        dcc.Input (id = "policy-id", type = "number", min = 1, step = 1,
                                   style = { 'display' : 'inline-block', 'margin-right' : 20 }),html.H6 ("Policy Name", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                          dcc.Input (id = "policy-name", type = "text")])
policy_parameter_elems.append (POLICY_ID_NAME)
POLICY_TYPE = html.Form ([html.H6 ("Policy Type", style = {
    'display' : 'inline-grid', 'height' : '50%', 'width' : '15%', 'font-size' : "75%"
}), dcc.Dropdown (id = "policy-type", options = ["Earthquake Multi Layer - Multi Location"], style = {'margin-right' : 20,
    'display' : 'inline-grid', 'height' : '50%', 'width' : '80%', 'font-size' : "80%"
})])
policy_parameter_elems.append (POLICY_TYPE)
POLICY_LIMIT = html.Form ([html.H6 ("Limit", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                           dcc.Input (id = "policy-limit", type = "number", min = 0,
                                      style = { 'display' : 'inline-block', 'margin-right' : 20 }),
                           html.H6 ("Currency", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                           dcc.Dropdown (id = "policy-type", options = ["EUR", "USD", "GBP", "CHF", "CNY"], style = {
                               'display' : 'inline-grid', 'height' : '50%', 'width' : '50%', 'font-size' : "80%"
                           })])
policy_parameter_elems.append (POLICY_LIMIT)
POLICY_INCEPTION_EXPIRY = html.Form ([html.H6 ("Inception", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                                      dcc.DatePickerSingle (id = "policy-inception",
                                                            style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                                      html.H6 ("Expiry", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                                      dcc.DatePickerSingle (id = "policy-expiry", style = {
                                          'display' : 'inline-grid', 'margin-right' : 20
                                      })])
policy_parameter_elems.append (POLICY_INCEPTION_EXPIRY)

PROTECTION_LAYERS = html.Div (
    [html.H6 ("Protection Layers", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
     html.Button ("Add Layer", id = "add-protection-layer-button", n_clicks = 0),
     html.Div (id = 'protection-layer-container', children = []), ])

policy_parameter_elems.append (PROTECTION_LAYERS)

ASSET_LOCATIONS = html.Div ([html.H6 ("Asset Locations", style = { 'display' : 'inline-grid', 'margin-right' : 20 }),
                             html.Button ("Add Location", id = "add-asset-location-button", n_clicks = 0),
                             html.Div (id = 'asset-location-container', children = []), ])

policy_parameter_elems.append (ASSET_LOCATIONS)


### ADD LAYERS

@app.callback (Output ('protection-layer-container', 'children'),
               [Input ('add-protection-layer-button', 'n_clicks'), Input ({
                                                                              "type" : "remove-protection-layer",
                                                                              "index" : ALL
                                                                          }, 'n_clicks')],
               State ('protection-layer-container', 'children'))
def add_protection_layer (n_clicks, n_clicks_2, children) :
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split ('.')[0]
    print (triggered_id, n_clicks, n_clicks_2)
    if n_clicks > 0 :
        if triggered_id == 'add-protection-layer-button' :
            new_layer = html.Div ([html.I ("Max Radius (km)", style = {
                'display' : 'inline-block', 'margin-right' : 20, 'margin-left' : 20, 'font-size' : "50%"
            }), dcc.Input (id = f"layer-{n_clicks}-max-radius", type = "number", min = 0, style = { 'width' : "10%" }),
                                   html.I ("Min Magnitude (Richter)", style = {
                                       'display' : 'inline-block', 'margin-right' : 20, 'margin-left' : 20,
                                       'font-size' : "50%"
                                   }), dcc.Input (id = f"layer-{n_clicks}-min-magnitude", type = "number", min = 0,
                                                  style = { 'width' : "10%" }), html.I ("Payout Ratio (%)", style = {
                    'display' : 'inline-block', 'margin-right' : 20, 'margin-left' : 20, 'font-size' : "50%"
                }), dcc.Input (id = f"layer-{n_clicks}-payout-ratio", type = "number", min = 0, max = 100.0,
                               style = { 'width' : "10%" }),
                                   html.Button ("X", id = { 'type' : 'remove-protection-layer', 'index' : n_clicks })],
                                  id = {
                                      'type' : 'layer-dynamic-deletable', 'index' : n_clicks
                                  })
            children.append (new_layer)
            return children
    print (len (n_clicks_2))
    if len (n_clicks_2) > 0 :
        delete_chart = json.loads (triggered_id)["index"]
        children = [chart for chart in children if "'index': " + str (delete_chart) not in str (chart)]
        return children
    return children


### ADD LOCATIONS
@app.callback (Output ('asset-location-container', 'children'),
               [Input ('add-asset-location-button', 'n_clicks'), Input ({
                   "type" : "remove-asset-location", "index" : ALL
               }, 'n_clicks')], State ('asset-location-container', 'children'))
def add_asset_location (n_clicks, n_clicks_2, children) :
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split ('.')[0]
    print (triggered_id, n_clicks, n_clicks_2)
    if n_clicks > 0 :
        if triggered_id == 'add-asset-location-button' :
            new_layer = html.Div ([html.I ("Latitude (-90,90)", style = {
                'display' : 'inline-block', 'margin-right' : 20, 'margin-left' : 20, 'font-size' : "50%"
            }), dcc.Input (id = f"asset-location-{n_clicks}-latitude", type = "number", min = -90, max = 90,
                           style = { 'width' : "10%" }), html.I ("Longitude (-180,180)", style = {
                'display' : 'inline-block', 'margin-right' : 20, 'margin-left' : 20, 'font-size' : "50%"
            }), dcc.Input (id = f"asset-location-{n_clicks}-longitude", type = "number", min = -180, max = 180,
                           style = { 'width' : "10%" }),
                                   html.Button ("X", id = { 'type' : 'remove-asset-location', 'index' : n_clicks })],
                                  id = {
                                      'type' : 'location-dynamic-deletable', 'index' : n_clicks
                                  })
            children.append (new_layer)
            return children
    if len (n_clicks_2) > 0 :
        delete_chart = json.loads (triggered_id)["index"]
        children = [chart for chart in children if "'index': " + str (delete_chart) not in str (chart)]
        return children
    return children


page_content_header = html.Div ("Enter Policy Terms And Conditions")

page_content = html.Div (className = "row", children = [page_content_header, html.Div (className = "row",
                                                                                       children =
                                                                                       policy_parameter_elems)])

layout = html.Div (
    children = [pb_log_out, pb_home_screen, pb_policy_monitoring, pb_policy_building, pb_policy_analysis, header,
                page_content, html.Br (), go_to_other_pages, home_screen, log_out])


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
        print ("Resu")
        return '/policy-monitoring'


# Create callbacks
@app.callback (Output ('pb_policy_building', 'pathname'), [Input ('policy-building-button', 'n_clicks')])
def go_to_policy_building (n_clicks) :
    print ("policy-building-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-building'


# Create callbacks
@app.callback (Output ('pb_policy_analysis', 'pathname'), [Input ('policy-analysis-button', 'n_clicks')])
def go_to_policy_analysis (n_clicks) :
    print ("policy-analysis-button", n_clicks)
    if n_clicks > 0 :
        return '/policy-analysis'


# Create callbacks
@app.callback (Output ('pb_home_screen', 'pathname'), [Input ('home-screen-button', 'n_clicks')])
def go_to_policy_analysis (n_clicks) :
    print ("policy-analysis-button", n_clicks)
    if n_clicks > 0 :
        return '/success'
