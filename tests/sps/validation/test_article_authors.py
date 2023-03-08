from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils

from packtools.sps.validation.article_authors import ArticleAuthorsValidation


class ArticleAuthorsValidationTest(TestCase):
	
	def test_without_role(self):
		xml =  ("""
		<article>
			<front>
				<article-meta>
					<contrib-group>
						<contrib contrib-type="author">
							<name>
								<surname>VENEGAS-MARTÍNEZ</surname>
								<given-names>FRANCISCO</given-names>
								<prefix>Prof</prefix>
								<suffix>Nieto</suffix>
							</name>
							<xref ref-type="aff" rid="aff1"/>
							</contrib>
							<contrib contrib-type="author">
							<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
							<name>
								<surname>Higa</surname>
								<given-names>Vanessa M.</given-names>
							</name>
							<xref ref-type="aff" rid="aff1">a</xref>
						</contrib>
					</contrib-group>
				</article-meta>
			</front>
		</article>
		""")
		list_content_type = [
			('Data curation',
			 'https://credit.niso.org/contributor-roles/data-curation/'),
			('Conceptualization',
			 'https://credit.niso.org/contributor-roles/conceptualization/'),
			('Formal analysis',
			 'https://credit.niso.org/contributor-roles/formal-analysis/'),
		]

		data = etree.fromstring(xml)
		messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(content_type_url=list_content_type)

		expected_output = {
				'errors': [
					"The author 'FRANCISCO VENEGAS-MARTÍNEZ' has no <role> tag assigned to him", 
					"The author 'Vanessa M. Higa' has no <role> tag assigned to him"
				], 
				'warnings': [],
				'invalid_role': [], 
				'invalid_content_type': []
			}

		self.assertEqual(messages, expected_output)
	
	def test_role_empty(self):
		xml =  ("""
		<article>
			<front>
				<article-meta>
					<contrib-group>
						<contrib contrib-type="author">
							<name>
								<surname>VENEGAS-MARTÍNEZ</surname>
								<given-names>FRANCISCO</given-names>
								<prefix>Prof</prefix>
								<suffix>Nieto</suffix>
							</name>
							<xref ref-type="aff" rid="aff1"/>
							<role></role>
							</contrib>
							<contrib contrib-type="author">
							<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
							<name>
								<surname>Higa</surname>
								<given-names>Vanessa M.</given-names>
							</name>
							<xref ref-type="aff" rid="aff1">a</xref>
							<role></role>
						</contrib>
					</contrib-group>
				</article-meta>
			</front>
		</article>
		""")
		list_content_type = [
			('Data curation',
			 'https://credit.niso.org/contributor-roles/data-curation/'),
			('Conceptualization',
			 'https://credit.niso.org/contributor-roles/conceptualization/'),
			('Formal analysis',
			 'https://credit.niso.org/contributor-roles/formal-analysis/'),
		]
		
		data = etree.fromstring(xml)
		messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(content_type_url=list_content_type)
		
		expected_output = {
				'errors': [
					"The author 'FRANCISCO VENEGAS-MARTÍNEZ' has an <role> tag empty assigned to him", 
					"The author 'Vanessa M. Higa' has an <role> tag empty assigned to him"
				], 
				'warnings': [],
				'invalid_role': [], 
				'invalid_content_type': []
			}
		
		self.assertEqual(messages, expected_output)

	def test_without_content_type(self):
		xml = ("""
			<article>
				<front>
					<article-meta>
						<contrib-group>
							<contrib contrib-type="author">
								<name>
									<surname>VENEGAS-MARTÍNEZ</surname>
									<given-names>FRANCISCO</given-names>
									<prefix>Prof</prefix>
									<suffix>Nieto</suffix>
								</name>
								<xref ref-type="aff" rid="aff1"/>
								<role>Data curation</role>
								<role>Concepalization</role>
								</contrib>
								<contrib contrib-type="author">
								<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
								<name>
									<surname>Higa</surname>
									<given-names>Vanessa M.</given-names>
								</name>
								<xref ref-type="aff" rid="aff1">a</xref>
								<role>Formal analysis</role>
							</contrib>
						</contrib-group>
					</article-meta>
				</front>
			</article>
			""")

		list_content_type = [
			('Data curation',
			 'https://credit.niso.org/contributor-roles/data-curation/'),
			('Conceptualization',
			 'https://credit.niso.org/contributor-roles/conceptualization/'),
			('Formal analysis',
			 'https://credit.niso.org/contributor-roles/formal-analysis/'),
		]

		expected_output = {
			'errors': [], 
			'warnings': [
					"The author 'FRANCISCO VENEGAS-MARTÍNEZ' has no content-type assign to <role>Data curation</role>", 
					"The author 'FRANCISCO VENEGAS-MARTÍNEZ' has no content-type assign to <role>Concepalization</role>",
					"The author 'Vanessa M. Higa' has no content-type assign to <role>Formal analysis</role>"
				],
			'invalid_role': [], 
			'invalid_content_type': []
		}
		
		data = etree.fromstring(xml)
		messages = ArticleAuthorsValidation(
			xmltree=data).validate_authors_role(content_type_url=list_content_type)


		self.assertEqual(messages, expected_output)

	def test_wrong_role_and_content_type(self):
		xml = ("""
		<article>
			<front>
				<article-meta>
					<contrib-group>
						<contrib contrib-type="author">
							<name>
								<surname>VENEGAS-MARTÍNEZ</surname>
								<given-names>FRANCISCO</given-names>
								<prefix>Prof</prefix>
								<suffix>Nieto</suffix>
							</name>
							<xref ref-type="aff" rid="aff1"/>
							<role content-type="https://credit.niso.org/contributor-roles/data-curan/">D curation</role>
							<role content-type="https://credit.niso.org/contributor-roles/conceptualizan/">Conceptualization</role>
							</contrib>
							<contrib contrib-type="author">
							<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
							<name>
								<surname>Higa</surname>
								<given-names>Vanessa M.</given-names>
							</name>
							<xref ref-type="aff" rid="aff1">a</xref>
							<role content-type="https://credit.niso.org/contributor-roles/formal-analysis/">Formal analysis</role>
						</contrib>
					</contrib-group>
				</article-meta>
			</front>
		</article>
		""")

		list_content_type = [
			('Data curation',
			 'https://credit.niso.org/contributor-roles/data-curation/'),
			('Conceptualization',
			 'https://credit.niso.org/contributor-roles/conceptualization/'),
			('Formal analysis',
			 'https://credit.niso.org/contributor-roles/formal-analysis/'),
		]

		expected_output = {
			'errors': [], 
			'warnings': [],
			'invalid_role': [
					"Author: FRANCISCO VENEGAS-MARTÍNEZ - Received: D curation, Expected: Data curation"
				], 
			'invalid_content_type': [
					"Author: FRANCISCO VENEGAS-MARTÍNEZ - Received: https://credit.niso.org/contributor-roles/data-curan/, Expected: https://credit.niso.org/contributor-roles/data-curation/",
					"Author: FRANCISCO VENEGAS-MARTÍNEZ - Received: https://credit.niso.org/contributor-roles/conceptualizan/, Expected: https://credit.niso.org/contributor-roles/conceptualization/"
			]
		}

		data = etree.fromstring(xml)
		messages = ArticleAuthorsValidation(
			xmltree=data).validate_authors_role(content_type_url=list_content_type)
		

		self.assertEqual(messages, expected_output)