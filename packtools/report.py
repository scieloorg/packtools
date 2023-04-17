from packtools.sps.validation import (
    aff,
    article_authors,
    article_license,
    article_toc_sections,
    article_xref,
    dates,
    front_articlemeta_issue
)        

def all_classes():
    classes = [
        aff.AffiliationValidation,
        article_authors.ArticleAuthorsValidation, # Necessita de CreditTerms
        article_license.ArticleLicenseValidation, # Necessida de Parametros expected value
        # article_toc_sections.ArticleTocSectionsValidation, # Necessida de Parametros expected value
        article_xref.ArticleXrefValidation,
        dates.ArticleDatesValidation, # Necessita de parametros order date
        front_articlemeta_issue.IssueValidation, # Necessida de parametros expected value
    ]
    return classes

class ReportXML:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def report(self):
        report = []
        for cla in all_classes():
            report.append(cla(self.xmltree).call_methods)
        import ipdb; ipdb.set_trace()