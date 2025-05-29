import hashlib
import logging
import os
from datetime import date
from gettext import gettext as _
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED


from lxml import etree

from packtools.sps.libs.requester import fetch_data
from packtools.sps.pid_provider.models.article_assets import ArticleAssets
from packtools.sps.pid_provider.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.pid_provider.models.article_authors import Authors
from packtools.sps.pid_provider.models.article_doi_with_lang import DoiWithLang
from packtools.sps.pid_provider.models.article_ids import ArticleIds
from packtools.sps.pid_provider.models.article_renditions import ArticleRenditions
from packtools.sps.pid_provider.models.article_titles import ArticleTitles
from packtools.sps.pid_provider.models.body import Body
from packtools.sps.pid_provider.models.dates import ArticleDates
from packtools.sps.pid_provider.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.pid_provider.models.journal_meta import ISSN, Acronym, Title
from packtools.sps.pid_provider.models.related_articles import RelatedItems

LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class GetXmlWithPreError(Exception):
    ...


class GetXmlWithPreFromURIError(Exception):
    ...


class GetXMLItemsError(Exception):
    ...


class GetXMLItemsFromZipFileError(Exception):
    ...


class XMLWithPreArticlePublicationDateError(Exception):
    ...


def get_xml_items(xml_sps_file_path, filenames=None):
    """
    Get XML items from XML file or Zip file

    Arguments
    ---------
        xml_sps_file_path: str

    Return
    ------
    dict iterator which keys are filename and xml_with_pre

    Raises
    ------
    GetXMLItemsError
    """
    try:
        name, ext = os.path.splitext(xml_sps_file_path)
        if ext == ".zip":
            return get_xml_items_from_zip_file(xml_sps_file_path, filenames)
        if ext == ".xml":
            with open(xml_sps_file_path) as fp:
                xml = get_xml_with_pre(fp.read())
                xml.xml_file_path = xml_sps_file_path
                item = os.path.basename(xml_sps_file_path)
            return [{"filename": item, "xml_with_pre": xml, "files": [item], "filenames": [item]}]
        raise TypeError(
            _("{} must be xml file or zip file containing xml").format(
                xml_sps_file_path
            )
        )
    except Exception as e:
        LOGGER.exception(e)
        raise GetXMLItemsError(
            _("Unable to get xml items from {}: {} {}").format(
                xml_sps_file_path, type(e), e
            )
        )


def get_xml_items_from_zip_file(xml_sps_file_path, filenames=None):
    """
    Return the first XML content in the Zip file.

    Arguments
    ---------
        xml_sps_file_path: str
        filenames: str list

    Return
    ------
    str
    """
    try:
        found = False
        with ZipFile(xml_sps_file_path) as zf:
            filenames = filenames or zf.namelist() or []
            _filenames = [
                os.path.basename(name)
                for name in zf.namelist() if name
            ]
            for item in filenames:
                if item.endswith(".xml"):
                    try:
                        content = zf.read(item)
                        xml_with_pre = get_xml_with_pre(content.decode("utf-8"))
                        xml_with_pre.zip_file_path = xml_sps_file_path
                        found = True
                        yield {
                            "filename": item,
                            "xml_with_pre": xml_with_pre,
                            "files": filenames,
                            "filenames": _filenames,
                        }
                    except Exception as e:
                        LOGGER.exception(f"Unable to get XMLWithPre from {xml_sps_file_path}/{item}")
                        continue
            if not found:
                raise TypeError(
                    f"{xml_sps_file_path} has no XML. Files found: {filenames}"
                )
    except Exception as e:
        LOGGER.exception(e)
        raise GetXMLItemsFromZipFileError(
            _("Unable to get xml items from zip file {}: {} {}").format(
                xml_sps_file_path, type(e), e
            )
        )


