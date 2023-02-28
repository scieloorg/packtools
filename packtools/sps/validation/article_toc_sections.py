from packtools.sps.models.article_toc_sections import ArticleTocSections


class ArticleTocSectionsValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_toc_sections = ArticleTocSections(xmltree)

    def validate_article_toc_sections(self, article_section_titles):
        for lang, text in self.article_toc_sections.article_section_dict.items():
            if text == article_section_titles.get(lang):
                message = "OK, section titles match the document"
                result = True
            else:
                message = "ERROR, section titles no match the document"
                result = False
            yield dict(
                object='article section title',
                expected_value=article_section_titles.get(lang),
                obtained_value=text,
                result=result,
                message=message
            )

    def validate_sub_article_toc_sections(self, sub_article_section_titles):
        for lang, text in self.article_toc_sections.sub_article_section_dict.items():
            if text == sub_article_section_titles.get(lang):
                message = "OK, section titles match the document"
                result = True
            else:
                message = "ERROR, section titles no match the document"
                result = False
            yield dict(
                object='sub-article section title',
                expected_value=sub_article_section_titles.get(lang),
                obtained_value=text,
                result=result,
                message=message
            )
