import hashlib
import logging
import os
import re
import traceback
from datetime import date
from functools import cached_property
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


class XMLWithPreMissingISSNError(Exception): ...


class GetXmlWithPreError(Exception): ...


class GetXmlWithPreFromURIError(Exception): ...


class GetXMLItemsError(Exception): ...


class GetXMLWithPreFromZipFileError(Exception): ...


def get_xml_items(xml_sps_file_path):
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
            return get_xml_with_pre_from_zip_file(xml_sps_file_path)
        if ext == ".xml":
            return [get_xml_with_pre_from_xml_file(xml_sps_file_path)]
        raise TypeError(
            _("{} must be xml file or zip file containing xml").format(
                xml_sps_file_path
            )
        )
    except Exception as e:
        raise GetXMLItemsError(
            _("Unable to get xml items from {}: {} {}").format(
                xml_sps_file_path, type(e), e
            )
        )


def get_xml_with_pre_from_xml_file(xml_sps_file_path):
    xml_name, ext = os.path.splitext(os.path.basename(xml_sps_file_path))
    try:
        try:
            content = None
            with open(xml_sps_file_path, encoding="utf-8") as fp:
                content = fp.read()
        except Exception as e:
            with open(xml_sps_file_path, encoding="iso-8859-1") as fp:
                content = fp.read()
        xml_with_pre = get_xml_with_pre(content)
        xml_with_pre.add_xml_info(xml_name, xml_sps_file_path)
        return {"xml_name": xml_name, "xml_with_pre": xml_with_pre}
    except Exception as e:
        return {
            "xml_name": xml_name,
            "error_message": str(e),
            "error_type": str(type(e)),
            "traceback": traceback.format_exc(),
        }


def get_xml_with_pre_from_zip_file(xml_sps_file_path):
    try:
        # Extração dos arquivos do ZIP
        xml_with_pre_items = []
        paths = []
        basenames = []
        items = {}
        with ZipFile(xml_sps_file_path) as zf:
            for item in zf.namelist():
                if item.startswith("."):
                    continue
                basename = os.path.basename(item)
                if not basename.endswith(".xml"):
                    paths.append(item)
                    basenames.append(basename)
                    continue

                xml_name, ext = os.path.splitext(basename)
                try:
                    zf_read = zf.read(item)
                    try:
                        content = zf_read.decode("utf-8")
                    except Exception as e:
                        content = zf_read.decode("iso-8859-1")
                    xml_with_pre = get_xml_with_pre(content)
                    xml_with_pre.add_xml_info(xml_name, item)
                    xml_with_pre_items.append(xml_with_pre)
                except Exception as e:
                    items[xml_name] = {
                        "xml_name": xml_name,
                        "error_message": str(e),
                        "error_type": str(type(e)),
                        "traceback": traceback.format_exc(),
                    }
        for xml_with_pre in xml_with_pre_items:
            xml_name = xml_with_pre.xml_name
            xml_with_pre.add_zip_info(xml_sps_file_path, paths, basenames)
            items[xml_with_pre.xml_name] = {
                "xml_name": xml_name,
                "xml_with_pre": xml_with_pre,
            }
        return list(items.values())
    except Exception as e:
        raise GetXMLWithPreFromZipFileError(
            _("Unable to get xml items from zip file {}: {} {}").format(
                xml_sps_file_path, type(e).__name__, e
            )
        )


def get_xml_items_from_zip_file(
    xml_sps_file_path,
    filenames=None,
):
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


def fix_number(value):
    """Converte zeros para None"""
    if not value:
        return None

    try:
        if int(value) == 0:
            return None
        return value
    except (TypeError, ValueError):
        # Valor não é numérico, retorna como está
        return value


# ==============================================================================
# 1. PARSER DE DOCTYPE
# ==============================================================================
class DOCTYPEParserMixin:
    """Gerencia o parsing e extração de informações do DOCTYPE."""

    def parse_doctype(self):
        """
        Extrai informações do DOCTYPE de forma pythônica.
        Atualiza self.DOCTYPE, self.public_id e self.system_id.
        """
        if not getattr(self, "xmlpre", None) or "<!DOCTYPE" not in self.xmlpre:
            return
        try:
            start = self.xmlpre.index("<!DOCTYPE")
            end = self.xmlpre.index(">", start) + 1
            self.DOCTYPE = self.xmlpre[start:end]

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


