import itertools

from packtools.sps.utils.xml_utils import (
    node_text_without_xref,
    get_parent_context,
    put_parent_context,
)


def get_node_without_subtag(node):
    """
    Função que retorna nó sem subtags.
    """
    return "".join(node.xpath(".//text()"))


class AffiliationExtractor:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def extract_article_meta(self):
        return self._xmltree.xpath(".//article-meta")

    @property
    def extract_front_stub(self):
        return self._xmltree.xpath(".//front-stub")

    @property
    def extract_contrib_group(self):
        return self._xmltree.xpath(".//contrib-group")

    def extract_affiliation_data(self, nodes, subtag):
        data = []
        address_aff = ["state", "city"]
        institution_aff = ["orgname", "orgdiv1", "orgdiv2", "original"]

        # Define se a extração vai ocorrer com subtags ou sem.
        aff_text = node_text_without_xref if subtag else get_node_without_subtag

        for node in nodes:
            for aff_node in node.xpath("aff"):

                affiliation_id = aff_node.get("id")

                try:
                    label = aff_node.xpath("label")[0].text
                except IndexError:
                    label = None

                institution = {}
                for inst in institution_aff:
                    try:
                        institution[inst] = aff_text(
                            aff_node.xpath(f'institution[@content-type="{inst}"]')[0]
                        )
                    except IndexError:
                        institution[inst] = ""

                address = {}
                for field in address_aff:
                    try:
                        address[field] = aff_text(
                            aff_node.xpath(
                                f'addr-line/named-content[@content-type="{field}"]'
                            )[0]
                        )
                    except IndexError:
                        address[field] = ""

                city = address["city"]
                state = address["state"]

                try:
                    country_node = aff_node.xpath("country")[0]
                    country = aff_text(country_node)
                    country_code = country_node.get("country", "")
                except IndexError:
                    country = ""
                    country_code = ""

                try:
                    email = aff_node.xpath("email")[0].text
                except IndexError:
                    email = ""

                data.append(
                    {
                        "id": affiliation_id,
                        "label": label,
                        "institution": [institution],
                        "city": city,
                        "state": state,
                        "country": [
                            {
                                "code": country_code,
                                "name": country,
                            }
                        ],
                        "email": email,
                    }
                )
        return data

    def get_affiliation_dict(self, subtag):
        data = {}
        for item in self.get_affiliation_data_from_multiple_tags(subtag):
            data[item["id"]] = item
        return data

    def get_affiliation_data_from_multiple_tags(self, subtag):
        list_nodes = []

        article_meta_node = self.extract_article_meta
        front_stub_node = self.extract_front_stub
        contrib_group_node = self.extract_contrib_group

        try:
            if article_meta_node[0].xpath("aff"):
                list_nodes.append(article_meta_node[0])
        except IndexError:
            pass

        try:
            if front_stub_node[0].xpath("aff"):
                list_nodes.append(front_stub_node[0])
        except IndexError:
            pass

        try:
            if contrib_group_node[0].xpath("aff"):
                list_nodes.append(contrib_group_node[0])
        except IndexError:
            pass

        data = self.extract_affiliation_data(nodes=list_nodes, subtag=subtag)

        return data


