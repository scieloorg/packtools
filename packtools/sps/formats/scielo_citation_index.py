from lxml import etree as ET

from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles


class SciELOCitationConverter:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.article = ArticleAndSubArticles(self.xml_tree)

    def create_articles_tag(self):
        if not (dtd_version := self.article.main_dtd_version):
            raise ValueError("dtd-version is required")

        NSMAP = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}
        schema_location = (
            "https://raw.githubusercontent.com/scieloorg/articles_meta/"
            "master/tests/xsd/scielo_sci/ThomsonReuters_publishing.xsd"
        )
        articles = ET.Element(
            "articles",
            nsmap=NSMAP,
            attrib={
                "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation": schema_location,
                "dtd-version": dtd_version
            }
        )

        return articles

    def create_article_tag(self):
        if not (article_lang := self.article.main_lang):
            raise ValueError("article lang is required")
        if not (article_type := self.article.main_article_type):
            raise ValueError("article type is required")
        article = ET.Element(
            "article",
            attrib={
                "lang_id": article_lang,
                "article-type": article_type
            }
        )

        return article

    def create_article_citation_index(self):
        article_citation_index = self.create_articles_tag()
        article_citation_index.append(self.create_article_tag())

        return article_citation_index
