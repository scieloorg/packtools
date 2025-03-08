from packtools.sps.validation import xml_validations
from packtools.sps.validation.xml_validator_rules import get_default_rules

def validate_xml_content(xmltree, rules):
    params = get_default_rules()
    params.update(rules or {})
    yield {
        "group": "journal-meta",
        "items": xml_validations.validate_journal_meta(xmltree, params),
    }
    yield {
        "group": "bibliographic strip",
        "items": xml_validations.validate_bibliographic_strip(xmltree, params),
    }
    yield {
        "group": "article attributes",
        "items": xml_validations.validate_article(xmltree, params),
    }
    yield {
        "group": "article-id",
        "items": xml_validations.validate_article_ids(xmltree, params),
    }
    yield {
        "group": "article dates",
        "items": xml_validations.validate_article_dates(xmltree, params),
    }
    yield {
        "group": "article languages",
        "items": xml_validations.validate_article_languages(xmltree, params),
    }
    yield {
        "group": "article languages",
        "items": xml_validations.validate_metadata_languages(xmltree, params),
    }
    yield {
        "group": "subject",
        "items": xml_validations.validate_article_toc_sections(xmltree, params),
    }
    yield {
        "group": "article-type",
        "items": xml_validations.validate_article_type(xmltree, params),
    }
    yield {
        "group": "contrib",
        "items": xml_validations.validate_article_contribs(xmltree, params),
    }
    yield {
        "group": "aff",
        "items": xml_validations.validate_affiliations(xmltree, params),
    }
    yield {
        "group": "author-notes",
        "items": xml_validations.validate_author_notes(xmltree, params)
    }
    yield {
        "group": "abstract",
        "items": xml_validations.validate_abstracts(xmltree, params),
    }
    yield {
        "group": "open science",
        "items": xml_validations.validate_open_science_actions(xmltree, params),
    }
    yield {
        "group": "funding data",
        "items": xml_validations.validate_funding_data(xmltree, params),
    }
    yield {
        "group": "id and rid",
        "items": xml_validations.validate_id_and_rid_match(xmltree, params),
    }
    yield {"group": "fig", "items": xml_validations.validate_figs(xmltree, params)}
    yield {
        "group": "table-wrap",
        "items": xml_validations.validate_tablewraps(xmltree, params),
    }
    yield {
        "group": "disp-formula",
        "items": xml_validations.validate_equations(xmltree, params),
    }
    yield {
        "group": "inline-formula",
        "items": xml_validations.validate_inline_equations(xmltree, params),
    }
    yield {
        "group": "reference",
        "items": xml_validations.validate_references(xmltree, params),
    }
    yield {
        "group": "related-article",
        "items": xml_validations.validate_related_articles(xmltree, params),
    }
    yield {
        "group": "fn",
        "items": xml_validations.validate_fns(xmltree, params),
    }
    yield {
        "group": "reviewer-report",
        "items": xml_validations.validate_peer_reviews(xmltree, params),    
    }
