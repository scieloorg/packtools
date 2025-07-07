import logging
from packtools.sps.utils import xml_utils
from packtools.sps.models.article_and_subarticles import Fulltext


logger = logging.getLogger(__name__)


def _looks_like_award_id(text):
    # TODO outros casos podem ser considerados, além do DOI
    invalid_patterns = [
        "doi.org",
    ]
    for pattern in invalid_patterns:
        if pattern in text:
            return False
    return True


def looks_like_award_ids(text, special_chars_award_id):
    items = []
    if has_digit(text):
        for word in text.split():
            if word.isalpha():
                continue
            if len(word) < 5:
                continue
            if has_digit(word):
                if _looks_like_award_id(word):
                    contract_number = []
                    for c in word:
                        if c.isalnum():
                            contract_number.append(c)
                        elif c in special_chars_award_id:
                            if len(contract_number) > 0:
                                contract_number.append(c)
                    while True:
                        if contract_number[-1] in special_chars_award_id:
                            contract_number = contract_number[:-1]
                        else:
                            break
                    items.append("".join(contract_number))
    return items


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
    params : dict
        Dictionary containing special characters configuration:
        - special_chars_funding: List of special characters allowed in funding source names
        - special_chars_award_id: List of special characters allowed in award IDs

    Returns
    -------
    list
        Arrangement containing a dictionary that correlates funding-source and award-id or values of one of the attributes.
    """

    def __init__(self, xmltree, params=None):
        self._xmltree = xmltree
        self.params = params or {"special_chars_award_id": ["/", ".", "-"]}

    def _process_paragraph_node(self, node):
        """
        Process a single paragraph node to extract award IDs.

        Parameters
        ----------
        node : lxml.etree.Element
            The paragraph node to process

        Returns
        -------
        dict
            Dictionary containing extracted award IDs and original text
        """
        text = " ".join(node.xpath(".//text()"))
        award_ids = list(looks_like_award_ids(text, self.params["special_chars_award_id"]))
        return {"look-like-award-id": award_ids, "text": text}

    @property
    def financial_disclosure(self):
        """
        Extract financial disclosure information from fn nodes.
        Returns a list of dictionaries containing award IDs and text found in financial-disclosure notes.
        """
        items = []
        for nodes in self._xmltree.xpath(
            ".//fn-group/fn[@fn-type='financial-disclosure']"
        ):
            for node in nodes.xpath("p"):
                node_data = self._process_paragraph_node(node)
                node_data["context"] = "financial-disclosure"
                items.append(node_data)
        return items

    @property
    def supported_by(self):
        """
        Extract supported-by information from fn nodes.
        Returns a list of dictionaries containing award IDs and text found in supported-by notes.
        """
        items = []
        for nodes in self._xmltree.xpath(".//fn-group/fn[@fn-type='supported-by']"):
            for node in nodes.xpath("p"):
                node_data = self._process_paragraph_node(node)
                node_data["context"] = "supported-by"
                items.append(node_data)
        return items

    @property
    def award_groups(self):
        """
        Extract award groups information from funding-group.
        Returns a list of dictionaries containing funding sources and award IDs.
        """
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group"):
            d = {
                "funding-source": [
                    xml_utils.get_node_without_subtag(source)
                    for source in node.xpath("funding-source")
                ],
                "award-id": [
                    xml_utils.get_node_without_subtag(id)
                    for id in node.xpath("award-id")
                ],
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
    def award_ids(self):
        items = []
        for node in self._xmltree.xpath(".//funding-group/award-group/award-id"):
            if node.text:
                items.append(node.text)
        return items

    @property
    def funding_statement(self):
        """
        De acordo com https://scielo.readthedocs.io/projects/scielo-publishing-schema/pt-br/latest/tagset/elemento-funding-statement.html?highlight=funding-statement
        <funding-statement> ocorre zero ou uma vez.

        Retorna o texto do funding-statement com espaços e quebras de linha normalizados.
        Se não houver o elemento, retorna None.
        """
        el = self._xmltree.find(".//funding-group/funding-statement")
        if el is None:
            return None
        # Obtem o texto bruto (com conteúdo de elementos filhos, se houver)
        raw_text = "".join(el.itertext())
        # Limpa quebras de linha e espaços duplicados
        cleaned_text = " ".join(raw_text.split())
        return cleaned_text if cleaned_text else None

    @property
    def funding_statement_data(self):
        node = self._xmltree.find(".//funding-group/funding-statement")
        items = []
        if node is not None:
            data = self._process_paragraph_node(node)
            data["context"] = "funding-statement"
            items.append(data)
        return items

    @property
    def principal_award_recipients(self):
        items = []
        for node in self._xmltree.xpath(
            ".//funding-group/award-group/principal-award-recipient"
        ):
            items.append(xml_utils.get_node_without_subtag(node))
        return items

    @property
    def principal_investigators(self):
        items = []
        for node in self._xmltree.xpath(
            ".//funding-group/award-group/principal-investigator/string-name"
        ):
            d = {
                "given-names": node.findtext("given-names"),
                "surname": node.findtext("surname"),
            }
            items.append(d)
        return items

    @property
    def ack(self):
        items = []
        for ack in self._xmltree.xpath(".//back//ack"):
            item = {"title": ack.findtext("title"), "p": []}
            for node in ack.xpath("p"):
                node_data = self._process_paragraph_node(node)
                item["p"].append(node_data["text"])
            items.append(item)
        return items

    @property
    def funding_ack(self):
        items = []        
        for node in self._xmltree.xpath(".//back//ack//p"):
            node_data = self._process_paragraph_node(node)
            node_data["context"] = "ack"
            items.append(node_data)
        return items

    @property
    def article_type(self):
        return self._xmltree.xpath(".")[0].get("article-type")

    @property
    def article_lang(self):
        return self._xmltree.xpath(".")[0].get(
            "{http://www.w3.org/XML/1998/namespace}lang"
        )

    @property
    def data(self):
        """
        Extracts various financial and funding-related information from the XML for validation purposes.

        Returns
        -------
        dict
            A dictionary containing various pieces of extracted information for validation purposes.
        """
        return {
            "article_type": self.article_type,
            "article_lang": self.article_lang,
            "financial_disclosure": self.financial_disclosure,
            "supported_by": self.supported_by,
            "award_groups": self.award_groups,
            "funding_sources": self.funding_sources,
            "funding_statement": self.funding_statement,
            "principal_award_recipients": self.principal_award_recipients,
            "ack": self.ack,
        }

    @property
    def look_like_award_ids(self):
        if not hasattr(self, "_look_like_award_ids"):
            self._look_like_award_ids = []

            for item in self.funding_ack:
                if item.get("look-like-award-id"):
                    self._look_like_award_ids.append(item)
            for item in self.supported_by:
                if item.get("look-like-award-id"):
                    self._look_like_award_ids.append(item)
            for item in self.financial_disclosure:
                if item.get("look-like-award-id"):
                    self._look_like_award_ids.append(item)
            for item in self.funding_statement_data:
                if item.get("look-like-award-id"):
                    self._look_like_award_ids.append(item)

        return self._look_like_award_ids

    def get_text(self, fulltext, xpath):
        texts = []
        for node in fulltext.node.xpath(xpath):
            texts.extend(node.xpath(".//text()"))
        return " ".join(texts)
    
    @property
    def statements_by_lang(self):
        langs = {}
        for node in self._xmltree.xpath(". | sub-article[@article-type='translation']"):
            fulltext = Fulltext(node)
            langs[fulltext.lang] = fulltext.attribs_parent_prefixed
            langs[fulltext.lang].update({
                "funding_statement": fulltext.front.findtext(".//funding-statement"),
                "texts": {
                    "ack": self.get_text(fulltext, "back/ack//p"),
                    "supported_by": self.get_text(fulltext, 'body//fn[@fn-type="supported-by"] | back//fn[@fn-type="supported-by"]'),
                    "financial_disclosure": self.get_text(fulltext, 'body//fn[@fn-type="financial-disclosure"] | back//fn[@fn-type="financial-disclosure"]'),                
                }
            })
        return langs
