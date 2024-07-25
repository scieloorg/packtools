from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class App:
    def __init__(self, node):
        self.node = node

    @property
    def app_id(self):
        return self.node.get("id")

    @property
    def app_label(self):
        return self.node.findtext("label")

    @property
    def data(self):
        return {"app_id": self.app_id, "app_label": self.app_label}


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
