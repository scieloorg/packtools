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
            "contrib_type_error_level": "ERROR",
            "contrib_role_error_level": "ERROR",
            "orcid_format_error_level": "ERROR",
            "orcid_is_registered_error_level": "ERROR",
            "affiliations_error_level": "ERROR",
            "name_error_level": "ERROR",
            "collab_error_level": "ERROR",
            "contrib_error_level": "ERROR",
            
            # ORCID validation function
            "is_orcid_registered": _callable_extern_validate_default,

            # Contrib type validation
            "contrib_type_list": ["author", "compiler"],
        }

    def validate_contrib_type(self):
        """
        Validates presence and value of @contrib-type attribute.

        SciELO Rules:
        - @contrib-type is mandatory
        - Valid values: 'author', 'compiler'
        - 'author' is mandatory for all documents except reviewer reports

        References:
        - SPS documentation: <contrib>: <name> e <collab>
        """
        error_level = self.data.get("contrib_type_error_level", "ERROR")
        contrib_type = self.contrib.get("contrib_type")
        parent_article_type = self.data.get("parent_article_type")
        valid_values = self.data.get("contrib_type_list", ["author", "compiler"])

        # 1. Verifica presença do atributo
        if not contrib_type:
            valid_values_str = ", ".join(valid_values)
            advice = f'{self.info} Add @contrib-type attribute to <contrib>. Valid values: {valid_values_str}'
            advice_text = (
                '{info} Add @contrib-type attribute to <contrib>. Valid values: {values}'
            )
            advice_params = {
                "info": self.info,
                "values": ", ".join(valid_values),
            }

            yield build_response(
                title="@contrib-type attribute",
                parent=self.contrib,
                item="contrib",
                sub_item="@contrib-type",
                validation_type="exist",
                is_valid=False,
                expected="@contrib-type attribute",
                obtained=None,
                advice=advice,
                data=self.contrib,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
            return

        # 2. Valida valor do atributo
        is_valid_value = contrib_type in valid_values

        if not is_valid_value:
            valid_values_str = " or ".join(valid_values)
            advice = f'{self.info} @contrib-type="{contrib_type}" is invalid. Use: {valid_values_str}'
            advice_text = (
                '{info} @contrib-type="{obtained}" is invalid. Use: {expected}'
            )
            advice_params = {
                "info": self.info,
                "obtained": contrib_type,
                "expected": " or ".join(valid_values),
            }

            yield build_response(
                title="@contrib-type value",
                parent=self.contrib,
                item="contrib",
                sub_item="@contrib-type",
                validation_type="value",
                is_valid=False,
                expected=valid_values,
                obtained=contrib_type,
                advice=advice,
                data=self.contrib,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

        # 3. Valida que 'author' é mandatório (exceto para reviewer report)
        if parent_article_type != "reviewer-report":
            is_author = contrib_type == "author"
            if not is_author:
                advice = f'{self.info} @contrib-type must be "author" for this document type (except reviewer reports)'
                advice_text = (
                    '{info} @contrib-type must be "author" for this document type (except reviewer reports)'
                )
                advice_params = {
                    "info": self.info,
                }

                yield build_response(
                    title="@contrib-type mandatory value",
                    parent=self.contrib,
                    item="contrib",
                    sub_item="@contrib-type",
                    validation_type="value",
                    is_valid=False,
                    expected="author",
                    obtained=contrib_type,
                    advice=advice,
                    data=self.contrib,
                    error_level=error_level,
                    advice_text=advice_text,
                    advice_params=advice_params,
                )

    def validate_role(self):
        try:
            roles = self.contrib["contrib_role"]
        except KeyError:
            parent = self.data.get("parent")
            parent_id = self.data.get("parent_id")
            parent_article_type = self.data.get("parent_article_type")

            advice = f"{self.info} Mark the contrib role. Consult SPS documentation for detailed instructions"
            advice_text = (
                "{info} Mark the contrib role. Consult SPS documentation for detailed instructions"
            )
            advice_params = {
                "info": self.info,
            }

            yield build_response(
                title=f"contributor role",
                parent=self.contrib,
                item="contrib",
                sub_item="role",
                validation_type="exist",
                is_valid=False,
                expected=f"<role> in <contrib>",
                obtained=None,
                advice=advice,
                data=self.contrib,
                error_level=self.data.get("contrib_role_error_level"),
                advice_text=advice_text,
                advice_params=advice_params,
            )
        else:
            for role in roles:
                validator = ContribRoleValidation(self.contrib, role, self.data)
                yield from validator.validate_role_specific_use()
                yield from validator.validate_credit()

    def validate_orcid_format(self):
        """
        Validates format of contributor ORCID identifiers.

        SciELO Rules:
        - ORCID is mandatory
        - Format: XXXX-XXXX-XXXX-XXXX (alphanumeric)
        - DO NOT use URLs (https://orcid.org/...)
        - Use only the alphanumeric identifier

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

        # NOVA VERIFICAÇÃO: Detecta URLs
        if _orcid and ("http://" in _orcid or "https://" in _orcid or "orcid.org" in _orcid):
            advice = f'{self.info} Do not use URLs. Extract only the alphanumeric identifier from {_orcid}'
            advice_text = (
                "{info} Do not use URLs. Extract only the alphanumeric identifier from {orcid}"
            )
            advice_params = {
                "info": self.info,
                "orcid": _orcid,
            }

            yield build_response(
                title="ORCID format - URL detected",
                parent=self.contrib,
                item="contrib-id",
                sub_item='@contrib-id-type="orcid"',
                validation_type="format",
                is_valid=False,
                expected="alphanumeric ORCID (XXXX-XXXX-XXXX-XXXX)",
                obtained=_orcid,
                advice=advice,
                data=self.contrib,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
            return

        # Validação de formato
        is_valid = bool(_orcid and re.match(_default_orcid, _orcid))
        expected_value = _orcid if is_valid else "valid ORCID"

        if _orcid:
            advice = f'Fix ORCID format <contrib-id contrib-id-type="orcid">{_orcid}</contrib-id>'
            advice_text = (
                'Fix ORCID format <contrib-id contrib-id-type="orcid">{orcid}</contrib-id>'
            )
            advice_params = {
                "orcid": _orcid,
            }
        else:
            advice = f'{self.info} Add ORCID <contrib-id contrib-id-type="orcid"></contrib-id> in <contrib>'
            advice_text = (
                '{info} Add ORCID <contrib-id contrib-id-type="orcid"></contrib-id> in <contrib>'
            )
            advice_params = {
                "info": self.info,
            }

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
            advice_text=advice_text,
            advice_params=advice_params,
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

        advice = f'{self.info} Unable to automatically check the {orcid}. Check it manually'
        advice_text = (
            '{info} Unable to automatically check the {orcid}. Check it manually'
        )
        advice_params = {
            "info": self.info,
            "orcid": orcid,
        }

        yield build_response(
            title="Registered ORCID",
            parent=self.contrib,
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="registered",
            is_valid=result["status"] == "registered",
            expected="registered",
            obtained=result["status"],
            advice=advice,
            data=result,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
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

        advice = f'{self.info} Add <xref ref-type="aff" rid=""> in <contrib>'
        advice_text = (
            '{info} Add <xref ref-type="aff" rid=""> in <contrib>'
        )
        advice_params = {
            "info": self.info,
        }

        yield build_response(
            title="affiliation",
            parent=self.contrib,
            item="contrib",
            sub_item="xref",
            validation_type="exist",
            is_valid=bool(affs),  # CORRIGIDO: válido quando TEM afiliações
            expected="affiliation",
            obtained=affs or None,
            advice=advice,
            data=self.contrib,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_name(self):
        """Validates presence of contributor name elements."""
        error_level = self.data["name_error_level"]
        item = self.contrib.get("contrib_name")

        advice = f"{self.info} Mark contributor name with <name> in <contrib>"
        advice_text = (
            "{info} Mark contributor name with <name> in <contrib>"
        )
        advice_params = {
            "info": self.info,
        }

        yield build_response(
            title="contributor name",
            parent=self.contrib,
            item="contrib",
            sub_item="name",
            validation_type="exist",
            is_valid=bool(item),
            expected="contributor name",
            obtained=item,
            advice=advice,
            data=self.contrib,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_collab(self):
        """Validates presence of collaboration information."""
        error_level = self.data["collab_error_level"]
        item = self.contrib.get("collab")

        advice = f"{self.info} Mark institutional contributor with <collab> in <contrib>"
        advice_text = (
            "{info} Mark institutional contributor with <collab> in <contrib>"
        )
        advice_params = {
            "info": self.info,
        }

        yield build_response(
            title="collab",
            parent=self.contrib,
            item="contrib",
            sub_item="collab",
            validation_type="exist",
            is_valid=bool(item),
            expected="collab",
            obtained=None,
            advice=advice,
            data=self.contrib,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
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
            advice_text = (
                "{info} Mark contributor with <name> and anonymous contributor with <anonymous/> in <contrib>"
            )
            advice_params = {
                "info": self.info,
            }
        else:
            expected = ["name", "collab"]
            value = self.contrib.get("contrib_name") or self.contrib.get("collab")
            advice = f"{self.info} Mark contributor with <name> and institutional contributor with <collab> in <contrib>"
            advice_text = (
                "{info} Mark contributor with <name> and institutional contributor with <collab> in <contrib>"
            )
            advice_params = {
                "info": self.info,
            }

        yield build_response(
            title="contributor",
            parent=self.contrib,
            item="contrib",
            sub_item=None,
            validation_type="exist",
            is_valid=bool(value),
            expected=expected,
            obtained=value,
            advice=advice,
            data=self.contrib,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate(self):
        """Runs all validation checks on contributor metadata."""
        yield from self.validate_contrib_type()
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
            "orcid_is_unique_error_level": "ERROR",
            "credit_consistency_error_level": "ERROR",
            "subarticle_collab_id_error_level": "ERROR",
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
        advice_text = ("ORCID must be unique. {questions}")
        advice_params = {
            "questions": questions,
        }

        yield build_response(
            title="Unique ORCID",
            parent=parent,
            item="contrib-id",
            sub_item='@contrib-id-type="orcid"',
            validation_type="uniqueness",
            is_valid=not bool(repeated_orcid),
            expected="Unique ORCID",
            obtained=repeated_orcid,
            advice=advice,
            data=repeated_orcid,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate(self):
        # A validação da unicidade do ORCID é feita uma única vez por artigo
        yield from self.validate_orcid_is_unique()

        # Nova validação: Consistência CRediT
        credit_validator = DocumentCreditConsistencyValidation(self.xmltree, self.params)
        yield from credit_validator.validate_credit_consistency()

        # Nova validação: IDs únicos em sub-articles
        subarticle_validator = SubArticleCollabIDValidation(self.xmltree, self.params)
        yield from subarticle_validator.validate()

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

        # Nova validação: Grupos completos
        collab_validator = CollabGroupValidation(self.node, self.params)
        yield from collab_validator.validate_collab_members_completeness()

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
                advice_text = (
                    'Add person authors, members of {collab}, with <contrib><name>...</name></contrib> in <contrib-group content-type="collab-list"></contrib-group>'
                )
                advice_params = {
                    "collab": self.text_contribs.collab,
                }
            else:
                type_value = contrib_group_data["type"]
                advice = f'Remove content-type="{type_value}" from <contrib-group content-type="{type_value}">'
                advice_text = (
                    'Remove content-type="{type}" from <contrib-group content-type="{type}">'
                )
                advice_params = {
                    "type": type_value,
                }

            yield build_response(
                title=f"{title} contributor group type",
                parent=self.text_contribs.attribs_parent_prefixed,
                item="contrib-group",
                sub_item="",
                validation_type="value",
                is_valid=valid,
                expected=expected_type,
                obtained=contrib_group_data["type"],
                advice=advice,
                data=contrib_group_data,
                error_level=self.params["collab_list_error_level"],
                advice_text=advice_text,
                advice_params=advice_params,
            )


class CollabGroupValidation:
    """
    Validates complete structure and requirements for collaboration groups.

    SciELO Rules:
    - Members in collab-list must have:
      1. Full name (described in PDF)
      2. Complete affiliation (described in PDF)
      3. ORCID (described in PDF)
    - Without this identification, authors cannot assign DOI to their curriculum
    """

    def __init__(self, node, params):
        self.params = self._get_default_params()
        self.params.update(params or {})
        self.node = node
        self.text_contribs = TextContribs(node)

    def _get_default_params(self):
        return {
            "collab_member_name_error_level": "ERROR",
            "collab_member_aff_error_level": "ERROR",
            "collab_member_orcid_error_level": "ERROR",
        }

    def validate_collab_members_completeness(self):
        """
        Validates that all members of a collaboration group have complete information.
        """
        # Encontra contrib-group com content-type="collab-list"
        collab_list_groups = [
            cg for cg in self.text_contribs.contrib_groups
            if cg.data.get("type") == "collab-list"
        ]

        if not collab_list_groups:
            return

        for contrib_group in collab_list_groups:
            for contrib_data in contrib_group.data.get("contribs", []):
                # Valida nome
                if not contrib_data.get("contrib_name"):
                    advice = "All members of collaboration group must have name <name> in <contrib-group content-type='collab-list'>"
                    advice_text = (
                        "All members of collaboration group must have name <name> in <contrib-group content-type='collab-list'>"
                    )
                    advice_params = {}

                    yield build_response(
                        title="collab member name",
                        parent=contrib_data,
                        item="contrib",
                        sub_item="name",
                        validation_type="exist",
                        is_valid=False,
                        expected="author name in collab-list",
                        obtained=None,
                        advice=advice,
                        data=contrib_data,
                        error_level=self.params["collab_member_name_error_level"],
                        advice_text=advice_text,
                        advice_params=advice_params,
                    )

                # Valida afiliação
                affs = contrib_data.get("affs") or []

                # Para collab-list, afiliação pode ser indicada via <xref ref-type="aff">
                contrib_xref = contrib_data.get("contrib_xref") or []
                has_aff_xref = any(
                    xref.get("ref_type") == "aff" or xref.get("ref-type") == "aff"
                    for xref in contrib_xref
                )

                # Tem afiliação se: affs populado OU xref para aff existe
                has_affiliation = bool(affs) or has_aff_xref

                if not has_affiliation:
                    advice = "All members of collaboration group must have complete affiliation <xref ref-type='aff'> (described in PDF)"
                    advice_text = (
                        "All members of collaboration group must have complete affiliation <xref ref-type='aff'> (described in PDF)"
                    )
                    advice_params = {}

                    yield build_response(
                        title="collab member affiliation",
                        parent=contrib_data,
                        item="contrib",
                        sub_item="xref",
                        validation_type="exist",
                        is_valid=False,
                        expected="affiliation for collab member",
                        obtained=None,
                        advice=advice,
                        data=contrib_data,
                        error_level=self.params["collab_member_aff_error_level"],
                        advice_text=advice_text,
                        advice_params=advice_params,
                    )

                # Valida ORCID (mais rigoroso para membros de grupo)
                orcid = contrib_data.get("contrib_ids", {}).get("orcid")
                if not orcid:
                    advice = (
                        "All members of collaboration group MUST have ORCID (described in PDF). "
                        "Without ORCID identification, authors cannot assign DOI as their work in curriculum databases"
                    )
                    advice_text = (
                        "All members of collaboration group MUST have ORCID (described in PDF). "
                        "Without ORCID identification, authors cannot assign DOI as their work in curriculum databases"
                    )
                    advice_params = {}

                    yield build_response(
                        title="collab member ORCID",
                        parent=contrib_data,
                        item="contrib-id",
                        sub_item='@contrib-id-type="orcid"',
                        validation_type="exist",
                        is_valid=False,
                        expected="ORCID for collab member",
                        obtained=None,
                        advice=advice,
                        data=contrib_data,
                        error_level=self.params["collab_member_orcid_error_level"],
                        advice_text=advice_text,
                        advice_params=advice_params,
                    )


class DocumentCreditConsistencyValidation:
    """
    Validates that CRediT taxonomy is used consistently across the document.

    SciELO Rule:
    - If using CRediT, use it for ALL contributors
    - Do not mix CRediT with other taxonomies
    - "All or nothing" principle
    """

    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.xml_contribs = XMLContribs(self.xmltree)
        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        return {
            "credit_consistency_error_level": "ERROR",
        }

    def validate_credit_consistency(self):
        """
        Validates "all or nothing" rule for CRediT taxonomy.
        """
        # Coleta estatísticas de uso de CRediT
        total_contribs = 0
        contribs_with_credit = 0
        contribs_without_credit = 0
        mixed_contribs = []  # Contribs que misturam CRediT e não-CRediT

        for contrib in self.xml_contribs.all_contribs:
            if contrib.get("anonymous"):
                continue

            roles = contrib.get("contrib_role", [])
            if not roles:
                continue

            total_contribs += 1
            has_credit = False
            has_non_credit = False

            for role in roles:
                if role.get("content-type"):
                    has_credit = True
                else:
                    has_non_credit = True

            # Detecta mistura no mesmo contrib
            if has_credit and has_non_credit:
                # Use fallback para evitar None em contribuidores institucionais
                name = contrib.get("contrib_full_name") or contrib.get("collab") or "<unknown contributor>"
                mixed_contribs.append(name)

            if has_credit:
                contribs_with_credit += 1
            else:
                contribs_without_credit += 1

        # Valida consistência
        if total_contribs == 0:
            return

        parent = self.xml_contribs.text_contribs.attribs_parent_prefixed

        # Caso 1: Mistura no mesmo contrib (erro grave)
        if mixed_contribs:
            advice = (
                "Do not mix CRediT taxonomy with other taxonomies in the same contributor. "
                "All roles for a contributor must use the same taxonomy."
            )
            advice_text = (
                "Do not mix CRediT taxonomy with other taxonomies in the same contributor. "
                "All roles for a contributor must use the same taxonomy."
            )
            advice_params = {}

            mixed_contribs_str = ', '.join(str(c) for c in mixed_contribs if c)

            yield build_response(
                title="CRediT taxonomy consistency - mixed roles",
                parent=parent,
                item="role",
                sub_item="@content-type",
                validation_type="consistency",
                is_valid=False,
                expected="consistent taxonomy (all CRediT or all non-CRediT)",
                obtained=f"mixed taxonomy in contributors: {mixed_contribs_str}",
                advice=advice,
                data={"mixed_contribs": mixed_contribs},
                error_level=self.params["credit_consistency_error_level"],
                advice_text=advice_text,
                advice_params=advice_params,
            )

        # Caso 2: Alguns usam CRediT, outros não (erro de consistência)
        if 0 < contribs_with_credit < total_contribs:
            advice = (
                "CRediT taxonomy must be used consistently: either ALL contributors use CRediT "
                "or NONE use it. Do not mix taxonomies in the document. "
                "SciELO Rule: 'tudo ou nada' (all or nothing)."
            )
            advice_text = (
                "CRediT taxonomy must be used consistently: either ALL contributors use CRediT "
                "or NONE use it. Do not mix taxonomies in the document. "
                "SciELO Rule: 'tudo ou nada' (all or nothing)."
            )
            advice_params = {}

            yield build_response(
                title="CRediT taxonomy consistency - document level",
                parent=parent,
                item="role",
                sub_item="@content-type",
                validation_type="consistency",
                is_valid=False,
                expected="consistent taxonomy across all contributors",
                obtained=(
                    f"{contribs_with_credit} contributors with CRediT, "
                    f"{contribs_without_credit} without CRediT"
                ),
                advice=advice,
                data={
                    "total_contribs": total_contribs,
                    "with_credit": contribs_with_credit,
                    "without_credit": contribs_without_credit,
                },
                error_level=self.params["credit_consistency_error_level"],
                advice_text=advice_text,
                advice_params=advice_params,
            )


class SubArticleCollabIDValidation:
    """
    Validates that collaboration IDs are unique between article and sub-articles.

    SciELO Rule:
    - If article uses id="collab", sub-article must use id="collab1"
    - If article uses rid="collab", sub-article must use rid="collab1"
    - Prevents ID collisions between translations and original
    """

    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.params = self._get_default_params()
        self.params.update(params or {})

    def _get_default_params(self):
        return {
            "subarticle_collab_id_error_level": "ERROR",
        }

    def collect_collab_ids(self, node, context="article"):
        """Coleta todos os IDs de colaboração em um nó."""
        ids = {"id": set(), "rid": set()}

        # Para article principal, excluir contrib dentro de sub-article
        # Para sub-article, buscar normalmente
        if context == "article":
            # Busca contrib[@id] que NÃO estão dentro de sub-article
            xpath_id = ".//contrib[@id][not(ancestor::sub-article)]"
            xpath_rid = ".//contrib[@rid][not(ancestor::sub-article)]"
        else:
            # Para sub-articles, buscar normalmente
            xpath_id = ".//contrib[@id]"
            xpath_rid = ".//contrib[@rid]"

        for contrib in node.xpath(xpath_id):
            collab_id = contrib.get("id")
            if collab_id:
                ids["id"].add((collab_id, context))

        for contrib in node.xpath(xpath_rid):
            collab_rid = contrib.get("rid")
            if collab_rid:
                ids["rid"].add((collab_rid, context))

        return ids

    def validate(self):
        """Valida unicidade de IDs entre article e sub-articles."""
        # Coleta IDs do article principal
        article_node = self.xmltree.find(".//article")
        if article_node is None:
            article_node = self.xmltree

        article_ids = self.collect_collab_ids(article_node, "article")

        # Para cada sub-article
        for sub_article in self.xmltree.findall(".//sub-article"):
            sub_article_type = sub_article.get("article-type", "")
            sub_article_id = sub_article.get("id", "unknown")

            sub_ids = self.collect_collab_ids(sub_article, f"sub-article({sub_article_id})")

            parent = {"parent": f"sub-article", "parent_id": sub_article_id, "parent_article_type": sub_article_type, "parent_lang": None}

            # Verifica colisões de @id
            article_id_values = {id_val for id_val, _ in article_ids["id"]}
            sub_id_values = {id_val for id_val, _ in sub_ids["id"]}
            collisions_id = article_id_values & sub_id_values

            if collisions_id:
                advice = (
                    f"Sub-article {sub_article_id} uses same @id as main article: {list(collisions_id)}. "
                    f"If article uses id='collab', sub-article should use id='collab1'"
                )
                advice_text = (
                    "Sub-article {sub_id} uses same @id as main article: {collisions}. "
                    "If article uses id='collab', sub-article should use id='collab1'"
                )
                advice_params = {
                    "sub_id": sub_article_id,
                    "collisions": ", ".join(list(collisions_id)),
                }

                yield build_response(
                    title="collaboration @id uniqueness in sub-article",
                    parent=parent,
                    item="contrib",
                    sub_item="@id",
                    validation_type="uniqueness",
                    is_valid=False,
                    expected="unique @id values between article and sub-article",
                    obtained=f"collision: {list(collisions_id)}",
                    advice=advice,
                    data={"collisions": list(collisions_id)},
                    error_level=self.params["subarticle_collab_id_error_level"],
                    advice_text=advice_text,
                    advice_params=advice_params,
                )

            # Verifica colisões de @rid
            article_rid_values = {rid_val for rid_val, _ in article_ids["rid"]}
            sub_rid_values = {rid_val for rid_val, _ in sub_ids["rid"]}
            collisions_rid = article_rid_values & sub_rid_values

            if collisions_rid:
                advice = (
                    f"Sub-article {sub_article_id} uses same @rid as main article: {list(collisions_rid)}. "
                    f"If article uses rid='collab', sub-article should use rid='collab1'"
                )
                advice_text = (
                    "Sub-article {sub_id} uses same @rid as main article: {collisions}. "
                    "If article uses rid='collab', sub-article should use rid='collab1'"
                )
                advice_params = {
                    "sub_id": sub_article_id,
                    "collisions": ", ".join(list(collisions_rid)),
                }

                yield build_response(
                    title="collaboration @rid uniqueness in sub-article",
                    parent=parent,
                    item="contrib",
                    sub_item="@rid",
                    validation_type="uniqueness",
                    is_valid=False,
                    expected="unique @rid values between article and sub-article",
                    obtained=f"collision: {list(collisions_rid)}",
                    advice=advice,
                    data={"collisions": list(collisions_rid)},
                    error_level=self.params["subarticle_collab_id_error_level"],
                    advice_text=advice_text,
                    advice_params=advice_params,
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
                {"term": "Conceptualization", "uri": "https://credit.niso.org/contributor-roles/conceptualization/"},
                {"term": "Data curation", "uri": "https://credit.niso.org/contributor-roles/data-curation/"},
                {"term": "Formal analysis", "uri": "https://credit.niso.org/contributor-roles/formal-analysis/"},
                {"term": "Funding acquisition", "uri": "https://credit.niso.org/contributor-roles/funding-acquisition/"},
                {"term": "Investigation", "uri": "https://credit.niso.org/contributor-roles/investigation/"},
                {"term": "Methodology", "uri": "https://credit.niso.org/contributor-roles/methodology/"},
                {"term": "Project administration", "uri": "https://credit.niso.org/contributor-roles/project-administration/"},
                {"term": "Resources", "uri": "https://credit.niso.org/contributor-roles/resources/"},
                {"term": "Software", "uri": "https://credit.niso.org/contributor-roles/software/"},
                {"term": "Supervision", "uri": "https://credit.niso.org/contributor-roles/supervision/"},
                {"term": "Validation", "uri": "https://credit.niso.org/contributor-roles/validation/"},
                {"term": "Visualization", "uri": "https://credit.niso.org/contributor-roles/visualization/"},
                {"term": "Writing – original draft", "uri": "https://credit.niso.org/contributor-roles/writing-original-draft/"},
                {"term": "Writing – review & editing", "uri": "https://credit.niso.org/contributor-roles/writing-review-editing/"}
            ],

            # List of valid contributor role types (CORRIGIDO)
            "contrib_role_specific_use_list": [
                "editor",
                "reviewer"
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
        advice_text = None
        advice_params = {}

        if not valid_uri:
            if expected_uri and uri:
                advice = f'{self.info} replace <role content-type="{uri}"> by <role content-type="{expected_uri}">'
                advice_text = ('{info} replace <role content-type="{uri}"> by <role content-type="{expected_uri}">')
                advice_params = {"info": self.info, "uri": uri, "expected_uri": expected_uri}
            elif expected_uri:
                advice = f'{self.info} replace <role>{text}</role> by <role content-type="{expected_uri}">{text}</role>'
                advice_text = ('{info} replace <role>{text}</role> by <role content-type="{expected_uri}">{text}</role>')
                advice_params = {"info": self.info, "text": text, "expected_uri": expected_uri}
            elif uri:
                expected_uris = list(credit_taxonomy_by_uri.keys())
                advice = f'{self.info} check if <role content-type="{uri}">{text}</role> has corresponding CRediT URI: {expected_uris}'
                advice_text = ('{info} check if <role content-type="{uri}">{text}</role> has corresponding CRediT URI')
                advice_params = {"info": self.info, "uri": uri, "text": text}
            elif text:
                expected_uris = list(credit_taxonomy_by_uri.keys())
                advice = f'{self.info} check if <role>{text}</role> has corresponding CRediT URI: {expected_uris}'
                advice_text = ('{info} check if <role>{text}</role> has corresponding CRediT URI')
                advice_params = {"info": self.info, "text": text}

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
            advice_text=advice_text,
            advice_params=advice_params,
        )
        
        if not valid_term:
            if uri:
                content_type = f' content-type="{uri}"'
            else:
                content_type = ''
            if expected_term and text:
                advice = f'{self.info} replace <role{content_type}>{text}</role> by <role{content_type}>{expected_term}</role>'
                advice_text = ('{info} replace <role{content_type}>{text}</role> by <role{content_type}>{expected_term}</role>')
                advice_params = {"info": self.info, "content_type": content_type, "text": text, "expected_term": expected_term}
            elif expected_term:
                advice = f'{self.info} replace <role{content_type}></role> by <role{content_type}>{expected_term}</role>'
                advice_text = ('{info} replace <role{content_type}></role> by <role{content_type}>{expected_term}</role>')
                advice_params = {"info": self.info, "content_type": content_type, "expected_term": expected_term}
            elif text:
                expected_terms = self.params["credit_taxonomy_by_terms"]
                advice = f'{self.info} check if <role{content_type}>{text}</role> has corresponding CRediT term: {expected_terms}'
                advice_text = ('{info} check if <role{content_type}>{text}</role> has corresponding CRediT term')
                advice_params = {"info": self.info, "content_type": content_type, "text": text}
            else:
                expected_terms = self.params["credit_taxonomy_by_terms"]
                advice = f'{self.info} check if <role{content_type}>{text}</role> has corresponding CRediT term: {expected_terms}'
                advice_text = ('{info} check if <role{content_type}>{text}</role> has corresponding CRediT term')
                advice_params = {"info": self.info, "content_type": content_type, "text": text}

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
            advice_text=advice_text,
            advice_params=advice_params,
        )
 
    def validate_role_specific_use(self):
        """
        Validates @specific-use attribute in <role>.

        SciELO Rule:
        - For reviewer reports: @specific-use is MANDATORY
        - Valid values: "reviewer", "editor"
        """
        expected = self.params["contrib_role_specific_use_list"]
        error_level = self.params["contrib_role_specific_use_error_level"]
        specific_use = self.contrib_role.get("specific-use")
        parent_article_type = self.contrib.get("parent_article_type")

        # Determina se specific-use é obrigatório
        is_reviewer_report = parent_article_type == "reviewer-report"

        # VALIDAÇÃO 1: Existência (obrigatório para reviewer-report)
        if not specific_use:
            if is_reviewer_report:
                # Para reviewer-report, ausência é ERRO
                advice = f'{self.info} add <role specific-use="[reviewer|editor]"> for reviewer report'
                advice_text = '{info} add <role specific-use=""> with {expected}'
                advice_params = {"info": self.info, "expected": " or ".join(expected)}

                yield build_response(
                    title="contributor role type (reviewer report)",
                    parent=self.contrib,
                    item="role",
                    sub_item="specific-use",
                    validation_type="exist",
                    is_valid=False,
                    expected="specific-use attribute",
                    obtained=None,
                    advice=advice,
                    data=self.contrib,
                    error_level=error_level,
                    advice_text=advice_text,
                    advice_params=advice_params,
                )
            # Para outros tipos, specific-use é opcional - não gera erro
            return

        # VALIDAÇÃO 2: Valor (se presente, deve ser válido)
        valid = specific_use in expected

        if not valid:
            expected_str = " or ".join(expected)
            advice = f'{self.info} replace <role specific-use="{specific_use}"> with {expected_str}'
            advice_text = '{info} replace <role specific-use="{specific_use}"> with {expected}'
            advice_params = {"info": self.info, "specific_use": specific_use, "expected": expected_str}

            yield build_response(
                title="contributor role type value",
                parent=self.contrib,
                item="role",
                sub_item="specific-use",
                validation_type="value in list",
                is_valid=False,
                expected=expected,
                obtained=specific_use,
                advice=advice,
                data=self.contrib,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

