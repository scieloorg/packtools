from packtools.sps.models.article_dates import ArticleDates
from packtools.sps.validation.aff import AffiliationsValidation
from packtools.sps.validation.article_abstract import (
    ArticleAbstractsValidation, HighlightsValidation,
    VisualAbstractsValidation)
from packtools.sps.validation.article_and_subarticles import (
    ArticleAttribsValidation, ArticleIdValidation, ArticleLangValidation,
    ArticleTypeValidation)
from packtools.sps.validation.references import \
    ArticleReferencesValidation
from packtools.sps.validation.article_contribs import ArticleContribsValidation
from packtools.sps.validation.article_data_availability import \
    DataAvailabilityValidation
from packtools.sps.validation.article_doi import ArticleDoiValidation
from packtools.sps.validation.article_license import ArticleLicenseValidation
from packtools.sps.validation.article_toc_sections import \
    ArticleTocSectionsValidation
from packtools.sps.validation.article_xref import ArticleXrefValidation
from packtools.sps.validation.dates import ArticleDatesValidation
from packtools.sps.validation.fig import ArticleFigValidation
from packtools.sps.validation.tablewrap import ArticleTableWrapValidation
from packtools.sps.validation.formula import ArticleDispFormulaValidation, ArticleInlineFormulaValidation
from packtools.sps.validation.front_articlemeta_issue import Pagination
from packtools.sps.validation.funding_group import FundingGroupValidation
from packtools.sps.validation.journal_meta import (JournalIdValidation,
                                                   PublisherNameValidation,
                                                   TitleValidation)

# remover journal
# from packtools.sps.validation.journal import xValidation



# PR pendente
# from packtools.sps.validation.article_author_notes import xValidation
# from packtools.sps.validation.footnotes import xValidation
# -
from packtools.sps.validation.metadata_langs import MetadataLanguagesValidation
# -
# from packtools.sps.validation.errata import xValidation
# from packtools.sps.validation.erratum import xValidation
# from packtools.sps.validation.peer_review import xValidation
# from packtools.sps.validation.preprint import xValidation
# from packtools.sps.validation.related_articles import xValidation

# completar
# from packtools.sps.validation.media import xValidation
# from packtools.sps.validation.supplementary_material import xValidation


def validate_affiliations(xmltree, params):
    country_codes_list = params["country_codes_list"]

    validator = AffiliationsValidation(xmltree, country_codes_list)

    aff_rules = params["aff_rules"]
    yield from validator.validate_main_affiliations(**aff_rules)

    translated_aff_rules = params["translated_aff_rules"]
    yield from validator.validate_translated_affiliations(**translated_aff_rules)


def validate_abstracts(xmltree, params):

    abstract_rules = params["abstract_rules"]
    validator = ArticleAbstractsValidation(xmltree)
    yield from validator.validate_abstracts_type(
        error_level=abstract_rules["abstract_type_error_level"],
        expected_abstract_type_list=abstract_rules["abstract_type_list"],
    )

    validator = AbstractsValidation(xmltree)
    yield from validator.validate_exists(
        article_type_requires=abstract_rules["article_type_requires"],
        article_type_unexpects=abstract_rules["article_type_unexpects"],
        article_type_neutral=abstract_rules["article_type_neutral"],
        article_type_accepts=[]
    )

    highlight_rules = params["highlight_rules"]

    validator = HighlightsValidation(xmltree)
    yield from validator.validate(
        kwd_error_level=highlight_rules["kwd_error_level"],
        title_error_level=highlight_rules["title_error_level"],
        p_error_level=highlight_rules["p_error_level"],
        list_error_level=highlight_rules["list_error_level"],
    )
    yield validator.validate_exists(
        article_type_requires=[],
        article_type_unexpects=highlight_rules["article_type_unexpects"],
        article_type_neutral=highlight_rules["article_type_neutral"],
        article_type_accepts=highlight_rules["article_type_accepts"]
    )

    graphical_abstract_rules = params["graphical_abstract_rules"]

    validator = VisualAbstractsValidation(xmltree)
    yield from validator.validate(
        kwd_error_level=graphical_abstract_rules["kwd_error_level"],
        title_error_level=graphical_abstract_rules["title_error_level"],
        graphic_error_level=graphical_abstract_rules["graphic_error_level"],
    )
    yield validator.validate_exists(
        article_type_requires=[],
        article_type_unexpects=graphical_abstract_rules["article_type_unexpects"],
        article_type_neutral=graphical_abstract_rules["article_type_neutral"],
        article_type_accepts=graphical_abstract_rules["article_type_accepts"]
    )


