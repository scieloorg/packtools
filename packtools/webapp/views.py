# coding: utf-8
from flask import g, Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.before_app_request
def add_context_settings():
    setattr(g, 'SETTINGS_MAX_UPLOAD_SIZE', current_app.config.get('SETTINGS_MAX_UPLOAD_SIZE'))
    setattr(g, 'PACKTOOLS_VERSION', current_app.config.get('PACKTOOLS_VERSION'))


@main.route('/')
def root():
    context = {}

    return render_template("validator/stylechecker.html", **context)