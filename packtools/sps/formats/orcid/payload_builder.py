from packtools.sps.models.article_contribs import Contrib
from packtools.sps.models.article_titles import ArticleTitles
from packtools.sps.models.journal_meta import Title
from packtools.sps.models.dates import XMLDates
from packtools.sps.models.article_doi_with_lang import DoiWithLang
from packtools.sps.models.aff import Affiliation
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles


class Author:
    def __init__(self, author_node, affs):
        self.author_obj = Contrib(author_node)
        self.name = self.author_obj.contrib_full_name
        self.orcid = self.author_obj.contrib_ids.get("orcid")
        self.affs = affs

    @property
    def email(self):
        for item in list(self.author_obj.contrib_xref):
            if rid := item.get("rid"):
                if email := self.affs.get(rid, {}).get("email"):
                    return email

    @property
    def data(self):
        if not (self.orcid and self.name):  # Obrigatórios
            return None
        return {
            "orcid_id": self.orcid,
            "author_email": self.email,
            "author_name": self.name,
        }


class Authors:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def affs(self):
        return Affiliation(self.xml_tree).affiliation_by_id

    @property
    def data(self):
        for author in self.xml_tree.xpath(".//contrib"):
            yield Author(author, self.affs).data


class Work:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.article_title = (ArticleTitles(xml_tree).article_title or {}).get(
            "plain_text"
        )
        self.journal_title = Title(xml_tree).journal_title
        self.article_type = ArticleAndSubArticles(xml_tree).main_article_type

    @property
    def pub_date(self):
        dates = XMLDates(self.xml_tree)
        pub_date_data = dates.epub_date or dates.collection_date

        if not pub_date_data or not pub_date_data.get("year"):
            return None

        pub_date = {"year": {"value": str(pub_date_data["year"])}}

        if month := pub_date_data.get("month"):
            pub_date["month"] = {"value": str(month).zfill(2)}

        if day := pub_date_data.get("day"):
            pub_date["day"] = {"value": str(day).zfill(2)}

        return pub_date

    @property
    def external_ids(self):
        """Extrai IDs externos usando DoiWithLang (obrigatório)"""
        doi_extractor = DoiWithLang(self.xml_tree)
        doi = doi_extractor.main_doi

        if not doi or not doi.strip():
            return None  # DOI é obrigatório

        external_ids = {
            "external-id": [
                {
                    "external-id-type": "doi",
                    "external-id-value": doi.strip(),
                    "external-id-url": {"value": f"https://doi.org/{doi.strip()}"},
                }
            ]
        }

        return external_ids

    @property
    def data(self):
        if not (
            self.article_title and self.journal_title and self.article_type
        ):  # Obrigatórios
            return None
        data = {
            "work_data": {
                "title": {
                    "title": {"value": self.article_title},
                },
                "journal-title": {"value": self.journal_title},
                "type": self.article_type,
            }
        }
        if not self.pub_date:
            return None
        data.update(self.pub_date)  # Obrigatório ano

        if self.external_ids:
            data.update(self.external_ids)  # Opcional

        return data


def build_payload(xml_tree):
    work_data = Work(xml_tree).data
    if not work_data:
        return

    for author_data in Authors(xml_tree).data:
        if author_data:
            yield {**author_data, **work_data}
