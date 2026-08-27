import hashlib
import logging
from functools import lru_cache, cached_property


LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class PidProviderXMLAdapter:
    def __init__(self, xml_with_pre, pkg_name=None):
        self.xml_with_pre = xml_with_pre
        self.pkg_name = pkg_name

    def tostring(self, pretty_print=False):
        return self.xml_with_pre.tostring(pretty_print=pretty_print)

    @cached_property
    def sps_pkg_name(self):
        return self.xml_with_pre.sps_pkg_name
    
    @property
    def deprecated_sps_pkg_name(self):
        return self.xml_with_pre.deprecated_sps_pkg_name

    @property
    def finger_print(self):
        return self.xml_with_pre.finger_print

    @cached_property
    def related_items(self):
        return self.xml_with_pre.related_items

    @cached_property
    def journal_issn_electronic(self):
        return self.xml_with_pre.journal_issn_electronic

    @cached_property
    def journal_issn_print(self):
        return self.xml_with_pre.journal_issn_print

    @cached_property
    def v2_prefix(self):
        # S + ISSN + YEAR ou 14 primeiros dígitos do pid clássico
        return self.xml_with_pre.v2_prefix

    @property
    def order(self):
        # até 5 dígitos, em geral 5 últimos dígitos do pid v2
        # NÃO pode ter cache pois tem setter
        return self.xml_with_pre.order

    @cached_property
    def volume(self):
        return self.xml_with_pre.volume

    @cached_property
    def number(self):
        return self.xml_with_pre.number

    @cached_property
    def suppl(self):
        return self.xml_with_pre.suppl

    @property
    def pub_year(self):
        return self.xml_with_pre.pub_year

    @property
    def article_pub_year(self):
        return self.xml_with_pre.article_pub_year

    @cached_property
    def main_doi(self):
        return self.xml_with_pre.main_doi

    @cached_property
    def main_toc_section(self):
        return self.xml_with_pre.main_toc_section

    @cached_property
    def is_aop(self):
        return self.xml_with_pre.is_aop

    @cached_property
    def elocation_id(self):
        return self.xml_with_pre.elocation_id

    @cached_property
    def fpage(self):
        return self.xml_with_pre.fpage

    @cached_property
    def fpage_seq(self):
        return self.xml_with_pre.fpage_seq

    @cached_property
    def lpage(self):
        return self.xml_with_pre.lpage

    @property
    def v2(self):
        # NÃO pode ter cache pois tem setter
        return self.xml_with_pre.v2

    @v2.setter
    def v2(self, value):
        self.xml_with_pre.v2 = value

    @property
    def v3(self):
        # NÃO pode ter cache pois tem setter
        return self.xml_with_pre.v3

    @v3.setter
    def v3(self, value):
        self.xml_with_pre.v3 = value

    @property
    def aop_pid(self):
        # NÃO pode ter cache pois tem setter
        return self.xml_with_pre.aop_pid

    @aop_pid.setter
    def aop_pid(self, value):
        self.xml_with_pre.aop_pid = value

    @order.setter
    def order(self, value):
        self.xml_with_pre.order = value

    @cached_property
    def z_links(self):
        return _str_with_64_char("|".join(self.xml_with_pre.links))

    @cached_property
    def z_collab(self):
        return _str_with_64_char(self.xml_with_pre.collab)

    @cached_property
    def z_surnames(self):
        return _str_with_64_char(
            "|".join(
                [
                    _standardize(person.get("surname"))
                    for person in self.xml_with_pre.authors.get("person")
                ]
            )
        )

    @cached_property
    def z_article_titles_texts(self):
        return _str_with_64_char(
            "|".join(sorted(self.xml_with_pre.article_titles_texts or []))
        )

    @cached_property
    def z_partial_body(self):
        return _str_with_64_char(self.xml_with_pre.partial_body)

    @cached_property
    def z_journal_title(self):
        return _str_with_64_char(self.xml_with_pre.journal_title)

    @property
    def data(self):
        return dict(
            pkg_name=self.sps_pkg_name,
            issn_print=self.journal_issn_print,
            issn_electronic=self.journal_issn_electronic,
            article_pub_year=self.article_pub_year,
            pub_year=self.pub_year,
            main_doi=self.main_doi,
            elocation_id=self.elocation_id,
            volume=self.volume,
            number=self.number,
            suppl=self.suppl,
            fpage=self.fpage,
            fpage_seq=self.fpage_seq,
            lpage=self.lpage,
            z_surnames=self.z_surnames or None,
            z_collab=self.z_collab or None,
            z_links=self.z_links,
            z_partial_body=self.z_partial_body,
        )

    def get_data_to_compare(
        self,
        max_body_fragment_length=300,
    ):
        if self.xml_with_pre.max_body_fragment_length != max_body_fragment_length:
            self.xml_with_pre.max_body_fragment_length = max_body_fragment_length
        return {
            "article_titles": self.xml_with_pre.article_titles_texts,
            "z_surnames": self.z_surnames,
            "z_collab": self.z_collab,
            "z_links": self.z_links,
            "body_fragment_fingerprint": self.xml_with_pre.body_fragment_fingerprint,
            "body_fragment": self.xml_with_pre.body_fragment,
        }


def _standardize(text):
    return (text or "").strip().upper()


def _str_with_64_char(text):
    """
    >>> import hashlib
    >>> m = hashlib.sha256()
    >>> m.update(b"Nobody inspects")
    >>> m.update(b" the spammish repetition")
    >>> m.digest()
    b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
    >>> m.digest_size
    32
    >>> m.block_size
    64
    hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()
    """
    if not text:
        return None
    return hashlib.sha256(_standardize(text).encode("utf-8")).hexdigest()
