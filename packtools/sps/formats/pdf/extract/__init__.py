"""
Extração: XML SPS -> blocos e runs (dicts), sem nada de DOCX.

Um módulo por família de elementos, nomeado pelo elemento principal:

- folhas reaproveitadas: ``title`` (label, title, caption), ``link`` (xref,
  ext-link), ``styles`` (italic, bold, sup... e break), ``graphic``,
  ``formula``;
- corpo: ``sec`` (sec e afins, p, app-group, disp-quote, preformat, fn),
  ``list_`` (list, def-list), ``table`` (table-wrap, table, alternatives),
  ``fig`` (fig, fig-group, table-wrap-group), ``ref_list`` (ref-list, ref),
  ``supplementary_material``;
- capa: ``article_meta`` (metadados, title-group), ``contrib_group``
  (contrib, aff, author-notes), ``abstract`` (abstract, kwd-group),
  ``citation`` (rodapé "como citar");
- base: ``runs``, ``registry``, ``context``, ``inline``, ``flow``,
  ``nodes``, ``languages``; e ``article``, que monta o documento.

Cada módulo de elemento registra seus handlers em registry.INLINE /
registry.BLOCK ao ser importado; por isso todos são importados aqui, e quem
usa o pacote (``extract.article``) já encontra o registro completo.
Elemento sem handler não se perde: vira contêiner genérico (ver
flow.handle_container).
"""

from packtools.sps.formats.pdf.extract import (  # noqa: F401  (registram handlers)
    fig,
    formula,
    graphic,
    link,
    list_,
    ref_list,
    sec,
    styles,
    supplementary_material,
    table,
)
