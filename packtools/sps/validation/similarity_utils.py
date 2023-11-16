import difflib


def how_similar(this, that):
    if this is None:
        this = 'None'
    if that is None:
        that = 'None'
    return difflib.SequenceMatcher(None, this.lower(), that.lower()).ratio()


def most_similar(similarity):
    items = []
    highiest_rate = 0
    ratio_list = similarity.keys()
    if len(ratio_list) > 0:
        ratio_list = sorted(ratio_list)
        ratio_list.reverse()
        highiest_rate = ratio_list[0]
        items = similarity[highiest_rate]

    return highiest_rate, items


def similarity(items, text, min_ratio=0):
    r = {}
    for item in items:
        rate = how_similar(item, text)
        if rate > min_ratio:
            if rate not in r.keys():
                r[rate] = []
            r[rate].append(item)
    return r


SUBJECTS_VS_ARTICLE_TYPE = dict([
    ('original article', 'research-article'),
    ('artigo original', 'research-article'),
    ('artículo original', 'research-article'),
    ('artigo', 'research-article'),
    ('relatório técnico', 'research-article'),
    ('informe técnico', 'research-article'),
    ('technical report', 'research-article'),
    ('comment', 'article-commentary'),
    ('coment', 'article-commentary'),
    ('updat', 'rapid-communication'),
    ('actualiza', 'rapid-communication'),
    ('atualiza', 'rapid-communication'),
    ('comunica', 'rapid-communication'),
    ('communica', 'rapid-communication'),
    ('brief report', 'brief-report'),
    ('nota de pesquisa', 'brief-report'),
    ('nota de investigación', 'brief-report'),
    ('research note', 'brief-report'),
    ('informe de caso', 'case-report'),
    ('relato de caso', 'case-report'),
    ('case report', 'case-report'),
    ('errata', 'correction'),
    ('erratum', 'correction'),
    ('interview', 'other'),
    ('point-of-view', 'editorial'),
    ('entrevista', 'other'),
    ('punto de vista', 'editorial'),
    ('ponto de vista', 'editorial'),
    ('letter', 'letter'),
    ('carta', 'letter'),
    ('reply', 'letter'),
    ('correspond', 'letter'),
    ('retraction', 'retraction'),
    ('retratación', 'retraction'),
    ('retractación', 'retraction'),
    ('retratação', 'retraction'),
    ('book review', 'book-review'),
    ('reseña', 'book-review'),
    ('resenha', 'book-review'),
    ('review', 'review-article'),
    ('revisão', 'review-article'),
    ('revisión', 'review-article'),
    ('resum', 'abstract'),
    ('parecer', 'referee-report'),
    ('peer review', 'referee-report'),
])