def get_sps_pkg_xml_items(xml_sps_file_path, filenames=None):
    """
    Get XML items from XML file or Zip file

    Arguments
    ---------
        xml_sps_file_path: str

    Return
    ------
    dict iterator which keys are filename and xml_with_pre

    Raises
    ------
    GetXMLItemsError
    """
    try:
        name, ext = os.path.splitext(xml_sps_file_path)
        if ext == ".zip":
            return get_sps_pkg_xml_items_from_zip_file(xml_sps_file_path, filenames)
        if ext == ".xml":
            with open(xml_sps_file_path) as fp:
                xml = get_xml_with_pre(fp.read())
                xml.xml_file_path = xml_sps_file_path
                item = os.path.basename(xml_sps_file_path)
            return [{"filename": item, "xml_with_pre": xml, "files": [item], "filenames": [item]}]
        return [
            {
                "error": _("{} must be xml file or zip file containing xml").format(
                    xml_sps_file_path
                )
            }
        ]

    except Exception as e:
        return [
            {
                "error": _("Unable to get xml items from {}: {} {}").format(
                    xml_sps_file_path, type(e), e
                )
            }
        ]


def get_sps_pkg_xml_items_from_zip_file(xml_sps_file_path, filenames=None):
    """
    Return the first XML content in the Zip file.

    Arguments
    ---------
        xml_sps_file_path: str
        filenames: str list

    Return
    ------
    str
    """
    try:
        filenames = []
        _filenames = []
        with ZipFile(xml_sps_file_path) as zf:
            filenames = filenames or zf.namelist() or []
            _filenames = [
                os.path.basename(name)
                for name in zf.namelist() if name
            ]
            for item in filenames:
                if item.endswith(".xml"):
                    try:
                        content = zf.read(item)
                        xml_with_pre = get_xml_with_pre(content.decode("utf-8"))
                        xml_with_pre.zip_file_path = xml_sps_file_path
                        yield {
                            "filename": item,
                            "xml_with_pre": xml_with_pre,
                            "files": filenames,
                            "filenames": _filenames,
                        }
                    except Exception as e:
                        yield {
                            "filename": item,
                            "files": filenames,
                            "filenames": _filenames,
                            "error": str(e),
                            "type_error": str(type(e)),
                        }
    except Exception as e:
        yield {
            "files": filenames,
            "filenames": _filenames,
            "error": str(e),
            "type_error": str(type(e)),
        }


def update_zip_file_xml(xml_sps_file_path, xml_file_path, content):
    """
    Save XML content in a Zip file.
    Return saved zip file path

    Arguments
    ---------
        xml_sps_file_path: str
        content: bytes

    Return
    ------
    str
    """
    with ZipFile(xml_sps_file_path, "w", compression=ZIP_DEFLATED) as zf:
        LOGGER.debug(
            "Try to write xml %s %s %s"
            % (xml_sps_file_path, xml_file_path, content[:100])
        )
        zf.writestr(xml_file_path, content)

    return os.path.isfile(xml_sps_file_path)


def create_xml_zip_file(xml_sps_file_path, content):
    """
    Save XML content in a Zip file.
    Return saved zip file path

    Arguments
    ---------
        xml_sps_file_path: str
        content: bytes

    Return
    ------
    bool

    Raises
    ------
    IOError
    """
    dirname = os.path.dirname(xml_sps_file_path)
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)

    basename = os.path.basename(xml_sps_file_path)
    name, ext = os.path.splitext(basename)

    with ZipFile(xml_sps_file_path, "w", compression=ZIP_DEFLATED) as zf:
        zf.writestr(name + ".xml", content)
    return os.path.isfile(xml_sps_file_path)


def get_zips(xml_sps_file_path):
    found = False
    with ZipFile(xml_sps_file_path) as zf:
        # obtém os components do zip
        filenames = zf.namelist() or []
        xmls = [
            os.path.splitext(os.path.basename(filename))[0]
            for filename in filenames if filename.endswith(".xml")]
        xmls = {key: [] for key in xmls}

        for key in list(xmls.keys()):
            for filename in filenames:
                name = os.path.basename(filename)
                if name in (key+".pdf", key+".xml"):
                    xmls[key].append(filename)
                elif name.startswith(key+"-") and not name.endswith(".xml"):
                    xmls[key].append(filename)
            filenames = list(set(filenames) - set(xmls[key]))

        with TemporaryDirectory() as tmpdirname:

            for key, files in xmls.items():

                zfile = os.path.join(tmpdirname, f"{key}.zip")
                with ZipFile(zfile, "w", compression=ZIP_DEFLATED) as zfw:
                    for item in files:
                        zfw.writestr(item, zf.read(item))

                with open(zfile, "rb") as zfw:
                    yield {"zipfilename": key+".zip", "content": zfw.read()}


