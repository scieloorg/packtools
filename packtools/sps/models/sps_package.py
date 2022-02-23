import itertools
import os
import logging
from copy import deepcopy

from lxml import etree

from dsm.utils import xml_utils
from dsm.utils.files import read_file


logger = logging.getLogger(__name__)


class NotAllowedtoChangeAttributeValueError(Exception):
    pass


class InvalidAttributeValueError(Exception):
    pass


class InvalidValueForOrderError(Exception):
    pass


class SPS_Package:
    def __init__(self, xml, original_filename=None):
        self.xmltree = xml_utils.get_xml_tree(xml)
        self._original_filename = original_filename
        self._assets = SPS_Assets(self.xmltree, self.scielo_pid_v3)

    @property
    def xmltree(self):
        return self._xmltree

    @xmltree.setter
    def xmltree(self, value):
        self._xmltree = value

    @property
    def identity(self):
        return Identity(self.xmltree)

    @property
    def subart_translations(self):
        return self._nodes_with_lang(
            './/sub-article[@article-type="translation"]'
        )

    def local_to_remote(self, uris_and_names):
        """
        URI assets from remote to local

        Example:
        from
        <graphic xlink:href="1234-0987-abc-09-01-gf01.tiff"/>

        to
        <graphic xlink:href="https://minio.scielo.br/v3/xmljdfoae.tiff"/>
        """
        _image_files = {
            item["name"]: item["uri"]
            for item in uris_and_names
        }
        for node in self.xmltree.xpath(
                ".//*[@xlink:href]",
                namespaces={"xlink": "http://www.w3.org/1999/xlink"}):
            href = node.get('{http://www.w3.org/1999/xlink}href')
            if ":" in href:
                continue
            remote = _image_files.get(href)
            if remote:
                node.set('{http://www.w3.org/1999/xlink}href', remote)

    @property
    def xml_content(self):
        return xml_utils.tostring(self.xmltree)

    @property
    def issn(self):
        return self.identity.issn

    @property
    def acron(self):
        return self.identity.acron

    @property
    def order(self):
        return self.identity.order

    @property
    def scielo_pid_v1(self):
        return self.identity.scielo_pid_v1

    @scielo_pid_v1.setter
    def scielo_pid_v1(self, value):
        self.identity.scielo_pid_v1 = value

    @property
    def scielo_pid_v2(self):
        return self.identity.scielo_pid_v2

    @scielo_pid_v2.setter
    def scielo_pid_v2(self, value):
        self.identity.scielo_pid_v2 = value

    @property
    def scielo_pid_v3(self):
        return self.identity.scielo_pid_v3

    @scielo_pid_v3.setter
    def scielo_pid_v3(self, value):
        self.identity.scielo_pid_v3 = value

    @property
    def aop_pid(self):
        return self.identity.aop_pid

    @aop_pid.setter
    def aop_pid(self, value):
        self.identity.aop_pid = value

    @property
    def doi(self):
        return self.identity.doi

    @doi.setter
    def doi(self, value):
        self.identity.doi = value

    @property
    def assets(self):
        return self._assets

    @property
    def lang(self):
        return self.xmltree.find(".").get(
            "{http://www.w3.org/XML/1998/namespace}lang")

    @property
    def article_type(self):
        return self.xmltree.find(".").get("article-type")

    @property
    def article_title(self):
        return formatted_text(
            self.xmltree.find(".//article-meta//article-title"))

    @property
    def article_titles(self):
        data = {}
        data[self.lang] = self.article_title

        for node, lang in self._nodes_with_lang(
                ".//article-meta//trans-title-group", "trans-title"):
            data[lang] = formatted_text(node)

        for node, lang in self._nodes_with_lang(
                ".//sub-article[@article-type='translation']",
                ".//front-stub/article-title"
                ):
            data[lang] = formatted_text(node)
        return data

    def get_regular_abstract(self, xpath=".//article-meta//abstract"):
        regular_abstract = None
        for _abstract in self.xmltree.findall(xpath):
            if not _abstract.get("abstract-type"):
                regular_abstract = _abstract
                break
        return regular_abstract

    @property
    def abstract(self):
        return formatted_text(
            self.get_regular_abstract(".//article-meta//abstract"))

    @property
    def abstracts(self):
        data = {}
        data[self.lang] = self.abstract

        for node, lang in self._nodes_with_lang(
                ".//article-meta//trans-abstract"):
            data[lang] = formatted_text(node)

        for node, lang in self._nodes_with_lang(
                ".//sub-article[@article-type='translation']",
                ".//front-stub/abstract"):
            data[lang] = formatted_text(node)
        return data

    @property
    def keywords_groups(self):
        data = {}
        for node, lang in self._nodes_with_lang(".//kwd-group"):
            data[lang] = []
            for kwd in node.findall(".//kwd"):
                data[lang].append(formatted_text(kwd))
        return data

    @property
    def subject(self):
        """
        <article-categories>
            <subj-group subj-group-type="heading">
                <subject>Scientific Communication</subject>
                <subj-group>
                    <subject>Food Safety</subject>
                </subj-group>
            </subj-group>
        </article-categories>
        """
        return formatted_text(
            self.xmltree.find(
                './/subj-group[@subj-group-type="heading"]/subject'
            )
        )

    @property
    def subjects(self):
        """
        <article-categories>
            <subj-group subj-group-type="heading">
                <subject>Scientific Communication</subject>
                <subj-group>
                    <subject>Food Safety</subject>
                </subj-group>
            </subj-group>
        </article-categories>
        """
        data = {}
        data[self.lang] = self.subject
        for subj, lang in self._nodes_with_lang(
                './/sub-article',
                './/subj-group[@subj-group-type="heading"]/subject'
                ):
            data[lang] = formatted_text(subj)
        return data

    @property
    def article_ids(self):
        return self.identity.article_ids

    @property
    def authors(self):
        """
        <contrib-group>
            <contrib contrib-type="author">
                <contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>
                <contrib-id contrib-id-type="scopus">24771926600</contrib-id>
                <name>
                    <surname>Einstein</surname>
                    <given-names>Albert</given-names>
                </name>
                ...
            </contrib>
            <contrib contrib-type="author">
                <contrib-id contrib-id-type="lattes">4760273612238540</contrib-id>
                <name>
                    <surname>Meneghini</surname>
                    <given-names>Rogerio</given-names>
                </name>
                ...
            </contrib>
            ...
        </contrib-group>
        """
        affiliations = self.affiliations
        for node in self.xmltree.findall(
                './/contrib[@contrib-type="author"]'):
            xref = node.find(".//xref[@ref-type='aff']")
            aff = None
            if xref is not None:
                aff = self.affiliations.get(xref.get("rid"))
            yield dict(
                surname=node.findtext(".//surname"),
                given_names=node.findtext(".//given-names"),
                orcid=node.findtext(".//contrib-id[@contrib-id-type='orcid']"),
                aff=aff
            )

    @property
    def affiliations(self):
        """
        <aff id="aff01">
            <label>1</label>
            <institution content-type="orgname">Fundação Oswaldo Cruz</institution>
            <institution content-type="orgdiv1">Escola Nacional de Saúde Pública Sérgio Arouca</institution>
            <institution content-type="orgdiv2">Centro de Estudos da Saúde do Trabalhador e Ecologia Humana</institution>
            <addr-line>
                <city>Manguinhos</city>
                <state>RJ</state>
            </addr-line>
            <country country="BR">Brasil</country>
            <email>maurosilva@foo.com</email>
            <institution content-type="original">Prof. da Fundação Oswaldo Cruz; da Escola Nacional de Saúde Pública Sérgio Arouca, do Centro de Estudos da Saúde do Trabalhador e Ecologia Humana. RJ - Manguinhos / Brasil. maurosilva@foo.com </institution>
        </aff>
        """
        if not hasattr(self, '_affiliations'):
            self._affiliations = {
                node.get("id"): (
                    node.findtext('.//institution[@content-type="orgname"]') or
                    node.findtext('.//institution')
                )
                for node in self.xmltree.findall(".//aff")
            }
        return self._affiliations

    @property
    def languages(self):
        return [self.lang] + [lang for node, lang in self.subart_translations]

    @property
    def elocation_id(self):
        return self.identity.elocation_id

    @property
    def fpage(self):
        return self.identity.fpage

    @property
    def fpage_seq(self):
        return self.identity.fpage_seq

    @property
    def lpage(self):
        return self.identity.lpage

    @property
    def volume(self):
        return self.identity.volume

    @property
    def number(self):
        return self.identity.number

    @property
    def supplement(self):
        return self.identity.supplement

    @property
    def document_pubdate(self):
        return self.identity.document_pubdate

    @property
    def documents_bundle_pubdate(self):
        return self.identity.documents_bundle_pubdate

    @property
    def year(self):
        return self.identity.year

    @property
    def documents_bundle_id(self):
        return self.identity.documents_bundle_id

    def _nodes_with_lang(self, lang_xpath, child_xpath=None):
        return (
            (
                child_xpath and node.find(child_xpath) or node,
                node.get('{http://www.w3.org/XML/1998/namespace}lang'),
            )
            for node in self.xmltree.findall(lang_xpath)
        )

    @property
    def package_name(self):
        return self.identity.package_name

    def remote_to_local(self, package_name):
        """
        URI assets from remote to local

        Example:
        from
        <graphic xlink:href="https://minio.scielo.br/v3/xmljdfoae.tiff"/>

        to
        <graphic xlink:href="1234-0987-abc-09-01-gf01.tiff"/>
        """
        self.assets.remote_to_local(package_name)

    # def asset_name(self, img_filename):
    #     if self._original_asset_name_prefix is None:
    #         raise ValueError(
    #             "SPS_Package._original_asset_name_prefix has an invalid value."
    #         )
    #     filename, ext = os.path.splitext(self._original_asset_name_prefix)
    #     suffix = img_filename
    #     if img_filename.startswith(filename):
    #         suffix = img_filename[len(filename) :]
    #     return "-g".join([self.package_name, suffix])


