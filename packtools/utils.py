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
import io

from lxml import etree, isoschematron
from PIL import Image
try:
    import pygments     # NOQA
    from pygments.lexers import get_lexer_for_mimetype
    from pygments.formatters import TerminalFormatter
except ImportError:
    pygments = False    # NOQA

from packtools import catalogs, exceptions


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


class WebImageGenerator:
    """Generate WEB Images versions of a given Image.

    Basic usage:

    .. code-block:: python

        image_generator = WebImageGenerator(image_filename, image_file_dir)
        new_filename = image_generator.convert2png()

    :param image_filename: image file name
    :param image_file_dir: directory where ``image_filename`` is and where new versions
        will be saved
    """

    def __init__(self, image_filename, image_file_dir):
        self.image_file_path = os.path.join(image_file_dir, image_filename)

    def convert2png(self):
        """Generate a PNG file from image file in the same directory with the same name,
        changing only the file extension."""
        new_filename = os.path.splitext(self.image_file_path)[0] + ".png"
        with Image.open(self.image_file_path) as tiff_file:
            png_file = tiff_file.copy()
            png_file.save(new_filename, "PNG")
        return new_filename

    def create_thumbnail(self):
        """Generate a thumbnail file from image file in the same directory with the same name,
        changing only the file name to ``*.thumbnail.jpg.``"""
        new_filename = os.path.splitext(self.image_file_path)[0] + ".thumbnail.jpg"
        with Image.open(self.image_file_path) as image_file:
            size = (267, 140)
            thumbnail_file = image_file.copy()
            thumbnail_file.thumbnail(size)
            thumbnail_file.save(new_filename, "JPEG")
        return new_filename


class XMLWebOptimiser(object):
    """Optimise XML document to be properly rendered to HTML, with alternatives to
    images.

    Basic usage:

    .. code-block:: python

        package = XMLWebOptimiser(xml_file, xml_filename)
        xml_etree = package.get_optimised_xml(get_optimised_image, get_image_thumbnail)

    :param xml_file: XML document, instance of ``etree._ElementTree``
    :param xml_filename: XML filename
    """

    def __init__(self, xml_file, xml_filename):
        self.xml_file = xml_file
        self.xml_filename = xml_filename

    def _get_all_images_to_optimise(self):
        paths = [
            './/graphic[@xlink:href and not(@specific-use="scielo-web")]',
            './/inline-graphic[@xlink:href and not(@specific-use="scielo-web")]',
        ]
        namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
        iterators = [self.xml_file.xpath(path, namespaces=namespaces) for path in paths]
        for image in itertools.chain(*iterators):
            image_filename = image.attrib.get("{http://www.w3.org/1999/xlink}href", "")
            if ".tif" in image_filename:
                path = '../{}[@xlink:href and @specific-use="scielo-web"]'.format(
                    image.tag
                )
                if len(image.xpath(path, namespaces=namespaces)) == 0:
                    yield image_filename, image

    def _get_all_images_to_thumbnail(self):
        path = "//graphic[@xlink:href]"
        namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
        images = self.xml_file.xpath(path, namespaces=namespaces)
        images_parents = {image.getparent() for image in images}
        for images_parent in images_parents:
            alternatives = images_parent.xpath(
                "./graphic[@xlink:href]", namespaces=namespaces
            )
            thumbnail = images_parent.xpath(
                './graphic[@xlink:href and starts-with(@content-type, "scielo-")]',
                namespaces=namespaces,
            )
            if len(alternatives) == 1 or len(thumbnail) == 0:
                image_filename = alternatives[0].attrib.get(
                    "{http://www.w3.org/1999/xlink}href", ""
                )
                yield image_filename, alternatives[0]

    def get_optimised_xml(self, get_optimised_image, get_image_thumbnail):
        """Get optimised XML, with WEB alternatives for images.

        :param get_optimised_image: function to get optimised image file from given file
            referenced in XML
        :param get_image_thumbnail: function to get image thumbnail from given file
            referenced in XML
        """
        for image_filename, image_element in self._get_all_images_to_optimise():
            try:
                new_filename = get_optimised_image(image_filename)
            except exceptions.SPPackageError as exc:
                LOGGER.error("Error optimising image: %s", str(exc))
            else:
                new_alternative = etree.Element(image_element.tag)
                new_alternative.set("{http://www.w3.org/1999/xlink}href", new_filename)
                new_alternative.set("specific-use", "scielo-web")

                image_parent = image_element.getparent()
                if image_parent.tag == "alternatives":
                    image_parent.append(new_alternative)
                else:
                    alternative_node = etree.Element("alternatives")
                    alternative_node.tail = image_element.tail
                    image_element.tail = None
                    alternative_node.append(image_element)
                    alternative_node.append(new_alternative)
                    image_parent.append(alternative_node)

        for image_filename, image_element in self._get_all_images_to_thumbnail():
            try:
                new_filename = get_image_thumbnail(image_filename)
            except exceptions.SPPackageError as exc:
                LOGGER.error("Error creating image thumbnail: %s", str(exc))
            else:
                new_alternative = etree.Element(image_element.tag)
                new_alternative.set("{http://www.w3.org/1999/xlink}href", new_filename)
                new_alternative.set("specific-use", "scielo-web")
                new_alternative.set("content-type", "scielo-267x140")

                image_parent = image_element.getparent()
                if image_parent.tag == "alternatives":
                    image_parent.append(new_alternative)
                else:
                    alternative_node = etree.Element("alternatives")
                    alternative_node.tail = image_element.tail
                    image_element.tail = None
                    alternative_node.append(image_element)
                    alternative_node.append(new_alternative)
                    image_parent.append(alternative_node)

        return self.xml_file


