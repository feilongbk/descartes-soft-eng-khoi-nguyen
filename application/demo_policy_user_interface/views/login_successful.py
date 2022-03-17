import warnings
from flask_login import logout_user, current_user
# Dash configuration
from dash import html, dcc
from dash.dependencies import Input, Output

from application.demo_policy_user_interface.server import app

warnings.filterwarnings ("ignore")

# Create success layout
STATE_VARIABLES = dict()

url_login_success = dcc.Location (id = 'url_login_success', refresh = True)
header = html.Div (className = "container", children = [html.Div (children = [html.Div (className = "row", children = [
    html.Div (className = "ten columns", children = [html.Br (), html.Div ('Login successfull' +str(current_user)), ]),

    html.Div (className = "two columns",
              children = [html.Br (), html.Button (id = 'back-button', children = 'Log '
                                                                                  'Out', n_clicks = 0)]

              )])]

                                                                  )

                                                        ])

layout = html.Div (children = [url_login_success, header,
                               html.Div (className = "container", children = [html.Div (children = [
                                   html.Div (className = "row", children = [html.Div (className = "ten columns",
                                                                                      children = [html.Br (), html.Div (
                                                                                          'Policy Monitor'), ]),

                                                                            html.Div (className = "ten columns",
                                                                                      children = [html.Br (),
                                                                                                  html.Button (
                                                                                                      id =
                                                                                                      'policy-monitor-button',
                                                                                                      children =
                                                                                                      'Policy Monitor',
                                                                                                      n_clicks = 0)]

                                                                                      )])]

                               )

                               ])

                               ])

# Create callbacks


@app.callback (Output ('url_login_success', 'pathname'), [Input ('back-button', 'n_clicks')])
def logout_dashboard (n_clicks) :
    print ("A", n_clicks)
    if n_clicks > 0 :
        return '/'


# Create callbacks
@app.callback (Output ('url_policy_monitor', 'pathname'), [Input ('policy-monitor-button', 'n_clicks')])
def go_to_policy_monitor (n_clicks) :
    print ("B")
    print (n_clicks)
    if n_clicks > 0 :
        print ("BB")
        return '/analyze-single-text'
