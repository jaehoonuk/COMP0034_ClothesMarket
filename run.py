# Author: Jaehoon Lim

from app import create_app

app = create_app('config.DevConfig')
app.app_context().push()