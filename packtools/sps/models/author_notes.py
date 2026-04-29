from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups
from packtools.sps.utils.xml_utils import process_subtags


class AuthorNotes(BaseNoteGroup):

    @property
    def corresp(self):
        return process_subtags(self.fn_parent_node.find("corresp"))

    @property
    def corresp_label(self):
        return process_subtags(self.fn_parent_node.find("corresp/label"))

    @property
    def corresp_title(self):
        return process_subtags(self.fn_parent_node.find("corresp/title"))

    @property
    def corresp_bold(self):
        return process_subtags(self.fn_parent_node.find("corresp/bold"))

    @property
    def corresp_data(self):
        return {
            "corresp": self.corresp,
            "corresp_label": self.corresp_label,
            "corresp_title": self.corresp_title,
            "corresp_bold": self.corresp_bold,
        }


class FulltextAuthorNotes(BaseNoteGroups):
    def __init__(self, node):
        super().__init__(node, "author-notes", AuthorNotes)

    @property
    def corresp_data(self):
        xpath = f"front//{self.fn_parent_tag_name} | front-stub//{self.fn_parent_tag_name}"

        for fn_parent_node in self.node.xpath(xpath):
            data = self.NoteGroupClass(fn_parent_node).corresp_data
            data.update(self.attribs_parent_prefixed)
            yield data


import warnings as _warnings


def __getattr__(name):
    _moved = {
        "XMLAuthorNotes": "packtools.sps.validation.models.author_notes",
    }
    if name in _moved:
        import importlib
        _warnings.warn(
            f"{name} has moved to {_moved[name]}. "
            f"Importing from packtools.sps.models.author_notes is deprecated.",
            DeprecationWarning,
            stacklevel=2,
        )
        mod = importlib.import_module(_moved[name])
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
