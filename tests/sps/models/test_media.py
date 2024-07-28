import unittest
from lxml import etree

from packtools.sps.models.media import Media, ArticleMedias


class MediaTest(unittest.TestCase):
    def setUp(self):
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
                <media mimetype="video" mime-subtype="mp4" xlink:href="media1.mp4">
                    <label>Media 1</label>
                </media>
            </body>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)
        self.media = Media(self.xml_tree.xpath(".//media")[0])

    def test_mimetype(self):
        self.assertEqual(self.media.mimetype, "video")

    def test_mime_subtype(self):
        self.assertEqual(self.media.mime_subtype, "mp4")

    def test_xlink_href(self):
        self.assertEqual(self.media.xlink_href, "media1.mp4")

    def test_data(self):
        expected = {
            "mimetype": "video",
            "mime_subtype": "mp4",
            "xlink_href": "media1.mp4",
        }
        obtained = self.media.data
        self.assertDictEqual(expected, obtained)


class ArticleMediasTest(unittest.TestCase):
    def setUp(self):
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
                <media mimetype="video" mime-subtype="mp4" xlink:href="media1.mp4">
                    <label>Media 1</label>
                </media>
            </body>
            <sub-article article-type="translation" xml:lang="en">
                <body>
                    <media mimetype="audio" mime-subtype="mp3" xlink:href="media2.mp3">
                        <label>Media 2</label>
                    </media>
                </body>
            </sub-article>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)

    def test_data(self):
        obtained = list(ArticleMedias(self.xml_tree).data())
        expected = [
            {
                "mimetype": "video",
                "mime_subtype": "mp4",
                "xlink_href": "media1.mp4",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
            },
            {
                "mimetype": "audio",
                "mime_subtype": "mp3",
                "xlink_href": "media2.mp3",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "en",
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
