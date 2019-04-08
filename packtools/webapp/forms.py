# coding: utf-8
from flask import current_app
from flask_wtf import FlaskForm
from flask_babelex import gettext as _
from wtforms import BooleanField, FileField, StringField, validators


class XMLUploadForm(FlaskForm):
    add_scielo_br_rules = BooleanField(default=True)
    url_static_file = StringField(label=_("URL to statics files"))
    file = FileField(label=_("File"), validators=[validators.input_required()])

    def validate_file(form, field):
        _file = field.data
        if _file:
            if _file.content_type not in ["text/xml", "application/xml"]:
                raise validators.ValidationError(
                    _(u"This type of file is not allowed! Please select another file.")
                )

            # _data = _file.read()
            # if len(_data) > current_app.config.get('SETTINGS_MAX_UPLOAD_SIZE', 0):
            #     raise validators.ValidationError(_(u"The file's size is too large! Please select a smaller file."))
