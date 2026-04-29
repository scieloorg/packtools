from packtools.sps.utils.xml_utils import put_parent_context, tostring


class Fig:
    def __init__(self, element):
        self.element = element

    def str_main_tag(self):
        return f'<fig fig-type="{self.fig_type}" id="{self.fig_id}">'

    def __str__(self):
        return tostring(self.element, xml_declaration=False)

    def xml(self, pretty_print=True):
        return tostring(node=self.element, doctype=None, pretty_print=pretty_print, xml_declaration=False)

    @property
    def fig_id(self):
        return self.element.get("id")

    @property
    def fig_type(self):
        return self.element.get("fig-type")

    @property
    def label(self):
        return self.element.findtext("label")

    @property
    def has_graphic(self):
        """
        Checks whether a <graphic> element exists anywhere inside <fig>.

        Returns:
            bool: True if at least one <graphic> element is present, False otherwise.
        """
        return self.element.find(".//graphic") is not None

    @property
    def graphic_href(self):
        graphic_element = self.element.find(".//graphic")
        if graphic_element is not None:
            return graphic_element.get("{http://www.w3.org/1999/xlink}href")
        return None

    @property
    def graphic_is_in_alternatives(self):
        """
        Checks whether the first <graphic> element is a direct child of <alternatives>.

        This is used to validate SVG usage: SVG files are only allowed inside
        <alternatives>. Checking the parent of the specific <graphic> element
        being validated avoids false positives when an <alternatives> block exists
        elsewhere in the <fig> but the primary <graphic> is outside it.

        Returns:
            bool: True if the first <graphic> element's parent is <alternatives>,
                  False otherwise.
        """
        graphic = self.element.find(".//graphic")
        if graphic is not None:
            parent = graphic.getparent()
            return parent is not None and parent.tag == "alternatives"
        return False

    @property
    def caption_text(self):
        caption_element = self.element.find(".//caption")
        if caption_element is not None:
            return caption_element.xpath("string()").strip()
        return ""

    @property
    def source_attrib(self):
        return self.element.findtext("attrib")

    @property
    def alternative_elements(self):
        alternative_elements = self.element.find(".//alternatives")
        if alternative_elements is not None:
            return [child.tag for child in alternative_elements]
        return []

    @property
    def file_extension(self):
        """
        Returns the file extension of the graphic href in lowercase.

        Normalising to lowercase avoids false negatives when extensions are
        written in uppercase or mixed case (e.g. .TIF, .JPG).

        Returns:
            str or None: Lowercase file extension if present, None otherwise.
        """
        file_name = self.graphic_href
        if file_name and "." in file_name:
            return file_name.split(".")[-1].lower()
        return None

    @property
    def graphic_alt_text(self):
        """
        Extracts alt-text from graphic (anywhere in fig, not just in alternatives).

        Returns:
            str or None: The text content of <alt-text> if present, None otherwise.
        """
        graphic = self.element.find(".//graphic")
        if graphic is not None:
            alt_text_elem = graphic.find("alt-text")
            if alt_text_elem is not None:
                return alt_text_elem.text
        return None

    @property
    def graphic_long_desc(self):
        """
        Extracts long-desc from graphic (anywhere in fig, not just in alternatives).

        Returns:
            str or None: The text content of <long-desc> if present, None otherwise.
        """
        graphic = self.element.find(".//graphic")
        if graphic is not None:
            long_desc_elem = graphic.find("long-desc")
            if long_desc_elem is not None:
                return long_desc_elem.text
        return None

    @property
    def xml_lang(self):
        """
        Extracts xml:lang attribute from fig element.

        Returns:
            str or None: The xml:lang attribute value if present, None otherwise.
        """
        return self.element.get("{http://www.w3.org/XML/1998/namespace}lang")

    @property
    def parent_name(self):
        """
        Gets the tag name of the parent element.

        Returns:
            str or None: The parent tag name if present, None otherwise.
        """
        parent = self.element.getparent()
        return parent.tag if parent is not None else None

    @property
    def data(self):
        return {
            "alternative_parent": "fig",
            "id": self.fig_id,
            "type": self.fig_type,
            "label": self.label,
            "has_graphic": self.has_graphic,
            "graphic": self.graphic_href,
            "graphic_is_in_alternatives": self.graphic_is_in_alternatives,
            "caption": self.caption_text,
            "source_attrib": self.source_attrib,
            "alternative_elements": self.alternative_elements,
            "file_extension": self.file_extension,
            "graphic_alt_text": self.graphic_alt_text,
            "graphic_long_desc": self.graphic_long_desc,
            "xml_lang": self.xml_lang,
            "parent_name": self.parent_name,
        }


class Figs:
    def __init__(self, node):
        """
        Initializes the Figs class with an XML node.

        Parameters:
        node : lxml.etree._Element
            The XML node (element) that contains one or more <fig> elements.
            This can be the root of an `xml_tree` or a node representing a `sub-article`.
        """
        self.node = node
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = self.node.get("article-type")

    def figs(self):
        if self.parent == "article":
            path = "./front//fig | ./body//fig | ./back//fig"
        else:
            path = ".//fig"

        for fig in self.node.xpath(path):
            data = Fig(fig).data
            yield put_parent_context(data, self.lang, self.article_type, self.parent, self.parent_id)


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "ArticleFigs": "packtools.sps.validation.models.fig",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.fig is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
