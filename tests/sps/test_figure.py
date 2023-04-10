from unittest import TestCase
from packtools.sps.utils import xml_utils


from packtools.sps.models.figures import Figure

from lxml import etree


class FiguresTest(TestCase):
    def test_extract_with_fig_group(self):
        xml = ("""
			<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="en">
				<front>
					<article-meta>
                        <fig-group id="dogpix4">
                            <caption><title>Figures 12-14 Bonnie Lassie</title>
                            <p>Three perspectives on My Dog</p>
                            </caption>
                        <fig id="fg-12">
                            <label>a.</label>
                                <caption>
                                    <title><p>View A: From the Front, Laughing</p></title>
                                </caption>
                                <graphic xlink:href="frontView.png"/>
                            </fig>
                        <fig id="fg-13">
                            <label>b.</label>
                            <caption>
                                <title><p>View B: From the Side, Best Profile</p></title>
                            </caption>
                            <graphic xlink:href="sideView.png"/>
                            </fig>
                        <fig id="fg-14">
                            <label>c.</label>
                            <caption>
                                <title><p>View C: In Motion, A Blur on Feet</p></title>
                            </caption>
                            <graphic xlink:href="motionView.png"/>
                        </fig>
                        </fig-group>
					</article-meta>
				</front>
			</article>
		""")
        xml = etree.fromstring(xml)
        extract = Figure(xml).extract_figures(subtag=False)
        
        expected_output = [
            {
			'fig_group_id': 'dogpix4', 
			'fig_group_title': 'Figures 12-14 Bonnie Lassie', 
			'figs': [
				{
				'id': 'fg-12', 
                'title': 'View A: From the Front, Laughing',
				'label': 'a.', 
				'graphic': 'frontView.png'
                }, 
                {
				'id': 'fg-13',
                'title': 'View B: From the Side, Best Profile', 
                'label': 'b.', 
                'graphic': 'sideView.png'
                }, 
                {
            	'id': 'fg-14',
                'title': 'View C: In Motion, A Blur on Feet', 
                'label': 'c.', 
                'graphic': 'motionView.png'
                }
            ]
            }
        ]
        
        self.assertEqual(extract, expected_output)


    def test_extract_with_fig_group_and_subtag(self):
        xml = ("""
			<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="en">
				<front>
					<article-meta>
                        <fig-group id="dogpix4">
                            <caption><title>Figures 12-14 Bonnie Lassie</title>
                            <p>Three perspectives on My Dog</p>
                            </caption>
                        <fig id="fg-12">
                            <label>a.</label>
                                <caption>
                                    <title><p>View A: From the Front, Laughing</p></title>
                                </caption>
                                <graphic xlink:href="frontView.png"/>
                            </fig>
                        <fig id="fg-13">
                            <label>b.</label>
                            <caption>
                                <title><p>View B: From the Side, Best Profile</p></title>
                            </caption>
                            <graphic xlink:href="sideView.png"/>
                            </fig>
                        <fig id="fg-14">
                            <label>c.</label>
                            <caption>
                                <title><p>View C: In <italic>Motion</italic>, A Blur on Feet</p></title>
                            </caption>
                            <graphic xlink:href="motionView.png"/>
                        </fig>
                        </fig-group>
					</article-meta>
				</front>
			</article>
		""")
        xml = etree.fromstring(xml)
        extract = Figure(xml).extract_figures(subtag=True)
        
        expected_output = [
            {
			'fig_group_id': 'dogpix4', 
			'fig_group_title': 'Figures 12-14 Bonnie Lassie', 
			'figs': [
				{
				'id': 'fg-12', 
                'title': '<p>View A: From the Front, Laughing</p>',
				'label': 'a.', 
				'graphic': 'frontView.png'
                }, 
                {
				'id': 'fg-13',
                'title': '<p>View B: From the Side, Best Profile</p>', 
                'label': 'b.', 
                'graphic': 'sideView.png'
                }, 
                {
            	'id': 'fg-14',
                'title': '<p>View C: In <italic>Motion</italic>, A Blur on Feet</p>', 
                'label': 'c.', 
                'graphic': 'motionView.png'
                }
            ]
            }
        ]
        
        self.assertEqual(extract, expected_output)


    def test_extract_without_fig_group(self):
        xml= xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0206.xml')
        extract = Figure(xml).extract_figures(subtag=False)

        expect_output = {
            'figs': [
            {
            'id': 'f01', 
            'label': 'Figure 1', 
            'title': 'Graphical representation of the characteristic and information curves of the items selected.', 
            'graphic': '0034-8910-rsp-48-2-0206-gf01'
            }, 
            {
            'id': 'f02', 
            'label': 'Figure 2', 
            'title': 'Total Information curve (10 items).', 
            'graphic': '0034-8910-rsp-48-2-0206-gf02'
            }, 
            {
            'id': 'f03', 
            'label': 
            'Figure 3', 
            'title': 'Graphical representation of the items and HIV/AIDS knowledge scores.', 
            'graphic': '0034-8910-rsp-48-2-0206-gf03'
            }, 
            {
            'id': 'f04', 
            'label': 'Figure 4', 
            'title': 'Items characteristic curves with differential item functioning.', 
            'graphic': '0034-8910-rsp-48-2-0206-gf04'
            }
            ]
        }

        self.assertEqual(extract, expect_output)