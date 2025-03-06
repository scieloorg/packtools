import re
from copy import deepcopy
from difflib import SequenceMatcher

from packtools.sps.models.v2.aff import FulltextAffiliations
from packtools.sps.validation.utils import build_response


class FulltextAffiliationsValidation:
    def __init__(self, node, params):
        """
        Initialize validation for FulltextAffiliations.

        Parameters
        ----------
        node : etree.Element
            XML node representing article or sub-article
        params : dict
            Validation parameters including country codes and error levels
        """
        self.node = node
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.fulltext_affs = FulltextAffiliations(node)
        self.translation_params = deepcopy(self.params)
        self.translation_params.update(
            params.get("translation_aff_rules") or {}
        )

    def get_default_params(self):
        return {
            "aff_components_error_level": "ERROR",
            "id_error_level": "CRITICAL",
            "label_error_level": "ERROR",
            "original_error_level": "CRITICAL",
            "orgname_error_level": "CRITICAL",
            "orgdiv1_error_level": "ERROR",
            "orgdiv2_error_level": "WARNING",
            "country_error_level": "CRITICAL",
            "country_code_error_level": "CRITICAL",
            "state_error_level": "WARNING",
            "city_error_level": "WARNING",
            "translation_aff_rules": {
                "id_error_level": "CRITICAL",
                "label_error_level": "ERROR",
                "original_error_level": "CRITICAL",
                "orgname_error_level": "INFO",
                "country_error_level": "INFO",
                "country_code_error_level": "INFO",
                "state_error_level": "INFO",
                "city_error_level": "INFO"
            },
            "translation_qty_error_level": "CRITICAL",
            "translation_similarity_error_level": "WARNING"
        }

    def validate_main_affiliations(self):
        """
        Validate all affiliations and their translations using AffiliationValidation.

        Yields
        ------
        dict
            Validation results for each affiliation and translation
        """
        # Validate main affiliations
        for aff in self.fulltext_affs.affiliations():
            validator = AffiliationValidation(aff, self.params)
            yield from validator.validate()

    def validate_translated_affiliations(self):
        for item in self.fulltext_affs.translations:
            validator = FulltextAffiliationsValidation(
                item.node, self.translation_params
            )
            yield from validator.validate()

    def validate_translations_consistency(self):
        main_affs = list(self.fulltext_affs.affiliations())
        for (
            lang,
            trans_affs,
        ) in self.fulltext_affs.translations_data_by_lang.items():
            # Check count match
            if len(main_affs) == len(trans_affs):
                # Compare content similarity for matched pairs
                for idx, (main_aff, trans_aff) in enumerate(
                    zip(main_affs, trans_affs)
                ):
                    validator = AffiliationValidation(
                        trans_aff, self.translation_params
                    )
                    yield from validator.validate_comparison(main_aff)
            else:
                yield build_response(
                    title="translation count mismatch",
                    parent=self.fulltext_affs.attribs_parent_prefixed,
                    item="aff",
                    sub_item="quantity",
                    validation_type="match",
                    is_valid=False,
                    expected=f"{len(main_affs)} affiliations",
                    obtained=f"{len(trans_affs)} affiliations",
                    advice="Ensure translation has same number of affiliations as main text",
                    error_level=self.params["translation_qty_error_level"],
                    data={
                        "main_count": len(main_affs),
                        "translation_count": len(trans_affs),
                        "language": lang,
                    },
                )

    def validate_not_translation_affiliations(self):
        """
        Validate affiliations of sub-article which are not translation

        Yields
        ------
        dict
            Validation results for each affiliation and translation
        """
        for item in self.fulltext_affs.not_translations:
            validator = FulltextAffiliationsValidation(item.node, self.params)
            yield from validator.validate()

    def validate(self):
        """
        Validate all affiliations and their translations

        Yields
        ------
        dict
            Validation results for each affiliation and translation
        """
        yield from self.validate_main_affiliations()
        yield from self.validate_translations_consistency()
        yield from self.validate_translated_affiliations()
        yield from self.validate_not_translation_affiliations()