class Identity:
    def __init__(self, xml_tree):
        self.xmltree = xml_tree

    @property
    def xmltree(self):
        return self._xmltree

    @xmltree.setter
    def xmltree(self, value):
        self._xmltree = value

    @property
    def journal_meta(self):
        return self.xmltree.find(".//journal-meta")

    @property
    def article_meta(self):
        return self.xmltree.find(".//article-meta")

    @property
    def order(self):
        _order = self.article_meta.findtext('.//article-id[@pub-id-type="other"]')
        if _order is None:
            _order = self.scielo_pid_v2[-5:]
        return int(_order)

    def _get_scielo_pid(self, specific_use):
        try:
            return self.article_meta.xpath(
                f'.//article-id[@specific-use="{specific_use}"]/text()'
            )[0]
        except (IndexError, AttributeError):
            return None

    def _set_scielo_pid(self, attr_value, specific_use, value):
        if attr_value is None:
            pid_node = etree.Element("article-id")
            pid_node.set("pub-id-type", "publisher-id")
            pid_node.set("specific-use", specific_use)
            pid_node.text = value
            self.article_meta.insert(0, pid_node)
        else:
            pid_node = self.article_meta.xpath(
                f'.//article-id[@specific-use="{specific_use}"]'
            )[0]
            pid_node.text = value

    @property
    def scielo_pid_v1(self):
        return self._get_scielo_pid("scielo-v1")

    @scielo_pid_v1.setter
    def scielo_pid_v1(self, value):
        self._set_scielo_pid(self.scielo_pid_v1, "scielo-v1", value)

    @property
    def scielo_pid_v2(self):
        return self._get_scielo_pid("scielo-v2")

    @scielo_pid_v2.setter
    def scielo_pid_v2(self, value):
        if not _is_allowed_to_update(self, "scielo_pid_v2", value):
            return
        self._set_scielo_pid(self.scielo_pid_v2, "scielo-v2", value)

    @property
    def scielo_pid_v3(self):
        return self._get_scielo_pid("scielo-v3")

    @scielo_pid_v3.setter
    def scielo_pid_v3(self, value):
        self._set_scielo_pid(self.scielo_pid_v3, "scielo-v3", value)

    @property
    def aop_pid(self):
        try:
            return self.article_meta.xpath(
                './/article-id[@specific-use="previous-pid" and '
                '@pub-id-type="publisher-id"]/text()'
            )[0]
        except IndexError:
            return None

    @aop_pid.setter
    def aop_pid(self, value):
        if not _is_allowed_to_update(self, "aop_pid", value):
            return
        if self.aop_pid is None:
            pid_node = etree.Element("article-id")
            pid_node.set("pub-id-type", "publisher-id")
            pid_node.set("specific-use", "previous-pid")
            pid_node.text = value
            self.article_meta.insert(1, pid_node)
        else:
            pid_node = self.article_meta.xpath(
                './/article-id[@specific-use="previous-pid" and '
                '@pub-id-type="publisher-id"]'
            )[0]
            pid_node.text = value

    @property
    def doi(self):
        try:
            return self.article_meta.xpath(
                "article-id[@pub-id-type='doi']")[0].text
        except (AttributeError, IndexError):
            return None

    @doi.setter
    def doi(self, value):
        node = self.article_meta.find(
            './/article-id[@pub-id-type="doi"]'
        )
        if node is None:
            node = etree.Element("article-id")
            node.set("pub-id-type", "doi")
            node.text = value
            self.article_meta.insert(0, node)
        else:
            node.text = value

    @property
    def issn(self):
        return (
            self.journal_meta.findtext('.//issn[@pub-type="epub"]') or
            self.journal_meta.findtext('.//issn[@pub-type="ppub"]') or
            self.journal_meta.findtext(".//issn")
        )

    @property
    def acron(self):
        return self.journal_meta.findtext(
            './/journal-id[@journal-id-type="publisher-id"]')

    @property
    def article_ids(self):
        """
        <article-id specific-use="scielo-v3" pub-id-type="publisher-id">JHVKpRBtgd47h5F6YDz6mSm</article-id>
        <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0103-636X2020000200719</article-id>
        <article-id specific-use="scielo-v1" pub-id-type="publisher-id">S0103-636X(20)000200719</article-id>
        <article-id pub-id-type="publisher-id">1980-4415v34n67a18</article-id>

        Returns
        -------
        dict
            ```
            {
                "v1": "S0103-636X(20)000200719",
                "v2": "S0103-636X2020000200719",
                "v3": "JHVKpRBtgd47h5F6YDz6mSm",
                "other": ["1980-4415v34n67a18"]
            }
            ```
        """
        data = {}
        for node in self.article_meta.findall(
                './/article-id[@pub-id-type="publisher-id"]'):
            use = node.get("specific-use") or "other"
            use = use.replace("scielo-", "")
            data[use] = node.text
        if data.get("other"):
            data["other"] = [data["other"]]
        return data

    @property
    def elocation_id(self):
        """
        <article-meta>
            ...
            <volume>10</volume>
            <issue>2</issue>
            <elocation-id>0102961</elocation-id>
            ...
        </article-meta>
        """
        return self.article_meta.findtext("elocation-id")

    @property
    def fpage(self):
        """
        <article-meta>
            ...
            <volume>10</volume>
            <issue>2</issue>
            <fpage>2961</fpage>
            ...
        </article-meta>
        """
        return self.article_meta.findtext("fpage")

    @property
    def fpage_seq(self):
        """
        <article-meta>
            ...
            <volume>10</volume>
            <issue>2</issue>
            <fpage seq="a">2961</fpage>
            ...
        </article-meta>
        """
        fpage = self.article_meta.find("fpage")
        if fpage is not None:
            return fpage.get("seq")

    @property
    def lpage(self):
        """
        <article-meta>
            ...
            <volume>10</volume>
            <issue>2</issue>
            <lpage>2961</lpage>
            ...
        </article-meta>
        """
        return self.article_meta.findtext("lpage")

    @property
    def volume(self):
        return self.article_meta.findtext("volume")

    @property
    def number(self):
        n, s = extract_number_and_supplment_from_issue_element(
            self.article_meta.findtext("issue")
        )
        return n

    @property
    def supplement(self):
        n, s = extract_number_and_supplment_from_issue_element(
            self.article_meta.findtext("issue")
        )
        return s

    @property
    def document_pubdate(self):
        xpaths = (
            'pub-date[@pub-type="epub"]',
            'pub-date[@date-type="pub"]',
            "pub-date",
        )
        return get_year_month_day(_match_pubdate(self.article_meta, xpaths))

    @property
    def documents_bundle_pubdate(self):
        xpaths = (
            'pub-date[@pub-type="epub-ppub"]',
            'pub-date[@pub-type="collection"]',
            'pub-date[@date-type="collection"]',
            "pub-date",
        )
        return get_year_month_day(_match_pubdate(self.article_meta, xpaths))

    @property
    def year(self):
        return self.documents_bundle_pubdate[0]

    @property
    def documents_bundle_id(self):
        issue = (
            self.supplement and f"{self.number}s{self.supplement}" or
            self.number
        )
        data = (
            self.journal_meta.issn,
            (
                (self.article_meta.volume or self.article_meta.number) and
                self.article_meta.documents_bundle_pubdate[0]
            ),
            self.article_meta.volume,
            issue,
            not self.article_meta.volume and not self.article_meta.number and "aop",
        )
        return "-".join([item for item in data if item])

    @property
    def package_name(self):
        doi = self.doi and self.doi.split("/")[-1]
        fpage = self.fpage
        if self.fpage_seq:
            fpage += self.fpage_seq
        last_item = str(fpage or self.elocation_id or self.order or doi).zfill(5)

        data = (
            self.issn,
            self.acron,
            self.volume,
            self.number,
            self.supplement and f"s{self.supplement}",
            last_item,
        )
        return "-".join([str(item).zfill(2) for item in data if item])


