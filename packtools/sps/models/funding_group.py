import logging

from packtools.sps.utils import xml_utils

logger = logging.getLogger(__name__)


def _looks_like_institution_name(text, special_chars):
    """
    Checks whether all characters in text are alphanumeric, spaces or belong to the list of characters considered valid
     in composing the name of the funding source.

    Example: special_chars = ['.', ',', '-']

    In other words, it checks whether a text is, potentially, the name of a funding source.
    """
    for char in text:
        if not (char.isalpha() or char.isspace() or char in special_chars):
            return False
    return True


def _looks_like_award_id(text):
    # TODO outros casos podem ser considerados, além do DOI
    invalid_patterns = ['doi.org', ]
    for pattern in invalid_patterns:
        if pattern in text:
            return False
    return True


def _get_first_number_sequence(text, special_chars):
    number = ""

    # encontra o primeiro caracter numérico em text
    for i, item in enumerate(text):
        if item.isdigit():
            text = text[i:]
            break
    # pega primeira sequência de caracteres numéricos ou permitidos na lista
    for i, item in enumerate(text):
        if item.isdigit() or item in special_chars:
            number += item
        else:
            break

    return number or None


def has_digit(text):
    for n in range(10):
        if str(n) in text:
            return True
    return False


class FundingGroup:
    """
    Class that performs the extraction of values for funding-source and award-id.
    To return both attributes, award_groups is used.
    To return only institutions, use funding_sources.

    Parameters
    ----------
    xml
        XML file that contains the attributes of interest.

    Returns
    -------
    list
        Arrangement containing a dictionary that correlates funding-source and award-id or values of one of the attributes.
    """

    def __init__(self, xmltree):
        self._xmltree = xmltree

    def fn_financial_information(self, special_chars_funding=None, special_chars_award_id=None):
        if special_chars_award_id is None:
            special_chars_award_id = []
        if special_chars_funding is None:
            special_chars_funding = []
        items = []
        for fn_type in ('financial-disclosure', 'supported-by'):
            funding_sources = []
            award_ids = []
            for nodes in self._xmltree.xpath(f".//fn-group/fn[@fn-type='{fn_type}']"):
                for node in nodes.xpath('p'):
                    text = xml_utils.node_plain_text(node)
                    if has_digit(text):
                        number = _get_first_number_sequence(text, special_chars_award_id)
                        if _looks_like_award_id(text) and number is not None:
                            award_ids.append(number)
                    else:
                        if _looks_like_institution_name(text, special_chars_funding):
                            funding_sources.append(text)

                items.append(
                    {
                        "fn-type": fn_type,
                        "look-like-funding-source": funding_sources,
                        "look-like-award-id": award_ids
                    }
                )
        return items

    @property
    def award_groups(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group"):
            d = {
                "funding-source": [xml_utils.get_node_without_subtag(source) for source in
                                   node.xpath("funding-source")],
                "award-id": [xml_utils.get_node_without_subtag(id) for id in node.xpath("award-id")]
            }
            items.append(d)
        return items

    @property
    def funding_sources(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/funding-source"):
            items.append(xml_utils.get_node_without_subtag(node))
        return items

    @property
    def funding_statement(self):
        """
        De acordo com https://scielo.readthedocs.io/projects/scielo-publishing-schema/pt-br/latest/tagset/elemento-funding-statement.html?highlight=funding-statement
        <funding-statement> ocorre zero ou uma vez.
        """
        return self._xmltree.findtext(".//funding-group/funding-statement")

    @property
    def principal_award_recipients(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/principal-award-recipient"):
            items.append(xml_utils.get_node_without_subtag(node))
        return items

    @property
    def principal_investigators(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/principal-investigator/string-name"):
            d = {
                "given-names": node.findtext("given-names"),
                "surname": node.findtext("surname")
            }
            items.append(d)
        return items

    @property
    def ack(self):
        items = []
        for node in self._xmltree.xpath(".//back//ack"):
            items.append(
                {
                    "title": node.findtext("title"),
                    "text": " ".join([xml_utils.get_node_without_subtag(paragraph) for paragraph in node.xpath("p")])
                }
            )
        return items

    @property
    def article_type(self):
        return self._xmltree.xpath(".")[0].get("article-type")

    @property
    def article_lang(self):
        return self._xmltree.xpath(".")[0].get("{http://www.w3.org/XML/1998/namespace}lang")

    def extract_funding_data(self, funding_special_chars=None, award_id_special_chars=None):
        """
        Extracts various financial and funding-related information from the XML.

        Parameters
        ----------
        funding_special_chars : list, optional
            List of special characters considered valid in the names of funding sources.
        award_id_special_chars : list, optional
            List of special characters considered valid in award IDs.

        Returns
        -------
        dict
            A dictionary containing various pieces of extracted information such as article type, language, financial
            information, award groups, funding sources, funding statement, principal award recipients, and acknowledgments.
        """
        return {
            # Tipo do artigo, obtido do atributo "article-type" no elemento raiz do XML.
            "article_type": self.article_type,
            # Idioma do artigo, obtida do atributo "lang" no namespace XML.
            "article_lang": self.article_lang,
            # Possíveis informações sobre financiamento extraídas do grupo de notas de rodapé financeiro.
            "fn_financial_information": self.fn_financial_information(funding_special_chars, award_id_special_chars),
            # Grupos de concessões, contendo fontes de financiamento e IDs de concessões.
            "award_groups": self.award_groups,
            # Fontes de financiamento listadas em "award-groups".
            "funding_sources": self.funding_sources,
            # Informações sobre financiamento obtidas em "funding-statement".
            "funding_statement": self.funding_statement,
            # Principais destinatários de concessões obtidas em "principal-award-recipient".
            "principal_award_recipients": self.principal_award_recipients,
            # Informações sobre financiamento obtidas em "ack".
            "ack": self.ack
        }

    @property
    def data(self):
        if self.award_groups:
            result = {}
            for item in self.award_groups:
                award_id = item.get("award-id")
                funding_source = item.get("funding-source")
                if award_id and funding_source:
                    for aid in award_id:
                        result[aid] = funding_source
            return result
