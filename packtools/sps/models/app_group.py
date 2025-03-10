from packtools.sps.models.label_and_caption import LabelAndCaption
from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class App(LabelAndCaption):
    @property
    def id(self):
        return self.node.get("id")

    @property
    def data(self):
        base_data = super().data or {}
        return {**base_data, "id": self.id}


class AppGroup:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def data(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xml_tree
        ):
            for app_node in node.xpath(".//app-group//app"):
                app_data = App(app_node).data
                yield put_parent_context(
                    app_data, lang, article_type, parent, parent_id
                )