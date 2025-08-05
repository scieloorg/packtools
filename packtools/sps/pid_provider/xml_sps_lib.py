import hashlib
import logging
import os
from datetime import date
from functools import lru_cache
from gettext import gettext as _
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree

from packtools.sps.libs.requester import fetch_data

# 4.7.1 packtools.sps.models.*
from packtools.sps.pid_provider.models.article_assets import ArticleAssets
from packtools.sps.pid_provider.models.article_and_subarticles import (
    ArticleAndSubArticles,
)
from packtools.sps.pid_provider.models.article_doi_with_lang import DoiWithLang
from packtools.sps.pid_provider.models.article_ids import ArticleIds
from packtools.sps.pid_provider.models.article_renditions import ArticleRenditions
from packtools.sps.pid_provider.models.body import Body
from packtools.sps.pid_provider.models.dates import ArticleDates
from packtools.sps.pid_provider.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.pid_provider.models.journal_meta import ISSN, Acronym, Title
from packtools.sps.pid_provider.models.related_articles import RelatedItems

LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class GetXmlWithPreError(Exception): ...


class GetXmlWithPreFromURIError(Exception): ...


class GetXMLItemsError(Exception): ...


class GetXMLItemsFromZipFileError(Exception): ...


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
            return get_xml_items_from_zip_file(
                xml_sps_file_path, filenames, capture_errors
            )
        if ext == ".xml":
            with open(xml_sps_file_path) as fp:
                xml = get_xml_with_pre(fp.read())
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

        raise TypeError(
            _("{} must be xml file or zip file containing xml").format(
                xml_sps_file_path
            )
        )
    except Exception as e:
        LOGGER.exception(e)
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


