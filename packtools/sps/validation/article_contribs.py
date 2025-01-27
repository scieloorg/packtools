import re

from packtools.sps.models.article_contribs import ArticleContribs, ContribGroup
from packtools.sps.validation.utils import format_response, build_response
from packtools.sps.utils.xml_utils import get_parent_data, get_parents


def _callable_extern_validate_default(orcid):
    raise NotImplementedError


def _response(contrib, is_valid, expected, obtained, author, error_level="ERROR"):
    return format_response(
        title="CRediT taxonomy",
        parent=contrib.get("parent"),
        parent_id=contrib.get("parent_id"),
        parent_article_type=contrib.get("parent_article_type"),
        parent_lang=contrib.get("parent_lang"),
        item="role",
        sub_item='@content-type="https://credit.niso.org/contributor-roles/*',
        validation_type="value in list",
        is_valid=is_valid,
        expected=expected,
        obtained=obtained,
        advice=f"Provide the correct CRediT taxonomy: {expected}",
        data=contrib,
        error_level=error_level,
    )


class ContribValidation:
    """Validates contributor information in scientific article XML."""

    def __init__(self, contrib, data):
        self.data = data
        self.contrib = contrib
        self.contrib_name = self.contrib.get("contrib_full_name")

    def validate_role(self):
        """
        Validates contributor roles against CRediT taxonomy.

        Returns
        -------
        generator
            Yields dicts with validation results containing:
            title, xpath, validation_type, response, expected_value,
            got_value, message, and advice fields.
        """
        error_level = self.data["credit_taxonomy_terms_and_urls_error_level"]
        credit_taxonomy_terms_and_urls = self.data["credit_taxonomy_terms_and_urls"]
        expected_value = [
            f'<role content-type="{role["uri"]}">{role["term"]}</role>'
            for role in credit_taxonomy_terms_and_urls
        ]

        obtained_value = [
            f'<role content-type="{role.get("content-type")}">{role.get("text")}</role>'
            for role in (self.contrib.get("contrib_role") or [])
        ]

        if obtained_value:
            for role in obtained_value:
                is_valid = role in expected_value
                yield _response(
                    contrib=self.contrib,
                    is_valid=is_valid,
                    expected=expected_value,
                    obtained=role,
                    author=self.contrib_name,
                    error_level=error_level,
                )
        else:
            yield _response(
                contrib=self.contrib,
                is_valid=False,
                expected=expected_value,
                obtained=None,
                author=self.contrib_name,
                error_level=error_level,
            )

    def validate_orcid_format(self):
        """
        Validates format of contributor ORCID identifiers.

        Returns
        -------
        generator
            Yields dicts with validation results containing:
            title, xpath, validation_type, response, expected_value,
            got_value, message, and advice fields.
        """
        error_level = self.data["orcid_format_error_level"]
        if not self.contrib_name:
            return

        _default_orcid = (
            r"^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}$"
        )

        _orcid = self.contrib.get("contrib_ids", {}).get("orcid")
        is_valid = bool(_orcid and re.match(_default_orcid, _orcid))
        expected_value = _orcid if is_valid else "valid ORCID"

        yield format_response(
            title="ORCID format",
            parent=self.contrib.get("parent"),
            parent_id=self.contrib.get("parent_id"),
            parent_article_type=self.contrib.get("parent_article_type"),
            parent_lang=self.contrib.get("parent_lang"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="format",
            is_valid=is_valid,
            expected=expected_value,
            obtained=_orcid,
            advice=(
                None if is_valid else f"Provide a valid ORCID for {self.contrib_name}"
            ),
            data=self.contrib,
            error_level=error_level,
        )

    def validate_orcid_is_registered(self):
        """
        Validates if contributor's ORCID is registered in ORCID database.

        Returns
        -------
        generator
            Yields dicts with validation results containing:
            title, xpath, validation_type, response, expected_value,
            got_value, message, and advice fields.
        """
        is_orcid_registered = self.data["is_orcid_registered"]
        error_level = self.data["orcid_is_registered_error_level"]
        if not self.contrib_name:
            return

        orcid = self.contrib.get("contrib_ids", {}).get("orcid")
        if not orcid:
            return

        is_orcid_registered = is_orcid_registered or _callable_extern_validate_default
        if not is_orcid_registered:
            return

        result = is_orcid_registered(orcid, self.contrib)

        yield format_response(
            title="Registered ORCID",
            parent=self.contrib.get("parent"),
            parent_id=self.contrib.get("parent_id"),
            parent_article_type=self.contrib.get("parent_article_type"),
            parent_lang=self.contrib.get("parent_lang"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="registered",
            is_valid=result["is_valid"],
            expected=self.contrib_name,
            obtained=result["data"],
            advice=(
                None
                if result["is_valid"]
                else f"Identify the correct ORCID for {self.contrib_name}"
            ),
            data=self.contrib,
            error_level=error_level,
        )

    def validate_affiliations(self):
        """
        Validates presence of contributor affiliations.

        Returns
        -------
        generator
            Yields dicts with validation results containing:
            title, item, sub_item, validation_type, response,
            expected_value, got_value, message, and advice fields.
        """
        error_level = self.data["affiliations_error_level"]
        affs = self.contrib.get("affs")
        if not affs:
            yield format_response(
                title="Author without affiliation",
                parent=self.contrib.get("parent"),
                parent_id=self.contrib.get("parent_id"),
                parent_article_type=self.contrib.get("parent_article_type"),
                parent_lang=self.contrib.get("parent_lang"),
                item="contrib",
                sub_item="aff",
                validation_type="exist",
                is_valid=False,
                expected="affiliation",
                obtained=None,
                advice=f"provide affiliation for {self.contrib_name}",
                data=self.contrib,
                error_level=error_level,
            )

    def validate_name(self):
        """Validates presence of contributor name elements."""
        error_level = self.data["name_error_level"]
        item = self.contrib.get("contrib_name")
        if not item:
            yield build_response(
                title="name",
                parent=self.contrib,
                item="contrib",
                sub_item="name",
                validation_type="exist",
                is_valid=False,
                expected="name",
                obtained=None,
                advice=f"provide name",
                data=self.contrib,
                error_level=error_level,
            )

    def validate_collab(self):
        """Validates presence of collaboration information."""
        error_level = self.data["collab_error_level"]
        item = self.contrib.get("collab")
        if not item:
            yield build_response(
                title="collab",
                parent=self.contrib,
                item="contrib",
                sub_item="collab",
                validation_type="exist",
                is_valid=False,
                expected="collab",
                obtained=None,
                advice=f"provide collab",
                data=self.contrib,
                error_level=error_level,
            )

    def validate_name_or_collab(self):
        """
        Validates that contributor has either name or collaboration info.
        For reviewer reports, checks for name or anonymous elements instead.
        """
        error_level = self.data["name_or_collab_error_level"]

        if self.contrib.get("parent_article_type") == "translation":
            parent_article_type = self.contrib.get("original_article_type")
        else:
            parent_article_type = self.contrib.get("parent_article_type")

        if parent_article_type == "reviewer-report":
            title = "name or anonymous"
            item = self.contrib.get("contrib_name") or self.contrib.get(
                "contrib_anonymous"
            )
        else:
            title = "name or collab"
            item = self.contrib.get("contrib_name") or self.contrib.get("collab")

        if not item:
            yield build_response(
                title=title,
                parent=self.contrib,
                item="contrib",
                sub_item=title,
                validation_type="exist",
                is_valid=False,
                expected=title,
                obtained=None,
                advice=f"provide {title}",
                data=self.contrib,
                error_level=error_level,
            )

    def validate(self):
        """Runs all validation checks on contributor metadata."""
        yield from self.validate_role()
        yield from self.validate_orcid_format()
        yield from self.validate_orcid_is_registered()
        yield from self.validate_affiliations()
        yield from self.validate_name_or_collab()


class ArticleContribsValidation:
    def __init__(self, xmltree, data):
        self.xmltree = xmltree
        self.data = data
        self.contribs = ArticleContribs(self.xmltree)

    @property
    def content_types(self):
        return [
            contrib_group.get("content-type")
            for contrib_group in self.xmltree.xpath(".//contrib-group")
        ]

    def validate_orcid_is_unique(self):
        """
        Checks whether a contributor's ORCID is unique.

        XML input
        ---------
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
                  <name>
                    <surname>Higa</surname>
                    <given-names>Vanessa M.</given-names>
                  </name>
                  <xref ref-type="aff" rid="aff1">a</xref>
                </contrib>
              </contrib-group>
            </article-meta>
          </front>
        </article>

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Unique ORCID',
                    'xpath': './/contrib-id[@contrib-id-type="orcid"]',
                    'validation_type': 'uniqueness',
                    'response': 'OK',
                    'expected_value': 'Unique ORCID values',
                    'got_value': ['0990-0001-0058-4853', '0000-3333-1238-6873'],
                    'message': 'Got ORCIDs and frequencies (\'0990-0001-0058-4853\', 1) | (\'0000-3333-1238-6873\', 1)',
                    'advice': None
                }
            ]
        """
        error_level = self.data["orcid_is_unique_error_level"]
        orcid_dict = {}
        for contrib in self.contribs.contribs:
            orcid = contrib.get("contrib_ids", {}).get("orcid")
            if orcid:
                orcid_dict.setdefault(orcid, set())
                orcid_dict[orcid].add(contrib.get("contrib_full_name"))

        is_valid = True
        diff = []
        for orcid, names in orcid_dict.items():
            if len(names) > 1:
                is_valid = False
                diff.append(orcid)

        # Para a realização dos testes é necessária uma ordem estável para os nomes
        obtained = {orcid: sorted(list(names)) for orcid, names in orcid_dict.items()}

        yield format_response(
            title="Unique ORCID",
            parent="article",
            parent_id=None,
            parent_article_type=self.xmltree.get("article-type"),
            parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="uniqueness",
            is_valid=is_valid,
            expected="Unique ORCID values",
            obtained=obtained,
            advice="Consider replacing the following ORCIDs that are not unique: {}".format(
                " | ".join(diff)
            ),
            data=None,
            error_level=error_level,
        )

    def validate(self):
        # A validação da unicidade do ORCID é feita uma única vez por artigo
        yield from self.validate_orcid_is_unique()

        for contrib in self.contribs.contribs:
            yield from ContribValidation(contrib, self.data).validate()

        validator = CollabListValidation(self.xmltree.find("."), self.data)
        yield from validator.validate()
        for item in self.xmltree.xpath("sub-article"):
            validator = CollabListValidation(item, self.data)
            yield from validator.validate()


class CollabListValidation:
    def __init__(self, parent_node, args):
        # parent_node (article ou sub-article)
        self.args = args
        self.parent_node = parent_node
        self.parent_data = get_parent_data(parent_node)

    @property
    def data(self):
        items = []
        for content_type, group in self.contrib_groups.items():
            for item in group.contribs:
                items.append(item)
        return items

    @property
    def contrib_groups(self):
        """
        <contrib-group>
            <contrib contrib-type="author" id="collab">
                <collab>The MARS Group</collab>
                <xref ref-type="author-notes" rid="fn1">1</xref>
            </contrib>
        </contrib-group>
        <contrib-group content-type="collab-list">
            <contrib contrib-type="author" rid="collab">
                <contrib-id contrib-id-type="orcid">0000-0001-0002-0003</contrib-id>
                <name>
                    <surname>Wright</surname>
                    <given-names>Rick W.</given-names>
                </name>
                <xref ref-type="aff" rid="aff1">1</xref>
            </contrib>
            <contrib/>
        </contrib-group>

        {
            None: ContribGroup,
            "collab-list": ContribGroup,

        }
        """
        if not hasattr(self, "_contrib_groups") or not self._contrib_groups:
            data = get_parent_data(self.parent_node)
            self._contrib_groups = {}
            for node in self.parent_node.xpath(data["xpath"]):
                for contrib_group in node.xpath(".//contrib-group"):
                    self._contrib_groups[contrib_group.get("content-type")] = (
                        ContribGroup(contrib_group)
                    )
        return self._contrib_groups

    def validate(self):
        if self.parent_node.xpath(".//contrib//collab"):
            yield from self.validate_contrib_group__collab()
            yield from self.validate_contrib_group__name()

    def validate_contrib_group__collab(self):
        try:
            contrib_group = self.contrib_groups[None]
        except KeyError:
            yield build_response(
                title="contrib-group/contrib/collab",
                parent=self.parent_data,
                item="contrib-group",
                sub_item="",
                validation_type="match",
                is_valid=False,
                expected="contrib-group",
                obtained=None,
                advice="Add contrib-group which has contrib/name",
                data=self.data,
                error_level=self.args["collab_list_error_level"],
            )
        else:
            for contrib in contrib_group.contribs:
                contrib.update(self.parent_data)
                validator = ContribValidation(contrib, self.args)
                yield from validator.validate_collab()

    def validate_contrib_group__name(self):
        try:
            contrib_group = self.contrib_groups["collab-list"]
        except KeyError:
            yield build_response(
                title="contrib-group/contrib/name",
                parent=self.parent_data,
                item="contrib-group",
                sub_item="collab-list",
                validation_type="match",
                is_valid=False,
                expected="contrib-group[@content-type='collab-list']",
                obtained=None,
                advice="Add content-type='collab-list' to contrib-group must have contrib/name",
                data=self.data,
                error_level=self.args["collab_list_error_level"],
            )
        else:
            for contrib in contrib_group.contribs:
                contrib.update(self.parent_data)
                validator = ContribValidation(contrib, self.args)
                yield from validator.validate_name()
