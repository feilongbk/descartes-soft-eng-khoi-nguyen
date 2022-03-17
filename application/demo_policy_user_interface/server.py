# Dash app initialization
import dash
# DEMO_APP_USER management initialization
import os
from flask_login import LoginManager, UserMixin
from application.demo_policy_user_interface.app_user_dao import DB, DEMO_APP_USER as base
from application.demo_policy_user_interface.app_database_driver import get_db_url


app = dash.Dash(
    __name__,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ]
)
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=get_db_url(),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

DB.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create DEMO_APP_USER class with UserMixin
class Demo_001_User(UserMixin, base):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return Demo_001_User.query.get(int(user_id))