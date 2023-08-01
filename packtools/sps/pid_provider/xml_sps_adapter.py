import hashlib
import logging
from gettext import gettext as _

from lxml import etree

LOGGER = logging.getLogger(__name__)
LOGGER_FMT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


class PidProviderXMLAdapter:
    def __init__(self, xml_with_pre, pkg_name=None):
        self.xml_with_pre = xml_with_pre
        self.pkg_name = pkg_name

    def __getattr__(self, name):
        logging.debug(type(self.xml_with_pre))
        try:
            return getattr(self.xml_with_pre, name)
        except Exception as e:
            logging.exception(e)
            raise AttributeError(
                f"Unable to get PidProviderXMLAdapter.{name} {type(e)} {e}"
            )

    @property
    def v2(self):
        return self.xml_with_pre.v2

    @v2.setter
    def v2(self, value):
        self.xml_with_pre.v2 = value

    @property
    def v3(self):
        return self.xml_with_pre.v3

    @v3.setter
    def v3(self, value):
        self.xml_with_pre.v3 = value

    @property
    def aop_pid(self):
        return self.xml_with_pre.aop_pid

    @aop_pid.setter
    def aop_pid(self, value):
        self.xml_with_pre.aop_pid = value

    @property
    def z_links(self):
        if not hasattr(self, "_links") or not self._links:
            self._links = _str_with_64_char("|".join(self.xml_with_pre.links))
        return self._links

    @property
    def z_collab(self):
        if not hasattr(self, "_collab") or not self._collab:
            self._collab = _str_with_64_char(self.xml_with_pre.collab)
        return self._collab

    @property
    def z_surnames(self):
        if not hasattr(self, "_surnames") or not self._surnames:
            self._surnames = _str_with_64_char(
                "|".join(
                    [
                        _standardize(person.get("surname"))
                        for person in self.authors.get("person")
                    ]
                )
            )
        return self._surnames

    @property
    def z_article_titles_texts(self):
        return _str_with_64_char(
            "|".join(sorted(self.xml_with_pre.article_titles_texts or []))
        )

    @property
    def z_partial_body(self):
        if not hasattr(self, "_partial_body") or not self._partial_body:
            self._partial_body = _str_with_64_char(self.xml_with_pre.partial_body)
        return self._partial_body

    def query_params(self, filter_by_issue=False, aop_version=False):
        """
        Get query parameters

        Arguments
        ---------
        filter_by_issue: bool
        aop_version: bool

        Returns
        -------
        dict
        """
        _params = dict(
            z_surnames=self.z_surnames or None,
            z_collab=self.z_collab or None,
        )
        if not any(_params.values()):
            _params["main_doi"] = self.main_doi

        if not any(_params.values()):
            _params["z_links"] = self.z_links

        if not any(_params.values()):
            _params["pkg_name"] = self.sps_pkg_name

        if not any(_params.values()):
            _params["z_partial_body"] = self.z_partial_body

        _params["elocation_id"] = self.elocation_id
        if aop_version:
            _params["issue__isnull"] = True
        else:
            if filter_by_issue:
                _params["issue__pub_year"] = self.pub_year
                _params["issue__volume"] = self.volume
                _params["issue__number"] = self.number
                _params["issue__suppl"] = self.suppl
                _params["fpage"] = self.fpage
                _params["fpage_seq"] = self.fpage_seq
                _params["lpage"] = self.lpage

        _params["journal__issn_print"] = self.journal_issn_print
        _params["journal__issn_electronic"] = self.journal_issn_electronic
        _params["article_pub_year"] = self.article_pub_year
        _params["z_article_titles_texts"] = self.z_article_titles_texts

        LOGGER.info(_params)
        return _params

    def adapt_query_params(self, params):
        """
        Adapt query parameters

        Parameters
        ----------
        params : dict

        Returns
        -------
        dict
        """
        try:
            params["main_doi__iexact"] = params["main_doi"]
        except KeyError:
            pass
        try:
            params["pkg_name__iexact"] = params["pkg_name"]
        except KeyError:
            pass

    @property
    def query_list(self):
        items = []
        if self.is_aop:
            LOGGER.info("self.is_aop")
            # o xml_adapter não contém dados de issue
            # não indica na consulta o valor para o atributo issue
            # então o registro encontrado pode ou não ter dados de issue
            params = self.query_params(aop_version=False)
            items.append(params)
        else:
            # o xml_adapter contém dados de issue
            # inclui na consulta os dados de issue
            LOGGER.info("not self.is_aop")
            params = self.query_params(filter_by_issue=True)
            items.append(params)

            # busca por registro cujo valor de issue is None
            params = self.query_params(aop_version=True)
            items.append(params)
        return items


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
