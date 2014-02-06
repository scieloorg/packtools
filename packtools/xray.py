#coding: utf-8
import os
import zipfile
import itertools
import logging
import hashlib

from lxml import etree

from . import utils


logger = logging.getLogger(__name__)


def get_xmlschema(path):
    xmlschema_doc = etree.parse(open(path, 'r'))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema


class SPSMixin(object):
    xmlschema = get_xmlschema(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'sps_xsd', 'sps.xsd'))

    @property
    def xmls(self):
        fps = self.get_fps('xml')
        for fp in fps:
            yield etree.parse(fp)

    @property
    def xml(self):
        xmls = list(itertools.islice(self.xmls, 2))
        if len(xmls) == 1:
            return xmls[0]
        else:
            raise AttributeError('there is not a single xml file' + str(len(xmls)))

    @property
    def meta(self):
        dct_mta = {}

        xml_nodes = {"journal_title": ".//journal-meta/journal-title-group/journal-title",
                     "journal_eissn": ".//journal-meta/issn[@pub-type='epub']",
                     "journal_pissn": ".//journal-meta/issn[@pub-type='ppub']",
                     "article_title": ".//article-meta/title-group/article-title",
                     "issue_year": ".//article-meta/pub-date/year",
                     "issue_volume": ".//article-meta/volume",
                     "issue_number": ".//article-meta/issue",
                     "supplement": ".//article-meta/supplement",
                     }
        for node_k, node_v in xml_nodes.items():
            node = self.xml.find(node_v)
            dct_mta[node_k] = getattr(node, 'text', None)

        return dct_mta

    def is_valid_meta(self):
        """
        Checks if the minimum required data to identify a package is present.
        """
        meta = self.meta
        return bool(meta['article_title'] and (
                    meta['journal_eissn'] or meta['journal_pissn']) and (
                    meta['issue_volume'] or meta['issue_number']))

    def is_valid_schema(self):
        """
        Checks if the XML is valid against SPS XSD.
        More info at: https://github.com/scieloorg/scielo_publishing_schema
        """
        return self.xmlschema.validate(self.xml)

    def is_valid_package(self):
        """
        Validate if exist at least one XML file and one PDF file
        """
        is_valid = True
        for ext in ['xml', 'pdf']:
            try:
                _ = self.get_ext(ext)
            except ValueError as e:
                is_valid = False

        return is_valid

    def is_valid(self):
        """
        Performs all package validations sequentialy.
        """
        return self.is_valid_package() and self.is_valid_schema() and self.is_valid_meta()


class Xray(object):

    def __init__(self, filename):
        """
        ``filename`` is the full path to a zip file.
        """
        if not zipfile.is_zipfile(filename):
            raise ValueError('%s is not a valid zipfile.' % filename)

        self._filename = filename
        self._zip_pkg = zipfile.ZipFile(filename, 'r')
        self._pkg_names = {}

        self._classify()

    def __del__(self):
        self._cleanup_package_fp()

    def _cleanup_package_fp(self):
        # raises AttributeError if the object have not
        # been initialized properly.
        try:
            self._zip_pkg.close()
        except AttributeError:
            pass

    def _classify(self):
        for fileinfo, filename in zip(self._zip_pkg.infolist(), self._zip_pkg.namelist()):
            # ignore directories and empty files
            if fileinfo.file_size:
                _, ext = filename.rsplit('.', 1)
                ext_node = self._pkg_names.setdefault(ext, [])
                ext_node.append(filename)

    def get_members(self):
        """
        Get a list of members.
        """
        members = []
        for names in self._pkg_names.values():
            for name in names:
                members.append(name)

        return members

    def get_ext(self, ext):
        """
        Get a list os members having ``ext`` as extension. Raises
        ValueError if the archive does not have any members matching
        the extension.
        """
        try:
            return self._pkg_names[ext]
        except KeyError:
            return []

    def get_fps(self, ext):
        """
        Get file objects for all members having ``ext`` as extension.
        If ``ext`` is not found in the archive, the iterator is empty.
        """
        filenames = self.get_ext(ext)
        if not filenames:
            raise StopIteration()

        for filename in filenames:
            yield self._zip_pkg.open(filename, 'r')

    @property
    def checksum(self):
        """
        Checksum the package file using sha1.
        """
        return utils.checksum_file(self._filename, hashlib.sha1)


class SPSPackage(SPSMixin, Xray):
    pass

