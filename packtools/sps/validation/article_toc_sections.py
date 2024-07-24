from packtools.sps.models.v2.article_toc_sections import ArticleTocSections
from packtools.sps.models.article_titles import ArticleTitles
from packtools.sps.validation.utils import format_response


class ArticleTocSectionsValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_toc_sections = ArticleTocSections(xmltree)
        self.article_titles = ArticleTitles(xmltree)

    def validate_article_toc_sections(self, expected_toc_sections, error_level="CRITICAL"):
        """
        Check whether the TOC sections matches the options provided in a standard list.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                            <subj-group subj-group-type="sub-heading">
                                <subject>Public Health</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                            <subj-group subj-group-type="sub-heading">
                                <subject>Saúde Pública</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>

        Params
        ------
        expected_toc_sections : dict, such as:
            {
                "en": ["Health Sciences"],
                "pt": ["Ciências da Saúde"]
            }
        level_error : str

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article section title validation',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'item': 'subj-group',
                    'sub_item': 'subject',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['Health Sciences'],
                    'got_value': 'Health Sciences',
                    'message': "Got Health Sciences, expected ['Health Sciences']",
                    'advice': None,
                    'data': {
                        'en': {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'text': 'Health Sciences'
                        },
                        'pt': {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'text': 'Ciências da Saúde'
                        }
                    },
                },...
            ]
        """
        obtained_toc_sections = self.article_toc_sections.sections_dict
        if obtained_toc_sections:
            obtained_langs = set(obtained_toc_sections)
            expected_langs = set(expected_toc_sections)
            all_langs = sorted(list(obtained_langs | expected_langs))
            common_langs = sorted(list(obtained_langs & expected_langs))

            for lang in all_langs:
                is_valid = False
                title = 'Article section title validation'
                validation = "exist"
                expected = expected_toc_sections.get(lang)
                obtained = obtained_toc_sections.get(lang)
                obtained_msg = obtained.get('text') if obtained else None
                advice = 'Provide missing section for language: {}'.format(lang)
                if lang in common_langs:
                    if obtained.get('text'):
                        # verifica se o título de seção está presente na lista esperada
                        is_valid = obtained.get('text') in expected
                        if obtained.get("parent") == "sub-article":
                            title = f'Sub-article (id={obtained.get("parent_id")}) section title validation'
                        validation = 'value in list'
                elif lang in obtained_langs:
                    advice = 'Remove unexpected section for language: {}'.format(lang)

                yield format_response(
                    title=title,
                    parent=obtained.get("parent"),
                    parent_id=obtained.get("parent_id"),
                    parent_article_type=obtained.get("parent_article_type"),
                    parent_lang=obtained.get("parent_lang"),
                    item="subj-group",
                    sub_item="subject",
                    is_valid=is_valid,
                    validation_type=validation,
                    expected=expected,
                    obtained=obtained_msg,
                    advice=advice,
                    data=obtained_toc_sections,
                    error_level=error_level,
                )
        else:
            yield format_response(
                title='Article or sub-article section title validation',
                parent='article',
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="subj-group",
                sub_item="subject",
                is_valid=False,
                validation_type="exist",
                expected=expected_toc_sections,
                obtained=obtained_toc_sections,
                advice='Provide a subject value for <subj-group subj-group-type="heading">',
                data=obtained_toc_sections,
                error_level=error_level,
            )

    def validade_article_title_is_different_from_section_titles(self, error_level="ERROR"):
        """
        Checks if the titles provided for article and sections are different from each other.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Health Sciences Studies</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                            <subj-group subj-group-type="sub-heading">
                                <subject>Public Health</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                            <subj-group subj-group-type="sub-heading">
                                <subject>Saúde Pública</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Estudos sobre Ciências da Saúde</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>

        Params
        ------
        level_error : str

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Article or sub-article section title validation',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'item': 'subj-group',
                    'sub_item': 'subject',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': "'Health Sciences Studies' (article title) different from 'Health Sciences' ("
                                      "section titles)",
                    'got_value': "article title: 'Health Sciences Studies', section titles: 'Health Sciences'",
                    'message': "Got article title: 'Health Sciences Studies', section titles: 'Health Sciences', "
                               "expected 'Health Sciences Studies' (article title) different from 'Health Sciences' ("
                               "section titles)",
                    'advice': None,
                    'data': {
                        'en': {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'text': 'Health Sciences'
                        },
                        'pt': {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'text': 'Ciências da Saúde'
                        }
                    },
                },...
            ]
        """
        obtained_toc_sections = self.article_toc_sections.sections_dict
        article_title = self.article_titles.article_title_dict

        for lang, sections in obtained_toc_sections.items():
            is_valid = article_title.get(lang) != sections.get('text')
            article = article_title.get(lang)
            section = sections.get("text")
            if sections.get("parent") == "article":
                validation_title = 'Article or sub-article section title validation'
            else:
                validation_title = f'Sub-article (id={sections.get("parent_id")}) section title validation'
            yield format_response(
                title=validation_title,
                parent=sections.get("parent"),
                parent_id=sections.get("parent_id"),
                parent_article_type=sections.get("parent_article_type"),
                parent_lang=sections.get("parent_lang"),
                item="subj-group",
                sub_item="subject",
                is_valid=is_valid,
                validation_type="match",
                expected='\'{}\' (article title) different from \'{}\' (section titles)'.format(article, section),
                obtained='article title: \'{}\', section titles: \'{}\''.format(article, section),
                advice="Provide different titles for article and section (subj-group[@subj-group-type='heading']/subject)",
                data=obtained_toc_sections,
                error_level=error_level,
            )

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
