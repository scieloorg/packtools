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
        self.data = self._get_default_params()
        self.data.update(data or {})
        self.contrib = contrib
        self.contrib_name = self.contrib.get("contrib_full_name")

    @property
    def info(self):
        if parent_id := self.data.get("parent_id"):
            return f'{self.contrib_name} (sub-article {parent_id}) :'
        return f'{self.contrib_name} :'

    def _get_default_params(self):
        return {
            # Error levels
            "contrib_role_error_level": "ERROR",
            "orcid_format_error_level": "ERROR",
            "orcid_is_registered_error_level": "ERROR",
            "affiliations_error_level": "ERROR",
            "name_error_level": "ERROR",
            "collab_error_level": "ERROR",
            "contrib_error_level": "ERROR",
            
            # ORCID validation function
            "is_orcid_registered": _callable_extern_validate_default
        }
    def validate_role(self):
        try:
            roles = self.contrib["contrib_role"]
        except KeyError:
            parent = self.data.get("parent")
            parent_id = self.data.get("parent_id")
            parent_article_type = self.data.get("parent_article_type")

            yield build_response(
                title=f"contributor role",
                parent=self.contrib,
                item="contrib",
                sub_item="role",
                validation_type="exist",
                is_valid=False,
                expected=f"<role> in <contrib>",
                obtained=None,
                advice=f"{self.info} Mark the contrib role. Consult SPS documentation for detailed instructions",
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

        _orcid = self.contrib.get("contrib_ids", {}).get("orcid") or ""
        is_valid = bool(_orcid and re.match(_default_orcid, _orcid))
        expected_value = _orcid if is_valid else "valid ORCID"
        if _orcid:
            advice = f'Fix ORCID format <contrib-id contrib-id-type="orcid">{_orcid}</contrib-id>'
        else:
            advice = f'{self.info} Add ORCID <contrib-id contrib-id-type="orcid"></contrib-id> in <contrib>'            

        yield build_response(
            title="ORCID format",
            parent=self.contrib,
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="format",
            is_valid=is_valid,
            expected="valid ORCID",
            obtained=_orcid,
            advice=advice or "(validate_orcid_format)",
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
        yield build_response(
            title="Registered ORCID",
            parent=self.contrib,
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="registered",
            is_valid=result["status"] == "registered",
            expected="registered",
            obtained=result["status"],
            advice=f'{self.info} Unable to automatically check the {orcid}. Check it manually',
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
        affs = [item["id"] for item in self.contrib.get("affs") or []]
        yield build_response(
            title="affiliation",
            parent=self.contrib,
            item="contrib",
            sub_item="xref",
            validation_type="exist",
            is_valid=not affs,
            expected="affiliation",
            obtained=affs,
            advice=f'{self.info} Add <xref ref-type="aff" rid=""> in <contrib>',
            data=self.contrib,
            error_level=error_level,
        )

    def validate_name(self):
        """Validates presence of contributor name elements."""
        error_level = self.data["name_error_level"]
        item = self.contrib.get("contrib_name")
        yield build_response(
            title="contributor name",
            parent=self.contrib,
            item="contrib",
            sub_item="name",
            validation_type="exist",
            is_valid=bool(item),
            expected="contributor name",
            obtained=item,
            advice=f"{self.info} Mark contributor name with <name> in <contrib>",
            data=self.contrib,
            error_level=error_level,
        )

    def validate_collab(self):
        """Validates presence of collaboration information."""
        error_level = self.data["collab_error_level"]
        item = self.contrib.get("collab")
        yield build_response(
            title="collab",
            parent=self.contrib,
            item="contrib",
            sub_item="collab",
            validation_type="exist",
            is_valid=bool(item),
            expected="collab",
            obtained=None,
            advice=f"{self.info} Mark institutional contributor with <collab> in <contrib>",
            data=self.contrib,
            error_level=error_level,
        )

    def validate_contrib(self):
        """
        Validates that contributor has either name or collaboration info.
        For reviewer reports, checks for name or anonymous elements instead.
        """
        error_level = self.data["contrib_error_level"]
        value = None
        expected = []
        if self.contrib.get("original_article_type") == "reviewer-report":
            expected = ["name", "anonymous"]
            value = self.contrib.get("contrib_name") or self.contrib.get("anonymous")
            advice = f"{self.info} Mark contributor with <name> and anonymous contributor with <anonymous/> in <contrib>"
        else:
            expected = ["name", "collab"]
            value = self.contrib.get("contrib_name") or self.contrib.get("collab")
            advice = f"{self.info} Mark contributor with <name> and institutional contributor with <collab> in <contrib>"

        yield build_response(
            title="contributor",
            parent=self.contrib,
            item="contrib",
            sub_item=None,
            validation_type="exist",
            is_valid=bool(value),
            expected=expected,
            obtained=value,
            advice=advice or '(validate_contrib)',
            data=self.contrib,
            error_level=error_level,
        )

    def validate(self):
        """Runs all validation checks on contributor metadata."""
        yield from self.validate_contrib()
        yield from self.validate_role()
        yield from self.validate_orcid_format()
        yield from self.validate_orcid_is_registered()
        yield from self.validate_affiliations()


class XMLContribsValidation:
    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.xml_contribs = XMLContribs(self.xmltree)
        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        # Include all params from ContribValidation plus its own
        return {
            "orcid_is_unique_error_level": "ERROR"
        }

    def validate_orcid_is_unique(self):
        error_level = self.params["orcid_is_unique_error_level"]
        orcid_dict = self.xml_contribs.contrib_full_name_by_orcid

        repeated_orcid = {
            k: sorted(v) for k, v in orcid_dict.items() if len(v) > 1
        }

        parent = self.xml_contribs.text_contribs.attribs_parent_prefixed

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
            expected="Unique ORCID",
            obtained=repeated_orcid,
            advice=advice or '(validate_orcid_is_unique)',
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
        self.params = self._get_default_params()
        self.params.update(params or {})
        self.node = node
        self.text_contribs = TextContribs(node)

    def _get_default_params(self):
        return {
            "collab_list_error_level": "ERROR"
        }

    def validate(self):
        for contrib_group in self.text_contribs.contrib_groups:
            contrib_group_data = contrib_group.data

            expected_type = None
            if contrib_group_data["has_collab"]:
                title = "institutional"
            elif contrib_group_data["has_name"]:
                title = "person"
                if self.text_contribs.collab:
                    expected_type = "collab-list"
            else:
                title = "anonymous"                

            valid = expected_type == contrib_group_data["type"]

            advice = ""
            if expected_type == "collab-list":
                advice = f'Add person authors, members of {self.text_contribs.collab}, with <contrib><name>...</name></contrib> in <contrib-group content-type="collab-list"></contrib-group>'
            else:
                type = contrib_group_data["type"]
                advice = f'Remove content-type="{type}" from <contrib-group content-type="{type}">'

            yield build_response(
                title=f"{title} contributor group type",
                parent=self.text_contribs.attribs_parent_prefixed,
                item="contrib-group",
                sub_item="",
                validation_type="value",
                is_valid=valid,
                expected=expected_type,
                obtained=contrib_group_data["type"],
                advice=advice or f'(validate {contrib_group_data})',
                data=contrib_group_data,
                error_level=self.params["collab_list_error_level"],
            )


class ContribRoleValidation:
    """Validates contributor information in scientific article XML."""

    def __init__(self, contrib, contrib_role, params):
        self.params = params
        self.contrib = contrib
        self.contrib_role = contrib_role

        self.params = self._get_default_params()
        self.params.update(params or {})
        self.index_credit_taxonomy()

    def index_credit_taxonomy(self):
        credit_taxonomy_by_uri = {}
        credit_taxonomy_by_term = {}
        credit_taxonomy_by_terms = []
        for item in self.params["credit_taxonomy_terms_and_urls"] or []:
            credit_taxonomy_by_terms.append(item["term"])
            credit_taxonomy_by_uri[item["uri"]] = item["term"]
            credit_taxonomy_by_term[item["term"].upper()] = item["uri"]
        self.params["credit_taxonomy_by_uri"] = credit_taxonomy_by_uri
        self.params["credit_taxonomy_by_term"] = credit_taxonomy_by_term
        self.params["credit_taxonomy_by_terms"] = credit_taxonomy_by_terms

    @property
    def info(self):
        contrib_name = self.contrib.get("contrib_full_name")
        if parent_id := self.contrib.get("parent_id"):
            return f'{contrib_name} (sub-article {parent_id}) :'
        return f'{contrib_name} :'

    def _get_default_params(self):
        return {
            # Error levels
            "credit_taxonomy_uri_error_level": "ERROR",
            "credit_taxonomy_term_error_level": "ERROR",
            "contrib_role_specific_use_error_level": "ERROR",

            # CRediT taxonomy terms and their URIs
            "credit_taxonomy_terms_and_urls": [
                {"term": "Conceptualization", "uri": "http://credit.niso.org/contributor-roles/conceptualization/"},
                {"term": "Data curation", "uri": "http://credit.niso.org/contributor-roles/data-curation/"},
                {"term": "Formal analysis", "uri": "http://credit.niso.org/contributor-roles/formal-analysis/"},
                {"term": "Funding acquisition", "uri": "http://credit.niso.org/contributor-roles/funding-acquisition/"},
                {"term": "Investigation", "uri": "http://credit.niso.org/contributor-roles/investigation/"},
                {"term": "Methodology", "uri": "http://credit.niso.org/contributor-roles/methodology/"},
                {"term": "Project administration", "uri": "http://credit.niso.org/contributor-roles/project-administration/"},
                {"term": "Resources", "uri": "http://credit.niso.org/contributor-roles/resources/"},
                {"term": "Software", "uri": "http://credit.niso.org/contributor-roles/software/"},
                {"term": "Supervision", "uri": "http://credit.niso.org/contributor-roles/supervision/"},
                {"term": "Validation", "uri": "http://credit.niso.org/contributor-roles/validation/"},
                {"term": "Visualization", "uri": "http://credit.niso.org/contributor-roles/visualization/"},
                {"term": "Writing – original draft", "uri": "http://credit.niso.org/contributor-roles/writing-original-draft/"},
                {"term": "Writing – review &amp; editing", "uri": "http://credit.niso.org/contributor-roles/writing-review-editing/"}
            ],

            # List of valid contributor role types
            "contrib_role_specific_use_list": [
                "author",
                "editor",
                "reviewer",
                "translator"
            ]
        }

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
        uri = self.contrib_role.get("content-type")
        text = self.contrib_role.get("text")
        if not uri and not text:
            return

        expected = self.params["credit_taxonomy_terms_and_urls"]
        if not expected:
            return

        uri_error_level = self.params["credit_taxonomy_uri_error_level"]
        term_error_level = self.params["credit_taxonomy_term_error_level"]
        credit_taxonomy_by_uri = self.params["credit_taxonomy_by_uri"]
        credit_taxonomy_by_term = self.params["credit_taxonomy_by_term"]

        expected_term = credit_taxonomy_by_uri.get(uri) or None
        expected_uri = credit_taxonomy_by_term.get(text and text.upper()) or None

        valid_uri = uri and expected_uri == uri
        valid_term = text and expected_term and (expected_term.upper() == text.upper())
        advice = ""
        if not valid_uri:
            if expected_uri and uri:
                advice = f'{self.info} replace <role content-type="{uri}"> by <role content-type="{expected_uri}">'
            elif expected_uri:
                advice = f'{self.info} replace <role>{text}</role> by <role content-type="{expected_uri}">{text}</role>'
            elif uri:
                expected_uris = list(credit_taxonomy_by_uri.keys())
                advice = f'{self.info} check if <role content-type="{uri}">{text}</role> has corresponding CRediT URI: {expected_uris}'                
            elif text:
                expected_uris = list(credit_taxonomy_by_uri.keys())
                advice = f'{self.info} check if <role>{text}</role> has corresponding CRediT URI: {expected_uris}'                
        yield build_response(
            title="CRediT taxonomy URI",
            parent=self.contrib,
            item="role",
            sub_item=None,
            validation_type="exist",
            is_valid=valid_uri,
            expected=expected_uri,
            obtained=uri,
            advice=advice,
            data=self.contrib,
            error_level=uri_error_level,
        )
        
        if not valid_term:
            if uri:
                content_type = f' content-type="{uri}"'
            else:
                content_type = ''
            if expected_term and text:
                advice = f'{self.info} replace <role{content_type}>{text}</role> by <role{content_type}>{expected_term}</role>'
            elif expected_term:
                advice = f'{self.info} replace <role{content_type}></role> by <role{content_type}>{expected_term}</role>'
            elif text:
                expected_terms = self.params["credit_taxonomy_by_terms"]
                advice = f'{self.info} check if <role{content_type}>{text}</role> has corresponding CRediT term: {expected_terms}'  
            else:
                expected_terms = self.params["credit_taxonomy_by_terms"]
                advice = f'{self.info} check if <role{content_type}>{text}</role> has corresponding CRediT term: {expected_terms}'  

        yield build_response(
            title="CRediT taxonomy term",
            parent=self.contrib,
            item="role",
            sub_item=None,
            validation_type="exist",
            is_valid=valid_term,
            expected=expected_term or "contributor role",
            obtained=text,
            advice=advice,
            data=self.contrib,
            error_level=term_error_level,
        )
 
    def validate_role_specific_use(self):
        expected = self.params["contrib_role_specific_use_list"]
        error_level = self.params["contrib_role_specific_use_error_level"]
        specific_use = self.contrib_role.get("specific-use")
        valid = specific_use in expected
        if specific_use:
            advice = f'{self.info} replace {specific_use} in <role specific-use="{specific_use}"> with {expected}'
        else:
            advice = f'{self.info} add contributor role type <contrib><role specific-use=""></role></contrib> with {expected}'
        yield build_response(
            title="contributor role",
            parent=self.contrib,
            item="role",
            sub_item="specific-use",
            validation_type="value in list",
            is_valid=valid,
            expected=expected,
            obtained=specific_use,
            advice=advice or f'(validate_role_specific_use {self.contrib_role})',
            data=self.contrib,
            error_level=error_level,
        )