class Affiliation:
    def __init__(self, xmltree):
        self._xmltree = xmltree

    @property
    def affiliation_list(self):
        """
        Returns a list of affiliations.

        Returns
        -------
        list of dict:
            {
                "id": affiliation_id or None,
                "label": label or None,
                "orgname": orgname or None,
                "orgdiv1": orgdiv1 or None,
                "orgdiv2": orgdiv2 or None,
                "original": original or None,
                "city": city or None,
                "state": state or None,
                "country_name": country_name or None,
                "country_code": country_code or None,
                "email": email or None,
            }
        """
        return list(self._get_affiliations_by_context())

    def _get_affiliations_by_context(self):
        """
        Generator function to get affiliations based on different contexts.
        """
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self._xmltree
        ):
            for aff_node in node.xpath(".//aff"):
                item = self._build_affiliation_item(aff_node, parent)
                yield put_parent_context(item, lang, article_type, parent, parent_id)

    def _build_affiliation_item(self, aff_node, parent):
        """
        Builds the affiliation item dictionary.

        Parameters
        ----------
        aff_node : lxml.etree.Element
            The XML element of the affiliation.
        parent : str
            The parent context.

        Returns
        -------
        dict
            The affiliation item.
        """
        loc_types = ("state", "city")
        inst_types = ("orgname", "orgdiv1", "orgdiv2", "original")

        affiliation_id = aff_node.get("id")
        label = aff_node.findtext("label")

        item = {
            "id": affiliation_id,
            "label": label,
        }

        if parent == "sub-article":
            item["original"] = self._get_institution_info(aff_node, ("original",))[
                "original"
            ]
        else:
            institution = self._get_institution_info(aff_node, inst_types)
            address = self._get_address_info(aff_node, loc_types)
            item.update(institution)
            item.update(address)

        return item

    def _get_institution_info(self, aff_node, inst_types):
        """
        Returns institution information.

        Parameters
        ----------
        aff_node : lxml.etree.Element
            The XML element of the affiliation.
        inst_types : tuple
            Types of institutions to be retrieved.

        Returns
        -------
        dict
            Institution information.
        """
        institution = {}
        for inst_type in inst_types:
            institution[inst_type] = aff_node.findtext(
                f'institution[@content-type="{inst_type}"]'
            )
        return institution

    def _get_address_info(self, aff_node, loc_types):
        """
        Returns address information.

        Parameters
        ----------
        aff_node : lxml.etree.Element
            The XML element of the affiliation.
        loc_types : tuple
            Types of locations to be retrieved.

        Returns
        -------
        dict
            Address information.
        """
        address = {}
        for loc_type in loc_types:
            address[loc_type] = aff_node.findtext(f"addr-line/{loc_type}")
            if not address[loc_type]:
                address[loc_type] = aff_node.findtext(
                    f'addr-line/named-content[@content-type="{loc_type}"]'
                )
        address["country_name"] = aff_node.findtext("country")
        address["country_code"] = self._get_country_code(aff_node)
        address["email"] = aff_node.findtext("email")
        return address

    def _get_country_code(self, aff_node):
        """
        Returns the country code.

        Parameters
        ----------
        aff_node : lxml.etree.Element
            The XML element of the affiliation.

        Returns
        -------
        str or None
            Country code, or None if not found.
        """
        try:
            return aff_node.find("country").get("country")
        except AttributeError:
            return None

    def get_affiliations_article(self):
        """
        Returns affiliations for parent = article.

        Returns
        -------
        dict of dict
            A dictionary of affiliations keyed by affiliation ID.
        """
        affiliations = {}
        for item in self._get_affiliations_by_context():
            if item["parent"] == "article":
                affiliations[item["id"]] = item
        return affiliations

    def get_affiliations_sub_article_translation(self):
        """
        Returns affiliations for parent = sub-article and article-type = translation.

        Returns
        -------
        dict of dict
            A dictionary of affiliations keyed by affiliation ID.
        """
        affiliations = {}
        for item in self._get_affiliations_by_context():
            if (
                item["parent"] == "sub-article"
                and item["parent_article_type"] == "translation"
            ):
                affiliations[item["id"]] = item
        return affiliations

    def get_affiliations_sub_article_non_translation(self):
        """
        Returns affiliations for parent = sub-article and article-type != translation.

        Returns
        -------
        dict of dict
            A dictionary of affiliations keyed by affiliation ID.
        """
        affiliations = {}
        for item in self._get_affiliations_by_context():
            if (
                item["parent"] == "sub-article"
                and item["parent_article_type"] != "translation"
            ):
                affiliations[item["id"]] = item
        return affiliations

    def get_affiliations_article_or_sub_article(self):
        """
        Returns affiliations for parent = article or parent = sub-article.

        Returns
        -------
        dict of dict
            A dictionary of affiliations keyed by affiliation ID.
        """
        return (
            self.get_affiliations_article()
            | self.get_affiliations_sub_article_translation()
        )
