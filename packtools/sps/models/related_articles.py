"""
<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
<italic>El coraje de la verdad</italic>
de Foucault.
<bold>Trans/form/ação</bold>
: revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
</related-article>
"""

from packtools.sps.utils.xml_utils import (
    get_parent_context,
    put_parent_context,
    tostring,
    remove_namespaces,
    node_plain_text,
)


class RelatedItems:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def related_articles(self):
        """
        <related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
        Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
        <italic>El coraje de la verdad</italic>
        de Foucault.
        <bold>Trans/form/ação</bold>
        : revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
        </related-article>
        """

        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xmltree
        ):
            for item in node.xpath(".//related-article"):
                d = {}
                for k in item.attrib:
                    if k == "{http://www.w3.org/1999/xlink}href":
                        d["href"] = item.attrib.get(k)
                    else:
                        d[k] = item.attrib.get(k)

                d["text"] = node_plain_text(item)
                d["xml"] = " ".join(
                    remove_namespaces(tostring(item, xml_declaration=False)).split()
                )
                yield put_parent_context(d, lang, article_type, parent, parent_id)

    @property
    def related_objects(self):
        # TODO
        pass


class Fulltext:
    """
    Processes article or sub-article node and provides methods to extract information
    """

    def __init__(self, node, original_article_type=None):
        """
        Initialize with an article or sub-article node

        Parameters
        ----------
        node : etree._Element
            XML node representing an article or sub-article
        """
        self.node = node
        self.original_article_type = original_article_type
        self._parent_data = {
            "parent": self.node.tag,
            "parent_id": self.node.get("id"),
            "parent_article_type": self.node.get("article-type"),
            "parent_lang": self.node.get("{http://www.w3.org/XML/1998/namespace}lang"),
            "original_article_type": original_article_type,
        }

    @property
    def parent_data(self):
        return self._parent_data

    @property
    def related_articles(self):
        """
        Extract all related articles information

        Returns
        -------
        list
            List of dictionaries containing related article information and parent data
        """
        nodes = self.node.xpath("./front | ./front-stub | ./body | ./back")
        for node in nodes:
            for related in node.xpath(".//related-article"):
                # Get all attributes from related-article
                related_data = dict(related.attrib)

                # Handle namespace prefixes in attributes
                for key, value in related.attrib.items():
                    if "}" in key:
                        clean_key = key.split("}")[-1]
                        related_data[clean_key] = value
                        del related_data[key]

                related_data["text"] = node_plain_text(related)
                related_data["xml"] = " ".join(
                    remove_namespaces(tostring(related, xml_declaration=False)).split()
                )

                # Add parent information
                related_data.update(self.parent_data)
                yield related_data

    @property
    def fulltexts(self):
        for node in self.node.xpath("sub-article"):
            if node.get("article-type") == "translation":
                original_article_type = self.node.get("article-type")
            else:
                original_article_type = None
            yield Fulltext(node, original_article_type=original_article_type)
