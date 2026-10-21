"""Constantes de citação reutilizáveis: estilos CSL e frases de "como citar"."""

import re
from pathlib import Path

CITATION_STYLES_DIR = Path(__file__).parent / "citation_styles"
# Herdado do old_pdf: só existe o estilo 'vancouver', uma variante do CSL
# "nlm-name-year" adaptada para o SciELO (ver o próprio .csl). O nome é um
# parâmetro para que uma configuração por periódico possa escolher outro .csl.
CITATION_STYLES = {"vancouver": "scielo_nlm_name_year.csl"}

# Herdado do old_pdf (#1349): frases (pt/en) que identificam a nota "como
# citar este artigo" pelo rótulo ou pelo início do <p>. fn-type="other" é um
# balaio genérico (agradecimento institucional, uso de IA, códigos JEL...), então
# pegar a primeira <fn fn-type="other"> punha a nota errada no rodapé; procurar
# só 'cit' no texto dava falso positivo/negativo.
CITE_AS_PHRASES = (
    r"como\s+citar",
    r"cita(?:ç|c)[aã]o\s+sugerida",
    r"cite\s+this\s+article\s+as",
    r"how\s+to\s+cite\s+this\s+article",
    r"how\s+to\s+cite",
    r"cite\s+as",
)
CITE_AS_RE = re.compile("|".join(CITE_AS_PHRASES), re.IGNORECASE)
CITE_AS_LEADING_RE = re.compile(
    r"^\s*(?:" + "|".join(CITE_AS_PHRASES) + r")\s*:?\s*", re.IGNORECASE
)
