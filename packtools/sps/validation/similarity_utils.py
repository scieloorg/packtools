import difflib


def how_similar(this, that):
    if this is None:
        this = 'None'
    if that is None:
        that = 'None'
    return difflib.SequenceMatcher(None, this.lower(), that.lower()).ratio()


def most_similar(similarity_scores):
    best_score = 0.0
    best_matches = []
    
    if not similarity_scores:
        return best_score, best_matches
        
    # Encontra a maior taxa de similaridade
    best_score = max(similarity_scores.keys())
    
    # Obtém a lista de itens correspondentes à maior taxa
    best_matches = similarity_scores[best_score]
    
    return best_score, best_matches


def similarity(items, text, min_ratio=0):
    r = {}
    for item in items:
        rate = how_similar(item, text)
        if rate > min_ratio:
            if rate not in r.keys():
                r[rate] = []
            r[rate].append(item)
    return r
