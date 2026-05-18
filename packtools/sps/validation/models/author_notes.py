from packtools.sps.models.author_notes import FulltextAuthorNotes


class XMLAuthorNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_author_notes(self):
        group = FulltextAuthorNotes(self.xml_tree.find("."))
        return {"corresp_data": list(group.corresp_data), "fns": list(group.items)}

    def sub_article_author_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            group = FulltextAuthorNotes(sub_article)
            yield {"corresp_data": list(group.corresp_data), "fns": list(group.items)}