# ==============================================================================
# 2. GESTÃO DE ARQUIVOS, ZIPS E COMPONENTES
# ==============================================================================
class PackagingAndFilesMixin:
    """Propriedades e métodos relacionados a arquivos, zips, assets e renditions."""

    # --------------------------------------------------------------------------
    # Aliases e Setters/Getters para Retrocompatibilidade
    # --------------------------------------------------------------------------
    @property
    def filename(self):
        return self.xml_name

    @filename.setter
    def filename(self, value):
        self.xml_name = value

    @property
    def files(self):
        return self.zip_namelist

    @files.setter
    def files(self, value):
        self.zip_namelist = value

    @property
    def filenames(self):
        return self.zip_basenames

    @filenames.setter
    def filenames(self, value):
        self.zip_basenames = value

    @property
    def source_filename(self):
        return self._submitted_filename

    @source_filename.setter
    def source_filename(self, value):
        self.submitted_filename = value

    @property
    def source_ext(self):
        return self._submitted_ext

    @source_ext.setter
    def source_ext(self, value):
        self._submitted_ext = value

    @property
    def submitted_filename(self) -> str:
        if self._submitted_filename:
            return f"{self._submitted_filename}{self._submitted_ext}"

    @submitted_filename.setter
    def submitted_filename(self, value: str):
        """Atribui o nome submetido e extrai/separa a extensão automaticamente."""
        if not value:
            self._submitted_filename = None
            self._submitted_ext = None
            return

        self._submitted_filename, ext = os.path.splitext(value)
        if ext:
            self._submitted_ext = ext.lower()
        self.is_html_source = bool(self.is_html_source or self.submitted_ext in [".html", ".htm"])

    @property
    def submitted_ext(self) -> str:
        """Extensão do arquivo submetido (ex: '.html', '.xml')."""
        if self._submitted_ext:
            return self._submitted_ext

    # --------------------------------------------------------------------------
    # Métodos Mutadores de Informações do Pacote
    # --------------------------------------------------------------------------
    def add_xml_info(self, xml_name, xml_file_path=None):
        self.xml_name = xml_name
        self.xml_file_path = xml_file_path

    def add_zip_info(self, zip_file_path, zip_namelist, zip_basenames):
        self.zip_basenames = zip_basenames
        self.zip_namelist = zip_namelist
        self.zip_file_path = zip_file_path

    def add_pkg_name_components(self, source_filename, pkg_name_version=3):
        self.pkg_name_version = pkg_name_version
        self.submitted_filename = source_filename
        if source_filename and source_filename.endswith(".xml"):
            self.provided_sps_pkg_name = source_filename[:-4]  # Remove .xml extension

    def get_zip_content(self, xml_filename, pretty_print=False):
        zip_content = None
        with TemporaryDirectory() as tmpdirname:
            temp_zip_file_path = os.path.join(tmpdirname, f"{xml_filename}.zip")
            with ZipFile(temp_zip_file_path, "w", compression=ZIP_DEFLATED) as zf:
                zf.writestr(xml_filename, self.tostring(pretty_print=pretty_print))
            with open(temp_zip_file_path, "rb") as fp:
                zip_content = fp.read()
        return zip_content

    # --------------------------------------------------------------------------
    # Componentes, Assets e Renditions
    # --------------------------------------------------------------------------
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


# ==============================================================================
# 3. NOMEAÇÃO DO PACOTE
# ==============================================================================
class LegacyPackageNamingMixin:
    """Regras de montagem do sps_pkg_name e suas variações históricas/deprecated."""

    @cached_property
    def legacy_sps_pkg_name_suffix(self):
        if self.elocation_id:
            return self.elocation_id
        if self.legacy_sps_pkg_name_fpage:
            return self.legacy_sps_pkg_name_fpage
        if self.main_doi:
            doi = self.main_doi
            if "/" in doi:
                doi = doi[doi.rfind("/") + 1 :]
            return doi.replace(".", "-")

    @cached_property
    def legacy_sps_pkg_name_fpage(self):
        fpage = fix_number(self.fpage)
        if not fpage:
            return None
        seq = self.fpage_seq
        if not seq:
            if self.lpage == fpage:
                seq = self.v2 and self.v2[-5:]
        if seq:
            return f"{fpage}_{seq}"
        return fpage

    @cached_property
    def deprecated_sps_pkg_name_fpage(self):
        fpage = fix_number(self.fpage)
        if not fpage:
            return None
        seq = self.fpage_seq or ""
        return f"{fpage}{seq}"

    @cached_property
    def legacy_alternative_sps_pkg_name_suffix(self):
        return self.order or self.filename

    def legacy_get_pkg_name_prefix(self, suppl):
        parts = [
            self.journal_issn_electronic or self.journal_issn_print,
            self.journal_acron,
            self.volume,
            self.number and self.number.zfill(2),
            suppl,
        ]
        return "-".join([part for part in parts if part])

    def legacy_get_pkg_name_suffix(self):
        parts = [
            self.elocation_id,
            self.fpage,
            self.fpage_seq,
            self.lpage,
            self.order or (self.v2 and self.v2[-5:]),
            self.source_filename,
        ]
        if not parts:
            raise ValueError("Unable to get pkg name suffix. No valid parts found.")
        return "_".join([part for part in parts if part])

    @cached_property
    def deprecated_sps_pkg_name_version_3(self):
        """Nome ficou muito diferente do que guia sps requer"""               
        if self.source_ext == ".xml":
            return self.source_filename

        parts = [
            self.legacy_get_pkg_name_prefix(suppl=self.sps_pkg_name_suppl),
            self.legacy_get_pkg_name_suffix(),
        ]
        return "-".join([part for part in parts if part])

    @cached_property
    def deprecated_sps_pkg_name_version_2(self):
        """Problema com o sufixo - número de páginas se repete por erro humano, usar mais dados para desambiguar."""
        parts = [
            self.legacy_get_pkg_name_prefix(suppl=self.sps_pkg_name_suppl),
            self.legacy_sps_pkg_name_suffix or self.legacy_alternative_sps_pkg_name_suffix,
        ]
        return "-".join([part for part in parts if part])

    @cached_property
    def deprecated_sps_pkg_name(self):
        """Tinha defeito na parte referente ao suppl (ausente o 's' antes do número)."""
        parts = [
            self.legacy_get_pkg_name_prefix(suppl=self.incorrect_sps_pkg_name_suppl),
            self.legacy_sps_pkg_name_suffix or self.legacy_alternative_sps_pkg_name_suffix,
        ]
        return "-".join([part for part in parts if part])

    @cached_property
    def deprecated_sps_pkg_name_list(self):
        return [
            self.deprecated_sps_pkg_name,
            self.deprecated_sps_pkg_name_version_2,
            self.deprecated_sps_pkg_name_version_3,
        ]

    @property
    def incorrect_sps_pkg_name_suppl(self):
        suppl = self.suppl
        if not suppl:
            return None
        try:
            if int(suppl) == 0:
                return "suppl"
        except (TypeError, ValueError):
            pass
        return suppl

    @property
    def sps_pkg_name_suppl(self):
        suppl = self.incorrect_sps_pkg_name_suppl
        if not suppl or suppl == "suppl":
            return suppl
        return f"s{suppl}"