def get_xml_with_pre_from_uri(uri, timeout=30):
    try:
        response = fetch_data(uri, timeout=timeout)
        xml_content = response.decode("utf-8")
    except Exception as e:
        raise GetXmlWithPreFromURIError(_("Unable to get xml from {}").format(uri))
    xml_with_pre = get_xml_with_pre(xml_content)
    xml_with_pre.uri = uri
    return xml_with_pre


def get_xml_with_pre(xml_content):
    try:
        xml_content = xml_content.strip()
        # return etree.fromstring(xml_content)
        pref, xml = split_processing_instruction_doctype_declaration_and_xml(
            xml_content
        )
        return XMLWithPre(pref, etree.fromstring(xml))

    except Exception as e:
        if xml_content:
            raise GetXmlWithPreError(
                "Unable to get xml with pre %s: %s ... %s"
                % (e, xml_content[:100], xml_content[-200:])
            )
        raise GetXmlWithPreError("Unable to get xml with pre %s" % e)


def split_processing_instruction_doctype_declaration_and_xml(xml_content):
    xml_content = xml_content.strip()

    if not xml_content.startswith("<?") and not xml_content.startswith("<!"):
        return "", xml_content
    if xml_content.endswith("/>"):
        # <article/>
        p = xml_content.rfind("<")
        if p >= 0:
            pre = xml_content[:p].strip()
            if pre.endswith(">"):
                return xml_content[:p], xml_content[p:]
            else:
                return "", xml_content

    p = xml_content.rfind("</")
    if p:
        # </article>
        endtag = xml_content[p:]
        starttag1 = endtag.replace("/", "").replace(">", " ")
        starttag2 = endtag.replace("/", "")
        for starttag in (starttag1, starttag2):
            p = xml_content.find(starttag)
            if p >= 0:
                pre = xml_content[:p].strip()
                if pre.endswith(">"):
                    return xml_content[:p], xml_content[p:]
                else:
                    return "", xml_content

    return "", xml_content


