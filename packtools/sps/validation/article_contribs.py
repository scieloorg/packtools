import re

from packtools.sps.models.article_contribs import TextContribs, XMLContribs
from packtools.sps.validation.utils import build_response


def _callable_extern_validate_default(orcid, data):
    return {
        "data": data,
        "orcid": orcid,
        "status": "unknown",
    }


class ContribValidation:
    """Validates contributor information in scientific article XML."""

    def __init__(self, contrib, data):
        self.data = data
        self.contrib = contrib
        self.contrib_name = self.contrib.get("contrib_full_name")

    def validate_role(self):
        try:
            roles = self.contrib["contrib_role"]
        except KeyError:
            yield build_response(
                title="role",
                parent=self.contrib,
                item="contrib",
                sub_item="role",
                validation_type="exist",
                is_valid=False,
                expected="contrib/role",
                obtained=None,
                advice=f"Provide contrib/role",
                data=self.contrib,
                error_level=self.data.get("contrib_role_error_level"),
            )
        else:
            for role in roles:
                validator = ContribRoleValidation(self.contrib, role, self.data)
                yield from validator.validate_role_specific_use()
                yield from validator.validate_credit()

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
        if self.contrib.get("anonymous"):
            return

        error_level = self.data["orcid_format_error_level"]
        if not self.contrib_name:
            return

        _default_orcid = (
            r"^[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}-[0-9a-zA-Z]{4}$"
        )

        _orcid = self.contrib.get("contrib_ids", {}).get("orcid")
        is_valid = bool(_orcid and re.match(_default_orcid, _orcid))
        expected_value = _orcid if is_valid else "valid ORCID"
        if not is_valid:
            yield build_response(
                title="ORCID format",
                parent=self.contrib,
                item="contrib-id",
                sub_item='@contrib-id-type="orcid"',
                validation_type="format",
                is_valid=is_valid,
                expected=expected_value,
                obtained=_orcid,
                advice=(
                    None
                    if is_valid
                    else f"Provide a valid ORCID for {self.contrib_name}"
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
        if self.contrib.get("anonymous"):
            return

        error_level = self.data["orcid_is_registered_error_level"]
        if not self.contrib_name:
            return

        orcid = self.contrib.get("contrib_ids", {}).get("orcid")
        if not orcid:
            return

        is_orcid_registered = self.data["is_orcid_registered"]
        is_orcid_registered = (
            is_orcid_registered or _callable_extern_validate_default
        )
        if not is_orcid_registered:
            return

        result = is_orcid_registered(orcid, self.contrib_name)
        if result["status"] != "registered":
            yield build_response(
                title="Registered ORCID",
                parent=self.contrib,
                item="contrib-id",
                sub_item='@contrib-id-type="orcid"',
                validation_type="registered",
                is_valid=result["status"] == "registered",
                expected="registered",
                obtained=result["status"],
                advice=f"Identify the correct ORCID for {self.contrib_name}",
                data=result,
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
        if not error_level and not affs:
            return
        if not affs:
            yield build_response(
                title="Required affiliation",
                parent=self.contrib,
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
        if self.contrib.get("original_article_type") == "reviewer-report":
            title = "name or anonymous"
            item = self.contrib.get("contrib_name") or self.contrib.get(
                "anonymous"
            )
        else:
            title = "name or collab"
            item = self.contrib.get("contrib_name") or self.contrib.get(
                "collab"
            )

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


class XMLContribsValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.params = params
        self.xml_contribs = XMLContribs(self.xmltree)

    def validate_orcid_is_unique(self):
        error_level = self.params["orcid_is_unique_error_level"]
        orcid_dict = self.xml_contribs.contrib_full_name_by_orcid

        repeated_orcid = {
            k: sorted(v) for k, v in orcid_dict.items() if len(v) > 1
        } or None

        parent = self.xml_contribs.text_contribs.attribs_parent_prefixed

        if repeated_orcid:
            questions = []
            for k, v in repeated_orcid.items():
                questions.append(f"{k} is assigned to {v}")
            questions = "; ".join(questions)
            advice = f"ORCID must be unique. {questions}"
            yield build_response(
                title="Unique ORCID",
                parent=parent,
                item="contrib-id",
                sub_item='@contrib-id-type="orcid"',
                validation_type="uniqueness",
                is_valid=not bool(repeated_orcid),
                expected="Unique ORCID values",
                obtained=repeated_orcid,
                advice=advice,
                data=repeated_orcid,
                error_level=error_level,
            )

    def validate(self):
        # A validação da unicidade do ORCID é feita uma única vez por artigo
        yield from self.validate_orcid_is_unique()

        validator = TextContribsValidation(self.xmltree.find("."), self.params)
        yield from validator.validate()


class TextContribsValidation:
    def __init__(self, node, params):
        self.node = node
        self.params = params
        self.text_contribs = TextContribs(node)

    def validate(self):
        for contrib in self.text_contribs.items:
            yield from ContribValidation(contrib, self.params).validate()

        validator = CollabListValidation(self.node, self.params)
        yield from validator.validate()

        for node in self.text_contribs.sub_articles:
            validator = TextContribsValidation(node, self.params)
            yield from validator.validate()


class CollabListValidation:
    def __init__(self, node, params):
        # node (article ou sub-article)
        self.params = params
        self.node = node
        self.text_contribs = TextContribs(node)

    @property
    def contrib_groups(self):
        d = {}
        for item in self.text_contribs.contrib_groups:
            d[item.type] = item.data["contribs"]
        return d

    def validate(self):
        if self.text_contribs.front.xpath(".//contrib//collab"):
            yield from self.validate_contrib_group__collab()
            yield from self.validate_contrib_group__name()

    def validate_contrib_group__collab(self):
        try:
            contrib_group = self.contrib_groups[None]
        except KeyError:
            yield build_response(
                title="contrib-group/contrib/collab",
                parent=self.text_contribs.attribs_parent_prefixed,
                item="contrib-group",
                sub_item="",
                validation_type="match",
                is_valid=False,
                expected="contrib-group",
                obtained=None,
                advice="Add content-type='collab-list' to contrib-group which has contrib/name",
                data=self.contrib_groups,
                error_level=self.params["collab_list_error_level"],
            )
        else:
            for contrib in contrib_group:
                validator = ContribValidation(contrib, self.params)
                yield from validator.validate_collab()

    def validate_contrib_group__name(self):
        try:
            contrib_group = self.contrib_groups["collab-list"]
        except KeyError:
            yield build_response(
                title="contrib-group/contrib/name",
                parent=self.text_contribs.attribs_parent_prefixed,
                item="contrib-group",
                sub_item="",
                validation_type="match",
                is_valid=False,
                expected="contrib-group",
                obtained=None,
                advice="Add content-type='collab-list' to contrib-group which has contrib/name",
                data=self.contrib_groups,
                error_level=self.params["collab_list_error_level"],
            )
        else:
            for contrib in contrib_group:
                validator = ContribValidation(contrib, self.params)
                yield from validator.validate_name()


class ContribRoleValidation:
    """Validates contributor information in scientific article XML."""

    def __init__(self, contrib, contrib_role, params):
        self.params = params
        self.contrib = contrib
        self.contrib_role = contrib_role

    def validate_credit(self):
        """
        Validates contributor roles against CRediT taxonomy.

        Returns
        -------
        generator
            Yields dicts with validation results containing:
            title, xpath, validation_type, response, expected_value,
            got_value, message, and advice fields.
        """
        expected = self.params["credit_taxonomy_terms_and_urls"]
        if not expected:
            return

        error_level = self.params["credit_taxonomy_terms_and_urls_error_level"]
        # uri, term vs content-type, text
        expected_items = {item["uri"]: item["term"] for item in expected}
        texts = {item["term"]: item["uri"] for item in expected}

        uri = self.contrib_role.get("content-type")
        text = self.contrib_role.get("text")

        try:
            expected_text = expected_items[uri]
            expected_uri = uri
        except KeyError:
            try:
                expected_uri = texts[text]
            except KeyError:
                # Credit URI does not match
                expected_uris = list(expected_items.keys())
                advice = f"Provide the correct CRediT taxonomy URI (role/@content-type): {expected_uris}"
            else:
                expected_uris = [expected_uri]
                advice = f"Provide the correct CRediT taxonomy URI (role/@content-type) for {text}: {expected_uris}"

            yield build_response(
                title="CRediT taxonomy URI",
                parent=self.contrib,
                item="role",
                sub_item="@content-type",
                validation_type="value in list",
                is_valid=False,
                expected=expected_uris,
                obtained=uri,
                advice=advice,
                data=self.contrib,
                error_level=error_level,
            )
        else:
            if not text == expected_text:
                yield build_response(
                    title="CRediT taxonomy term",
                    parent=self.contrib,
                    item="role",
                    sub_item=None,
                    validation_type="value",
                    is_valid=False,
                    expected=expected_text,
                    obtained=text,
                    advice=f"Check the CRediT taxonomy term (role) for {uri}",
                    data=self.contrib,
                    error_level=error_level,
                )

    def validate_role_specific_use(self):
        expected = self.params["contrib_role_specific_use_list"]
        error_level = self.params["contrib_role_specific_use_error_level"]
        specific_use = self.contrib_role.get("specific-use")
        if specific_use not in expected:
            yield build_response(
                title="specific-use",
                parent=self.contrib,
                item="role",
                sub_item="specific-use",
                validation_type="value in list",
                is_valid=False,
                expected=expected,
                obtained=specific_use,
                advice=f"Provide the correct role/@specific-use: {expected}",
                data=self.contrib,
                error_level=error_level,
            )
