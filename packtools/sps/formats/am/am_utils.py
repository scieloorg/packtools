def simple_field(key, value):
    if value:
        return {key: [{"_": value}]}
    return {}


def complex_field(key, value):
    if value:
        return {key: [value]}
    return {}


def add_item(dictionary, key, value):
    if value is not None:
        dictionary[key] = value


def multiple_complex_field(key, value_list):
    if value_list:
        return {key: value_list}
    return {}

def format_date(date_dict, fields):
    """
    Concatena campos de uma data (como 'year', 'month', 'day') em uma string compacta.
    Retorna None se o dicionário for None ou se todos os campos estiverem ausentes.
    """
    if not date_dict:
        return None
    parts = [date_dict.get(field, "") for field in fields]
    return "".join(parts) if any(parts) else None

ARTICLE_TYPE_MAP = {
    "research-article": "oa",
    "editorial": "ed",
    "abstract": "ab",
    "announcement": "an",
    "article-commentary": "co",
    "case-report": "cr",
    "letter": "le",
    "review-article": "ra",
    "rapid-communication": "sc",
    "addendum": "addendum",
    "book-review": "rc",
    "books-received": "books-received",
    "brief-report": "rn",
    "calendar": "calendar",
    "clinical-trial": "oa",
    "collection": "zz",
    "correction": "er",
    "discussion": "discussion",
    "dissertation": "dissertation",
    "editorial-material": "ed",
    "in-brief": "pr",
    "introduction": "ed",
    "meeting-report": "meeting-report",
    "news": "news",
    "obituary": "obituary",
    "oration": "oration",
    "partial-retraction": "partial-retraction",
    "product-review": "product-review",
    "reply": "reply",
    "reprint": "reprint",
    "retraction": "re",
    "translation": "translation",
    "technical-report": "oa",
    "other": "zz",
    "guideline": "guideline",
    "interview": "in",
    "data-article": "data-article",
}
