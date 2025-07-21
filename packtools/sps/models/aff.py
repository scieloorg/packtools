import html
import re


from packtools.sps.utils.xml_utils import (
    node_text_without_fn_xref,
    get_parent_context,
    put_parent_context,
)


def extract_node_text_cleaned(node):
    """
    Retorna o conteúdo textual completo de um nó XML (<aff>, por exemplo),
    com os textos das subtags concatenados, espaços apropriados e texto limpo:

    - Remove múltiplos espaços e quebras de linha
    - Corrige pontuação com espaçamento incorreto (ex: '85. 040' → '85.040')
    - Decodifica entidades HTML
    - Garante separação entre blocos textuais
    """

    # Coleta os textos das subtags em ordem
    texts = [text for text in node.itertext()]

    # Junta os blocos com espaço
    raw_text = " ".join(texts)

    # Remove espaços múltiplos
    cleaned = " ".join(raw_text.split())

    # Corrige espaçamento após ponto decimal (ex: '85. 040' → '85.040')
    cleaned = re.sub(r'(?<=\d)\. (?=\d)', '.', cleaned)

    # Decodifica entidades HTML
    cleaned = html.unescape(cleaned)

    return cleaned


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
        aff_text = node_text_without_fn_xref if subtag else get_node_without_subtag

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
        Retorna lista de afiliações

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

        loc_types = ("state", "city")
        inst_types = ("orgname", "orgdiv1", "orgdiv2", "original", "normalized")

        for node, lang, article_type, parent, parent_id in get_parent_context(
            self._xmltree
        ):

            for aff_node in node.xpath(".//aff"):

                affiliation_id = aff_node.get("id")

                label = aff_node.findtext("label")

                institution = {}
                for inst_type in inst_types:
                    institution[inst_type] = aff_node.findtext(
                        f'institution[@content-type="{inst_type}"]'
                    )

                address = {}
                for loc_type in loc_types:
                    address[loc_type] = aff_node.findtext(f"addr-line/{loc_type}")
                    if not address[loc_type]:
                        address[loc_type] = aff_node.findtext(
                            f'addr-line/named-content[@content-type="{loc_type}"]'
                        )
                address["country_name"] = aff_node.findtext("country")

                try:
                    address["country_code"] = aff_node.find("country").get("country")
                except AttributeError:
                    address["country_code"] = None

                address["email"] = aff_node.findtext("email")

                item = {
                    "id": affiliation_id,
                    "label": label,
                    "original_affiliation_text": extract_node_text_cleaned(aff_node)
                }
                item.update(institution)
                item.update(address)
                yield put_parent_context(item, lang, article_type, parent, parent_id)

    @property
    def affiliation_by_id(self):
        """
        Retorna as afiliações indexadas pelo seu id

        Returns
        -------
        dict of dict, which key is id
        {"aff1":
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
        }
        """
        data = {}
        for item in self.affiliation_list:
            data[item["id"]] = item
        return data
