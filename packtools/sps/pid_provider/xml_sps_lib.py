import hashlib
import logging
import os
from datetime import date
from functools import lru_cache, cached_property
from gettext import gettext as _
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED
from zlib import crc32

from lxml import etree

from packtools.sps.libs.requester import fetch_data
from packtools.sps.pid_provider.name2number import fix_pre_loading

# 4.7.1 packtools.sps.models.*
from packtools.sps.pid_provider.models.article_assets import ArticleAssets
from packtools.sps.pid_provider.models.article_and_subarticles import (
    ArticleAndSubArticles,
)
from packtools.sps.pid_provider.models.article_doi_with_lang import DoiWithLang
from packtools.sps.pid_provider.models.article_ids import ArticleIds
from packtools.sps.pid_provider.models.article_renditions import ArticleRenditions
from packtools.sps.pid_provider.models.body import Body
from packtools.sps.pid_provider.models.dates import (
    ArticleDates,
    format_date,
    XMLWithPreArticlePublicationDateError,
)
from packtools.sps.pid_provider.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.pid_provider.models.journal_meta import ISSN, Acronym, Title
from packtools.sps.pid_provider.models.related_articles import RelatedItems

LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class GetXmlWithPreError(Exception): ...


class GetXmlWithPreFromURIError(Exception): ...


class GetXMLItemsError(Exception): ...


class GetXMLWithPreFromZipFileError(Exception): ...


class XMLWithPreArticlePublicationDateError(Exception): ...


def get_xml_items(xml_sps_file_path, filenames=None, capture_errors=None):
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
            return get_xml_with_pre_from_zip_file(
                xml_sps_file_path, filenames, capture_errors
            )
        if ext == ".xml":
            try:
                return get_xml_with_pre_from_xml_file(xml_sps_file_path, "utf-8")
            except GetXmlWithPreError as e:
                return get_xml_with_pre_from_xml_file(xml_sps_file_path, "iso-8859-1")

        raise TypeError(
            _("{} must be xml file or zip file containing xml").format(
                xml_sps_file_path
            )
        )
    except Exception as e:
        if capture_errors:
            return [
                {
                    "error": _("Unable to get xml items from {}: {} {}").format(
                        xml_sps_file_path, type(e), e
                    )
                }
            ]
        raise GetXMLItemsError(
            _("Unable to get xml items from {}: {} {}").format(
                xml_sps_file_path, type(e), e
            )
        )


def get_xml_with_pre_from_xml_file(xml_sps_file_path, encoding):
    with open(xml_sps_file_path, encoding=encoding) as fp:
        content = fp.read()
    xml = get_xml_with_pre(content)
    xml.file_path = xml_sps_file_path
    item = os.path.basename(xml_sps_file_path)
    return [
        {
            "filename": item,
            "xml_with_pre": xml,
            "files": [item],
            "filenames": [item],
        }
    ]


def get_xml_with_pre_from_zip_file(
    xml_sps_file_path, filenames=None, capture_errors=False
):
    """
    Extract and process XML items from a ZIP file.

    Parameters
    ----------
    xml_sps_file_path : str
        Path to the ZIP file
    filenames : list of str, optional
        Specific files to process. If None, processes all files.

    Yields
    ------
    dict
        Success: {filename, xml_with_pre, files, filenames}
        XML error: {filename, files, filenames, error, type_error}
        ZIP error: {files, filenames, error, type_error}

    Notes
    -----
    Yields errors as dicts instead of raising. Check for 'error' key.
    """
    try:
        paths = []
        basenames = []

        zip_data = get_xml_items_from_zip_file(
            xml_sps_file_path,
            filenames,
        )
        xml_files = zip_data.get("xml_files")
        if not xml_files:
            raise TypeError(f"{xml_sps_file_path} has no XML files")

        paths = zip_data.get("paths")
        basenames = zip_data.get("basenames")

        for basename, xml_file in xml_files:
            try:
                response = {
                    "filename": xml_file,
                    "files": paths,
                    "filenames": basenames,
                }
                xml_with_pre = get_xml_with_pre_from_zip_file_component(
                    xml_sps_file_path, xml_file
                )
                xml_with_pre.zip_file_path = xml_sps_file_path
                response["xml_with_pre"] = xml_with_pre
                yield response
            except Exception as e:
                if not capture_errors:
                    raise GetXMLWithPreFromZipFileError(
                        f"Error in {xml_sps_file_path}/{xml_file}"
                    )
                response["error"] = str(e)
                response["type_error"] = type(e).__name__
                yield response

    except Exception as e:
        if not capture_errors:
            raise GetXMLWithPreFromZipFileError(
                _("Unable to get xml items from zip file {}: {} {}").format(
                    xml_sps_file_path, type(e).__name__, e
                )
            )
        yield {
            "files": paths,
            "filenames": basenames,
            "error": str(e),
            "type_error": type(e).__name__,
        }