def validate_article(xmltree, params):
    article_rules = params["article_rules"]
    specific_use_list = list(article_rules["specific_use_list"].keys())
    sps_version = xmltree.find(".").get("specific-use")
    dtd_version_list = article_rules["specific_use_list"].get(sps_version)

    validator = ArticleAttribsValidation(xmltree)
    yield from validator.validate_specific_use(
        specific_use_list=specific_use_list,
        error_level=article_rules["specific_use_error_level"],
    )
    yield from validator.validate_dtd_version(
        dtd_version_list=dtd_version_list,
        error_level=article_rules["dtd_version_error_level"],
    )


def validate_article_languages(xmltree, params):
    article_languages_rules = params["article_languages_rules"]
    validator = ArticleLangValidation(xmltree)
    yield from validator.validate_language(
        language_codes_list=params["language_codes_list"],
        error_level=article_languages_rules["error_level"],
    )


def validate_article_type(xmltree, params):
    article_type_rules = params["article_type_rules"]
    journal_data = params["journal_data"]

    validator = ArticleTypeValidation(xmltree)
    yield from validator.validate_article_type(
        article_type_list=article_type_rules["article_type_list"],
        error_level=article_type_rules["article_type_error_level"],
    )

    try:
        yield from validator.validate_article_type_vs_subject_similarity(
            subjects_list=journal_data["subjects_list"],
            expected_similarity=article_type_rules[
                "article_type_vs_subject_expected_similarity"
            ],
            error_level=article_type_rules[
                "article_type_vs_subject_expected_similarity_error_level"
            ],
            target_article_types=article_type_rules[
                "article_type_vs_subject_target_article_types"
            ],
        )
    except KeyError:
        pass


def validate_article_ids(xmltree, params):
    article_ids_rules = params["article_ids_rules"]
    article_doi_rules = params["article_doi_rules"]

    validator = ArticleIdValidation(xmltree)
    yield from validator.validate_article_id_other(article_ids_rules["error_level"])

    validator = ArticleDoiValidation(xmltree)
    yield from validator.validate_doi_exists(
        error_level=article_doi_rules["error_level"]
    )

    yield from validator.validate_doi_registered(
        callable_get_data=params.get("doi_api_get"),
        error_level=article_doi_rules["registered_doi_error_level"],
    )
    yield from validator.validate_all_dois_are_unique(
        error_level=article_doi_rules["unique_error_level"]
    )
    yield from validator.validate_different_doi_in_translation(
        error_level=article_doi_rules["translation_doi_error_level"]
    )


def validate_references(xmltree, params):
    references_rules = params["references_rules"]
    validator = ArticleReferencesValidation(xmltree)
    yield from validator.validate()


def validate_article_contribs(xmltree, params):
    is_orcid_registered = params.get("is_orcid_registered")
    article_contribs_rules = params["article_contribs_rules"]
    validator = ArticleContribsValidation(xmltree, article_contribs_rules, is_orcid_registered)
    yield from validator.validate()


def validate_open_science_actions(xmltree, params):
    license_rules = params["license_rules"]
    data_availability_rules = params["data_availability_rules"]

    validator = ArticleLicenseValidation(xmltree)
    try:
        yield validator.validate_license_code(
            expected_code=params["journal_data"]["license_code"],
            error_level=license_rules["error_level"],
        )
    except KeyError:
        pass

    validator = DataAvailabilityValidation(xmltree)
    yield from validator.validate_data_availability(
        specific_use_list=data_availability_rules["specific_use_list"],
        error_level=data_availability_rules["error_level"],
    )


def validate_article_toc_sections(xmltree, params):
    article_toc_section_rules = params["article_toc_section_rules"]

    validator = ArticleTocSectionsValidation(xmltree)

    try:
        yield from validator.validate_article_toc_sections(
            expected_toc_sections=params["journal_data"]["subjects_list"],
            error_level=article_toc_section_rules["error_level"],
        )
    except KeyError:
        pass

    yield from validator.validade_article_title_is_different_from_section_titles(
        error_level=article_toc_section_rules["similar_to_article_title_error_level"]
    )

    yield from validator.validate_article_section_and_subsection_number(
        error_level=article_toc_section_rules["unexpected_subsection_error_level"]
    )


def validate_id_and_rid_match(xmltree, params):
    id_and_rid_match_rules = params["id_and_rid_match_rules"]

    validator = ArticleXrefValidation(xmltree)
    yield from validator.validate_xref_rid_has_corresponding_element_id(
        error_level=id_and_rid_match_rules["required_id_error_level"]
    )

    yield from validator.validate_element_id_has_corresponding_xref_rid(
        id_and_rid_match_rules["elements_required_rid"],
        error_level=id_and_rid_match_rules["required_rid_error_level"]
    )
    


