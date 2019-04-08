# coding:utf-8
import os
import re
from distutils import util

from flask import Markup
from slugify import slugify


dict_status = {"ok": "success"}
label_status_translation = {
    "ok": "success",
    "error": "important",
    "in-progress": "info",
}


def asbool(s):
    """ Return the boolean value ``True`` if the case-lowered value of string
    input ``s`` is any of ``t``, ``true``, ``y``, ``on``, or ``1``, otherwise
    return the boolean value ``False``. If ``s`` is the value ``None``,
    return ``False``. If ``s`` is already one of the boolean values ``True``
    or ``False``, return it."""
    return bool(util.strtobool(s))


def clean_uri(text):
    if text.startswith("http"):
        return Markup(text)
    else:
        return Markup(os.path.basename(text))


def utility_processor():
    def default(value, default):
        return value or default

    def trans_status(status, to_label=False):
        status = slugify(status.lower())
        if asbool(to_label):
            return label_status_translation.get(status, status)
        return dict_status.get(status, status)

    return dict(trans_status=trans_status, default=default)
