# index page
from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import logout_user, current_user

from application.demo_policy_user_interface.server import app
from views import login_successful, login, login_failed, logout, policy_simulation,analysis_result

header = html.Div (className = 'header',
    children = html.Div (className = 'container-width', style = { 'height' : '100%' },
        children = [html.Img (src = 'assets/dash-logo-stripe.svg', className = 'logo'), html.Div (className = 'links', children = [
            html.Div (id = 'user-name', className = 'link'), html.Div (id = 'logout', className = 'link'),

        ])]))

app.layout = html.Div ([header,
    html.Div ([html.Div (html.Div (id = 'page-content', className = 'content'), className = 'content-container'), ],
        className = 'container-width'), dcc.Location (id = 'url', refresh = False), ])


@app.callback (Output ('page-content', 'children'), [Input ('url', 'pathname')])
def display_page (pathname) :
    print(pathname)
    if pathname == '/' :
        return login.layout
    elif pathname == '/login' :
        return login.layout
    elif pathname == '/success' :
        if current_user.is_authenticated :
            return login_successful.layout
        else :
            return login_failed.layout
    elif pathname == '/logout' :
        if current_user.is_authenticated :
            logout_user ()
            return logout.layout
        else :
            return logout.layout
    elif pathname == policy_simulation.ENDPOINT :
        if current_user.is_authenticated :
            return policy_simulation.layout
        else :
            return login_failed.layout
    elif pathname == analysis_result.ENDPOINT :
        if current_user.is_authenticated :
            return analysis_result.layout
        else :
            return login_failed.layout

    else :
        return '404'


@app.callback (Output ('user-name', 'children'), [Input ('page-content', 'children')])
def cur_user (input1) :
    if current_user.is_authenticated :
        return html.Div (
            'Current user: ' + current_user.username)  # 'DEMO_APP_USER authenticated' return username in get_id()
    else :
        return ''


@app.callback (Output ('logout', 'children'), [Input ('page-content', 'children')])
def user_logout (input1) :
    if current_user.is_authenticated :
        return html.A ('Logout', href = '/logout')
    else :
        return ''


if __name__ == '__main__' :
    app.run_server (debug = True, port = 2022)
