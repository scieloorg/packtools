def simple_field(key, value):
    if value:
        return {
                key: [
                    {
                        "_": value
                    }
                ]
            }
    return {}


def simple_data(value):
    """
    {
        "_": "Revista Latino-Americana de Enfermagem"
    }
    """
    return {"_": value}

def multiple_simple_data(values):
    """
    [
      {
        "_": "International Nursing Index"
      },
      ...
    ],
    """
    return [simple_data(v) for v in values]

def orcid(author):
    value = author["contrib_ids"]["orcid"]
    if not value:
        value = "ND"
    return {"k": value}

def given_names(author):
    value = author["contrib_name"]["given-names"]
    if not value:
        value = "ND"
    return {"n": value}

def surname(author):
    value = author["contrib_name"]["surname"]
    if not value:
        value = "ND"
    return {"s": value}

def aff_id(author):
    try:
        value = author["affs"][0]["id"]
    except (KeyError, IndexError, TypeError):
        value = "ND"
    return {"1": value}

def role(author):
    try:
        value = author["contrib_role"][0]["text"]
    except (KeyError, IndexError, TypeError):
        value = "ND"
    return {"r": value}

def data(xml_tree):
    journal = journal_meta.Title(xml_tree)
    article_meta = front_articlemeta_issue.ArticleMetaIssue(xml_tree)
    ids = article_ids.ArticleIds(xml_tree)
    authors = article_contribs.XMLContribs(xml_tree)
    return {
        "journal_title": journal.abbreviated_journal_title or None,
        "volume": article_meta.volume or None,
        "code": ids.v2 or None,
        "order": article_meta.order_string_format or None,
        "authors": authors.contribs or None
    }

def field_v30(params):
    title = params["journal_title"]
    if title:
        return {"v30": multiple_simple_data([title])}
    return None

def field_v31(params):
    volume = params["volume"]
    if volume:
        return {"v31": multiple_simple_data([volume])}
    return None

def field_code(params):
    code = params["code"]
    if code:
        return {"code": code}
    return None

def field_v121(params):
    order = params["order"]
    if order:
        return {"v121": multiple_simple_data([order])}
    return None

def field_v10(params):
    authors = params["authors"]
    if not authors:
        return None
    result = []
    for author in authors:
        author_dict = {}
        for extractor in (orcid, given_names, aff_id, surname, role):
            author_dict.update(extractor(author))

        author_dict.update(simple_data(""))
        result.append(author_dict)
    return {"v10": result}
