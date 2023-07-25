"""
<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
<italic>El coraje de la verdad</italic>
de Foucault.
<bold>Trans/form/ação</bold>
: revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
</related-article>
"""

from unittest import TestCase

from packtools.sps.utils import xml_utils
from packtools.sps.models.related_articles import RelatedItems


class RelatedItemsTest(TestCase):

    def test_related_items(self):
        xml = (
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
              <related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
                Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
                <italic>El coraje de la verdad</italic>
                de Foucault.
                <bold>Trans/form/ação</bold>
                : revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
                </related-article>
            </article>
            """
        )
        related = RelatedItems(xml_utils.get_xml_tree(xml))
        for i, item in enumerate(related.related_articles):
            with self.subTest(i):
                self.assertDictEqual(
                    {
                        "ext-link-type": "doi",
                        "id": "A01",
                        "related-article-type": "commentary-article",
                        "href": "10.1590/0101-3173.2022.v45n1.p139",
                    },
                    item
                )


