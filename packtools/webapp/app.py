# coding:utf-8
import os
import logging

from flask import Flask, render_template
from flask_babelex import Babel

from .custom_filters import clean_uri, utility_processor
from .views import main as main_bp


LOGGER = logging.getLogger(__name__)


def create_app(settings_ns):

    babel = Babel()
    app = Flask(
        __name__,
        static_url_path="/static",
        static_folder="static",
        instance_relative_config=False,
    )

    app.config.from_object(settings_ns)

    app.register_blueprint(main_bp)
    app.jinja_env.filters["clean_uri"] = clean_uri
    app.context_processor(utility_processor)
    babel.init_app(app)

    if app.config["DEBUG"]:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
        except ImportError:
            LOGGER.info('cannot import lib "flask_debugtoolbar". '
                        'Make sure it is installed and available in the '
                        'import path.')
        else:
            toolbar = DebugToolbarExtension()
            toolbar.init_app(app)

    return app


app = create_app(os.environ.get(
    "APP_SETTINGS", "packtools.webapp.config.default.ProductionConfig"))
