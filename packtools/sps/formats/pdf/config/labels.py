"""Textos fixos que o PDF gera (títulos padrão), por idioma do documento."""

LABELS = {
    "references": {"en": "References", "pt": "Referências", "es": "Referencias"},
    "appendix": {"en": "Appendix", "pt": "Apêndice", "es": "Apéndice"},
    "supplementary_material": {
        "en": "Supplementary Material",
        "pt": "Material suplementar",
        "es": "Material suplementario",
    },
}

DEFAULT_LANGUAGE = "en"


def label(key, lang=None):
    """
    Devolve o texto fixo no idioma pedido.

    Parâmetros
    ----------
    key : str
        Chave de LABELS (ex. ``"references"``).
    lang : str, optional
        Idioma do documento (``xml:lang``); só o código principal conta
        (``"pt-BR"`` -> ``"pt"``).

    Retorna
    -------
    str
        O texto no idioma; em inglês quando o idioma não está em LABELS.
    """
    texts = LABELS[key]
    return texts.get((lang or "").split("-")[0].lower(), texts[DEFAULT_LANGUAGE])


def has_language(lang):
    """
    Indica se há textos fixos para o idioma.

    Parâmetros
    ----------
    lang : str or None
        Idioma do documento.

    Retorna
    -------
    bool
        True se todas as chaves de LABELS têm o idioma.
    """
    code = (lang or "").split("-")[0].lower()
    return all(code in texts for texts in LABELS.values())