class XMLWithPre:
    """
    Preserva o texto anterior ao elemento `root`
    """

    def __init__(self, xmlpre, xmltree, pretty_print=True):
        self.xmlpre = xmlpre or ""
        self.xmltree = xmltree
        self.filename = None
        self.pretty_print = pretty_print
        self.files = None
        self.filenames = None
        self.uri = None
        self.zip_file_path = None
        self.xml_file_path = None
        self._DOCTYPE = None
        self._public_id = None
        self._system_id = None
        self.relative_system_id = None
        self._sps_version = None
        self.errors = None

    @property
    def data(self):
        return dict(
            sps_pkg_name=self.sps_pkg_name,
            pid_v3=self.v3,
            pid_v2=self.v2,
            aop_pid=self.aop_pid,
            filename=self.filename,
            files=self.files,
            filenames=self.filenames,
        )

    @classmethod
    def create(cls, path=None, uri=None, capture_errors=False, timeout=30):
        """
        Returns instance of XMLWithPre

        path : str
            zip or XML file
        uri : str
            XML file URI
        """
        if path:
            errors = []
            if capture_errors:
                items = get_sps_pkg_xml_items(path)
            else:
                items = get_xml_items(path)

            for item in items:
                if not item:
                    continue
                if item.get("error"):
                    errors.append(item)
                else:
                    item["xml_with_pre"].filename = item["filename"]
                    item["xml_with_pre"].files = item.get("files")
                    item["xml_with_pre"].filenames = item.get("filenames")
                    item["xml_with_pre"].errors = errors
                    yield item["xml_with_pre"]
        if uri:
            yield get_xml_with_pre_from_uri(uri, timeout)

    @property
    def DOCTYPE(self):
        if self._DOCTYPE is None:
            if '<!DOCTYPE' in self.xmlpre:
                self._DOCTYPE = self.xmlpre[self.xmlpre.find('<!DOCTYPE'):]
                self._DOCTYPE = self._DOCTYPE[:self._DOCTYPE.find('>')+1]
        return self._DOCTYPE

    @property
    def public_id(self):
        if self._public_id is None:
            if self.DOCTYPE is not None:
                self._public_id = self.DOCTYPE[self.DOCTYPE.find('"')+1:]
                self._public_id = self._public_id[:self._public_id.find('"')]
        return self._public_id

    @property
    def system_id(self):
        if self._system_id is None:
            if 'http' in self.DOCTYPE:
                self._system_id = self.DOCTYPE[self.DOCTYPE.find('"http')+1:]
                self._system_id = self._system_id[:self._system_id.find('"')]
            if self.public_id:
                _text = self.DOCTYPE[self.DOCTYPE.find(self.public_id)+len(self.public_id):]
                _text = _text[_text.find('"')+1:]
                _text = _text[_text.find('"')+1:]
                self.relative_system_id = _text[:_text.find('"')]
        return self._system_id

    @property
    def sps_version(self):
        try:
            return self.xmltree.find(".").get("specific-use")
        except (AttributeError, TypeError, ValueError):
            return None

    def update_xml_in_zip_file(self):
        if self.zip_file_path and self.filename:
            with ZipFile(self.zip_file_path, "a", compression=ZIP_DEFLATED) as zf:
                zf.writestr(
                    self.filename,
                    self.tostring(pretty_print=True),
                )

    def get_zip_content(self, xml_filename, pretty_print=False):
        zip_content = None
        with TemporaryDirectory() as tmpdirname:
            temp_zip_file_path = os.path.join(tmpdirname, f"{xml_filename}.zip")
            with ZipFile(temp_zip_file_path, "w", compression=ZIP_DEFLATED) as zf:
                zf.writestr(xml_filename, self.tostring(pretty_print=pretty_print))
            with open(temp_zip_file_path, "rb") as fp:
                zip_content = fp.read()
        return zip_content

    @property
    def sps_pkg_name_suffix(self):
        if self.is_aop and self.main_doi:
            doi = self.main_doi
            if "/" in doi:
                doi = doi[doi.rfind("/") + 1 :]
            return doi.replace(".", "-")
        if self.elocation_id:
            return self.elocation_id
        if self.fpage:
            try:
                fpage = int(self.fpage)
            except (TypeError, ValueError):
                return self.fpage
            if fpage != 0:
                return self.fpage + (self.fpage_seq or "")

    @property
    def alternative_sps_pkg_name_suffix(self):
        try:
            return self.v2[-5:]
        except TypeError:
            return self.filename

    @property
    def sps_pkg_name(self):
        try:
            suppl = self.suppl
            if suppl and int(suppl) == 0:
                suppl = "suppl"
        except (TypeError, ValueError):
            pass

        xml_acron = Acronym(self.xmltree)
        parts = [
            self.journal_issn_electronic or self.journal_issn_print,
            xml_acron.text,
            self.volume,
            self.number and self.number.zfill(2),
            suppl,
            self.sps_pkg_name_suffix or self.alternative_sps_pkg_name_suffix,
        ]
        return "-".join([part for part in parts if part])

    @property
    def article_id_parent(self):
        """
        Retorna o nó pai dos elementos article-id (v2, v3, aop_pid)
        """
        try:
            return self.xmltree.xpath(".//article-meta")[0]
        except IndexError:
            node = self.xmltree.find(".")
            front = node.find("front")
            if front is None:
                front = etree.Element("front")
                node.append(front)
            parent = etree.Element("article-meta")
            front.append(parent)
            return parent

    def tostring(self, pretty_print=False):
        return self.xmlpre + etree.tostring(
            self.xmltree,
            encoding="utf-8",
            pretty_print=pretty_print,
        ).decode(
            "utf-8"
        )

    def update_ids(self, v3, v2, aop_pid):
        """
        Atualiza todos os elementos article-id (v2, v3, aop_pid)
        """
        self.article_ids.v3 = v3
        self.article_ids.v2 = v2
        if aop_pid:
            self.article_ids.aop_pid = aop_pid

    @property
    def related_items(self):
        return RelatedItems(self.xmltree).related_articles

    @property
    def links(self):
        # Ha casos de related-article sem href
        # <related-article id="pr03" related-article-type="press-release" specific-use="processing-only"/>
        return [item["href"] for item in self.related_items if item.get("href")]

    @property
    def article_ids(self):
        return ArticleIds(self.xmltree)

    @property
    def v3(self):
        return self.article_ids.v3

    @property
    def v2(self):
        return self.article_ids.v2

    @property
    def aop_pid(self):
        return self.article_ids.aop_pid

    @property
    def order(self):
        return self.article_ids.other

    @order.setter
    def order(self, value):
        try:
            new_value = str(int(value)).zfill(5)
        except (TypeError, ValueError, AttributeError):
            new_value = None

        if not new_value or len(new_value) > 5:
            raise ValueError(
                "can't set attribute XMLWithPre.order. "
                "Expected value must a 5 characters digit. Got: %s" % value
            )
        try:
            node = self.xmltree.xpath('.//article-id[@pub-id-type="other"]')[0]
        except IndexError:
            node = None

        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "other")
            parent = self.article_id_parent
            parent.insert(1, node)
        node.text = new_value

    @v2.setter
    def v2(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                "can't set attribute XMLWithPre.v2. "
                "Expected value must have 23 characters. Got: %s" % value
            )
        try:
            node = self.xmltree.xpath('.//article-id[@specific-use="scielo-v2"]')[0]
        except IndexError:
            node = None
        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "scielo-v2")
            parent = self.article_id_parent
            parent.insert(1, node)
        node.text = value

    @v3.setter
    def v3(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                "can't set attribute XMLWithPre.v3. "
                "Expected value must have 23 characters. Got: %s" % value
            )
        try:
            node = self.xmltree.xpath('.//article-id[@specific-use="scielo-v3"]')[0]
        except IndexError:
            node = None

        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "scielo-v3")
            parent = self.article_id_parent
            parent.insert(1, node)
        if node is not None:
            node.text = value

    @aop_pid.setter
    def aop_pid(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                "can't set attribute XMLWithPre.aop_pid. "
                "Expected value must have 23 characters. Got: %s" % value
            )
        try:
            node = self.xmltree.xpath(
                './/article-id[@specific-use="previous-pid" and '
                '@pub-id-type="publisher-id"]'
            )[0]
        except IndexError:
            node = None

        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "previous-pid")
            parent = self.article_id_parent
            parent.insert(1, node)
        if node is not None:
            node.text = value

    @property
    def v2_prefix(self):
        return (
            f"S{self.journal_issn_electronic or self.journal_issn_print}{self.pub_year}"
        )

    @property
    def article_doi_with_lang(self):
        if (
            not hasattr(self, "_article_doi_with_lang")
            or not self._article_doi_with_lang
        ):
            # [{"lang": "en", "value": "DOI"}]
            doi_with_lang = DoiWithLang(self.xmltree)
            self._main_doi = doi_with_lang.main_doi
            self._article_doi_with_lang = doi_with_lang.data
        return self._article_doi_with_lang

    @property
    def main_doi(self):
        if not hasattr(self, "_main_doi") or not self._main_doi:
            # [{"lang": "en", "value": "DOI"}]
            doi_with_lang = DoiWithLang(self.xmltree)
            self._main_doi = doi_with_lang.main_doi
        return self._main_doi

    @property
    def main_toc_section(self):
        """
        <subj-group subj-group-type="heading">
            <subject>Articles</subject>
        </subj-group>
        """
        if not hasattr(self, "_main_toc_section") or not self._main_toc_section:
            # [{"lang": "en", "value": "DOI"}]
            node = self.xmltree.find('.//subj-group[@subj-group-type="heading"]')
            if node is None:
                self._main_toc_section = None
            else:
                self._main_toc_section = node.findtext("./subject")
        return self._main_toc_section

    @property
    def issns(self):
        if not hasattr(self, "_issns") or not self._issns:
            # [{"type": "epub", "value": "1234-9876"}]
            issns = ISSN(self.xmltree)
            self._issns = {item["type"]: item["value"] for item in issns.data}
        return self._issns

    @property
    def is_aop(self):
        if not hasattr(self, "_is_aop") or not self._is_aop:
            items = (
                self.article_meta_issue.volume,
                self.article_meta_issue.number,
                self.article_meta_issue.suppl,
            )
            self._is_aop = not any(items)
        return self._is_aop

    @property
    def xml_dates(self):
        if not hasattr(self, "_xml_dates") or not self._xml_dates:
            # ("year", "month", "season", "day")
            self._xml_dates = ArticleDates(self.xmltree)
        return self._xml_dates

    @property
    def article_meta_issue(self):
        # artigos podem ser publicados sem estarem associados a um fascículo
        # Neste caso, não há volume, número, suppl, fpage, fpage_seq, lpage
        # Mas deve ter ano de publicação em qualquer caso
        if not hasattr(self, "_article_meta_issue") or not self._article_meta_issue:
            self._article_meta_issue = ArticleMetaIssue(self.xmltree)
        return self._article_meta_issue

    @property
    def volume(self):
        if not hasattr(self, "_volume") or not self._volume:
            self._volume = self.article_meta_issue.volume
        return self._volume

    @property
    def number(self):
        if not hasattr(self, "_number") or not self._number:
            self._number = self.article_meta_issue.number
        return self._number

    @property
    def suppl(self):
        if not hasattr(self, "_suppl") or not self._suppl:
            self._suppl = self.article_meta_issue.suppl
        return self._suppl

    @property
    def fpage(self):
        if not hasattr(self, "_fpage") or not self._fpage:
            self._fpage = self.article_meta_issue.fpage
        return self._fpage

    @property
    def fpage_seq(self):
        if not hasattr(self, "_fpage_seq") or not self._fpage_seq:
            self._fpage_seq = self.article_meta_issue.fpage_seq
        return self._fpage_seq

    @property
    def lpage(self):
        if not hasattr(self, "_lpage") or not self._lpage:
            self._lpage = self.article_meta_issue.lpage
        return self._lpage

    @property
    def elocation_id(self):
        if not hasattr(self, "_elocation_id") or not self._elocation_id:
            self._elocation_id = self.article_meta_issue.elocation_id
        return self._elocation_id

    @property
    def pub_year(self):
        if not hasattr(self, "_pub_year") or not self._pub_year:
            try:
                self._pub_year = (
                    self.article_meta_issue.collection_date.get("year") or
                    self.article_meta_issue.article_date.get("year")
                )
            except AttributeError:
                return None
        return self._pub_year

    @property
    def authors(self):
        if not hasattr(self, "_authors") or not self._authors:
            authors = Authors(self.xmltree)
            self._authors = {
                "person": authors.contribs,
                "collab": authors.collab or None,
            }
        return self._authors

    @property
    def article_titles(self):
        if not hasattr(self, "_article_titles") or not self._article_titles:
            # list of dict which keys are lang and text
            article_titles = ArticleTitles(self.xmltree)
            self._article_titles = article_titles.data
        return self._article_titles

    @property
    def partial_body(self):
        if not hasattr(self, "_partial_body") or not self._partial_body:
            self._partial_body = None
            try:
                body = Body(self.xmltree)
                for text in body.main_body_texts:
                    if text:
                        self._partial_body = text
                        break
            except AttributeError:
                self._partial_body = None
        return self._partial_body

    @property
    def collab(self):
        if not hasattr(self, "_collab") or not self._collab:
            self._collab = self.authors.get("collab")
        return self._collab

    @property
    def journal_title(self):
        if not hasattr(self, "_journal_title") or not self._journal_title:
            self._journal_title = Title(self.xmltree).journal_title
        return self._journal_title

    @property
    def journal_issn_print(self):
        if not hasattr(self, "_journal_issn_print") or not self._journal_issn_print:
            # list of dict which keys are
            # href, ext-link-type, related-article-type
            self._journal_issn_print = self.issns.get("ppub")
        return self._journal_issn_print

    @property
    def journal_issn_electronic(self):
        if (
            not hasattr(self, "_journal_issn_electronic")
            or not self._journal_issn_electronic
        ):
            # list of dict which keys are
            # href, ext-link-type, related-article-type
            self._journal_issn_electronic = self.issns.get("epub")
        return self._journal_issn_electronic

    @property
    def article_publication_date(self):
        if (
            not hasattr(self, "_article_publication_date")
            or not self._article_publication_date
        ):
            # ("year", "month", "season", "day")
            self._article_publication_date = None
            _date = self.xml_dates.article_date
            if _date:
                try:
                    d = date(
                        int(_date["year"]),
                        int(_date["month"]),
                        int(_date["day"]),
                    )
                except (ValueError, TypeError, KeyError) as e:
                    raise XMLWithPreArticlePublicationDateError(
                        _(
                            "Unable to get XMLWithPre.article_publication_date {} {} {}"
                        ).format(_date, type(e), e)
                    )
                else:
                    self._article_publication_date = f"{_date['year']}-{_date['month'].zfill(2)}-{_date['day'].zfill(2)}"
        return self._article_publication_date

    @article_publication_date.setter
    def article_publication_date(self, value):
        """
        value : dict (keys: year, month, day)
        """
        try:
            node = self.xmltree.xpath(".//article-meta//pub-date[@date-type='pub']")[0]
        except IndexError:
            try:
                node = self.xmltree.xpath(".//article-meta//pub-date[@pub-type='epub']")[0]
            except IndexError:
                node = None
        if node is None:
            node = etree.Element("pub-date")
            node.set("date-type", "pub")
            node.set("publication-format", "electronic")

            # https://jats.nlm.nih.gov/publishing/tag-library/1.3/element/article-meta.html
            pub_date_preceding_siblings = (
                "pub-date",
                "author-notes",
                "aff",
                "contrib-group",
                "title-group",
                "article-categories",
                "article-version-alternatives",
                "article-version",
                "article-id",
            )
            for sibling_name in pub_date_preceding_siblings:
                try:
                    self.xmltree.find(f".//article-meta/{sibling_name}").addnext(node)
                    break
                except AttributeError:
                    continue

        if node is not None:
            try:
                numbers = {k: int(v) for k, v in value.items()}
                d = date(numbers.get("year"), numbers.get("month"), numbers.get("day"))
            except (ValueError, TypeError):
                raise ValueError(f"Unable to set {value} to article publcation date")

            for name, max_length in zip(("day", "month", "year"), (2, 2, 4)):
                elem = node.find(name)
                if elem is None:
                    elem = etree.Element(name)
                    node.append(elem)
                elem.text = str(numbers[name]).zfill(max_length)

    @property
    def article_pub_year(self):
        if not hasattr(self, "_article_pub_year") or not self._article_pub_year:
            # ("year", "month", "season", "day")
            try:
                self._article_pub_year = self.xml_dates.article_date["year"]
            except (ValueError, TypeError, KeyError) as e:
                self._article_pub_year = self.pub_year
        return self._article_pub_year

    @property
    def article_titles_texts(self):
        if not hasattr(self, "_article_titles_texts") or not self._article_titles_texts:
            self._article_titles_texts = [
                item["plain_text"] for item in self.article_titles if item["plain_text"]
            ]
        return self._article_titles_texts

    @property
    def finger_print(self):
        return generate_finger_print(self.tostring(pretty_print=self.pretty_print))

    @property
    def main_lang(self):
        return ArticleAndSubArticles(self.xmltree).main_lang

    @property
    def langs(self):
        for item in ArticleAndSubArticles(self.xmltree).data:
            yield item["lang"]

    @property
    def components(self):
        _components = {}
        for item in self.renditions:
            _components[item["name"]] = item
        for item in self.assets:
            _components[item["name"]] = item
        return _components

    @property
    def assets(self):
        items = []
        xml_assets = ArticleAssets(self.xmltree)
        for xml_graphic in xml_assets.items:
            if xml_graphic.xlink_href in items:
                continue
            items.append(xml_graphic.xlink_href)
            component_type = (
                "supplementary-material"
                if xml_graphic.is_supplementary_material
                else "asset"
            )
            yield {
                "name": xml_graphic.xlink_href,
                "xml_elem_id": xml_graphic.id,
                "component_type": component_type,
            }

    @property
    def renditions(self):
        xml_renditions = ArticleRenditions(self.xmltree)
        for item in xml_renditions.article_renditions:
            name = self.sps_pkg_name + ".pdf" if item.is_main_language else f"{self.sps_pkg_name}-{item.language}.pdf"
            yield {
                "name": name,
                "lang": item.language,
                "component_type": "rendition",
                "main": item.is_main_language,
            }


def generate_finger_print(content):
    if not content:
        return None
    if isinstance(content, str):
        content = content.upper()
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()
