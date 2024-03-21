from packtools.sps.utils import xml_utils


class BaseTextNode:
    def __init__(
        self,
        node,
        lang,
        tags_to_keep=None,
        tags_to_keep_with_content=None,
        tags_to_remove_with_content=None,
        tags_to_convert_to_html=None,
    ):
        self._node = node
        self._lang = lang
        self.configure(
            tags_to_keep,
            tags_to_keep_with_content,
            tags_to_remove_with_content,
            tags_to_convert_to_html,
        )

    def configure(
        self,
        tags_to_keep=None,
        tags_to_keep_with_content=None,
        tags_to_remove_with_content=None,
        tags_to_convert_to_html=None,
    ):
        self.tags_to_keep = tags_to_keep
        self.tags_to_keep_with_content = tags_to_keep_with_content
        self.tags_to_remove_with_content = tags_to_remove_with_content
        self.tags_to_convert_to_html = tags_to_convert_to_html

    @property
    def item(self):
        return dict(
            lang=self._lang,
            plain_text=self.plain_text,
            html_text=self.html_text,
        )

    @property
    def plain_text(self):
        return xml_utils.node_plain_text(self._node)

    @property
    def html_text(self):
        # se desejável modificar o resultado, executar configure antes de html_text
        return xml_utils.process_subtags(
                self._node,
                self.tags_to_keep,
                self.tags_to_keep_with_content,
                self.tags_to_remove_with_content,
                self.tags_to_convert_to_html,
        )
