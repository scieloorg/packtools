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
from PIL import Image, ImageFile
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
    :param file_bytes: image file bytes
    """

    def __init__(self, image_filename, image_file_dir, file_bytes=None):
        self.filename = image_filename
        self.thumbnail_size = (267, 140)
        self.image_file_path = os.path.join(image_file_dir, image_filename)
        self._image_object = self._get_image_object(file_bytes)

    def _get_image_object(self, file_bytes):
        if file_bytes is not None:
            parser = ImageFile.Parser()
            try:
                parser.feed(file_bytes)
                image = parser.close()
            except IOError as exc:
                raise exceptions.WebImageGeneratorError(
                    'Error reading image "%s": %s' % (self.filename, str(exc))
                )
            else:
                return image

    @property
    def png_filename(self):
        return os.path.splitext(self.filename)[0] + ".png"

    @property
    def thumbnail_filename(self):
        return os.path.splitext(self.filename)[0] + ".thumbnail.jpg"

    def convert2png(self, destination_path=None):
        """Generate a PNG file from image file with the same name, changing only the
        file extension. If ``destination_path`` is given, the new image is saved in it,
        otherwise it is saved in the same directory as original image.
        """
        try:
            tiff_file = Image.open(self.image_file_path)
        except (OSError, IOError, ValueError) as exc:
            raise exceptions.WebImageGeneratorError(
                'Error opening image file "%s": %s' % (self.image_file_path, str(exc))
            )
        else:
            png_file = tiff_file.copy()
            new_filename = os.path.splitext(self.image_file_path)[0] + ".png"
            if destination_path is not None and len(destination_path) > 0:
                new_filename = os.path.join(
                    destination_path, os.path.basename(new_filename)
                )
            try:
                png_file.save(new_filename, "PNG")
                return new_filename
            except (ValueError, IOError) as exc:
                raise exceptions.WebImageGeneratorError(
                    'Error saving image file "%s": %s' % (new_filename, str(exc))
                )
            finally:
                tiff_file.close()

    def create_thumbnail(self, destination_path=None):
        """Generate a thumbnail file from image file with the same name, changing only
        the file name to ``*.thumbnail.jpg``. If ``destination_path`` is given, the new
        image is saved in it, otherwise it is saved in the same directory as original image.
        """
        try:
            image_file = Image.open(self.image_file_path)
        except (OSError, IOError, ValueError) as exc:
            raise exceptions.WebImageGeneratorError(
                'Error opening image file "%s": %s' % (self.image_file_path, str(exc))
            )
        else:
            thumbnail_file = image_file.copy()
            new_filename = os.path.splitext(self.image_file_path)[0] + ".thumbnail.jpg"
            if destination_path is not None and len(destination_path) > 0:
                new_filename = os.path.join(
                    destination_path, os.path.basename(new_filename)
                )
            thumbnail_file.thumbnail(self.thumbnail_size)
            try:
                thumbnail_file.save(new_filename, "JPEG")
                return new_filename
            except (ValueError, IOError) as exc:
                raise exceptions.WebImageGeneratorError(
                    'Error saving image file "%s": %s' % (new_filename, str(exc))
                )
            finally:
                image_file.close()

    def _get_bytes(self, format):
        image_file = io.BytesIO()
        try:
            self._image_object.convert("RGB").save(image_file, format)
        except (ValueError, IOError) as exc:
            raise exceptions.WebImageGeneratorError(
                'Error optimising image bytes from "%s": %s' % (self.filename, str(exc))
            )
        else:
            return image_file.getvalue()

    def get_png_bytes(self):
        """Generate a PNG image byte-like object from image file set in
        ``self._image_object``."""
        if self._image_object is None:
            raise exceptions.WebImageGeneratorError(
                'Error optimising image bytes from "%s": '
                "no original file bytes was given." % self.filename
            )

        return self._get_bytes("PNG")

    def get_thumbnail_bytes(self):
        """Generate a thumbnail image byte-like object from image file set in
        ``self._image_object``."""
        if self._image_object is None:
            raise exceptions.WebImageGeneratorError(
                'Error optimising image bytes from "%s": '
                'no original file bytes was given.'
                % self.filename
            )

        self._image_object.thumbnail(self.thumbnail_size)
        return self._get_bytes("JPEG")


class XMLWebOptimiser(object):
    """Optimise XML document to be properly rendered to HTML, with alternatives to
    images.

    Basic usage:

    .. code-block:: python

        xml_web_optimiser = XMLWebOptimiser(
            filename, image_filenames, read_file, stop_if_error
        )
        bytes = xml_web_optimiser.get_xml_file()
        optimised_assets = xml_web_optimiser.get_optimised_assets()
        assets_thumbnails = xml_web_optimiser.get_assets_thumbnails()

    :param filename: (str) XML file name
    :param image_filenames: (list) list of image file names 
    :param read_file: function to read file content from source which raises
        exceptions.SPPackageError if an error occurs during the file reading
    :param work_dir: directory path to work with image optimization
    :param stop_if_error: (bool) if True, it raises exceptions.XMLWebOptimiserError for
        handled exceptions, otherwise it logs error message.
    """

    def __init__(
        self, filename, image_filenames, read_file, work_dir, stop_if_error=False
    ):
        self.filename = filename
        self.work_dir = work_dir
        self.stop_if_error = stop_if_error
        self._optimised_assets = []
        self._assets_thumbnails = []
        if read_file is None:
            raise exceptions.XMLWebOptimiserError(
                "Error instantiating XMLWebOptimiser: read_file cannot be None"
            )
        self._read_file = read_file
        self._xml_file = XML(io.BytesIO(self._read_file(filename)))
        self._image_filenames = self._get_all_graphic_images_from_xml(image_filenames)

    def _get_all_graphic_images_from_xml(self, image_filenames):
        namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
        graphic_filename = set()
        for elem in self._xml_file.xpath(
            './/graphic[@xlink:href] | .//inline-graphic[@xlink:href]',
            namespaces=namespaces
        ):
            href_text = elem.attrib.get("{http://www.w3.org/1999/xlink}href")
            if href_text is not None and href_text in image_filenames:
                graphic_filename.add(href_text)
            else:
                for image_filename in image_filenames:
                    if href_text in image_filename:
                        graphic_filename.add(image_filename)

        return graphic_filename

    def _handle_image_exception(self, exception):
        if self.stop_if_error:
            raise exception
        else:
            LOGGER.info(str(exception))

    def _get_all_images_to_optimise(self):
        def is_image_to_optimise(image):
            image_filename = image.attrib.get("{http://www.w3.org/1999/xlink}href", "")
            __, filename_ext = os.path.splitext(image_filename)
            if filename_ext.startswith(".tif") or len(filename_ext) == 0:
                is_optimised_siblings = [
                    sibling
                    for sibling in image.xpath(
                        '../{}[@specific-use="scielo-web"]'.format(image.tag),
                        namespaces={"xlink": "http://www.w3.org/1999/xlink"},
                    )
                    if sibling.tag == image.tag
                ]
                if len(is_optimised_siblings) == 0:
                    return True
            return False

        paths = [
            './/graphic[@xlink:href and not(@specific-use="scielo-web")]',
            './/inline-graphic[@xlink:href and not(@specific-use="scielo-web")]',
        ]
        namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
        iterators = [
            self._xml_file.xpath(path, namespaces=namespaces) for path in paths
        ]
        for image in itertools.chain(*iterators):
            if is_image_to_optimise(image):
                image_filename = image.attrib["{http://www.w3.org/1999/xlink}href"]
                LOGGER.debug('Found <%s xlink:href="%s">', image.tag, image_filename)
                yield image_filename, image

    def _get_all_images_to_thumbnail(self):
        namespaces = {"xlink": "http://www.w3.org/1999/xlink"}
        images = self._xml_file.xpath("//graphic[@xlink:href]", namespaces=namespaces)
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
                    "{http://www.w3.org/1999/xlink}href"
                )
                yield image_filename, alternatives[0]

    def _get_web_image_generator(self, image_filename):
        try:
            image_file_bytes = self._read_file(image_filename)
        except exceptions.SPPackageError as exc:
            self._handle_image_exception(exc)
        else:
            try:
                web_image_generator = WebImageGenerator(
                    image_filename, self.work_dir, image_file_bytes
                )
            except exceptions.WebImageGeneratorError as exc:
                self._handle_image_exception(exc)
            else:
                return web_image_generator

    def _add_optimised_image(self, image_filename):
        web_image_generator = self._get_web_image_generator(image_filename)
        if web_image_generator is not None:
            try:
                png_bytes = web_image_generator.get_png_bytes()
            except exceptions.WebImageGeneratorError as exc:
                self._handle_image_exception(exc)
            else:
                self._optimised_assets.append(
                    (web_image_generator.png_filename, png_bytes)
                )
                return web_image_generator.png_filename

    def _add_assets_thumbnails(self, image_filename):
        web_image_generator = self._get_web_image_generator(image_filename)
        if web_image_generator is not None:
            try:
                thumbnail_bytes = web_image_generator.get_thumbnail_bytes()
            except exceptions.WebImageGeneratorError as exc:
                self._handle_image_exception(exc)
            else:
                self._assets_thumbnails.append(
                    (web_image_generator.thumbnail_filename, thumbnail_bytes)
                )
                return web_image_generator.thumbnail_filename

    def _get_similar_filename(self, image_filename):
        for filename in self._image_filenames:
            filename_root, filename_ext = os.path.splitext(filename)
            if filename_root == image_filename and ".tif" in filename_ext:
                LOGGER.debug('Found similar file name: "%s"', image_filename)
                return True, filename
        else:
            msg_error = 'No file named "%s" in package'
            if self.stop_if_error:
                raise exceptions.XMLWebOptimiserError(msg_error % image_filename)
            else:
                LOGGER.error(msg_error, image_filename)
                return False, None

    def _get_optimised_image_with_filename(self, image_filename, add_image):
        optimise = True
        if image_filename not in self._image_filenames:
            LOGGER.debug('"%s" not found in package_files', image_filename)
            optimise, image_filename = self._get_similar_filename(image_filename)
        if optimise:
            LOGGER.debug('Optimising image file "%s"', image_filename)
            return add_image(image_filename)

    def _add_alternative_to_alternatives_tag(
        self, image_element, alternative_attr_values
    ):
        image_parent = image_element.getparent()
        new_alternative = etree.Element(image_element.tag)
        for attrb, value in alternative_attr_values:
            new_alternative.set(attrb, value)
        if image_parent.tag == "alternatives":
            image_parent.append(new_alternative)
        else:
            alternative_node = etree.Element("alternatives")
            alternative_node.tail = image_element.tail
            image_element.tail = None
            alternative_node.append(image_element)
            alternative_node.append(new_alternative)
            image_parent.append(alternative_node)

    def get_xml_file(self):
        """Get a byte-like optimised XML, with WEB alternatives for images."""
        for image_filename, image_element in self._get_all_images_to_optimise():
            new_filename = self._get_optimised_image_with_filename(
                image_filename, self._add_optimised_image
            )
            if new_filename is not None:
                alternative_attr_values = (
                    ("{http://www.w3.org/1999/xlink}href", new_filename),
                    ("specific-use", "scielo-web"),
                )
                self._add_alternative_to_alternatives_tag(
                    image_element, alternative_attr_values
                )

        for image_filename, image_element in self._get_all_images_to_thumbnail():
            new_filename = self._get_optimised_image_with_filename(
                image_filename, self._add_assets_thumbnails
            )
            if new_filename is not None:
                alternative_attr_values = (
                    ("{http://www.w3.org/1999/xlink}href", new_filename),
                    ("specific-use", "scielo-web"),
                    ("content-type", "scielo-267x140"),
                )
                self._add_alternative_to_alternatives_tag(
                    image_element, alternative_attr_values
                )

        return etree.tostring(
            self._xml_file,
            xml_declaration=True,
            method="xml",
            encoding="utf-8",
            pretty_print=True,
        )

    def get_optimised_assets(self):
        """Generate tuples of PNG file name and bytes of each image produced by TIFF
        images referenced in XML content."""
        for optimised_asset in self._optimised_assets:
            yield optimised_asset

    def get_assets_thumbnails(self):
        """Generate tuples of thumbnail file name and bytes of each image produced by
        images referenced in XML content."""
        for asset_thumbnail in self._assets_thumbnails:
            yield asset_thumbnail


class SPPackage(object):
    """Adapter that manipulate SciELO Publishing Packages.

    Basic usage:

    .. code-block:: python

        package = SPPackage(package_file, extracted_package)
        package.optimise()

    :param package_file: SciELO Publishing Package, instance of ``zipfile.ZipFile``
    :param extracted_package: path to extract package files and optimise them
    """

    def __init__(self, package_file, extracted_package, stop_if_error=False):
        self._package_file = package_file
        self._extracted_package = extracted_package
        self._stop_if_error = stop_if_error

    @classmethod
    def from_file(cls, package_file_path, extracted_package=None, stop_if_error=False):
        """Factory of SPPackage instances.

        :param package_file_path: Path to the SciELO Publishing Package file, instance
               of ``zipfile.ZipFile``
        """

        if not zipfile.is_zipfile(package_file_path):
            raise ValueError("File is not a zip file")

        package2optimise = zipfile.ZipFile(package_file_path)
        if extracted_package is None:
            extracted_package = os.path.splitext(package_file_path)[0]
        return cls(package2optimise, extracted_package, stop_if_error)

    def _optimise_to_zipfile(
        self, new_package_file_path, xml_filename, zipped_filenames
    ):
        with zipfile.ZipFile(new_package_file_path, "a") as new_zip_file:
            zipped_files = []
            xml_web_optimiser = self._get_optimise_web_xml(
                xml_filename, zipped_filenames
            )
            # Write optimised XML to new Zipfile
            optimised_xml = xml_web_optimiser.get_xml_file()
            xml_zip_info = self._package_file.getinfo(xml_filename)
            LOGGER.debug('Writing XML file "%s" in package', xml_filename)
            new_zip_file.writestr(
                xml_filename, optimised_xml, xml_zip_info.compress_type
            )
            zipped_files.append(xml_filename)
            # Write optimised assets to new Zipfile
            LOGGER.debug('Writing asset files in package')
            for asset_filename, asset_bytes in xml_web_optimiser.get_optimised_assets():
                if asset_bytes is not None:
                    LOGGER.debug('Writing file "%s"', asset_filename)
                    new_zip_file.writestr(asset_filename, asset_bytes)
                    zipped_files.append(asset_filename)
            LOGGER.debug('Writing asset thumbnail files in package')
            for (
                asset_filename,
                asset_bytes,
            ) in xml_web_optimiser.get_assets_thumbnails():
                if asset_bytes is not None:
                    LOGGER.debug('Writing file "%s"', asset_filename)
                    new_zip_file.writestr(asset_filename, asset_bytes)
                    zipped_files.append(asset_filename)
            return zipped_files

    def _write_files_left(self, new_package_file_path, files_to_write):
        # Write files left to new Zipfile
        with zipfile.ZipFile(new_package_file_path, "a") as new_zip_file:
            for file_to_write in files_to_write:
                zip_info = self._package_file.getinfo(file_to_write)
                LOGGER.debug('Writing file "%s"', file_to_write)
                new_zip_file.writestr(
                    file_to_write,
                    self._package_file.read(file_to_write),
                    zip_info.compress_type,
                )

    def _get_optimise_web_xml(self, xml_filename, xml_related_files):
        image_filenames = [
            filename
            for filename in xml_related_files
            if not os.path.splitext(filename)[-1] == ".pdf"
        ]
        return XMLWebOptimiser(
            xml_filename,
            image_filenames,
            self._read_file,
            self._extracted_package,
            self._stop_if_error,
        )

    def _read_file(self, image_to_optimise):
        try:
            image_bytes = self._package_file.read(image_to_optimise)
        except KeyError as exc:
            raise exceptions.SPPackageError(
                "No file named {} in package".format(image_to_optimise)
            )
        else:
            return image_bytes

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
        if new_package_file_path is None:
            new_package_file_path = self._extracted_package + "_optimised.zip"
        LOGGER.info(
            "Generating new SciELO Publishing Package %s", new_package_file_path
        )
        zipped_filenames = self._package_file.namelist()
        xmls_filenames = [
            xml_filename
            for xml_filename in zipped_filenames
            if os.path.splitext(xml_filename)[-1] == ".xml"
        ]
        optimised_filenames = []
        for i, xml_filename in enumerate(xmls_filenames):
            LOGGER.info(
                "Optimizing XML file %s [%s/%s]", xml_filename, i, len(xmls_filenames)
            )
            filename_root, __ = os.path.splitext(xml_filename)
            optimised_filenames += self._optimise_to_zipfile(
                new_package_file_path, xml_filename, zipped_filenames
            )

        LOGGER.info(
            "Writing remained files from package in new SciELO Publishing Package"
        )
        self._write_files_left(
            new_package_file_path, set(zipped_filenames) - set(optimised_filenames)
        )

        if preserve_files:
            with zipfile.ZipFile(new_package_file_path) as new_zip_file:
                new_zip_file.extractall(self._extracted_package)
