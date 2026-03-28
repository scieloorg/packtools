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

from packtools.sps.validation.supplementary_material import XmlSupplementaryMaterialValidation
from packtools.sps.validation.history import HistoryValidation
from packtools.sps.validation.ext_link import ExtLinkValidation
from packtools.sps.validation.list import ArticleListValidation
from packtools.sps.validation.graphic import XMLGraphicValidation


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
    id_and_rid_match_rules = params.get("id_and_rid_match_rules") or {}
    xref_rules = params.get("xref_rules") or {}
    merged_rules = {}
    merged_rules.update(id_and_rid_match_rules)
    merged_rules.update(xref_rules)
    validator = ArticleXrefValidation(xmltree, merged_rules)
    yield from validator.validate_rid_presence()
    yield from validator.validate_ref_type_presence()
    yield from validator.validate_ref_type_value()
    yield from validator.validate_bibr_presence()
    yield from validator.validate_rid_has_corresponding_id()
    yield from validator.validate_transcript_xref()
    yield from validator.validate_aff_self_closing()
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
    
    # Existing validations
    yield from validator.validate_required_award_ids()
    yield from validator.validate_funding_statement()
    
    # New SPS 1.10 validations
    yield from validator.validate_funding_group_uniqueness(
        error_level=funding_data_rules.get("funding_group_uniqueness_error_level", "ERROR")
    )
    yield from validator.validate_funding_statement_presence(
        error_level=funding_data_rules.get("funding_statement_error_level", "CRITICAL")
    )
    yield from validator.validate_funding_source_in_award_group(
        error_level=funding_data_rules.get("funding_source_in_award_group_error_level", "CRITICAL")
    )
    yield from validator.validate_label_absence(
        error_level=funding_data_rules.get("label_absence_error_level", "ERROR")
    )
    yield from validator.validate_title_absence(
        error_level=funding_data_rules.get("title_absence_error_level", "ERROR")
    )
    yield from validator.validate_award_id_funding_source_consistency(
        error_level=funding_data_rules.get("award_id_consistency_error_level", "WARNING")
    )


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
    validator = XmlSupplementaryMaterialValidation(xmltree, rules)
    yield from validator.validate()


def validate_history(xmltree, params):
    """Validate the <history> element according to SPS 1.10 rules."""
    rules = {}
    rules.update(params.get("history_dates_rules", {}))
    validator = HistoryValidation(xmltree, rules)
    yield from validator.validate()

def validate_ext_links(xmltree, params):
    """
    Validates ext-link elements according to SPS 1.10 specification.

    Validates:
    - Mandatory attributes (@ext-link-type, @xlink:href)
    - URL format (must start with http:// or https://)
    - Allowed ext-link-type values
    - Descriptive text (accessibility)
    - @xlink:title requirement for generic/URL text
    """
    ext_link_rules = params["ext_link_rules"]
    validator = ExtLinkValidation(xmltree, ext_link_rules)
    yield from validator.validate_ext_link_type_presence()
    yield from validator.validate_xlink_href_presence()
    yield from validator.validate_xlink_href_format()
    yield from validator.validate_ext_link_type_value()
    yield from validator.validate_descriptive_text()
    yield from validator.validate_xlink_title_when_generic()


def validate_lists(xmltree, params):
    rules = params["list_rules"]
    validator = ArticleListValidation(xmltree, rules)
    
    
def validate_graphics(xmltree, params):
    """
    Validates <graphic> and <inline-graphic> elements according to SPS 1.10 specification.

    Validates:
    - @id attribute (required for both <graphic> and <inline-graphic>)
    - @xlink:href attribute (required, with valid file extension)
    - File extensions (.jpg, .jpeg, .png, .tif, .tiff, .svg)
    - .svg only allowed inside <alternatives>

    Note: Accessibility validation (<alt-text>, <long-desc>) is handled separately
    by validate_accessibility_data() via XMLAccessibilityDataValidation.
    """
    graphic_rules = params["graphic_rules"]
    validator = XMLGraphicValidation(xmltree, graphic_rules)
    yield from validator.validate()
