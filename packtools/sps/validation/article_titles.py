from packtools.sps.models.article_titles import ArticleTitles


class ArticleTitlesValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.title = ArticleTitles(xmltree)

    def validate_article_title(self, expected_value):
        result = dict(
            expected_value=expected_value,
            obteined_value=self.title.article_title,
            match=expected_value == self.title.article_title
        )

        return result

    def validate_sub_article_title(self, expected_value):
        result = dict(
            expected_value=expected_value,
            obteined_value=self.title.sub_article_titles,
            match=expected_value == self.title.sub_article_titles
        )

        return result

    def validate_trans_title(self, expected_value):
        result = dict(
            expected_value=expected_value,
            obteined_value=self.title.trans_titles,
            match=expected_value == self.title.trans_titles
        )

        return result

    def validate_article_title_differs_from_trans_title(self):
        title = self.title.article_title
        trans = self.title.trans_titles

        return title not in trans
