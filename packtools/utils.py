#coding: utf-8
from __future__ import unicode_literals
import logging
import functools
import itertools
import os
import glob
import sys
import json
import unicodedata
import zipfile

from lxml import etree, isoschematron
try:
    import pygments     # NOQA
    from pygments.lexers import get_lexer_for_mimetype
    from pygments.formatters import TerminalFormatter
except ImportError:
    pygments = False    # NOQA

from packtools import catalogs


LOGGER = logging.getLogger(__name__)


PY2 = sys.version_info[0] == 2


try:
    # available on lxml >= 3.4.0
    NOIDS_XMLPARSER = etree.XMLParser(collect_ids=False)
except TypeError:
    LOGGER.info('cannot instantiate an XML parser that avoids the collection '
                'of ids from elements.')
    NOIDS_XMLPARSER = etree.XMLParser()


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


def get_schematron_from_buffer(buff, parser=NOIDS_XMLPARSER):
    """Returns an ``isoschematron.Schematron`` for ``buff``.

    The default parser doesn't collect ids on a hash table, i.e.:
    ``collect_ids=False``.
    """
    xmlschema_doc = etree.parse(buff, parser)
    return isoschematron.Schematron(xmlschema_doc)


def get_schematron_from_filepath(filepath):
    with open(filepath, mode='rb') as buff:
        return get_schematron_from_buffer(buff)


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

    :param paths: Collection of paths. A path can be relative, absolute or a 
                  glob expression.
    """
    def _inner_generator():
        for path in paths:
            ylock = True
            if not path.startswith(('http:', 'https:')):
                # try to expand wildchars and get the absolute path
                for fpath in glob.iglob(path):
                    yield os.path.abspath(fpath).strip()
                    ylock = False

            # args must not be suppressed, even the invalid
            if ylock:
                yield path.strip()

    for path in _inner_generator():
        if PY2:
            yield path.decode(encoding=sys.getfilesystemencoding())
        else:
            yield path


def prettify(jsonobj, colorize=True):
    """ Serialize and prettify a Python object as JSON.

    On windows, bypass pygments colorization.

    Function copied from Circus process manager:
    https://github.com/circus-tent/circus/blob/master/circus/circusctl.py
    """

    json_str = json.dumps(jsonobj, indent=2, sort_keys=True)
    if colorize and pygments and not sys.platform.startswith('win'):
        LOGGER.info('using pygments to highlight the output')
        try:
            lexer = get_lexer_for_mimetype("application/json")
            return pygments.highlight(json_str, lexer, TerminalFormatter())
        except Exception as exc:
            LOGGER.exception(exc)

    return json_str


def normalize_string(unistr):
    """Return the NFKC form for the unicode string ``unistr``.

    The normal form KD (NFKD) will apply the compatibility decomposition, i.e.
    replace all compatibility characters with their equivalents, followed by
    the canonical composition.
    """
    return unicodedata.normalize('NFKC', unistr)


class Xray(object):
    """Zip-file introspector.

    :param zip_file: instance of ``zipfile.ZipFile``.
    """
    def __init__(self, zip_file):
        self._zipfile = zip_file

    @classmethod
    def fromfile(cls, filepath):
        if not zipfile.is_zipfile(filepath):
            raise ValueError('cannot read "%s": not a valid zipfile' % filepath)

        zip_file = zipfile.ZipFile(filepath, 'r')
        return cls(zip_file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def show_sorted_members(self):
        """Shows the package members sorted by their file extensions.
        """
        sorted_members = {}
        for member in self.show_members():
            _, ext = member.rsplit('.', 1)
            ext_node = sorted_members.setdefault(ext.lower(), [])
            ext_node.append(member)

        return sorted_members

    def show_members(self):
        """Shows the package members.
        """
        return [filename for fileinfo, filename
                in zip(self._zipfile.infolist(), self._zipfile.namelist())
                if fileinfo.file_size]

    def get_file(self, member, mode='r'):
        """Get file object for member.

        A complete list of members can be checked
        calling :meth:`show_members`.

        :param member: a zip member, e.g. 'foo.xml'
        """
        try:
            return self._zipfile.open(member, mode)

        except KeyError:
            raise ValueError('cannot open file "%s": file doesn\'t exist' % member)

    def close(self):
        """Close the archive file.
        """
        self._zipfile.close()


def resolve_schematron_filepath(value):
    """Determine the filepath for ``value``.

    The lookup is run against all known schemas from
    :data:`packtools.catalogs.SCH_SCHEMAS`. If ``value`` is already a filepath,
    than it is returned as it is.
    """
    try:
        lookup_builtin = value.startswith('@')
    except AttributeError as exc:
        # the `from` clause cannot be used due to compatibility with python 2.
        raise TypeError('invalid input type for text string: "value"')

    if lookup_builtin:
        path = catalogs.SCH_SCHEMAS.get(value[1:])
        if path:
            return path
        else:
            raise ValueError('cannot resolve schematron "%s"' % value)
    elif os.path.lexists(value):
        return value
    else:
        raise ValueError('could not locate file "%s" (I/O failure)' % value)
         