class SPPackage(object):
    """Adapter that manipulate SciELO Publishing Packages.

    Basic usage:

    .. code-block:: python

        package = SPPackage(package_file, extracted_package)
        package.optimise()

    :param package_file: SciELO Publishing Package, instance of ``zipfile.ZipFile``
    :param extracted_package: path to extract package files and optimise them
    """

    def __init__(self, package_file, extracted_package):
        self._package_file = package_file
        self._extracted_package = extracted_package

    @classmethod
    def from_file(cls, package_file_path, extracted_package=None):
        """Factory of SPPackage instances.

        :param package_file_path: Path to the SciELO Publishing Package file, instance
               of ``zipfile.ZipFile``
        """

        if not zipfile.is_zipfile(package_file_path):
            raise ValueError("File is not a zip file")

        package2optimise = zipfile.ZipFile(package_file_path)
        if extracted_package is None:
            extracted_package = os.path.splitext(package_file_path)[0]
        return cls(package2optimise, extracted_package)

    def _optimise_xml_to_web(self, parsed_xml, xml_filename):

        xml_web_optimiser = XMLWebOptimiser(parsed_xml, xml_filename)
        optimised_xml = xml_web_optimiser.get_optimised_xml(
            self.create_optimised_image, self.create_image_thumbnail
        )
        with open(
            os.path.join(self._extracted_package, xml_filename), "wb"
        ) as xml_file:
            xml_file.write(etree.tostring(optimised_xml))

    def _optimise_image(self, image_to_optimise, do_optimisation):
        try:
            self._package_file.extract(image_to_optimise, self._extracted_package)
        except KeyError as exc:
            raise exceptions.SPPackageError(
                "No file named {} in package".format(image_to_optimise)
            )
        else:
            optimised_file_path = do_optimisation()
            os.remove(os.path.join(self._extracted_package, image_to_optimise))
            return os.path.split(optimised_file_path)[-1]

    def create_optimised_image(self, image_to_optimise):
        """Create WEB image alternative of an image in SciELO Publishing Package.

        :param image_to_optimise: image file name in SciELO Publishing Package.
        """
        web_image_generator = WebImageGenerator(
            image_to_optimise, self._extracted_package
        )
        return self._optimise_image(image_to_optimise, web_image_generator.convert2png)

    def create_image_thumbnail(self, large_image):
        """Create image thumbnail of an image in SciELO Publishing Package.

        :param large_image: image file name in SciELO Publishing Package.
        """
        web_image_generator = WebImageGenerator(large_image, self._extracted_package)
        return self._optimise_image(large_image, web_image_generator.create_thumbnail)

    def optimise(self, new_package_file_path=None, preserve_files=True):
        """Optimise SciELO Publishing Package to have WEB images alternatives.

        For each XML file in package, optimise XML with WEB images alternatives.
        In the end, creates a new SciELO Publishing Package, compressed in a ZIP file,
        with previous content and updates all optimised XMLs and the web images
        versions.
        
        :param new_package_file_path (default=None): Path to optimised SciELO Publishing
            Package file. If not given, it will be the same path and file name of the
            original package file ended with ``_optimised.zip``.
        :param preserve_files (default=True): preserve extracted and optimised files in
            aux directory. If False, it will delete files after written in new Package.
        """
        xmls_filenames = [
            xml_filename
            for xml_filename in self._package_file.namelist()
            if os.path.splitext(xml_filename)[-1] == ".xml"
        ]
        for i, xml_filename in enumerate(xmls_filenames):
            LOGGER.info(
                "Optimizing XML file %s [%s/%s]", xml_filename, i, len(xmls_filenames)
            )
            self._optimise_xml_to_web(
                XML(io.BytesIO(self._package_file.read(xml_filename))), xml_filename
            )
        files_to_update = os.listdir(self._extracted_package)
        if len(files_to_update) > 0:
            files_to_copy = set(self._package_file.namelist()) - set(files_to_update)
            if new_package_file_path is None:
                new_package_file_path = self._extracted_package + "_optimised.zip"
            LOGGER.info(
                "Generating new SciELO Publishing Package %s", new_package_file_path
            )
            with zipfile.ZipFile(new_package_file_path, "w") as new_zip_file:
                for zipped_file in files_to_copy:
                    zip_info = self._package_file.getinfo(zipped_file)
                    new_zip_file.writestr(
                        zipped_file,
                        self._package_file.read(zipped_file),
                        zip_info.compress_type,
                    )
                for filename in files_to_update:
                    LOGGER.info("Updating %s file in package", filename)
                    file_path = os.path.join(self._extracted_package, filename)
                    new_zip_file.write(file_path, filename)
                    if not preserve_files:
                        os.remove(file_path)
            if not preserve_files:
                os.rmdir(self._extracted_package)