def get_xml_items_from_zip_file(
    xml_sps_file_path,
    filenames=None,
):
    """
    Extract and process XML items from a ZIP file.

    Parameters
    ----------
    xml_sps_file_path : str
        Path to the ZIP file
    filenames : list of str, optional
        Specific files to process. If None, processes all files.

    Yields
    ------
    dict
        Success: {filename, xml_with_pre, files, filenames}
        XML error: {filename, files, filenames, error, type_error}
        ZIP error: {files, filenames, error, type_error}

    Notes
    -----
    Yields errors as dicts instead of raising. Check for 'error' key.
    """
    basenames = []
    zip_components = []
    xml_files = []
    with ZipFile(xml_sps_file_path) as zf:
        zip_components = zf.namelist()
        basenames = list(os.path.basename(n) for n in zip_components if n)

        for item in zip_components:
            if not item.endswith(".xml"):
                continue

            basename = os.path.basename(item)
            if basename.startswith("."):
                continue

            if not filenames or basename in filenames:
                xml_files.append((basename, item))
    return {
        "basenames": basenames,
        "paths": zip_components,
        "xml_files": xml_files,
    }


def get_xml_with_pre_from_zip_file_component(xml_sps_file_path, xml_file):
    with ZipFile(xml_sps_file_path) as zf:
        zf_read = zf.read(xml_file)
        try:
            return get_xml_with_pre(zf_read.decode("utf-8"))
        except Exception as e:
            return get_xml_with_pre(zf_read.decode("iso-8859-1"))


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
            for filename in filenames
            if filename.endswith(".xml")
        ]
        xmls = {key: [] for key in xmls}

        for key in list(xmls.keys()):
            for filename in filenames:
                name = os.path.basename(filename)
                if name in (key + ".pdf", key + ".xml"):
                    xmls[key].append(filename)
                elif name.startswith(key + "-") and not name.endswith(".xml"):
                    xmls[key].append(filename)
            filenames = list(set(filenames) - set(xmls[key]))

        with TemporaryDirectory() as tmpdirname:

            for key, files in xmls.items():

                zfile = os.path.join(tmpdirname, f"{key}.zip")
                with ZipFile(zfile, "w", compression=ZIP_DEFLATED) as zfw:
                    for item in files:
                        zfw.writestr(item, zf.read(item))

                with open(zfile, "rb") as zfw:
                    yield {"zipfilename": key + ".zip", "content": zfw.read()}


def get_xml_with_pre_from_uri(uri, timeout=30):
    try:
        response = fetch_data(uri, timeout=timeout)
        xml_with_pre = get_xml_with_pre(response.decode("utf-8"))
        xml_with_pre.uri = uri
        return xml_with_pre
    except Exception as e:
        raise GetXmlWithPreFromURIError(_("Unable to get xml from {}").format(uri))


def get_xml_with_pre(xml_content):
    try:
        # return etree.fromstring(xml_content)
        pref, xml = split_processing_instruction_doctype_declaration_and_xml(
            xml_content
        )
        try:
            return XMLWithPre(pref, etree.fromstring(xml))
        except etree.XMLSyntaxError as e:
            return XMLWithPre(pref, etree.fromstring(fix_pre_loading(xml)))
    except Exception as e:
        if xml_content:
            raise GetXmlWithPreError(
                "Unable to get xml with pre %s: %s ... %s"
                % (e, xml_content[:100], xml_content[-200:])
            )
        raise GetXmlWithPreError("Unable to get xml with pre %s" % e)


