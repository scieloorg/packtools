from packtools.sps.models.v2.article_xref import XMLCrossReference
from packtools.sps.validation.utils import format_response


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
            ),
            "attrib_name_and_value_requires_xref": [
                "materials",
                "methods",
                "results",
                "discussion"
            ],
            "xref_rid_error_level": "ERROR",
            "element_id_error_level": "ERROR",
            "attrib_name_and_value_requires_xref_error_level": "WARNING"
        }

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
                element_name = xref.get("element_name")
                xref_content = xref.get("content")
                advice = (
                    f'Found {xref.get("xml")}, but not found the corresponding {xref.get("elem_xml")}'
                )

                yield format_response(
                    title=f'<xref> is linked to {element_name}',
                    parent="article",
                    parent_id=None,
                    parent_article_type=self.xml_tree.get("article-type"),
                    parent_lang=self.xml_tree.get(
                        "{http://www.w3.org/XML/1998/namespace}lang"
                    ),
                    item="xref",
                    sub_item="@rid",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=f'{element_name} which id="{rid}"',
                    obtained=element_data,
                    advice=advice,
                    data={"xref": xref, "element": element_data, "missing_xrefs": self.missing_xrefs, "missing_elems": self.missing_elems},
                    error_level=self.params["xref_rid_error_level"],
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
            for id, elems in self.xml_cross_refs.elems_by_id(element_name).items():
                for elem_data in elems:
                    tag = elem_data.get("tag")
                    xrefs = xrefs_by_rid.get(id)
                    is_valid = bool(xrefs)
                    tag_and_attribs = elem_data.get("tag_and_attribs")
                    xref_xml = elem_data.get("xref_xml")

                    label = elem_data.get("label")
                    if label:
                        advice = (
                            f'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                            f'Mark {label}, mention to {tag_and_attribs}, with {xref_xml}'
                        )
                    else:
                        advice = (
                            f'Found {tag_and_attribs}, but no corresponding {xref_xml} was found. '
                        )

                    yield format_response(
                        title=f'{tag_and_attribs} is linked to <xref>',
                        parent=elem_data.get("parent"),
                        parent_id=elem_data.get("parent_id"),
                        parent_article_type=elem_data.get("parent_article_type"),
                        parent_lang=elem_data.get("parent_lang"),
                        item=elem_data.get("tag"),
                        sub_item="@id",
                        validation_type="match",
                        is_valid=is_valid,
                        expected=xref_xml,
                        obtained=xrefs,
                        advice=advice,
                        data={"element": elem_data, "xref": xrefs, "missing_xrefs": self.missing_xrefs, "missing_elems": self.missing_elems},
                        error_level=error_level,
                    )

    def validate_attrib_name_and_value_has_corresponding_xref(self):
        """
        Checks if sections with specific sec-type attributes have corresponding xref references.
        Only validates sections whose sec-type is in the sec_type_requires_rid list.

        Yields
        ------
        dict
            A dictionary containing validation results with standard keys.
        """
        attribs = self.params["attrib_name_and_value_requires_xref"] or []
        error_level = self.params["attrib_name_and_value_requires_xref_error_level"]

        for elems in self.xml_cross_refs.elems_by_id(attribs=attribs).values():
            for elem_data in elems:
                tag = elem_data.get("tag")
                
                xrefs = self.xrefs_by_rid.get(id)
                is_valid = bool(xrefs)
                xref_xml = elem_data.get("xref_xml")
                xml = elem_data.get("xml")
                tag_and_attribs = elem_data.get("tag_and_attribs")
                advice = (
                    f'Found {xml}, but no corresponding {self.xref_xml} was found. '
                    f'Mark the {xml} cross-references using {self.xref_xml}'
                )
                
                yield build_response(
                    title=f'{tag_and_attribs} is linked to <xref>',
                    parent=elem_data,
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
                        "attrib": attrib
                    },
                    error_level=error_level,
                )