class PackageNamingMixin:
    """
    Mixin para gerenciamento transparente e desacoplado da nomenclatura de pacotes.
    """
    # -------------------------------------------------------------------------
    # HIGIENIZAÇÃO SPS ESTREITA
    # -------------------------------------------------------------------------
    def get_fpage_for_pkg_name_suffix(self):
        """
        xml nativo: fpage pode ser usada para desambiguar, pois forma o nome do pacote,
        html: fpage não é confiável, pois o order ou o submitted_file são usados no nome do pacote,
        fpage pode gerar ambiguidade
        """
        if not self.fpage:
            return None
        if not self.order:
            return None
        order = str(int(self.order))
        if order == self.fpage:
            return self.fpage
        return self.order

    def get_fpage_suffix(self) -> str:
        """
        Calcula o sufixo de paginação combinando fpage + fpage_seq SEM separador.
        Retorna None se for detectado fpage 'fake'.
        Exemplo válido: fpage='365', fpage_seq='a' -> '365a'
        """
        fpage = self.get_fpage_for_pkg_name_suffix()
        if not fpage:
            return None

        seq = self.fpage_seq or ""
        return f"{fpage}{seq}"

    def get_page_suffix(self) -> str:
        """
        Calcula o sufixo de paginação combinando fpage + fpage_seq SEM separador.
        Retorna None se for detectado fpage 'fake'.
        Exemplo válido: fpage='365', fpage_seq='a' -> '365a'
        """
        fpage = self.get_fpage_for_pkg_name_suffix()
        if not fpage:
            return None

        seq = self.fpage_seq or ""
        lpage = self.lpage and f"-{self.lpage}" or ""
        return f"{fpage}{seq}{lpage}"

    def get_main_doi_for_pkg_name_suffix(self) -> str:
        """
        Retorna o sufixo do DOI principal (após a barra) para uso no nome do pacote.
        Exemplo: '10.1234/abcd.efgh' -> 'abcd.efgh'
        """
        main_doi = self.main_doi
        if not main_doi or "/" not in main_doi:
            return None
        return main_doi.split("/")[-1]

    def get_body_fragment_for_pkg_name_suffix(self) -> str:
        """
        Gera um fragmento de hash do corpo do artigo para uso no nome do pacote.
        Útil quando outros identificadores não estão disponíveis.
        """
        body_content = self.get_body_fragment(max_length=300)
        if not body_content:
            return None
        # Gerar um hash MD5 do conteúdo do corpo e retornar os primeiros 8 caracteres
        return hashlib.md5(body_content.encode("utf-8").lower()).hexdigest()[:8]

    def get_submitted_filename_for_pkg_name_suffix(self) -> str:
        """
        Retorna o nome do arquivo submetido (sem extensão) para uso no nome do pacote.
        Útil quando outros identificadores não estão disponíveis.
        """
        if not self.submitted_filename:
            return None
        return self._submitted_filename.lower()

    def get_lang_suffix(self, lang):
        lang_suffix = ""
        main_lang = getattr(self, "main_lang", "")
        if lang and main_lang and lang.lower() != main_lang.lower():
            lang_suffix = f"-{lang.lower()}"
        return lang_suffix

    def get_suppl_for_pkg_name_suffix(self):
        """
        Retorna o sufixo do pacote SPS para suplementos:
        'suppl' para valor 0
        's{valor}' para valores diferentes de 0
        """
        suppl = self.suppl
        if suppl is None:
            return None
        try:
            if int(suppl) == 0:
                return "suppl"
        except (TypeError, ValueError):
            pass
        return f"s{suppl}"

    # -------------------------------------------------------------------------
    # RESOLUÇÃO DE SUFIXO (Estratégias Sequenciais)
    # -------------------------------------------------------------------------
    def get_pkg_suffix(self, strategies: list = None) -> str:
        """
        Avalia a lista ordenada de estratégias e retorna o PRIMEIRO dado válido.

        Estratégias suportadas:
        - 'elocation_id': ID de localização eletrônica
        - 'fpage': fpage + fpage_seq (desconsiderando fpage fake)
        - 'page': fpage + fpage_seq + lpage (desconsiderando fpage fake)
        - 'order': Ordem do artigo
        - 'body_fragment': usando body_fragment_fingerprint
        - 'submitted_filename': Nome do arquivo enviado pelo produtor
        - 'doi_suffix': Sufixo após a barra do DOI
        """
        if not strategies:
            strategies = [
                "elocation_id",
                "submitted_filename",
                "order",
                "fpage",
                "page",
                "body_fragment",
                "doi_suffix",
            ]

        for strategy in strategies:
            val = None
            if strategy == "elocation_id":
                val = self.elocation_id
            elif strategy == "order":
                val = getattr(self, "order", None)
            elif strategy == "fpage":
                val = self.get_fpage_suffix()
            elif strategy == "page":
                val = self.get_page_suffix()
            elif strategy == "submitted_filename":
                val = self.get_submitted_filename_for_pkg_name_suffix()
            elif strategy == "doi_suffix":
                 val = self.get_main_doi_for_pkg_name_suffix()
            elif strategy == "body_fragment":
                val = self.get_body_fragment_for_pkg_name_suffix()
            if val:
                sanitized = sanitize_name(val)
                if sanitized:
                    return sanitized

        raise ValueError(
            f"Unable to get pkg name suffix. No valid strategy produced a value. Strategies tried: {strategies}"
        )

    # -------------------------------------------------------------------------
    # RESOLUÇÃO DE PREFIXO
    # -------------------------------------------------------------------------
    @cached_property
    def sps_issue_segment(self):
        """
        Segmento volume-número-suplemento, usado por XMLNamingMixin.get_sps_prefix
        para montar variações genéricas de nome (matching ORM).
        """
        parts = [
            self.volume,
            self.number and self.number.zfill(2),
            self.get_suppl_for_pkg_name_suffix(),
        ]
        if not any(parts):
            parts = [self.pub_year]
        return "-".join(p for p in parts if p)

    def get_sps_prefix(self, issn: str = None) -> str:
        """Gera o prefixo determinístico: ISSN-Acrônimo-Volume-Número-Suplemento."""
        chosen_issn = issn or self.sps_issn
        if not chosen_issn:
            raise ValueError(
                "Unable to get SPS prefix. No ISSN available. Provide an ISSN or ensure the XML has a valid journal_issn_electronic or journal_issn_print."
            )
        if not self.journal_acron:
            raise ValueError(
                "Unable to get SPS prefix. No journal acronym available. Ensure the XML has a valid journal_acron."
            )
        if not self.sps_issue_segment:
            raise ValueError(
                "Unable to get SPS prefix. No issue segment available. Ensure the XML has valid volume, number, and/or suppl."
            )
        prefix_parts = [
            chosen_issn,
            self.journal_acron,
            self.sps_issue_segment,
        ]
        return "-".join([p for p in prefix_parts if p])

    # -------------------------------------------------------------------------
    # CONSTRUTOR DE PACOTES
    # -------------------------------------------------------------------------
    def build_pkg_name(self, suffix: str, prefix: str = None, lang: str = None) -> str:
        """Junta o prefixo fornecido/gerado com o sufixo e idioma secundário."""
        if not suffix:
            raise ValueError("Suffix is required to build package name.")
        base_prefix = prefix or self.get_sps_prefix()
        lang_suffix = self.get_lang_suffix(lang)
        return sanitize_name(f"{base_prefix}-{suffix}{lang_suffix}")

    # -------------------------------------------------------------------------
    # CONVENÇÕES PADRÃO
    # -------------------------------------------------------------------------
    def build_sps_pkg_name(self, lang: str = None, issn: str = None) -> str:
        """Gera o nome do pacote no padrão SPS utilizando a busca de sufixo padrão."""
        prefix = self.get_sps_prefix(issn=issn)
        suffix = self.get_pkg_suffix(
            strategies=["elocation_id", "order", "submitted_filename"]
        )
        return sanitize_sps_name(self.build_pkg_name(suffix=suffix, prefix=prefix, lang=lang))

    def get_pmc_pkg_name(self, revision_number=None) -> str:
        """Gera o nome do pacote no padrão PMC (jour-vol-iss-uid)."""
        acron = getattr(self, "journal_acron", None) or "jour"
        vol = getattr(self, "volume", None) or "0"
        iss = getattr(self, "number", None) or "0"
        uid = self.get_pkg_suffix(
            strategies=["elocation_id", "fpage", "order", "uid"]
        )
        revision = ""
        if revision_number:
            revision = f".r{revision_number}"
        return sanitize_name(f"{acron}-{vol}-{iss}-{uid}{revision}")

    # -------------------------------------------------------------------------
    # VARIAÇÕES PARA DJANGO ORM E VISÃO DICTIONARY
    # -------------------------------------------------------------------------
    @property
    def pkg_name_variations(self) -> list:
        """
        Retorna TODAS as variações de nomes para buscas de match no Django ORM.
        Considera ISSN eletrônico, impresso, originais e traduções.
        """
        variations = set()

        if self.submitted_filename:
            variations.add(self.submitted_filename)

        for issn in self.available_issns:
            try:
                variations.add(self.build_sps_pkg_name(issn=issn))
            except ValueError:
                pass

        variations.update(self.deprecated_sps_pkg_name_list)

        try:
            variations.add(self.built_sps_pkg_name)
        except ValueError:
            pass

        if provided_sps_pkg_name := self.provided_sps_pkg_name:
            variations.add(provided_sps_pkg_name)
        if self.xml_name:
            variations.add(self.xml_name)
        return variations

    @property
    def built_sps_pkg_name(self) -> str:
        """Retorna o nome do pacote SPS construído com base nas regras atuais."""
        return self._built_sps_pkg_name

    @built_sps_pkg_name.setter
    def built_sps_pkg_name(self, value):
        self._built_sps_pkg_name = value

    @property
    def provided_sps_pkg_name(self) -> str:
        """Retorna o nome do pacote SPS fornecido no XML, se presente."""
        return self._provided_sps_pkg_name

    @provided_sps_pkg_name.setter
    def provided_sps_pkg_name(self, value):
        if not value:
            self._provided_sps_pkg_name = None
            return
        # não sanitizar, pois pode ser nome legado
        self._provided_sps_pkg_name = value

    def set_sps_pkg_data(self):
        if self._sps_pkg_name_origin and self._sps_pkg_name:
            return
        if name := self.provided_sps_pkg_name:
            self._sps_pkg_name_origin = "provided_sps_pkg_name"
            self._sps_pkg_name = name
            return
        if name := self.built_sps_pkg_name:
            self._sps_pkg_name_origin = "built_sps_pkg_name"
            self._sps_pkg_name = name
            return
        if name := self.xml_name:
            self._sps_pkg_name_origin = "xml_name"
            self._sps_pkg_name = name
            return
        # comportamento defensivo em caso de não ajuste no upload / core
        # versão mais compatível com o guia sps 1.10
        self._sps_pkg_name_origin = "deprecated_sps_pkg_name_version_2"
        self._sps_pkg_name = self.deprecated_sps_pkg_name_version_2

    @property
    def sps_pkg_name(self):
        if not self._sps_pkg_name_origin or not self._sps_pkg_name:
            self.set_sps_pkg_data()
        return self._sps_pkg_name

    @property
    def sps_pkg_name_origin(self):
        if not self._sps_pkg_name_origin or not self._sps_pkg_name:
            self.set_sps_pkg_data()
        return self._sps_pkg_name_origin

    @property
    def pkg_names_dict(self) -> dict:
        """Panorama estruturado dos nomes do documento."""
        return {
            "pmc_pkg_name": self.get_pmc_pkg_name(),
            "built_sps_pkg_name": self.built_sps_pkg_name,
            "provided_sps_pkg_name": self.provided_sps_pkg_name,
            "sps_pkg_name": self.sps_pkg_name,
            "sps_pkg_name_origin": self.sps_pkg_name_origin,
            "pkg_name_list": self.pkg_name_variations,}

    @property
    def sps_pkg_names_dict(self):
        return {
            "sps_pkg_name": self.sps_pkg_name,
            "sps_pkg_name_origin": self.sps_pkg_name_origin,
            "pkg_name_list": self.pkg_name_variations,
            "built_sps_pkg_name": self.built_sps_pkg_name,
            "built_sps_pkg_name_now": self.build_sps_pkg_name(),
            "provided_sps_pkg_name": self.provided_sps_pkg_name,
        }

    @property
    def input_files_dict(self):
        return {
            "xml_name": self.xml_name,
            "zip_namelist": self.zip_namelist,
            "zip_basenames": self.zip_basenames,
            "zip_file_path": self.zip_file_path,
            "xml_file_path": self.xml_file_path,
            "submitted_filename": self.submitted_filename,
            "submitted_ext": self.submitted_ext,
            "is_html": self.is_html_source,
            "provided_sps_pkg_name": self.provided_sps_pkg_name,
        }