class SPS_Assets:
    """
    './/graphic[@xlink:href]',
    './/media[@xlink:href]',
    './/inline-graphic[@xlink:href]',
    './/supplementary-material[@xlink:href]',
    './/inline-supplementary-material[@xlink:href]',
    """

    def __init__(self, xml_tree, v3):
        self._xml_tree = xml_tree
        self._v3 = v3
        self._assets_uri_and_node = self.get_assets_uri_and_node()
        self._get_assets_which_have_id()
        self._get_assets_which_have_no_id()

    def get_assets_uri_and_node(self, node=None):
        """
        Get a list of tuples (uri, node).

        Retorna uma lista de tuplas (uri, node).

        Returns
        -------
        list of strings
            lista de uri dos ativos digitais no XML
        """
        nodes = []
        # obtém os assets da árvore inteira ou a partir de um node
        xmltree = node or self._xml_tree
        for node in xmltree.xpath(
                ".//*[@xlink:href]",
                namespaces={"xlink": "http://www.w3.org/1999/xlink"}):
            href = node.attrib["{http://www.w3.org/1999/xlink}href"]
            if self._is_valid_sps_asset_uri(href):
                nodes.append((href, node))
        return nodes

    def _is_valid_sps_asset_uri(self, href):
        return "/" not in href or f"/{self._v3}/" in href

    @property
    def assets_uri_and_node(self):
        """
        Retorna uma lista das URIs dos ativos digitais de ``xml_tree``.

        Returns
        -------
        list of strings
            lista de uri dos ativos digitais no XML
        """
        return self._assets_uri_and_node

    def _get_assets_which_have_id(self):
        self._assets_which_have_id = []
        for node in self._xml_tree.xpath(".//*[@id]"):
            if node.tag == "sub-article":
                continue
            i = 0
            for uri, child_node in self.get_assets_uri_and_node(node):
                self._assets_which_have_id.append(
                    SPS_Asset(child_node, node, _id=i)
                )
                i += 1

    @property
    def assets_which_have_id(self):
        return self._assets_which_have_id

    @property
    def assets_which_have_no_id(self):
        return self._assets_which_have_no_id

    def _get_assets_which_have_no_id(self):
        has_id = [item.asset_node for item in self.assets_which_have_id]

        i = 0
        self._assets_which_have_no_id = []
        for uri, node in self.assets_uri_and_node:
            if node not in has_id:
                i += 1
                self._assets_which_have_no_id.append(
                    SPS_Asset(node, _id=i)
                )

    @property
    def items(self):
        return self.assets_which_have_id + self.assets_which_have_no_id

    def remote_to_local(self, package_name):
        """
        URI assets from remote to local

        Example:
        from
        <graphic xlink:href="https://minio.scielo.br/v3/xmljdfoae.tiff"/>

        to
        <graphic xlink:href="1234-0987-abc-09-01-gf01.tiff"/>
        """
        for asset in self.items:
            asset.remote_to_local(package_name)


