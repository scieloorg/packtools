from packtools.sps.models.article_toc_sections import ArticleTocSections
from packtools.sps.models.article_titles import ArticleTitles


class ArticleTocSectionsValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_toc_sections = ArticleTocSections(xmltree)
        self.article_titles = ArticleTitles(xmltree)

    def validate_article_toc_sections(self, expected_toc_sections):
        resp = []
        for lang, text in self.article_toc_sections.all_section_dict.items():
            if text == self.article_toc_sections.article_section_dict.get(lang):
                obj = 'article section title'
            else:
                obj = 'sub-article section title'
            if text in (expected_toc_sections.get(lang) or []):
                message = "OK, section titles match the document"
                result = True
            else:
                message = "ERROR, section titles no match the document"
                result = False
            resp.append(
                dict(
                    object=obj,
                    expected_value=expected_toc_sections.get(lang),
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
                message = 'ERROR: Article title ("{}") must not be the same as the section title ("{}")'.format(article_title.get(lang), text)
                result = False

        resp.append(
            dict(
                object='section title',
                article_title=article_title,
                section_title=section_titles,
                result=result,
                message=message
            )
        )
        return resp

    
    def validate(self, data):
        """
        Função que executa as validações da classe ArticleTocSectionsValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.
        
        """
        toc_sections_results = {
            'article_toc_sections_validation': 
                self.validate_article_toc_sections(data['expected_toc_sections'])
            }
        title_results = {
            'article_title_validation': self.validade_article_title_is_different_from_section_titles()
            }
        
        toc_sections_results.update(title_results)
        return toc_sections_results