def split_processing_instruction_doctype_declaration_and_xml(xml_content):
    if not xml_content:
        return "", ""

    xml_content = xml_content.strip()
    if not xml_content:
        return "", ""

    if xml_content.endswith("</article>") or xml_content.endswith("<article/>"):
        p = xml_content.find("<article")
        if p >= 0:
            if ' xmlns="http://jats.nlm.nih.gov" ' in xml_content:
                xml_content = xml_content.replace('xmlns="http://jats.nlm.nih.gov"', "")
            return xml_content[:p], xml_content[p:]

    p = xml_content.rfind("<")
    if p >= 0:
        if xml_content.endswith("/>"):
            start = p + 1
            end = -2
        else:
            start = p + 2
            end = -1
        tag = xml_content[start:end]

        p = xml_content.find(f"<{tag}")
        if p >= 0:
            return xml_content[:p], xml_content[p:]

    return "", xml_content.strip()


class XMLWithPre:
    """
    Preserva o texto anterior ao elemento `root`
    """

    def __init__(self, xmlpre, xmltree, pretty_print=True):
        self.xmltree = xmltree
        self.xmlpre = xmlpre or ""

        # Parse DOCTYPE uma única vez durante init
        self.DOCTYPE = None
        self.public_id = None
        self.system_id = None
        if self.xmlpre and "<!DOCTYPE" in self.xmlpre:
            self.parse_doctype()

        self.pretty_print = pretty_print
        self.filename = None
        self.files = None
        self.filenames = None
        self.uri = None
        self.zip_file_path = None
        self.xml_file_path = None
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
    def create(
        cls, path=None, uri=None, xml_content=None, capture_errors=False, timeout=30
    ):
        """
        Returns instance of XMLWithPre

        path : str
            zip or XML file
        uri : str
            XML file URI
        """
        if path:
            errors = []
            xml_with_pre = None
            for item in get_xml_items(path, capture_errors):
                if not item:
                    continue
                try:
                    xml_with_pre = item["xml_with_pre"]
                    xml_with_pre.filename = item["filename"]
                    xml_with_pre.files = item.get("files")
                    xml_with_pre.filenames = item.get("filenames")
                    xml_with_pre.errors = item.get("error")
                    yield xml_with_pre
                except KeyError:
                    errors.append(item)
            if not xml_with_pre:
                raise GetXmlWithPreError("Unable to get xml with pre %s" % str(errors))
        if xml_content:
            yield get_xml_with_pre(xml_content)
        if uri:
            yield get_xml_with_pre_from_uri(uri, timeout)

    def parse_doctype(self):
        """
        Extrai informações do DOCTYPE de forma pythônica.

        Returns:
            DoctypeInfo com doctype, public_id e system_id
        """
        if not self.xmlpre or "<!DOCTYPE" not in self.xmlpre:
            return
        try:
            # Extrai DOCTYPE
            start = self.xmlpre.index("<!DOCTYPE")
            end = self.xmlpre.index(">", start) + 1
            self.DOCTYPE = self.xmlpre[start:end]

            # Parse dos IDs usando split
            parts = self.DOCTYPE.split('"')

            if "PUBLIC" in self.DOCTYPE and len(parts) >= 4:
                self.public_id = parts[1]
                self.system_id = (
                    parts[3] if parts[3].startswith(("http://", "https://")) else None
                )
                return

            if "SYSTEM" in self.DOCTYPE and len(parts) >= 2:
                self.system_id = (
                    parts[1] if parts[1].startswith(("http://", "https://")) else None
                )

        except (ValueError, IndexError):
            return

    @cached_property
    def sps_version(self):
        try:
            return self.xmltree.find(".").get("specific-use")
        except (AttributeError, TypeError, ValueError):
            return None

    def get_zip_content(self, xml_filename, pretty_print=False):
        zip_content = None
        with TemporaryDirectory() as tmpdirname:
            temp_zip_file_path = os.path.join(tmpdirname, f"{xml_filename}.zip")
            with ZipFile(temp_zip_file_path, "w", compression=ZIP_DEFLATED) as zf:
                zf.writestr(xml_filename, self.tostring(pretty_print=pretty_print))
            with open(temp_zip_file_path, "rb") as fp:
                zip_content = fp.read()
        return zip_content

    @cached_property
    def sps_pkg_name_suffix(self):
        if self.elocation_id:
            return self.elocation_id
        if self.sps_pkg_name_fpage:
            return self.sps_pkg_name_fpage
        if self.main_doi:
            doi = self.main_doi
            if "/" in doi:
                doi = doi[doi.rfind("/") + 1 :]
            return doi.replace(".", "-")

    @cached_property
    def sps_pkg_name_fpage(self):
        fpage = self.fpage
        if not fpage:
            return None
        try:
            if int(fpage) == 0:
                return None
        except (TypeError, ValueError):
            pass
        seq = self.fpage_seq
        if not seq:
            if self.lpage == fpage:
                seq = self.v2 and self.v2[-5:]
        if seq:
            return f"{fpage}_{seq}"
        return fpage

    @cached_property
    def alternative_sps_pkg_name_suffix(self):
        return self.order or self.filename

    @cached_property
    def sps_pkg_name(self):
        """Cache do nome do pacote SPS que é usado frequentemente"""
        xml_acron = Acronym(self.xmltree)
        parts = [
            self.journal_issn_electronic or self.journal_issn_print,
            xml_acron.text,
            self.volume,
            self.number and self.number.zfill(2),
            self.sps_pkg_name_suppl,
            self.sps_pkg_name_suffix or self.alternative_sps_pkg_name_suffix,
            self.additional_sps_pkg_name_suffix,
        ]
        return "-".join([part for part in parts if part])
    
    @property
    def sps_pkg_name_suppl(self):
        suppl = self.suppl
        if not suppl:
            return None
        try:
            if int(suppl) == 0:
                return "suppl"
        except (TypeError, ValueError):
            pass
        return f"s{suppl}"

    @cached_property
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
        ).decode("utf-8")

    def update_ids(self, v3, v2, aop_pid):
        """
        Atualiza todos os elementos article-id (v2, v3, aop_pid)
        """
        self.article_ids.v3 = v3
        self.article_ids.v2 = v2
        if aop_pid:
            self.article_ids.aop_pid = aop_pid

    @cached_property
    def related_items(self):
        return RelatedItems(self.xmltree).related_articles

    @cached_property
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
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "scielo-v3")
            parent = self.article_id_parent
            parent.insert(1, node)
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
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "previous-pid")
            parent = self.article_id_parent
            parent.insert(1, node)
        node.text = value

    @property
    def v2_prefix(self):
        return (
            f"S{self.journal_issn_electronic or self.journal_issn_print}{self.pub_year}"
        )

    @cached_property
    def article_doi_with_lang(self):
        # [{"lang": "en", "value": "DOI"}]
        return DoiWithLang(self.xmltree).data

    @cached_property
    def main_doi(self):
        # [{"lang": "en", "value": "DOI"}]
        return DoiWithLang(self.xmltree).main_doi

    @cached_property
    def main_toc_section(self):
        """
        <subj-group subj-group-type="heading">
            <subject>Articles</subject>
        </subj-group>
        """
        node = self.xmltree.find('.//subj-group[@subj-group-type="heading"]')
        if node is not None:
            return node.findtext("./subject")

    @cached_property
    def issns(self):
        # [{"type": "epub", "value": "1234-9876"}]
        return {item["type"]: item["value"] for item in ISSN(self.xmltree).data}

    @cached_property
    def is_aop(self):
        if self.volume:
            try:
                return int(self.volume) == 0
            except (ValueError, TypeError):
                return False
            return False
        if self.number:
            try:
                return int(self.number) == 0
            except (ValueError, TypeError):
                return False
            return False
        return True

    @cached_property
    def article_meta_issue(self):
        # artigos podem ser publicados sem estarem associados a um fascículo
        # Neste caso, não há volume, número, suppl, fpage, fpage_seq, lpage
        # Mas deve ter ano de publicação em qualquer caso
        return ArticleMetaIssue(self.xmltree)

    @cached_property
    def volume(self):
        return self.article_meta_issue.volume

    @cached_property
    def number(self):
        return self.article_meta_issue.number

    @cached_property
    def suppl(self):
        return self.article_meta_issue.suppl

    @cached_property
    def fpage(self):
        return self.article_meta_issue.fpage

    @cached_property
    def fpage_seq(self):
        return self.article_meta_issue.fpage_seq

    @cached_property
    def lpage(self):
        return self.article_meta_issue.lpage

    @cached_property
    def elocation_id(self):
        return self.article_meta_issue.elocation_id

    @cached_property
    def pub_year(self):
        return self.collection_pub_year or self.article_pub_year

    @cached_property
    def authors(self):
        authors_dict = {}
        names = []
        collab = None

        contrib_group = self.xmltree.find(".//article-meta//contrib-group")
        if contrib_group is not None:
            for item in contrib_group.xpath(".//surname"):
                content = " ".join(
                    [
                        text.strip()
                        for text in item.xpath(".//text()")
                        if (text or "").strip()
                    ]
                )
                names.append({"surname": content})

            for item in contrib_group.xpath(".//collab"):
                content = " ".join(
                    [
                        text.strip()
                        for text in item.xpath(".//text()")
                        if (text or "").strip()
                    ]
                )
                collab = content

        return {
            "person": names,
            "collab": collab,
        }

    @cached_property
    def article_titles(self):
        # list of dict which keys are lang and text
        xpath = "|".join(
            [
                ".//article-meta//article-title",
                ".//article-meta//trans-title",
                ".//front-stub//article-title",
                ".//front-stub//trans-title",
            ]
        )
        titles = []
        for item in self.xmltree.xpath(xpath):
            title = " ".join(
                [
                    text.strip()
                    for text in item.xpath(".//text()")
                    if text and text.strip()
                ]
            )
            titles.append(title)
        return sorted(titles)

    @cached_property
    def partial_body(self):
        try:
            body = Body(self.xmltree)
            for text in body.main_body_texts:
                if (text or "").strip():
                    return text
        except AttributeError:
            pass
        return None

    @cached_property
    def collab(self):
        return self.authors.get("collab")

    @cached_property
    def journal_title(self):
        return Title(self.xmltree).journal_title

    @cached_property
    def journal_issn_print(self):
        # list of dict which keys are
        # href, ext-link-type, related-article-type
        return self.issns.get("ppub")

    @cached_property
    def journal_issn_electronic(self):
        # list of dict which keys are
        # href, ext-link-type, related-article-type
        return self.issns.get("epub")

    def get_complete_publication_date(self, default_month=6, default_day=15):
        try:
            xml = ArticleDates(self.xmltree)
        except Exception as e:
            logging.exception(e)
            return None
        try:
            return xml.article_date_isoformat
        except Exception as e:
            data = xml.article_date
            return date(
                int(data["year"]),
                int(data.get("month") or default_month),
                int(data.get("day") or default_day),
            ).isoformat()
        return self.article_publication_date
    @property
    def article_publication_date(self):
        try:
            return ArticleDates(self.xmltree).article_date_isoformat
        except Exception as e:
            logging.exception(e)
            return self.pub_year

    @article_publication_date.setter
    def article_publication_date(self, value):
        """
        value : dict (keys: year, month, day)
        """
        try:
            if isinstance(value, str):
                parts = value.split("-")
                value = {
                    "day": parts[2],
                    "month": parts[1],
                    "year": parts[0],
                }
            formatted = format_date(**value)
        except Exception as e:
            raise XMLWithPreArticlePublicationDateError(
                f"Unable to set article_publication_date with {value}. Date with valid year, month, day is required"
            )

        try:
            node = self.xmltree.xpath(
                ".//article-meta//pub-date[@date-type='pub' or @pub-type='epub' or @pub-type='epub-ppub']"
            )[0]
            if node.get("pub-type") == "epub-ppub":
                node.set("pub-type", "collection")
                raise IndexError  # força criar novo nó pub-date (epub)
        except IndexError:
            node = etree.Element("pub-date")
            if self.xmltree.xpath(".//article-meta//pub-date[@pub-type]"):
                # mais antigo
                node.set("pub-type", "epub")
            else:
                # mais recente
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
            articlemeta_node = self.xmltree.find(".//article-meta")
            for sibling_name in pub_date_preceding_siblings:
                try:
                    articlemeta_node.find(sibling_name).addnext(node)
                    break
                except AttributeError:
                    continue

        previous = None
        for name, val in zip(("day", "month", "year"), reversed(formatted.split("-"))):
            elem = node.find(name)
            if elem is None:
                elem = etree.Element(name)
                if previous is None:
                    node.insert(0, elem)
                else:
                    previous.addnext(elem)
            elem.text = val
            previous = elem

    @property
    def article_pub_year(self):
        return ArticleDates(self.xmltree).article_year

    @cached_property
    def collection_pub_year(self):
        return ArticleDates(self.xmltree).collection_year

    @cached_property
    def article_titles_texts(self):
        return self.article_titles

    @property
    def finger_print(self):
        if self.xmltree.xpath(".//comment()"):
            for item in XMLWithPre.create(
                xml_content=self.tostring(pretty_print=self.pretty_print)
            ):
                remove_comments(item.xmltree)
                return generate_finger_print(item.tostring(pretty_print=True))
        else:
            return generate_finger_print(self.tostring(pretty_print=self.pretty_print))

    @cached_property
    def main_lang(self):
        return ArticleAndSubArticles(self.xmltree).main_lang

    @cached_property
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
            name = (
                self.sps_pkg_name + ".pdf"
                if item.is_main_language
                else f"{self.sps_pkg_name}-{item.language}.pdf"
            )
            yield {
                "name": name,
                "lang": item.language,
                "component_type": "rendition",
                "main": item.is_main_language,
            }

    def get_article_pid_suffix(self):
        return self.elocation_id or self.fpage or self.order or ""

    def generate_issue_pid_suffix(self):
        return str(self.generate_order()).zfill(4)

    def generate_order_for_supplement(self, suppl_start=1000):
        return suppl_start + extract_number(self.suppl)

    def generate_order_for_number(self, spe_start=2000):
        number = self.number
        if "spe" in number:
            part = number.split("spe")[-1]
            return spe_start + extract_number(part)
        if number == "ahead":
            return 9999
        return extract_number(number)

    def generate_order(self, suppl_start=1000, spe_start=2000):
        if self.suppl:
            return self.generate_order_for_supplement(suppl_start)
        if not self.number:
            return 1
        return self.generate_order_for_number(spe_start) or 1

    def generated_pid_v2(self, journal_pid=None, issue_pid=None):
        parts = ["S"]
        if issue_pid:
            parts.append(issue_pid)
        else:
            if journal_pid:
                parts.append(journal_pid)
            elif self.journal_issn_electronic:
                parts.append(self.journal_issn_electronic)
            elif self.journal_issn_print:
                parts.append(self.journal_issn_print)
            else:
                raise ValueError("Unable to generate pid v2: no journal_pid")
            parts.append(self.pub_year)
            parts.append(self.generate_issue_pid_suffix())

        parts.append(string_to_5_digits(self.get_article_pid_suffix()))
        if parts.count(None):
            raise ValueError(f"Unable to generate pid v2: {parts}")
        pid_v2 = "".join(parts)
        if len(pid_v2) == 23:
            return pid_v2
        raise ValueError(f"Unable to generate pid v2: {parts} {pid_v2}")


def string_to_5_digits(input_string):
    return (crc32(input_string.encode()) & 0xFFFFFFFF) % 100000


def extract_number(value):
    if not value:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        digits = "".join([c for c in value if c.isdigit()])
        return int(digits) if digits else 0


def generate_finger_print(content):
    if not content:
        return None
    if isinstance(content, str):
        content = content.upper()
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def remove_comments(xmltree):
    """
    Remove todos os nós de comentário de uma árvore XML.

    Args:
      root: O elemento raiz da árvore XML (lxml.etree._Element).
    """
    # Encontra todos os comentários na árvore
    comments_to_remove = xmltree.find(".").xpath("//comment()")

    # Itera sobre a lista de comentários e os remove
    for comment in comments_to_remove:
        parent = comment.getparent()
        if parent is not None:
            parent.remove(comment)
