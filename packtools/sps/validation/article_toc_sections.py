from packtools.sps.models.article_toc_sections import ArticleTocSections
from packtools.sps.models.article_titles import ArticleTitles


class ArticleTocSectionsValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_toc_sections = ArticleTocSections(xmltree)
        self.article_titles = ArticleTitles(xmltree)

    def validate_article_toc_sections(self, article_section_titles):
        resp = []
        number_of_titles_found = len(self.article_toc_sections.article_section_dict) + \
                                 len(self.article_toc_sections.sub_article_section_dict)
        number_of_titles_expected = len(article_section_titles)
        if number_of_titles_found != number_of_titles_expected:
            resp.append(
                dict(
                    object='section title',
                    expected_value=f"{number_of_titles_expected} section titles",
                    obtained_value=f"{number_of_titles_found} section titles",
                    result=False,
                    message="ERROR, number of titles found is different from the expected number of titles"
                )
            )
        else:
            for lang, text in self.article_toc_sections.article_section_dict.items():
                if text == article_section_titles.get(lang):
                    message = "OK, section titles match the document"
                    result = True
                else:
                    message = "ERROR, section titles no match the document"
                    result = False
                resp.append(
                    dict(
                        object='article section title',
                        expected_value=article_section_titles.get(lang),
                        obtained_value=text,
                        result=result,
                        message=message
                    )
                )
            for lang, text in self.article_toc_sections.sub_article_section_dict.items():
                if text == article_section_titles.get(lang):
                    message = "OK, section titles match the document"
                    result = True
                else:
                    message = "ERROR, section titles no match the document"
                    result = False
                resp.append(
                    dict(
                        object='sub-article section title',
                        expected_value=article_section_titles.get(lang),
                        obtained_value=text,
                        result=result,
                        message=message
                    )
                )
        return resp

    def validade_article_title_is_different_from_section_titles(self):
        section_titles = self.article_toc_sections.article_section_dict
        section_titles.update(self.article_toc_sections.sub_article_section_dict)
        article_title = self.article_titles.article_title_dict
        resp = []
        message = "OK, all section titles are different from the title of the article"
        result = True
        for lang, text in section_titles.items():
            if text == article_title.get(lang):
                message = "ERROR, there is at least one section title that corresponds to the title of the article"
                result = False

        resp.append(
            dict(
                object='section title',
                expected_value=article_title,
                obtained_value=section_titles,
                result=result,
                message=message
            )
        )
        return resp
