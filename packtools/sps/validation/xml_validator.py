from packtools.sps.validation import xml_validations


def validate_xml_content(xmltree, rules):
    params = rules.params
    yield {
        "group": "journal_meta",
        "items": xml_validations.validate_journal_meta(xmltree, params),
    }
    yield {
        "group": "bibliographic_strip",
        "items": xml_validations.validate_bibliographic_strip(xmltree, params),
    }
    yield {
        "group": "article",
        "items": xml_validations.validate_article(xmltree, params),
    }
    yield {
        "group": "article_ids",
        "items": xml_validations.validate_article_ids(xmltree, params),
    }
    yield {
        "group": "article_dates",
        "items": xml_validations.validate_article_dates(xmltree, params),
    }
    yield {
        "group": "article_languages",
        "items": xml_validations.validate_article_languages(xmltree, params),
    }
    yield {
        "group": "article_toc_sections",
        "items": xml_validations.validate_article_toc_sections(xmltree, params),
    }
    yield {
        "group": "article_type",
        "items": xml_validations.validate_article_type(xmltree, params),
    }
    yield {
        "group": "article_contribs",
        "items": xml_validations.validate_article_contribs(xmltree, params),
    }
    yield {
        "group": "aff",
        "items": xml_validations.validate_affiliations(xmltree, params),
    }
    yield {
        "group": "abstract",
        "items": xml_validations.validate_abstracts(xmltree, params),
    }
    yield {
        "group": "open_science_actions",
        "items": xml_validations.validate_open_science_actions(xmltree, params),
    }
    yield {
        "group": "funding_data",
        "items": xml_validations.validate_funding_data(xmltree, params),
    }
    yield {
        "group": "id and rid match",
        "items": xml_validations.validate_id_and_rid_match(xmltree, params),
    }
    yield {"group": "figs", "items": xml_validations.validate_figs(xmltree, params)}
    yield {
        "group": "article_references",
        "items": xml_validations.validate_references(xmltree, params),
    }