def get_xml_items_from_zip_file(
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
    filenames = None
    basenames = None
    try:
        with ZipFile(xml_sps_file_path) as zf:
            zip_files = zf.namelist()
            check_files = filenames or zip_files
            xml_files = (f for f in check_files if f.endswith(".xml"))

            if not xml_files:
                raise TypeError(f"{xml_sps_file_path} has no XML files")

            basenames = (os.path.basename(n) for n in zip_files if n)
            for xml_file in xml_files:
                try:
                    xml_with_pre = get_xml_with_pre(zf.read(xml_file).decode("utf-8"))
                    xml_with_pre.zip_file_path = xml_sps_file_path
                    yield {
                        "filename": xml_file,
                        "xml_with_pre": xml_with_pre,
                        "files": check_files,
                        "filenames": basenames,
                    }
                except Exception as e:
                    if not capture_errors:
                        LOGGER.exception(f"Error in {xml_sps_file_path}/{xml_file}")

                    yield {
                        "filename": xml_file,
                        "files": check_files,
                        "filenames": basenames,
                        "error": str(e),
                        "type_error": type(e).__name__,
                    }
    except Exception as e:
        LOGGER.exception(e)
        if not capture_errors:
            raise GetXMLItemsFromZipFileError(
                _("Unable to get xml items from zip file {}: {} {}").format(
                    xml_sps_file_path, type(e).__name__, e
                )
            )
        yield {
            "files": filenames,
            "filenames": basenames,
            "error": str(e),
            "type_error": type(e).__name__,
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
        return XMLWithPre(pref, etree.fromstring(xml))

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

    return "", xml_content


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
        if self.xmlpre and '<!DOCTYPE' in self.xmlpre:
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

            for item in get_xml_items(path, capture_errors):
                if not item:
                    continue

                xml_with_pre = item["xml_with_pre"]
                xml_with_pre.filename = item["filename"]
                xml_with_pre.files = item.get("files")
                xml_with_pre.filenames = item.get("filenames")
                xml_with_pre.errors = item.get("error") 
                yield xml_with_pre

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
        if not self.xmlpre or '<!DOCTYPE' not in self.xmlpre:
            return
        try:
            # Extrai DOCTYPE
            start = self.xmlpre.index('<!DOCTYPE')
            end = self.xmlpre.index('>', start) + 1
            self.DOCTYPE = self.xmlpre[start:end]
            
            # Parse dos IDs usando split
            parts = self.DOCTYPE.split('"')
            
            if 'PUBLIC' in self.DOCTYPE and len(parts) >= 4:
                self.public_id = parts[1]
                self.system_id = parts[3] if parts[3].startswith(('http://', 'https://')) else None
                return

            if 'SYSTEM' in self.DOCTYPE and len(parts) >= 2:
                self.system_id = parts[1] if parts[1].startswith(('http://', 'https://')) else None
                
        except (ValueError, IndexError):
            return

    @property
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

    @property
    def sps_pkg_name_suffix(self):
        if self.elocation_id:
            return self.elocation_id
        if self.fpage:
            try:
                if not int(self.fpage) == 0:
                    return self.fpage + (self.fpage_seq or "")
            except (TypeError, ValueError):
                return self.fpage + (self.fpage_seq or "")
        if self.main_doi:
            doi = self.main_doi
            if "/" in doi:
                doi = doi[doi.rfind("/") + 1 :]
            return doi.replace(".", "-")

    @property
    def alternative_sps_pkg_name_suffix(self):
        try:
            return self.v2[-5:]
        except TypeError:
            return self.filename

    @property
    @lru_cache(maxsize=1)
    def sps_pkg_name(self):
        """Cache do nome do pacote SPS que é usado frequentemente"""
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
        ).decode("utf-8")

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
    @lru_cache(maxsize=1)
    def article_doi_with_lang(self):
        # [{"lang": "en", "value": "DOI"}]
        return DoiWithLang(self.xmltree).data

    @property
    @lru_cache(maxsize=1)
    def main_doi(self):
        # [{"lang": "en", "value": "DOI"}]
        return DoiWithLang(self.xmltree).main_doi

    @property
    @lru_cache(maxsize=1)
    def main_toc_section(self):
        """
        <subj-group subj-group-type="heading">
            <subject>Articles</subject>
        </subj-group>
        """
        node = self.xmltree.find('.//subj-group[@subj-group-type="heading"]')
        if node is not None:
            return node.findtext("./subject")

    @property
    @lru_cache(maxsize=1)
    def issns(self):
        # [{"type": "epub", "value": "1234-9876"}]
        return {item["type"]: item["value"] for item in ISSN(self.xmltree).data}

    @property
    @lru_cache(maxsize=1)
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

    @property
    def xml_dates(self):
        # ("year", "month", "season", "day")
        return ArticleDates(self.xmltree)

    @property
    @lru_cache(maxsize=1)
    def article_meta_issue(self):
        # artigos podem ser publicados sem estarem associados a um fascículo
        # Neste caso, não há volume, número, suppl, fpage, fpage_seq, lpage
        # Mas deve ter ano de publicação em qualquer caso
        return ArticleMetaIssue(self.xmltree)

    @property
    @lru_cache(maxsize=1)
    def volume(self):
        return self.article_meta_issue.volume

    @property
    @lru_cache(maxsize=1)
    def number(self):
        return self.article_meta_issue.number

    @property
    @lru_cache(maxsize=1)
    def suppl(self):
        return self.article_meta_issue.suppl

    @property
    @lru_cache(maxsize=1)
    def fpage(self):
        return self.article_meta_issue.fpage

    @property
    @lru_cache(maxsize=1)
    def fpage_seq(self):
        return self.article_meta_issue.fpage_seq

    @property
    @lru_cache(maxsize=1)
    def lpage(self):
        return self.article_meta_issue.lpage

    @property
    @lru_cache(maxsize=1)
    def elocation_id(self):
        return self.article_meta_issue.elocation_id

    @property
    @lru_cache(maxsize=1)
    def pub_year(self):
        try:
            return (
                self.article_meta_issue.collection_date.get("year")
                or self.article_pub_year
            )
        except AttributeError:
            return None

    @property
    @lru_cache(maxsize=1)
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
                        if text.strip()
                    ]
                )
                names.append({"surname": content})

            for item in contrib_group.xpath(".//collab"):
                content = " ".join(
                    [
                        text.strip()
                        for text in item.xpath(".//text()")
                        if text.strip()
                    ]
                )
                collab = content

        return {
            "person": names,
            "collab": collab,
        }

    @property
    @lru_cache(maxsize=1)
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
                [text.strip() for text in item.xpath(".//text()") if text.strip()]
            )
            titles.append(title)
        return sorted(titles)

    @property
    @lru_cache(maxsize=1)
    def partial_body(self):
        try:
            body = Body(self.xmltree)
            for text in body.main_body_texts:
                if text:
                    return text
        except AttributeError:
            pass
        return None

    @property
    @lru_cache(maxsize=1)
    def collab(self):
        return self.authors.get("collab")

    @property
    @lru_cache(maxsize=1)
    def journal_title(self):
        return Title(self.xmltree).journal_title

    @property
    @lru_cache(maxsize=1)
    def journal_issn_print(self):
        # list of dict which keys are
        # href, ext-link-type, related-article-type
        return self.issns.get("ppub")

    @property
    @lru_cache(maxsize=1)
    def journal_issn_electronic(self):
        # list of dict which keys are
        # href, ext-link-type, related-article-type
        return self.issns.get("epub")

    @property
    def article_publication_date(self):
        # ("year", "month", "season", "day")
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
                return f"{_date['year']}-{_date['month'].zfill(2)}-{_date['day'].zfill(2)}"
        return None

    @article_publication_date.setter
    def article_publication_date(self, value):
        """
        value : dict (keys: year, month, day)
        """
        try:
            node = self.xmltree.xpath(".//article-meta//pub-date[@date-type='pub']")[0]
        except IndexError:
            try:
                node = self.xmltree.xpath(
                    ".//article-meta//pub-date[@pub-type='epub']"
                )[0]
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
        # ("year", "month", "season", "day")
        try:
            return self.xml_dates.article_date["year"]
        except (ValueError, TypeError, KeyError) as e:
            return self.pub_year

    @property
    @lru_cache(maxsize=1)
    def article_titles_texts(self):
        return self.article_titles

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


def generate_finger_print(content):
    if not content:
        return None
    if isinstance(content, str):
        content = content.upper()
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()
