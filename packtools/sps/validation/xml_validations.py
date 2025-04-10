from packtools.sps.validation.aff import FulltextAffiliationsValidation
from packtools.sps.validation.article_abstract import (
    XMLAbstractsValidation,
)
from packtools.sps.validation.article_and_subarticles import (
    ArticleIdValidation,
    ArticleLangValidation,
    ArticleTypeValidation,
    JATSAndDTDVersionValidation,
)
from packtools.sps.validation.article_contribs import XMLContribsValidation
from packtools.sps.validation.article_data_availability import (
    DataAvailabilityValidation,
)
from packtools.sps.validation.article_doi import ArticleDoiValidation
from packtools.sps.validation.article_license import ArticleLicenseValidation
from packtools.sps.validation.article_toc_sections import XMLTocSectionsValidation
from packtools.sps.validation.article_xref import ArticleXrefValidation
from packtools.sps.validation.author_notes import XMLAuthorNotesValidation
from packtools.sps.validation.dates import FulltextDatesValidation
from packtools.sps.validation.fig import ArticleFigValidation
from packtools.sps.validation.fn import XMLFnGroupValidation
from packtools.sps.validation.formula import (
    ArticleDispFormulaValidation,
    ArticleInlineFormulaValidation,
)
from packtools.sps.validation.front_articlemeta_issue import (
    PaginationValidation,
    IssueValidation,
)
from packtools.sps.validation.funding_group import FundingGroupValidation
from packtools.sps.validation.journal_meta import (
    JournalIdValidation,
    PublisherNameValidation,
    TitleValidation,
)
from packtools.sps.validation.metadata_langs import MetadataLanguagesValidation
from packtools.sps.validation.peer_review import XMLPeerReviewValidation
from packtools.sps.validation.references import ReferencesValidation
from packtools.sps.validation.related_articles import XMLRelatedArticlesValidation
from packtools.sps.validation.tablewrap import ArticleTableWrapValidation

from packtools.sps.validation.media import XMLMediaValidation
from packtools.sps.validation.accessibility_data import XMLAccessibilityDataValidation
from packtools.sps.validation.app_group import AppValidation

# from packtools.sps.validation.supplementary_material import XMLSupplementaryMaterialValidation


def validate_affiliations(xmltree, params):
    aff_rules = {}
    aff_rules.update(params["aff_rules"])
    aff_rules["country_codes_list"] = params["country_codes_list"]
    validator = FulltextAffiliationsValidation(xmltree, aff_rules)
    yield from validator.validate()


def validate_abstracts(xmltree, params):
    validator = XMLAbstractsValidation(xmltree, params)
    yield from validator.validate()


def validate_article(xmltree, params):
    validator = JATSAndDTDVersionValidation(xmltree, params["article_rules"])
    yield from validator.validate()


def validate_article_languages(xmltree, params):
    rules = {}
    rules.update(params["article_languages_rules"])
    rules["language_codes_list"] = params["language_codes_list"]
    validator = ArticleLangValidation(xmltree, rules)
    yield from validator.validate_language()


def validate_article_type(xmltree, params):
    article_type_rules = params["article_type_rules"]

    rules = {}
    rules.update(article_type_rules)
    rules["journal_data"] = params["journal_data"]

    validator = ArticleTypeValidation(xmltree, rules)
    yield from validator.validate_article_type()
    yield from validator.validate_article_type_vs_subject_similarity()


def validate_article_ids(xmltree, params):

    validator = ArticleIdValidation(xmltree, params["article_ids_rules"])
    yield from validator.validate_article_id_other()

    article_doi_rules = params["article_doi_rules"]
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
        yield from validator.validate_license_code(
            expected_code=params["journal_data"]["license_code"],
            error_level=license_rules["error_level"],
        )
    except (TypeError, KeyError):
        pass

    validator = DataAvailabilityValidation(xmltree, data_availability_rules)
    yield from validator.validate_data_availability()

    validator = XMLFnGroupValidation(xmltree, params["fn_rules"])
    yield from validator.validate_edited_by()


def validate_article_toc_sections(xmltree, params):
    rules = {}
    rules["journal_data"] = params.get("journal_data")
    rules.update(params["article_toc_section_rules"])

    validator = XMLTocSectionsValidation(xmltree, rules)
    yield from validator.validate()


def validate_id_and_rid_match(xmltree, params):
    id_and_rid_match_rules = params["id_and_rid_match_rules"]
    validator = ArticleXrefValidation(xmltree, id_and_rid_match_rules)
    yield from validator.validate_xref_rid_has_corresponding_element_id()
    yield from validator.validate_element_id_has_corresponding_xref_rid()
    yield from validator.validate_attrib_name_and_value_has_corresponding_xref()


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
    rules = {}
    rules.update(params)

    validator = IssueValidation(xmltree, rules)
    yield from validator.validate()

    validator = PaginationValidation(xmltree, rules)
    yield validator.validate()


def validate_funding_data(xmltree, params):
    funding_data_rules = params["funding_data_rules"]
    validator = FundingGroupValidation(xmltree, funding_data_rules)
    yield from validator.validate_required_award_ids()
    yield from validator.validate_funding_statement()


def validate_journal_meta(xmltree, params):
    # FIXME nome dos métodos devem ser verbos validate()

    try:
        journal_data = params["journal_data"]
        if not journal_data:
            return
    except KeyError:
        return

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
    except (TypeError, KeyError):
        pass


def validate_metadata_languages(xmltree, params):
    validator = MetadataLanguagesValidation(xmltree)
    yield from validator.validate(params["metadata_languages_rules"]["error_level"])


def validate_related_articles(xmltree, params):
    validator = XMLRelatedArticlesValidation(xmltree, params["related_article_rules"])
    yield from validator.validate()


def validate_fns(xmltree, params):
    validator = XMLFnGroupValidation(xmltree, params["fn_rules"])
    yield from validator.validate()


def validate_author_notes(xmltree, params):
    validator = XMLAuthorNotesValidation(xmltree, params["author_notes_rules"])
    yield from validator.validate()


def validate_peer_reviews(xmltree, params):
    rules = {}
    rules.update(params["related_article_rules"])
    rules.update(params["peer_review_rules"])

    validator = XMLPeerReviewValidation(xmltree, rules)
    yield from validator.validate()


def validate_accessibility_data(xmltree, params):
    rules = {}
    rules.update(params["accessibility_data_rules"])
    validator = XMLAccessibilityDataValidation(xmltree, rules)
    yield from validator.validate()


def validate_media(xmltree, params):
    rules = {}
    rules.update(params["visual_resource_base_rules"])
    validator = XMLMediaValidation(xmltree, rules)
    yield from validator.validate()


def validate_app_group(xmltree, params):
    rules = {}
    rules.update(params["app_group_rules"])
    validator = AppValidation(xmltree, rules)
    yield from validator.validate()


def validate_supplementary_materials(xmltree, params):
    # TODO
    rules = {}
    rules.update(params["supplementary_materials_rules"])
    validator = XMLSupplementaryMaterialValidation(xmltree, rules)
    yield from validator.validate()
