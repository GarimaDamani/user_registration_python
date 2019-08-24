from .app import app
import os
import logging
from logging.config import fileConfig
# from datetime import timedelta
from .controllers.main_controller import create_db


@app.before_first_request
def setup():
    logging.config.fileConfig('config/logging.cfg')
    create_db()
    app.secret_key = os.urandom(24)
    # app.permanent_session_lifetime = timedelta(minutes=2)


if __name__ == '__main__':
    setup()
    app.run()
