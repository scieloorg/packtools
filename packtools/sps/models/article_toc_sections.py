class ArticleTocSections:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def subj_group_type(self):
        return self.xmltree.findtext('.//article-meta//'
                                     'subj-group[@subj-group-type="heading"]/'
                                     'subject') or ''

    @property
    def subj_group(self):
        return self.xmltree.findtext('.//article-meta//'
                                     'subj-group[@subj-group-type="heading"]/'
                                     'subj-group/subject') or ''