class AffiliationValidation:
    def __init__(self, affiliation: dict, params: dict):
        """
        Initialize the AffiliationValidation object.

        Parameters
        ----------
        affiliation : dict
            A dictionary containing the affiliation data.
        params: dict
            Dictionary containing validation parameters including:
            - country_codes_list: List of valid country codes
            - error_levels: Dict with error levels for each validation type
        """
        self.params = self.get_default_params()
        self.params.update(params or {})

        if not params.get("country_codes_list"):
            raise ValueError(
                "AffiliationValidation requires list of country codes"
            )

        self.affiliation = affiliation
        self.original = self.affiliation.get("original")
        self.original_components = {
            "orgname": self.affiliation.get("orgname"),
            "orgdiv1": self.affiliation.get("orgdiv1"),
            "orgdiv2": self.affiliation.get("orgdiv2"),
            "country_name": self.affiliation.get("country_name"),
            "state": self.affiliation.get("state"),
            "city": self.affiliation.get("city")
        }

    def get_default_params(self):
        return {
            "aff_components_error_level": "ERROR",
            "id_error_level": "CRITICAL",
            "label_error_level": "ERROR",
            "original_error_level": "CRITICAL",
            "orgname_error_level": "CRITICAL",
            "orgdiv1_error_level": "ERROR",
            "orgdiv2_error_level": "WARNING",
            "country_error_level": "CRITICAL",
            "country_code_error_level": "CRITICAL",
            "state_error_level": "WARNING",
            "city_error_level": "WARNING",
            "translation_aff_rules": {
                "id_error_level": "CRITICAL",
                "label_error_level": "ERROR",
                "original_error_level": "CRITICAL",
                "orgname_error_level": "INFO",
                "country_error_level": "INFO",
                "country_code_error_level": "INFO",
                "state_error_level": "INFO",
                "city_error_level": "INFO"
            },
            "translation_qty_error_level": "CRITICAL",
            "translation_similarity_error_level": "WARNING",
            "min_expected_similarity": {
                "original": 0.5,
                "orgname": 1,
                "orgdiv1": 0.6,
                "orgdiv2": 0.6,
                "city": 0.6,
                "state": 0.6,
                "country": 0.6,
                "country_code": 1,
            }
        }
    @property
    def info(self):
        aff_id = self.affiliation.get("id") or self.affiliation.get("original")
        parent = self.affiliation.get("parent_id") or self.affiliation.get("parent")
        return f'({parent} - {aff_id})'
        
    def validate_original(self):
        error_level = self.params["original_error_level"]

        yield build_response(
            title="original",
            parent=self.affiliation,
            item="institution",
            sub_item='@content-type="original"',
            validation_type="exist",
            is_valid=bool(self.original),
            expected="original affiliation",
            obtained=self.original,
            advice=f'Mark the complete original affiliation text with <institution content-type="original"> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_orgname(self):
        orgname = self.affiliation.get("orgname")
        error_level = self.params["orgname_error_level"]

        yield build_response(
            title="orgname",
            parent=self.affiliation,
            item="institution",
            sub_item='@content-type="orgname"',
            validation_type="exist",
            is_valid=bool(orgname),
            expected="orgname",
            obtained=orgname,
            advice=f'Mark the main institution with <institution content-type="orgname"> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_orgdiv1(self):
        orgdiv1 = self.affiliation.get("orgdiv1")
        error_level = self.params["orgdiv1_error_level"]

        yield build_response(
            title="orgdiv1",
            parent=self.affiliation,
            item="institution",
            sub_item='@content-type="orgdiv1"',
            validation_type="exist",
            is_valid=bool(orgdiv1),
            expected="orgdiv1 affiliation",
            obtained=orgdiv1,
            advice=f'Mark the first hierarchical subdivision with <institution content-type="orgdiv1"> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_orgdiv2(self):
        orgdiv2 = self.affiliation.get("orgdiv2")
        error_level = self.params["orgdiv2_error_level"]

        yield build_response(
            title="orgdiv2",
            parent=self.affiliation,
            item="institution",
            sub_item='@content-type="orgdiv2"',
            validation_type="exist",
            is_valid=bool(orgdiv2),
            expected="orgdiv2 affiliation",
            obtained=orgdiv2,
            advice=f'Mark the second hierarchical subdivision with <institution content-type="orgdiv2"> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_label(self):
        label = self.affiliation.get("label")
        error_level = self.params["label_error_level"]

        yield build_response(
            title="label",
            parent=self.affiliation,
            item="aff",
            sub_item="label",
            validation_type="exist",
            is_valid=bool(label),
            expected="label",
            obtained=label,
            advice=f'Mark affiliation label with <label> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_country(self):
        country = self.affiliation.get("country_name")
        error_level = self.params["country_error_level"]

        yield build_response(
            title="country name",
            parent=self.affiliation,
            item="aff",
            sub_item="country",
            validation_type="exist",
            is_valid=bool(country),
            expected="country name",
            obtained=country,
            advice=f'Mark affiliation country with <country> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_country_code(self):
        country_code = self.affiliation.get("country_code")
        error_level = self.params["country_code_error_level"]
        country_codes_list = self.params["country_codes_list"]

        is_valid = country_code in country_codes_list
        yield build_response(
            title="country code",
            parent=self.affiliation,
            item="country",
            sub_item="@country",
            validation_type="value in list",
            is_valid=is_valid,
            expected=(
                country_code if is_valid else f"one of {country_codes_list}"
            ),
            obtained=country_code,
            advice=f'Complete <country country=""> in <aff> with a valid value: {country_codes_list} for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_state(self):
        state = self.affiliation.get("state")
        error_level = self.params["state_error_level"]

        yield build_response(
            title="state",
            parent=self.affiliation,
            item="addr-line",
            sub_item="state",
            validation_type="exist",
            is_valid=bool(state),
            expected="state",
            obtained=state,
            advice=f'Mark affiliation state with <addr-line><state> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_city(self):
        city = self.affiliation.get("city")
        error_level = self.params["city_error_level"]

        yield build_response(
            title="city",
            parent=self.affiliation,
            item="addr-line",
            sub_item="city",
            validation_type="exist",
            is_valid=bool(city),
            expected="city",
            obtained=city,
            advice=f'Mark affiliation city with <addr-line><city> in <aff> for {self.original}',
            data=self.affiliation,
            error_level=error_level,
        )

    def validate_id(self):
        aff_id = self.affiliation.get("id")
        error_level = self.params["id_error_level"]

        yield build_response(
            title="id",
            parent=self.affiliation,
            item="aff",
            sub_item="@id",
            validation_type="exist",
            is_valid=bool(aff_id),
            expected="affiliation ID",
            obtained=aff_id,
            advice='Complete <aff id=""> with affiliation identifier. Consult the documentation of SPS of the current version',
            data=self.affiliation,
            error_level=error_level,
        )

    def compare(self, main_aff: dict):
        """
        Compare similarity between two self.affiliations.

        Parameters
        ----------
        main_aff : dict
            Affiliation dictionaries to compare

        """
        config = self.params["min_expected_similarity"]

        correct = 0
        items = []
        got = {}
        for field, min_expected_sim in config.items():
            main_value = main_aff.get(field) or ""
            translation = self.affiliation.get(field) or ""

            main_words = [
                w.strip() for w in main_value.upper().split() if w.strip()
            ]
            tran_words = [
                w.strip() for w in translation.upper().split() if w.strip()
            ]

            _main_value = sorted(main_words)
            _translation = sorted(tran_words)
            score1 = SequenceMatcher(None, _main_value, _translation).ratio()

            _main_value = " ".join(main_words)
            _translation = " ".join(tran_words)
            score2 = SequenceMatcher(None, _main_value, _translation).ratio()

            got[field] = max([score1, score2])

            valid = got[field] >= min_expected_sim

            t_info = self.affiliation.get("id") or self.affiliation.get("label")
            m_info = main_aff.get("id") or main_aff.get("label")
            
            if not valid:
                items.append(f'{field}: {main_value} ({m_info}) x {translation} ({t_info})')
            
            if valid or (_main_value and not _translation):
                correct += 1
        return {
            "valid": correct,
            "invalid": len(items) - correct,
            "items": items,
            "got": got,
        }

    def validate_comparison(self, main_aff: dict):
        """
        Compare similarity between main_aff and self.affiliations.

        Parameters
        ----------
        main_aff : dict
            Affiliation dictionaries to compare

        """
        result = self.compare(main_aff)
        invalid = result["invalid"]
        if invalid:
            got = result["got"]
            items = result["items"]

            aff_info = self.affiliation.get("id") or self.affiliation
            main_info = main_aff.get("id") or main_aff

            advice = f'Compare {main_info} and {aff_info}. Make sure they are corresponding'
            yield build_response(
                title=f"low similarity",
                parent=self.affiliation,
                item="aff",
                sub_item="translation",
                validation_type="similarity",
                is_valid=False,
                expected=f'{main_info} and {aff_info} are similar',
                obtained=f'{main_info} and {aff_info} are not similar',
                advice=advice,
                error_level=self.params["translation_similarity_error_level"],
                data=items,
            )

    def validate_aff_components(self):
        if not self.original:
            return

        original = self.original
        found = {}
        not_found = {}
        for k, v in sorted(self.original_components.items(), key=lambda x: len(x[1] or ''), reverse=True):
            if v and v in original:
                original = original.replace(v, "", 1)
                found.update({k: v})
                is_valid = True
                advice = None

                yield build_response(
                    title="original",
                    parent=self.affiliation,
                    item="institution",
                    sub_item='@content-type="original"',
                    validation_type="exist",
                    is_valid=is_valid,
                    expected=f'{k} marked',
                    obtained=v,
                    advice=advice,
                    data={k: v},
                    error_level=self.params["aff_components_error_level"]
                )

            else:
                not_found.update({k: v})

        words = [word for word in original.split() if word.isalnum() and len(word) > 2]
        if words:
            for k, v in not_found.items():
                if v:
                    advice = f'{self.info}: {v} ({k}) not found in {self.original}'
                else:
                    advice = f'{self.info}: {k} was not marked. Check {k} is found in {self.original}'
                
                is_valid = False
                yield build_response(
                    title="original",
                    parent=self.affiliation,
                    item="institution",
                    sub_item='@content-type="original"',
                    validation_type="exist",
                    is_valid=is_valid,
                    expected=f'{k} marked',
                    obtained=v,
                    advice=advice,
                    data={k: v, "original": self.original},
                    error_level=self.params["aff_components_error_level"]
                )

    def validate(self):
        """
        Validate all aspects of the affiliation.

        Yields
        ------
        dict
            Validation results for each aspect of the affiliation.
        """
        yield from self.validate_id()
        yield from self.validate_label()
        yield from self.validate_original()
        yield from self.validate_orgname()
        yield from self.validate_orgdiv1()
        yield from self.validate_orgdiv2()
        yield from self.validate_country()
        yield from self.validate_country_code()
        yield from self.validate_state()
        yield from self.validate_city()
        yield from self.validate_aff_components()