class SPS_Asset:
    def __init__(self, asset_node, parent_node_with_id=None, _id=None):
        self._parent_node_with_id = parent_node_with_id
        self._asset_node = asset_node
        # _id é o índice para img dentro de um elemento que tenha `@id` ou
        # no contexto do artigo inteiro
        self._id = _id
        self.uri = self.xlink_href
        self.filename = self.xlink_href

    def __str__(self):
        return xml_utils.tostring(self._asset_node)

    @property
    def tag(self):
        if self._parent_node_with_id is not None:
            return self._parent_node_with_id.tag
        return ""

    @property
    def asset_node(self):
        return self._asset_node

    @property
    def id(self):
        return self._id

    @property
    def content_type(self):
        return self._asset_node.get("content-type") or ""

    @property
    def type(self):
        """
        -g: figure graphic
        -i: inline graphic
        -e: equation
        -s: supplementary data file
        """
        if "display-formula" in self.tag:
            return "e"
        if "supplementary" in self.tag:
            return "s"
        if "inline" in self.tag:
            return "i"
        return "g"

    @property
    def suffix(self):
        if self.content_type:
            alternative_id = f"-{self.content_type}"
        else:
            alternative_id = self.id or ""
        return f"-{self.type}{alternative_id}"

    @property
    def ext(self):
        ign, ext = os.path.splitext(self.xlink_href)
        return ext

    @property
    def xlink_href(self):
        return self._asset_node.get("{http://www.w3.org/1999/xlink}href")

    @xlink_href.setter
    def xlink_href(self, value):
        # obtém o valor atual de xlink_href
        current = self.xlink_href

        # guarda valor de `current` em uri ou filename
        self.uri = current
        self.filename = current

        # guarda valor de `value` (novo) em uri ou filename
        self.uri = value
        self.filename = value

        # atualiza o valor de xlink href
        self._asset_node.set("{http://www.w3.org/1999/xlink}href", value)

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, value):
        if "/" in value:
            self._uri = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if "/" not in value:
            self._filename = value

    def remote_to_local(self, package_name):
        self.xlink_href = self.get_name(package_name)

    def get_name(self, package_name):
        return f"{package_name}{self.suffix}{self.ext}"