# ==============================================================================
# 4. IDENTIFICADORES (PIDs: v2, v3, aop_pid, order)
# ==============================================================================
class IdentifiersMixin:
    """Manipulação e geração de IDs SciELO (article-id)."""

    @cached_property
    def article_id_parent(self):
        """Retorna o nó pai dos elementos article-id."""
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

    @property
    def article_ids(self):
        return ArticleIds(self.xmltree)

    @property
    def v3(self):
        return self.article_ids.v3

    @v3.setter
    def v3(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                f"can't set attribute XMLWithPre.v3. Expected value must have 23 characters. Got: {value}"
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

    @property
    def v2(self):
        return self.article_ids.v2

    @v2.setter
    def v2(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                f"can't set attribute XMLWithPre.v2. Expected value must have 23 characters. Got: {value}"
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

    @property
    def aop_pid(self):
        return self.article_ids.aop_pid

    @aop_pid.setter
    def aop_pid(self, value):
        value = value and value.strip()
        if not value or len(value) != 23:
            raise ValueError(
                f"can't set attribute XMLWithPre.aop_pid. Expected value must have 23 characters. Got: {value}"
            )
        try:
            node = self.xmltree.xpath(
                './/article-id[@specific-use="previous-pid" and @pub-id-type="publisher-id"]'
            )[0]
        except IndexError:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "previous-pid")
            parent = self.article_id_parent
            parent.insert(1, node)
        node.text = value

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
                f"can't set attribute XMLWithPre.order. Expected value must a 5 characters digit. Got: {value}"
            )
        try:
            node = self.xmltree.xpath('.//article-id[@pub-id-type="other"]')[0]
        except IndexError:
            node = etree.Element("article-id")
            node.set("pub-id-type", "other")
            parent = self.article_id_parent
            parent.insert(1, node)
        node.text = new_value

    def update_ids(self, v3, v2, aop_pid):
        """Atualiza todos os elementos article-id (v2, v3, aop_pid)."""
        self.article_ids.v3 = v3
        self.article_ids.v2 = v2
        if aop_pid:
            self.article_ids.aop_pid = aop_pid

    # --------------------------------------------------------------------------
    # Suporte a Múltiplos PIDs v2 (v2_list)
    # --------------------------------------------------------------------------
    @property
    def v2_list(self):
        items = []
        for node in self.xmltree.xpath('.//article-id[@specific-use="scielo-v2"]'):
            items.append(
                {
                    "assigning-authority": node.get("assigning-authority"),
                    "pid": node.text,
                }
            )
        return items

    @v2_list.setter
    def v2_list(self, items):
        if not items:
            return
        for item in items:
            item = item or {}
            self._set_v2_item(item.get("assigning-authority"), item.get("pid"))

    def _set_v2_item(self, assigning_authority, pid):
        pid = pid and pid.strip()
        if not pid or len(pid) != 23:
            raise ValueError(
                f"can't set attribute XMLWithPre.v2_list. Expected pid value must have 23 characters. Got: {pid}"
            )
        if assigning_authority:
            matches = self.xmltree.xpath(
                './/article-id[@specific-use="scielo-v2" and @assigning-authority=$aa]',
                aa=assigning_authority,
            )
        else:
            matches = self.xmltree.xpath(
                './/article-id[@specific-use="scielo-v2" and not(@assigning-authority)]'
            )
        try:
            node = matches[0]
        except IndexError:
            node = etree.Element("article-id")
            node.set("pub-id-type", "publisher-id")
            node.set("specific-use", "scielo-v2")
            if assigning_authority:
                node.set("assigning-authority", assigning_authority)
            parent = self.article_id_parent
            existing_article_ids = parent.findall("article-id")
            if existing_article_ids:
                existing_article_ids[-1].addnext(node)
            else:
                parent.insert(0, node)
        node.text = pid

    # --------------------------------------------------------------------------
    # Algoritmo de Geração Dinâmica de PID v2
    # --------------------------------------------------------------------------
    @property
    def v2_prefix(self):
        return f"S{self.journal_issn_electronic or self.journal_issn_print}{self.pub_year}"

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


