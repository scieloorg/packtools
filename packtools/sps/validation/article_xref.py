from packtools.sps.models.v2.article_xref import XMLCrossReference
from packtools.sps.validation.utils import build_response


# Allowed values for @ref-type per SPS 1.10
REF_TYPES = [
    "aff",
    "app",
    "author-notes",
    "bibr",
    "bio",
    "boxed-text",
    "contrib",
    "corresp",
    "disp-formula",
    "fig",
    "fn",
    "list",
    "sec",
    "supplementary-material",
    "table",
    "table-fn",
]


class ArticleXrefValidation:
    def __init__(self, xml_tree, params=None):
        self.xml_tree = xml_tree
        self.xml_cross_refs = XMLCrossReference(xml_tree)

        # Get default parameters and update with provided params if any
        self.params = self.get_default_params()
        if params:
            self.params.update(params)

        self.xrefs_by_rid = self.xml_cross_refs.xrefs_by_rid()

        ids = set(self.xml_cross_refs.elems_by_id("*").keys())
        rids = set(self.xrefs_by_rid.keys())

        self.missing_xrefs = list(ids - rids)
        self.missing_elems = list(rids - ids)

        self._parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": self.xml_tree.get("article-type"),
            "parent_lang": self.xml_tree.get(
                "{http://www.w3.org/XML/1998/namespace}lang"
            ),
        }

    @staticmethod
    def get_default_params():
        """
        Returns the default parameters for validation.

        Returns
        -------
        dict
            Default parameters dictionary with all validation settings.
        """
        return {
            "elements_requires_xref_rid": (
                "fig",
                "disp-formula",
                "table-wrap",
                "ref",
                "aff",
                "corresp",
            ),
            "attrib_name_and_value_requires_xref": [
                {"name": "sec-type", "value": "transcript"}
            ],
            "xref_rid_error_level": "ERROR",
            "element_id_error_level": "ERROR",
            "attrib_name_and_value_requires_xref_error_level": "CRITICAL",
            "rid_presence_error_level": "CRITICAL",
            "ref_type_presence_error_level": "CRITICAL",
            "ref_type_value_error_level": "ERROR",
            "bibr_presence_error_level": "ERROR",
            "rid_id_correspondence_error_level": "ERROR",
            "transcript_xref_error_level": "WARNING",
            "aff_self_closing_error_level": "INFO",
            "ref_type_list": REF_TYPES,
        }

    def validate_rid_presence(self):
        """
        Validates that all <xref> elements have a non-empty @rid attribute.

        Yields
        ------
        dict
            Validation result for each <xref> element.
        """
        error_level = self.params["rid_presence_error_level"]
        for xref_data in self.xml_cross_refs.all_xrefs():
            rid = xref_data.get("rid")
            is_valid = bool(rid and rid.strip())
            yield build_response(
                title="xref @rid",
                parent=self._parent,
                item="xref",
                sub_item="@rid",
                validation_type="exist",
                is_valid=is_valid,
                expected="@rid attribute with a non-empty value",
                obtained=rid,
                advice=f'Provide a valid @rid attribute for <xref>',
                data=xref_data,
                error_level=error_level,
                advice_text='Provide a valid @rid attribute for <xref>',
                advice_params={},
            )

    def validate_ref_type_presence(self):
        """
        Validates that all <xref> elements have a non-empty @ref-type attribute.

        Yields
        ------
        dict
            Validation result for each <xref> element.
        """
        error_level = self.params["ref_type_presence_error_level"]
        for xref_data in self.xml_cross_refs.all_xrefs():
            ref_type = xref_data.get("ref-type")
            is_valid = bool(ref_type and ref_type.strip())
            yield build_response(
                title="xref @ref-type",
                parent=self._parent,
                item="xref",
                sub_item="@ref-type",
                validation_type="exist",
                is_valid=is_valid,
                expected="@ref-type attribute with a non-empty value",
                obtained=ref_type,
                advice=f'Provide a valid @ref-type attribute for <xref>',
                data=xref_data,
                error_level=error_level,
                advice_text='Provide a valid @ref-type attribute for <xref>',
                advice_params={},
            )

    def validate_ref_type_value(self):
        """
        Validates that @ref-type values are in the list of allowed values.

        Yields
        ------
        dict
            Validation result for each <xref> element with a @ref-type.
        """
        error_level = self.params["ref_type_value_error_level"]
        ref_type_list = self.params.get("ref_type_list", REF_TYPES)
        for xref_data in self.xml_cross_refs.all_xrefs():
            ref_type = xref_data.get("ref-type")
            if not ref_type or not ref_type.strip():
                continue
            is_valid = ref_type in ref_type_list
            yield build_response(
                title="xref @ref-type value",
                parent=self._parent,
                item="xref",
                sub_item="@ref-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=str(ref_type_list),
                obtained=ref_type,
                advice=f'Replace "{ref_type}" with one of the allowed values: {ref_type_list}',
                data=xref_data,
                error_level=error_level,
                advice_text='Replace "{ref_type}" with one of the allowed values: {ref_type_list}',
                advice_params={"ref_type": ref_type, "ref_type_list": str(ref_type_list)},
            )

    def validate_bibr_presence(self):
        """
        Validates that the document contains at least one <xref ref-type="bibr">.
        SciELO Brasil criterion.

        Yields
        ------
        dict
            Validation result for the bibr presence check.
        """
        error_level = self.params["bibr_presence_error_level"]
        all_xrefs = self.xml_cross_refs.all_xrefs()
        bibr_count = sum(1 for x in all_xrefs if x.get("ref-type") == "bibr")
        is_valid = bibr_count > 0
        yield build_response(
            title="xref @ref-type bibr",
            parent=self._parent,
            item="xref",
            sub_item='@ref-type="bibr"',
            validation_type="exist",
            is_valid=is_valid,
            expected='at least one <xref ref-type="bibr">',
            obtained=f"{bibr_count} found",
            advice='Add at least one <xref ref-type="bibr"> to the document (SciELO Brasil criterion)',
            data={"bibr_count": bibr_count},
            error_level=error_level,
            advice_text='Add at least one <xref ref-type="bibr"> to the document (SciELO Brasil criterion)',
            advice_params={"bibr_count": str(bibr_count)},
        )

    def validate_rid_has_corresponding_id(self):
        """
        Validates that every @rid in <xref> has a corresponding @id in the document.

        Yields
        ------
        dict
            Validation result for each <xref> with a @rid.
        """
        error_level = self.params["rid_id_correspondence_error_level"]
        all_ids = self.xml_cross_refs.all_ids()
        for xref_data in self.xml_cross_refs.all_xrefs():
            rid = xref_data.get("rid")
            if not rid or not rid.strip():
                continue
            rid = rid.strip()
            is_valid = rid in all_ids
            yield build_response(
                title="xref @rid id correspondence",
                parent=self._parent,
                item="xref",
                sub_item="@rid",
                validation_type="match",
                is_valid=is_valid,
                expected=f'element with @id="{rid}"',
                obtained=rid if is_valid else None,
                advice=f'@rid="{rid}" in <xref> has no corresponding @id in the document',
                data=xref_data,
                error_level=error_level,
                advice_text='@rid="{rid}" in <xref> has no corresponding @id in the document',
                advice_params={"rid": rid},
            )

    def validate_transcript_xref(self):
        """
        Validates that when <sec sec-type="transcript"> exists, there is a
        <xref ref-type="sec"> referencing it.

        Yields
        ------
        dict or None
            Validation result, or None if no transcript sections exist.
        """
        error_level = self.params["transcript_xref_error_level"]
        transcript_ids = self.xml_cross_refs.transcript_sections()
        if not transcript_ids:
            return

        xrefs_by_rid = self.xrefs_by_rid
        for sec_id in transcript_ids:
            xrefs = xrefs_by_rid.get(sec_id)
            has_sec_xref = False
            if xrefs:
                has_sec_xref = any(
                    x.get("ref-type") == "sec" for x in xrefs
                )
            yield build_response(
                title="xref for transcript section",
                parent=self._parent,
                item="xref",
                sub_item='@ref-type="sec"',
                validation_type="match",
                is_valid=has_sec_xref,
                expected=f'<xref ref-type="sec" rid="{sec_id}">',
                obtained=xrefs if has_sec_xref else None,
                advice=f'Add <xref ref-type="sec" rid="{sec_id}"> to reference the transcript section',
                data={"transcript_sec_id": sec_id},
                error_level=error_level,
                advice_text='Add <xref ref-type="sec" rid="{sec_id}"> to reference the transcript section',
                advice_params={"sec_id": sec_id},
            )

    def validate_aff_self_closing(self):
        """
        Validates that <xref ref-type="aff"> without text content uses
        self-closing format (INFO-level recommendation).

        Yields
        ------
        dict
            Validation result for each aff xref without text content.
        """
        error_level = self.params["aff_self_closing_error_level"]
        for xref_data in self.xml_cross_refs.all_xrefs():
            ref_type = xref_data.get("ref-type")
            if ref_type != "aff":
                continue
            has_text = xref_data.get("has_text_content", True)
            if has_text:
                continue
            rid = xref_data.get("rid", "")
            yield build_response(
                title="xref aff self-closing",
                parent=self._parent,
                item="xref",
                sub_item="@ref-type",
                validation_type="format",
                is_valid=False,
                expected=f'<xref ref-type="aff" rid="{rid}"/>',
                obtained=xref_data.get("xml", ""),
                advice=f'For @ref-type="aff" without text content, use self-closing: <xref ref-type="aff" rid="{rid}"/>',
                data=xref_data,
                error_level=error_level,
                advice_text='For @ref-type="aff" without text content, use self-closing: <xref ref-type="aff" rid="{rid}"/>',
                advice_params={"rid": rid},
            )

    def validate_xref_rid_has_corresponding_element_id(self):
        """
        Checks if all `rid` attributes (source) in `<xref>` elements have corresponding `id` attributes (destination)
        in the XML document.

        Yields
        ------
        dict
            A dictionary containing validation results with standard keys.
        """
        elements_by_id = self.xml_cross_refs.elems_by_id("*")
        for rid, xrefs in self.xrefs_by_rid.items():
            for xref in xrefs:
                element_data = elements_by_id.get(rid)
                is_valid = bool(element_data)
                element_name = xref.get("elem_name")
                advice = (
                    f'Found {xref.get("tag_and_attribs")}, but not found the corresponding {xref.get("elem_xml")}'
                )

                yield build_response(
                    title=f'<xref> is linked to {element_name}',
                    parent=self._parent,
                    item="xref",
                    sub_item="@rid",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=f'{element_name} which id="{rid}"',
                    obtained=element_data,
                    advice=advice,
                    data={
                        "xref": xref,
                        "element": element_data,
                        "missing_xrefs": self.missing_xrefs,
                        "missing_elems": self.missing_elems,
                    },
                    error_level=self.params["xref_rid_error_level"],
                    advice_text='Found {tag_and_attribs}, but not found the corresponding {elem_xml}',
                    advice_params={
                        "tag_and_attribs": xref.get("tag_and_attribs"),
                        "elem_xml": xref.get("elem_xml"),
                    },
                )

    def validate_element_id_has_corresponding_xref_rid(self):
        """
        Checks if all `id` attributes (destination) in the XML document have corresponding `rid` attributes (source)
        in `<xref>` elements.

        Yields
        ------
        dict
            A dictionary containing validation results with standard keys.
        """
        elements_requires_xref_rid = self.params["elements_requires_xref_rid"]
        error_level = self.params["element_id_error_level"]
        xrefs_by_rid = self.xrefs_by_rid
        elements_requires_xref_rid = set(elements_requires_xref_rid)

        for element_name in elements_requires_xref_rid:
            for id_val, elems in self.xml_cross_refs.elems_by_id(element_name).items():
                for elem_data in elems:
                    tag = elem_data.get("tag")
                    xrefs = xrefs_by_rid.get(id_val)
                    is_valid = bool(xrefs)
                    tag_and_attribs = elem_data.get("tag_and_attribs")
                    xref_xml = elem_data.get("xref_xml")

                    label = elem_data.get("label")
                    if label:
                        advice = (
                            f'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                            f'Mark {label}, mention to {tag_and_attribs}, with {xref_xml}'
                        )
                        advice_text = (
                            'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                            'Mark {label}, mention to {tag_and_attribs}, with {xref_xml}'
                        )
                        advice_params = {
                            "tag_and_attribs": tag_and_attribs,
                            "xref_xml": xref_xml,
                            "label": label,
                        }
                    else:
                        advice = (
                            f'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                        )
                        advice_text = (
                            'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                        )
                        advice_params = {
                            "tag_and_attribs": tag_and_attribs,
                            "xref_xml": xref_xml,
                        }

                    yield build_response(
                        title=f'{tag_and_attribs} is linked to <xref>',
                        parent={
                            "parent": elem_data.get("parent"),
                            "parent_id": elem_data.get("parent_id"),
                            "parent_article_type": elem_data.get("parent_article_type"),
                            "parent_lang": elem_data.get("parent_lang"),
                        },
                        item=elem_data.get("tag"),
                        sub_item="@id",
                        validation_type="match",
                        is_valid=is_valid,
                        expected=xref_xml,
                        obtained=xrefs,
                        advice=advice,
                        data={
                            "element": elem_data,
                            "xref": xrefs,
                            "missing_xrefs": self.missing_xrefs,
                            "missing_elems": self.missing_elems,
                        },
                        error_level=error_level,
                        advice_text=advice_text,
                        advice_params=advice_params,
                    )

    def validate_attrib_name_and_value_has_corresponding_xref(self):
        """
        Checks if sections with specific sec-type attributes have corresponding xref references.
        Only validates sections whose sec-type is in the attrib_name_and_value_requires_xref list.

        Yields
        ------
        dict
            A dictionary containing validation results with standard keys.
        """
        attribs = self.params["attrib_name_and_value_requires_xref"] or []
        error_level = self.params["attrib_name_and_value_requires_xref_error_level"]

        for elem_id, elems in self.xml_cross_refs.elems_by_id(attribs=attribs).items():
            for elem_data in elems:
                tag = elem_data.get("tag")

                xrefs = self.xrefs_by_rid.get(elem_id)
                is_valid = bool(xrefs)
                xref_xml = elem_data.get("xref_xml")
                tag_and_attribs = elem_data.get("tag_and_attribs")
                advice = (
                    f'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                    f'Mark the {tag_and_attribs} cross-references using {xref_xml}'
                )

                yield build_response(
                    title=f'{tag_and_attribs} is linked to <xref>',
                    parent={
                        "parent": elem_data.get("parent"),
                        "parent_id": elem_data.get("parent_id"),
                        "parent_article_type": elem_data.get("parent_article_type"),
                        "parent_lang": elem_data.get("parent_lang"),
                    },
                    item=tag,
                    sub_item="@id",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=xref_xml,
                    obtained=xrefs,
                    advice=advice,
                    data={
                        "element": elem_data,
                        "xref": xrefs,
                        "missing_xrefs": self.missing_xrefs,
                        "missing_elems": self.missing_elems,
                    },
                    error_level=error_level,
                    advice_text='Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                    'Mark the {tag_and_attribs} cross-references using {xref_xml}',
                    advice_params={
                        "tag_and_attribs": tag_and_attribs,
                        "xref_xml": xref_xml,
                    },
                )