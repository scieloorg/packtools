#coding: utf-8
from __future__ import unicode_literals
import hmac
import types
import hashlib
import logging
import functools
import itertools
import os
import glob

from lxml import etree

from packtools import catalogs


logger = logging.getLogger(__name__)


def _feed_hash(message, hash):
    """
    Feeds `hash` with `message` in order to
    generate a digest.
    """
    if hasattr(message, 'read'):
        while True:
            chunk = message.read(1024)
            if not chunk:
                break
            hash.update(chunk)

    elif isinstance(message, types.StringType):
        hash.update(message)

    else:
        raise TypeError('Unsupported type %s' % type(message))


def authenticate_message(message, secret='sekretz'):
    """
    Returns a digest for the message based on the given secret

    ``message`` is the file object or byte string to be calculated
    ``secret`` is a shared key used by the hash algorithm
    """
    hash = hmac.new(secret, '', hashlib.sha1)
    _feed_hash(message, hash)

    return hash.hexdigest()


def checksum_file(filepath, callable):
    """
    Returns a digest for the filepath based on the given secret

    ``filepath`` is the file to have its bytes calculated
    ``secret`` is a shared key used by the hash algorithm
    """
    with open(filepath, 'rb') as f:
        hash = callable()
        _feed_hash(f, hash)

    return hash.hexdigest()


def setdefault(object, attribute, producer):
    """
    Like dict().setdefault but for object attributes.
    """
    if not hasattr(object, attribute):
        setattr(object, attribute, producer())

    return getattr(object, attribute)


def cachedmethod(wrappee):
    """Caches method calls within known arguments.
    """
    @functools.wraps(wrappee)
    def wrapper(self, *args, **kwargs):
        key = (args, tuple(kwargs.items()))
        cache_attrname = '__' + wrappee.__name__

        cache = setdefault(self, cache_attrname, lambda: {})
        if key not in cache:
            cache[key] = wrappee(self, *args, **kwargs)

        return cache[key]

    return wrapper


def get_static_assets(xml_et):
    """Returns an iterable with all static assets referenced by xml_et.
    """
    paths = [
        '//graphic[@xlink:href]',
        '//media[@xlink:href]',
        '//inline-graphic[@xlink:href]',
        '//supplementary-material[@xlink:href]',
        '//inline-supplementary-material[@xlink:href]',
    ]

    iterators = [xml_et.iterfind(path, namespaces={'xlink': 'http://www.w3.org/1999/xlink'})
            for path in paths]

    elements = itertools.chain(*iterators)

    return [element.attrib['{http://www.w3.org/1999/xlink}href'] for element in elements]


def make_file_checker(path):
    """Returns a function that looks for a given filename in path.
    """
    dir_contents = set(os.listdir(path))
    def file_checker(filename):
        return filename in dir_contents

    return file_checker


def XML(file, no_network=True, load_dtd=True):
    """Parses `file` to produce an etree instance.

    The XML can be retrieved given its filesystem path,
    an URL or a file-object.

    :param file: Path to the XML file, URL or file-object.
    :param no_network: (optional) prevent network access for external DTD.
    :param load_dtd: (optional) load DTD during parse-time.
    """
    parser = etree.XMLParser(remove_blank_text=True,
                             load_dtd=load_dtd,
                             no_network=no_network)
    xml = etree.parse(file, parser)

    return xml


def config_xml_catalog(wrapped):
    """Decorator that wraps the execution of a function, setting-up and
    tearing-down the ``XML_CATALOG_FILES`` environment variable for the current
    process.

    .. code-block:: python

       @config_xml_catalog
       def main(xml_filepath):
           xml = XMLValidator(xml_filepath)
           # do some work here
    """
    @functools.wraps(wrapped)
    def wrapper(*args, **kwargs):
        try:
            os.environ['XML_CATALOG_FILES'] = catalogs.XML_CATALOG
            _return = wrapped(*args, **kwargs)

        finally:
            del(os.environ['XML_CATALOG_FILES'])

        return _return
    return wrapper


def flatten(paths):
    """ Produces absolute path for each path in paths.

    Glob expansions are allowed.
    :param paths: Collection of paths. A path can be relative, absolute or a glob expression.
    """
    for path in paths:
        ylock = True
        if not path.startswith(('http:', 'https:')):
            # try to expand wildchars and get the absolute path
            for fpath in glob.iglob(path):
                yield os.path.abspath(fpath)
                ylock = False

        # args must not be suppressed, even the invalid
        if ylock == True:
            yield path