# ==============================================================================
# 5. METADADOS DO ARTIGO (Datas, Títulos, Autores, Corpo, Periódico)
# ==============================================================================
class ArticleMetadataMixin:
    """Extração e manipulação de metadados do artigo JATS."""

    # --------------------------------------------------------------------------
    # Periódico & Seções
    # --------------------------------------------------------------------------
    @cached_property
    def journal_acron(self):
        return Acronym(self.xmltree).text

    @cached_property
    def journal_title(self):
        return Title(self.xmltree).journal_title

    @cached_property
    def issns(self):
        return {item["type"]: item["value"] for item in ISSN(self.xmltree).data}

    @cached_property
    def journal_issn_print(self):
        return self.issns.get("ppub")

    @cached_property
    def journal_issn_electronic(self):
        return self.issns.get("epub")

    @property
    def available_issns(self) -> list:
        """
        Retorna a lista de ISSNs disponíveis (eletrônico e impresso).

        Raises
        ------
        XMLWithPreMissingISSNError: Se nenhum ISSN for encontrado no XML.
        """
        issns = [item for item in self.issns.values() if item]
        if not issns:
            raise XMLWithPreMissingISSNError(
                f"Não foi possível determinar o nome do pacote para o arquivo '{self}': "
                f"Nenhum ISSN (eletrônico ou impresso) foi encontrado no XML."
            )
        return issns

    @property
    def sps_issn(self) -> str:
        """Retorna o ISSN principal (eletrônico priorizado, ou primeiro disponível)."""
        return self.available_issns[0]

    @cached_property
    def main_toc_section(self):
        node = self.xmltree.find('.//subj-group[@subj-group-type="heading"]')
        if node is not None:
            return node.findtext("./subject")

    # --------------------------------------------------------------------------
    # Fascículo / Edição
    # --------------------------------------------------------------------------
    @cached_property
    def article_meta_issue(self):
        return ArticleMetaIssue(self.xmltree)

    @cached_property
    def is_aop(self):
        return not (self.volume or self.number)

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

    # --------------------------------------------------------------------------
    # Datas de Publicação
    # --------------------------------------------------------------------------
    @property
    def _article_dates(self):
        return ArticleDates(self.xmltree)

    @cached_property
    def pub_year(self):
        return self.collection_pub_year or self.article_pub_year

    @property
    def article_pub_year(self):
        return self._article_dates.article_year

    @cached_property
    def collection_pub_year(self):
        return self._article_dates.collection_year

    @property
    def article_publication_date(self):
        try:
            return self._article_dates.article_date_isoformat
        except Exception:
            return self.pub_year

    @article_publication_date.setter
    def article_publication_date(self, value):
        try:
            if isinstance(value, str):
                parts = value.split("-")
                value = {"day": parts[2], "month": parts[1], "year": parts[0]}
            formatted = format_date(**value)
        except Exception:
            raise XMLWithPreArticlePublicationDateError(
                f"Unable to set article_publication_date with {value}. Date with valid year, month, day is required"
            )

        try:
            node = self.xmltree.xpath(
                ".//article-meta//pub-date[@date-type='pub' or @pub-type='epub' or @pub-type='epub-ppub']"
            )[0]
            if node.get("pub-type") == "epub-ppub":
                node.set("pub-type", "collection")
                raise IndexError
        except IndexError:
            node = etree.Element("pub-date")
            if self.xmltree.xpath(".//article-meta//pub-date[@pub-type]"):
                node.set("pub-type", "epub")
            else:
                node.set("date-type", "pub")
                node.set("publication-format", "electronic")

            pub_date_preceding_siblings = (
                "pub-date", "author-notes", "aff", "contrib-group",
                "title-group", "article-categories", "article-version-alternatives",
                "article-version", "article-id",
            )
            articlemeta_node = self.xmltree.find(".//article-meta")
            added = False
            for sibling_name in pub_date_preceding_siblings:
                try:
                    articlemeta_node.find(sibling_name).addnext(node)
                    added = True
                    break
                except AttributeError:
                    continue
            if not added:
                pub_date_following_siblings = (
                    "volume", "volume-id", "volume-series", "issue", "issue-id",
                    "issue-title", "issue-title-group", "issue-sponsor", "issue-part",
                    "volume-issue-group", "isbn", "supplement", "fpage", "lpage",
                    "page-range", "elocation-id", "email", "ext-link", "uri",
                    "product", "supplementary-material", "history", "pub-history",
                    "permissions", "self-uri", "related-article", "related-object",
                    "abstract", "trans-abstract", "kwd-group", "funding-group",
                    "support-group", "conference", "counts", "custom-meta-group",
                )
                for sibling_name in pub_date_following_siblings:
                    try:
                        articlemeta_node.find(sibling_name).addprevious(node)
                        added = True
                        break
                    except AttributeError:
                        continue
            if not added:
                articlemeta_node.append(node)

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

    def get_complete_publication_date(self, default_month=6, default_day=15):
        try:
            return self._article_dates.article_date_isoformat
        except Exception:
            pass
        try:
            year = month = day = None
            data = self._article_dates.article_date
            if data:
                year = data.get("year")
                month = data.get("month")
                day = data.get("day")
            return date(
                int(year or self.pub_year),
                int(month or default_month),
                int(day or default_day),
            ).isoformat()
        except (TypeError, KeyError):
            raise XMLWithPreArticlePublicationDateError(
                f"Unable to get complete publication date from {data}"
            )

    # --------------------------------------------------------------------------
    # Autores, Títulos e Conteúdo do Artigo
    # --------------------------------------------------------------------------
    @cached_property
    def authors(self):
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

        return {"person": names, "collab": collab}

    @cached_property
    def collab(self):
        return self.authors.get("collab")

    @cached_property
    def article_titles(self):
        xpath = "|".join([
            ".//article-meta//article-title",
            ".//article-meta//trans-title",
            ".//front-stub//article-title",
            ".//front-stub//trans-title",
        ])
        titles = []
        for item in self.xmltree.xpath(xpath):
            title = " ".join(
                [text.strip() for text in item.xpath(".//text()") if text and text.strip()]
            )
            titles.append(title)
        return sorted(titles)

    @cached_property
    def article_titles_texts(self):
        return self.article_titles

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

    def get_body_fragment(self, max_length):
        text = " ".join(" ".join(self.xmltree.xpath(".//body//text()")).split())
        if max_length:
            return text[:max_length].lower()
        return text.lower()

    @property
    def body_fingerprint(self):
        return generate_finger_print(self.get_body_fragment(max_length=None))

    @property
    def body_fragment_fingerprint(self):
        return generate_finger_print(self.get_body_fragment(300))

    def get_article_data(self, max_body_fragment_length=300):
        try:
            persons = self.authors.get("person") or []
            surnames = [p.get("surname") for p in persons if p.get("surname")]
        except Exception:
            surnames = []
        return {
            "surnames": surnames,
            "collab": self.collab,
            "links": self.links,
            "article_titles": self.article_titles_texts,
            "partial_body": self.partial_body,
            "body_fragment": self.get_body_fragment(max_body_fragment_length),
        }

    # --------------------------------------------------------------------------
    # Idiomas, DOIs e Relacionamentos
    # --------------------------------------------------------------------------
    @cached_property
    def _article_and_subarticles(self):
        return ArticleAndSubArticles(self.xmltree)

    @cached_property
    def main_lang(self):
        return self._article_and_subarticles.main_lang

    @cached_property
    def langs(self):
        for item in self._article_and_subarticles.data:
            yield item["lang"]

    @cached_property
    def _doi_with_lang(self):
        return DoiWithLang(self.xmltree)

    @cached_property
    def article_doi_with_lang(self):
        return self._doi_with_lang.data

    @cached_property
    def main_doi(self):
        return self._doi_with_lang.main_doi

    @cached_property
    def related_items(self):
        return RelatedItems(self.xmltree).related_articles

    @cached_property
    def links(self):
        return [item["href"] for item in self.related_items if item.get("href")]


