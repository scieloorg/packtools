"""
Model for extracting ext-link elements from XML documents.

<ext-link> is used for marking external links/hyperlinks in scientific articles.
It ensures accessibility and interoperability of external references.

Example:
    <ext-link ext-link-type="uri"
              xlink:href="https://www.scielo.br/"
              xlink:title="SciELO Scientific Library">
        SciELO Brasil
    </ext-link>
"""
from functools import cached_property

from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import node_plain_text


class ExtLink(Fulltext):
    """
    Extracts ext-link elements from article or sub-article nodes.

    Processes article/sub-article and provides methods to extract
    ext-link information including attributes and text content.
    """

    @property
    def parent_data(self):
        """Returns parent context data for validation."""
        return self.attribs_parent_prefixed

    @property
    def ext_links(self):
        """
        Extract all ext-link elements with their attributes and context.

        Yields
        ------
        dict
            Dictionary containing ext-link information:
            - ext_link_type: Value of @ext-link-type attribute
            - xlink_href: Value of @xlink:href attribute
            - xlink_title: Value of @xlink:title attribute (optional)
            - text: Plain text content of the element
            - parent: Parent element tag
            - parent_id: Parent element id
            - parent_lang: Parent element language
            - parent_article_type: Parent article type

        Example:
            [
                {
                    'ext_link_type': 'uri',
                    'xlink_href': 'https://www.scielo.br/',
                    'xlink_title': 'SciELO Platform',
                    'text': 'SciELO Brasil',
                    'parent': 'article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'parent_article_type': 'research-article'
                }
            ]
        """
        nodes = self.node.xpath("./front | ./front-stub | ./body | ./back")

        for node in nodes:
            for ext_link in node.xpath(".//ext-link"):
                ext_link_data = {}

                for key, value in ext_link.attrib.items():
                    if "}" in key:
                        # Remove namespace prefix
                        # e.g. {http://www.w3.org/1999/xlink}href -> href
                        key = key.split("}")[-1]

                    if key == "href":
                        ext_link_data["xlink_href"] = value
                    elif key == "title":
                        ext_link_data["xlink_title"] = value
                    elif key == "ext-link-type":
                        ext_link_data["ext_link_type"] = value
                    else:
                        ext_link_data[key] = value

                ext_link_data.setdefault("ext_link_type", None)
                ext_link_data.setdefault("xlink_href", None)
                ext_link_data.setdefault("xlink_title", None)

                ext_link_data["text"] = node_plain_text(ext_link) or ""
                ext_link_data.update(self.parent_data)

                yield ext_link_data

    @property
    def fulltexts(self):
        """Yields direct child sub-articles as ExtLink instances."""
        for node in self.node.xpath("sub-article"):
            yield ExtLink(node)


class ArticleExtLinks:
    """
    Main class for extracting all ext-links from an XML document.

    Processes main article and all sub-articles to extract ext-link information.
    """

    def __init__(self, xmltree):
        """
        Initialize with XML tree.

        Parameters
        ----------
        xmltree : lxml.etree._Element
            The root element of the XML document
        """
        self.xmltree = xmltree
        self._ext_link = ExtLink(xmltree)

    @cached_property
    def ext_links(self):
        """
        Extract all ext-links from main article and sub-articles at any depth.

        Uses recursive traversal via ExtLink.fulltexts to correctly preserve
        parent context at each nesting level, covering arbitrarily deep
        sub-article structures.

        Returns
        -------
        list
            List of all ext-link dictionaries from article and sub-articles.
            Result is cached after the first call.
        """
        return list(self._collect_ext_links(self._ext_link))

    def _collect_ext_links(self, fulltext):
        """
        Recursively yield ext-links from a fulltext node and all its children.

        Parameters
        ----------
        fulltext : ExtLink
            The current fulltext node to process

        Yields
        ------
        dict
            ext-link data dictionaries
        """
        yield from fulltext.ext_links
        for child in fulltext.fulltexts:
            yield from self._collect_ext_links(child)
