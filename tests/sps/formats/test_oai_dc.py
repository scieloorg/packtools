    def test_get_identifier(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<journal-meta>'
            '<journal-id>0718-7181</journal-id>'
            '<issn>0718-7181</issn>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id>S0718-71812022000200217</article-id>'
            '<article-id pub-id-type="doi">10.7764/aisth.72.12</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<identifier>oai:scielo:S0718-71812022000200217</identifier>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        get_identifier(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

    def test_get_set_spec(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<front>'
            '<journal-meta>'
            '<journal-id>0718-7181</journal-id>'
            '<issn>0718-7181</issn>'
            '</journal-meta>'
            '<article-meta>'
            '<article-id>S0718-71812022000200217</article-id>'
            '<article-id pub-id-type="doi">10.7764/aisth.72.12</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        expected = (
            '<setSpec>0718-7181</setSpec>'
        )

        xml_oai_dc = ET.fromstring(
            '<record/>'
        )

        get_set_spec(xml_oai_dc, xml_tree)

        self.obtained = ET.tostring(xml_oai_dc, encoding="utf-8").decode("utf-8")

        self.assertIn(expected, self.obtained)