def validate_article_dates(xmltree, params):
    article_dates_rules = params["article_dates_rules"]
    history_dates_rules = params["history_dates_rules"]
    related_article_rules = params["related_article_rules"]

    validator = ArticleDatesValidation(xmltree)
    yield from validator.validate_number_of_digits_in_article_date(
        error_level=article_dates_rules["article_date_format_error_level"]
    )
    result = validator.validate_article_date(
        error_level=article_dates_rules["article_date_value_error_level"]
    )
    if result:
        yield result

    result = validator.validate_collection_date(
        error_level=article_dates_rules["collection_date_value_error_level"]
    )
    if result:
        yield result

    # TODO required_events depends on article_type

    required_events = [
        item["type"] for item in history_dates_rules["date_list"] if item["required"]
    ]

    # FIXME
    # try:
    #     for related_article in related_articles:
    #         required_events.append(
    #             related_article_rules["required_history_events"][related_article_type]
    #         )
    # except KeyError:
    #     pass
    order = [item["type"] for item in history_dates_rules["date_list"]]
    yield from validator.validate_history_dates(
        order=order,
        required_events=required_events,
        error_level=history_dates_rules["error_level"],
    )

    # FIXME remover validate() que usa métodos inexistentes


def validate_figs(xmltree, params):
    rules = params["fig_rules"]
    rules.update(params["article_type_rules"])
    validator = ArticleFigValidation(xmltree, rules)
    yield from validator.validate()


def validate_tablewraps(xmltree, params):
    rules = params["table_wrap_rules"]
    rules.update(params["article_type_rules"])
    validator = ArticleTableWrapValidation(xmltree, rules)
    yield from validator.validate()


def validate_equations(xmltree, params):
    rules = params["disp_formula_rules"]
    rules.update(params["article_type_rules"])
    validator = ArticleDispFormulaValidation(xmltree, rules)
    yield from validator.validate()


def validate_inline_equations(xmltree, params):
    rules = params["inline_formula_rules"]
    rules.update(params["article_type_rules"])
    validator = ArticleInlineFormulaValidation(xmltree, rules)
    yield from validator.validate()


def validate_bibliographic_strip(xmltree, params):
    pagination_rules = params["pagination_rules"]

    # TODO adicionar error_level, corrigir o nome da classe
    # FIXME
    #   File "/Users/roberta.takenaka/github.com/scieloorg/packtools/packtools/packtools/sps/validation/front_articlemeta_issue.py", line 391, in validation_pagination_attributes_exist
    # yield format_response(
    # TypeError: format_response() missing 3 required positional arguments: 'parent_article_type', 'parent_lang', and 'error_level'

    # validator = Pagination(xmltree)
    # yield from validator.validation_pagination_attributes_exist(
    #     # error_level=pagination_rules["error_level"],
    # )


def validate_funding_data(xmltree, params):
    funding_data_rules = params["funding_data_rules"]

    # FIXME o nome do método não está condizendo com o que está fazendo, que é validar source + award-id; usar verbo para o método
    # TODO a classe deve ter um método que identifique se nos elementos fn e ack há algum número que possa ser do número do contrato e que não esteja identificado como award-id
    validator = FundingGroupValidation(xmltree)
    yield from validator.funding_sources_exist_validation(
        error_level=funding_data_rules["error_level"],
    )


def validate_journal_meta(xmltree, params):
    # FIXME nome dos métodos devem ser verbos validate()

    try:
        journal_data = params["journal_data"]
        if not journal_data:
            return
    except KeyError:
        pass

    journal_rules = params["journal_rules"]
    validator = TitleValidation(xmltree)

    yield from validator.abbreviated_journal_title_validation(
        expected_value=journal_data["abbrev_journal_title"],
        error_level=journal_rules["abbrev_journal_title_error_level"],
    )

    validator = PublisherNameValidation(xmltree)
    yield from validator.validate_publisher_names(
        publisher_name_list=journal_data["publisher_name_list"],
        error_level=journal_rules["publisher_name_list_error_level"],
    )

    try:
        validator = JournalIdValidation(xmltree)
        yield from validator.nlm_ta_id_validation(
            expected_value=journal_data["nlm_journal_title"],
            error_level=journal_rules["nlm_journal_title_error_level"],
        )
    except KeyError:
        pass


def validate_metadata_languages(xmltree, params):
    validator = MetadataLanguagesValidation(xmltree)
    yield from validator.validate(params["metadata_languages_rules"]["error_level"])