# ==============================================================================
# 6. CLASSE PRINCIPAL: XMLWithPre
# ==============================================================================
class XMLWithPre(
    DOCTYPEParserMixin,
    PackagingAndFilesMixin,
    PackageNamingMixin,
    LegacyPackageNamingMixin,
    IdentifiersMixin,
    ArticleMetadataMixin,
):
    """Preserva o texto anterior ao elemento `root` e agrupa a manipulação do XML SciELO."""

    def __init__(self, xmlpre, xmltree, pretty_print=True):
        self.xmltree = xmltree
        self.xmlpre = xmlpre or ""

        # DOCTYPE
        self.DOCTYPE = None
        self.public_id = None
        self.system_id = None
        if self.xmlpre and "<!DOCTYPE" in self.xmlpre:
            self.parse_doctype()

        # Atributos gerais
        self.pretty_print = pretty_print
        self.uri = None
        self.zip_file_path = None
        self.xml_file_path = None
        self.relative_system_id = None
        self._sps_version = None
        self.errors = None
        self.pkg_name_version = None

        # Atributos de arquivo
        self.xml_name = None
        self.zip_basenames = None
        self.zip_namelist = None
        self._submitted_filename = None
        self._submitted_ext = None
        self._provided_sps_pkg_name = None
        self._built_sps_pkg_name = None
        self.is_html_source = None
        self._sps_pkg_name_origin = None
        self._sps_pkg_name = None

    def __str__(self):
        return self.xml_name or self.submitted_filename or self.zip_file_path or self.uri or "<XMLWithPre>"

    # --------------------------------------------------------------------------
    # Construtores & Serializadores
    # --------------------------------------------------------------------------
    @classmethod
    def create(
        cls, path=None, uri=None, xml_content=None, capture_errors=False, timeout=30,
        xml_native_name=None,
        html_name=None,
        built_name=None,
    ):
        """Retorna gerador de instâncias de XMLWithPre."""
        if path:
            errors = []
            xml_with_pre = None
            for item in get_xml_items(path):
                if not item:
                    continue
                try:
                    xml_with_pre = item["xml_with_pre"]
                    xml_with_pre.add_pkg_name(xml_native_name=xml_native_name, html_name=html_name, built_name=built_name)
                    yield xml_with_pre
                except (KeyError, ValueError) as e:
                    errors.append(item)
            if not xml_with_pre or errors:
                raise GetXmlWithPreError(f"Unable to get xml with pre {errors}")
        if xml_content:
            yield get_xml_with_pre(xml_content)
            return
        if uri:
            yield get_xml_with_pre_from_uri(uri, timeout)
            return

    def add_pkg_name(self, xml_native_name=None, html_name=None, built_name=None):
        if xml_native_name:
            self.provided_sps_pkg_name = xml_native_name
            self.submitted_filename = xml_native_name + ".xml"
        elif html_name:
            self.submitted_filename = html_name + ".html"
        if built_name:
            self._built_sps_pkg_name = built_name

    def tostring(self, pretty_print=False):
        return self.xmlpre + etree.tostring(
            self.xmltree,
            encoding="utf-8",
            pretty_print=pretty_print,
        ).decode("utf-8")

    @cached_property
    def sps_version(self):
        try:
            return self.xmltree.find(".").get("specific-use")
        except (AttributeError, TypeError, ValueError):
            return None

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

    @property
    def data(self):
        data = dict(
            sps_pkg_name=self.sps_pkg_name,
            pid_v3=self.v3,
            pid_v2=self.v2,
            aop_pid=self.aop_pid,
            filename=self.filename,
            files=self.files,
            filenames=self.filenames,
            pkg_names=self.deprecated_sps_pkg_name_list,
        )
        return data

    def get_data(self, input_files=None, sps_pkg_names=None, pkg_names=False, article=False, max_body_fragment_length=300):
        data = self.data
        if input_files:
            data.update(self.input_files_dict)
        if pkg_names:
            data.update(self.pkg_names_dict)
        if sps_pkg_names:
            data.update(self.sps_pkg_names_dict)
        if article:
            data.update(self.get_article_data(max_body_fragment_length))
        return data
    

def string_to_5_digits(input_string):
    return str((crc32(input_string.encode()) & 0xFFFFFFFF) % 100000)


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


def sanitize_name(value: str) -> str:
    """
    Regra estrita do SPS: Proibido underline (_), ponto (.),
    acentuação, espaços ou caracteres especiais. Permite apenas [a-zA-Z0-9-].
    """
    if not value:
        return ""
    clean = str(value).replace(" ", "")
    clean = re.sub(r"[^a-zA-Z0-9\-]", "", clean)
    return re.sub(r"-+", "-", clean).strip("-")


def sanitize_sps_name(value: str) -> str:
    """
    Regra estrita do SPS: Proibido underline (_), ponto (.),
    acentuação, espaços ou caracteres especiais. Permite apenas [a-zA-Z0-9-].
    """
    if not value:
        return ""
    clean = str(value).replace("_", "-").replace(".", "-").replace(" ", "")
    clean = re.sub(r"[^a-zA-Z0-9\-]", "", clean)
    return re.sub(r"-+", "-", clean).strip("-")
