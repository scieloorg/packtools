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
from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import (
    node_plain_text,
    tostring,
    remove_namespaces,
)


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
        
        Returns
        -------
        list
            List of dictionaries containing ext-link information:
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
        # Search in front, body and back sections
        nodes = self.node.xpath("./front | ./front-stub | ./body | ./back")
        
        for node in nodes:
            for ext_link in node.xpath(".//ext-link"):
                ext_link_data = {}
                
                # Extract attributes, handling namespace prefixes
                for key, value in ext_link.attrib.items():
                    if "}" in key:
                        # Remove namespace prefix (e.g., {http://www.w3.org/1999/xlink}href -> href)
                        key = key.split("}")[-1]
                    
                    # Map xlink attributes to snake_case
                    if key == "href":
                        ext_link_data["xlink_href"] = value
                    elif key == "title":
                        ext_link_data["xlink_title"] = value
                    elif key == "ext-link-type":
                        ext_link_data["ext_link_type"] = value
                    else:
                        ext_link_data[key] = value
                
                # Set None for missing attributes
                ext_link_data.setdefault("ext_link_type", None)
                ext_link_data.setdefault("xlink_href", None)
                ext_link_data.setdefault("xlink_title", None)
                
                # Extract text content
                ext_link_data["text"] = node_plain_text(ext_link) or ""
                
                # Add parent context
                ext_link_data.update(self.parent_data)
                
                yield ext_link_data
    
    @property
    def fulltexts(self):
        """Recursively process sub-articles."""
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
    
    @property
    def ext_links(self):
        """
        Extract all ext-links from main article and sub-articles.
        
        Returns
        -------
        list
            List of all ext-link dictionaries from article and sub-articles
        """
        ext_links = []
        
        # Main article ext-links
        ext_links.extend(list(self._ext_link.ext_links))
        
        # Sub-articles ext-links (recursively)
        for fulltext in self._ext_link.fulltexts:
            ext_links.extend(list(fulltext.ext_links))
            # Handle nested sub-articles
            for nested_fulltext in fulltext.fulltexts:
                ext_links.extend(list(nested_fulltext.ext_links))
        
        return ext_links
