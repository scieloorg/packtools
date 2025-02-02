from packtools.sps.validation.aff import FulltextAffiliationsValidation
from packtools.sps.validation.article_abstract import (
    AbstractsValidation,
    ArticleAbstractsValidation,
    HighlightsValidation,
    VisualAbstractsValidation,
)
from packtools.sps.validation.article_and_subarticles import (
    ArticleAttribsValidation,
    ArticleIdValidation,
    ArticleLangValidation,
    ArticleTypeValidation,
)
from packtools.sps.validation.article_contribs import XMLContribsValidation
from packtools.sps.validation.article_data_availability import (
    DataAvailabilityValidation,
)
from packtools.sps.validation.article_doi import ArticleDoiValidation
from packtools.sps.validation.article_license import ArticleLicenseValidation
from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation
from packtools.sps.validation.article_xref import ArticleXrefValidation
from packtools.sps.validation.author_notes import XMLAuthorNotesValidation
from packtools.sps.validation.dates import FulltextDatesValidation
from packtools.sps.validation.fig import ArticleFigValidation
from packtools.sps.validation.fn import XMLFnGroupValidation
from packtools.sps.validation.formula import (
    ArticleDispFormulaValidation,
    ArticleInlineFormulaValidation,
)
from packtools.sps.validation.funding_group import FundingGroupValidation
from packtools.sps.validation.journal_meta import (
    JournalIdValidation,
    PublisherNameValidation,
    TitleValidation,
)

# PR pendente
# -
from packtools.sps.validation.metadata_langs import MetadataLanguagesValidation
from packtools.sps.validation.peer_review import XMLPeerReviewValidation
from packtools.sps.validation.references import ReferencesValidation

# -
# from packtools.sps.validation.errata import xValidation
# from packtools.sps.validation.erratum import xValidation
# from packtools.sps.validation.preprint import xValidation
from packtools.sps.validation.related_articles import XMLRelatedArticlesValidation
from packtools.sps.validation.tablewrap import ArticleTableWrapValidation

# remover journal
# from packtools.sps.validation.journal import xValidation


# completar
# from packtools.sps.validation.media import xValidation
# from packtools.sps.validation.supplementary_material import xValidation


def validate_affiliations(xmltree, params):
    aff_rules = params["aff_rules"]
    validator = FulltextAffiliationsValidation(xmltree, aff_rules)
    yield from validator.validate()


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
        article_type_accepts=[],
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
        article_type_accepts=highlight_rules["article_type_accepts"],
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
        article_type_accepts=graphical_abstract_rules["article_type_accepts"],
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
    validator = ReferencesValidation(xmltree, references_rules)
    yield from validator.validate()


def validate_article_contribs(xmltree, params):
    rules = {}
    rules.update(params["article_contribs_rules"])

    # callable (customized) which checks orcid is registered
    rules["is_orcid_registered"] = params.get("is_orcid_registered")
    validator = XMLContribsValidation(xmltree, rules)
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
        error_level=id_and_rid_match_rules["required_rid_error_level"],
    )


def validate_article_dates(xmltree, params):
    article_dates_rules = params["article_dates_rules"]
    validator = FulltextDatesValidation(xmltree, article_dates_rules)
    yield from validator.validate()


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
    validator = FundingGroupValidation(xmltree, funding_data_rules)
    yield from validator.validate_required_award_ids()


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


def validate_related_articles(xmltree, params):
    validator = XMLRelatedArticlesValidation(xmltree, params["related_articles_rules"])
    yield from validator.validate()


def validate_fns(xmltree, params):
    validator = XMLFnGroupValidation(xmltree, params["fn_rules"])
    yield from validator.validate()


def validate_author_notes(xmltree, params):
    validator = XMLAuthorNotesValidation(xmltree, params["author_notes_rules"])
    yield from validator.validate()


def validate_peer_reviews(xmltree, params):
    validator = XMLPeerReviewValidation(xmltree, params["peer_review_rules"])
    yield from validator.validate()
