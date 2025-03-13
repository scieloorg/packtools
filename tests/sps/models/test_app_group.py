import unittest
from lxml.etree import Element, SubElement, QName
from packtools.sps.models.app_group import App, XmlAppGroup


XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"


class AppTest(unittest.TestCase):
    def setUp(self):
        """Configuração inicial dos elementos XML para cada teste."""

        self.app_group = Element("app-group", nsmap={"xlink": XLINK_NAMESPACE})

        # Criando primeiro <app> com <graphic>
        self.app1 = SubElement(self.app_group, "app", {"id": "app1"})
        SubElement(self.app1, "label").text = "Appendix 1"
        SubElement(self.app1, "graphic", {QName(XLINK_NAMESPACE, "href"): "image1.jpg"})

        # Criando segundo <app> com <media>
        self.app2 = SubElement(self.app_group, "app", {"id": "app2"})
        SubElement(self.app2, "label").text = "Appendix 2"
        media = SubElement(self.app2, "media", {
            "mimetype": "video",
            "mime-subtype": "mp4",
            QName(XLINK_NAMESPACE, "href"): "video1.mp4"
        })
        SubElement(media, "label").text = "Video 1"
        caption = SubElement(media, "caption")
        SubElement(caption, "title").text = "Video 1"

        self.app = App(self.app_group.xpath(".//app")[0])

    def test_app_id(self):
        self.assertEqual(self.app.id, "app1")

    def test_app_label(self):
        self.assertEqual(self.app.label, "Appendix 1")

    def test_data(self):
        expected = {
            'attrib': None,
            'caption': None,
            'graphics': [{'alt_text': None,
                        'content_type': None,
                        'id': None,
                        'long_desc': None,
                        'speakers': None,
                        'tag': 'graphic',
                        'transcript': None,
                        'xlink_href': 'image1.jpg'}],
            'id': 'app1',
            'label': 'Appendix 1',
            'media': []
        }
        obtained = self.app.data
        self.assertDictEqual(expected, obtained)


class AppGroupTest(unittest.TestCase):
    def setUp(self):
        """Criação do XML em memória para testes de AppGroup."""

        self.xml_tree = Element("article", nsmap={"xlink": XLINK_NAMESPACE})
        self.app_group = SubElement(self.xml_tree, "app-group")

        # Criando primeiro <app> com <graphic>
        self.app1 = SubElement(self.app_group, "app", {"id": "app1"})
        SubElement(self.app1, "label").text = "Appendix 1"
        SubElement(self.app1, "graphic", {QName(XLINK_NAMESPACE, "href"): "image1.jpg"})

        # Criando segundo <app> com <media>
        self.app2 = SubElement(self.app_group, "app", {"id": "app2"})
        SubElement(self.app2, "label").text = "Appendix 2"
        media = SubElement(self.app2, "media", {
            "mimetype": "video",
            "mime-subtype": "mp4",
            QName(XLINK_NAMESPACE, "href"): "video1.mp4"
        })
        SubElement(media, "label").text = "Video 1"
        caption = SubElement(media, "caption")
        SubElement(caption, "title").text = "Video 1"

    def test_data(self):
        self.maxDiff = None
        obtained = list(XmlAppGroup(self.xml_tree).data())
        self.assertEqual(len(obtained), 2)


if __name__ == "__main__":
    unittest.main()