# Funções

# def is_valid_value_for_order(value):
#     try:
#         if not (0 < int(value) <= 99999):
#             raise ValueError
#     except (ValueError, TypeError):
#         raise InvalidValueForOrderError(
#             "Invalid value for 'order': %s" %
#             value
#         )
#     else:
#         return True


# def is_valid_value_for_language(value):
#     if len(value or "") != 2:
#         raise ValueError
#     return True


# def is_valid_value_for_issns(issns_dict):
#     """
#     Expected issns_dict is a dict
#     keys: 'epub' and/or 'ppub'
#     values: issn (1234-5678)
#     """
#     try:
#         if len(issns_dict) == 0 or not set(issns_dict.keys()).issubset({'epub', 'ppub'}):
#             raise ValueError(
#                 f"Expected dict which keys are 'epub' and/or 'ppub'. Found {issns_dict}")
#         if len(issns_dict.keys()) != len(set(issns_dict.values())):
#             raise ValueError(f"{issns_dict} has duplicated values")
#         for v in issns_dict.values():
#             if len(v) != 9 or v[4] != "-":
#                 raise ValueError(f"{v} is not an ISSN")
#     except AttributeError:
#         raise ValueError(
#             f"Expected dict which keys are 'epub' and/or 'ppub'. Found {issns_dict}")
#     return True


def _match_pubdate(node, pubdate_xpaths):
    """
    Retorna o primeiro match da lista de pubdate_xpaths
    """
    for xpath in pubdate_xpaths:
        pubdate = node.find(xpath)
        if pubdate is not None:
            return pubdate
