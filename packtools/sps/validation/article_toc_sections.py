from packtools.sps.models.v2.article_toc_sections import ArticleTocSections
from packtools.sps.models.article_titles import ArticleTitles
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationExpectedTocSectionsException


class ArticleTocSectionsValidation:
    def __init__(self, xmltree, expected_toc_sections=None):
        self.xmltree = xmltree
        self.article_toc_sections = ArticleTocSections(xmltree)
        self.article_titles = ArticleTitles(xmltree)
        self.expected_toc_sections = expected_toc_sections

    def validate_article_toc_sections(self, expected_toc_sections=None, error_level="CRITICAL"):
        """
        Check whether the TOC sections match the options provided in a standard list.

        Params
        ------
        expected_toc_sections : dict, such as:
            {
                "en": ["Health Sciences"],
                "pt": ["Ciências da Saúde"]
            }
        error_level : str

        Returns
        -------
        generator of dict
            A generator that yields dictionaries with validation results.
        """
        expected_toc_sections = expected_toc_sections or self.expected_toc_sections
        if not expected_toc_sections:
            raise ValidationExpectedTocSectionsException("Function requires a dict of expected toc sections.")
        obtained_toc_sections = self.article_toc_sections.sections_dict
        if obtained_toc_sections:
            obtained_langs = sorted(list(set(obtained_toc_sections)))
            for lang in obtained_langs:
                obtained_toc_sections_by_lang = obtained_toc_sections.get(lang)
                for obtained in obtained_toc_sections_by_lang:
                    # Valida o valor do atributo subj-group-type
                    if (subject_type := obtained.get("subj_group_type")) != "heading":
                        yield format_response(
                            title="Attribute '@subj-group-type' validation",
                            parent=obtained.get("parent") if obtained else None,
                            parent_id=obtained.get("parent_id") if obtained else None,
                            parent_article_type=obtained.get("parent_article_type") if obtained else None,
                            parent_lang=obtained.get("parent_lang") if obtained else None,
                            item="subj-group",
                            sub_item="@subj-group-type",
                            is_valid=False,
                            validation_type="match",
                            expected="heading",
                            obtained=subject_type,
                            advice="the value for '@subj-group-type' must be heading",
                            data=obtained_toc_sections,
                            error_level=error_level,
                        )

                    else:
                        # Se subj-group-type está correto, valida o título
                        is_valid = False
                        expected = expected_toc_sections.get(lang)
                        obtained_subject = obtained.get('section') if obtained else None
                        validation_type = 'exist'
                        if obtained_subject:
                            # verifica se o título de seção está presente na lista esperada
                            is_valid = obtained_subject.split(":")[0] in expected
                            validation_type = 'value in list'
                        yield format_response(
                            title='Document section title validation',
                            parent=obtained.get("parent") if obtained else None,
                            parent_id=obtained.get("parent_id") if obtained else None,
                            parent_article_type=obtained.get("parent_article_type") if obtained else None,
                            parent_lang=obtained.get("parent_lang") if obtained else None,
                            item="subj-group",
                            sub_item="subject",
                            is_valid=is_valid,
                            validation_type=validation_type,
                            expected=expected if expected else "subject value",
                            obtained=obtained_subject,
                            advice='Provide missing section for language: {}'.format(lang),
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
        article_titles = self.article_titles.article_title_dict

        for lang, sections in obtained_toc_sections.items():
            for section in sections:
                article_title = article_titles.get(lang)
                section_title = section["section"].split(':')[0] if section["section"] else None
                is_valid = article_title != section_title

                yield format_response(
                    title="Document title must not be similar to section title",
                    parent=section.get("parent"),
                    parent_id=section.get("parent_id"),
                    parent_article_type=section.get("parent_article_type"),
                    parent_lang=section.get("parent_lang"),
                    item="subj-group",
                    sub_item="subject",
                    is_valid=is_valid,
                    validation_type="match",
                    expected='\'{}\' (article title) different from \'{}\' (section titles)'.format(article_title, section_title),
                    obtained='article title: \'{}\', section titles: \'{}\''.format(article_title, section_title),
                    advice="Provide different titles for article and section (subj-group[@subj-group-type='heading']/subject)",
                    data=obtained_toc_sections,
                    error_level=error_level,
                )

    def validate_article_section_and_subsection_number(self, error_level="CRITICAL"):
        for lang, subject in self.article_toc_sections.sections_dict.items():
            _subjects = [item.get("section") for item in subject]
            has_multiple_subjects = len(subject) > 1
            has_subsections = len(subject[0].get("subsections", [])) > 0 if not has_multiple_subjects else False

            if has_multiple_subjects:
                yield format_response(
                    title="Multiple Subjects Validation in Article TOC",
                    parent=subject[0].get("parent"),
                    parent_id=subject[0].get("parent_id"),
                    parent_article_type=subject[0].get("parent_article_type"),
                    parent_lang=subject[0].get("parent_lang"),
                    item="subj-group",
                    sub_item="subject",
                    is_valid=False,
                    validation_type="exist",
                    expected="only one subject per language",
                    obtained=" | ".join(_subjects),
                    advice=f"Ensure only one subject per language. Current subjects: {_subjects}.",
                    data=subject,
                    error_level=error_level,
                )
            if has_subsections:
                yield format_response(
                    title="Subsections Validation in Article TOC",
                    parent=subject[0].get("parent"),
                    parent_id=subject[0].get("parent_id"),
                    parent_article_type=subject[0].get("parent_article_type"),
                    parent_lang=subject[0].get("parent_lang"),
                    item="subj-group",
                    sub_item="subsection",
                    is_valid=False,
                    validation_type="exist",
                    expected="Subsections should follow the appropriate structure.",
                    obtained=f"Found subsections in subject: {_subjects[0]}.",
                    advice="Review the subsection structure under each subject.",
                    data=subject,
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
