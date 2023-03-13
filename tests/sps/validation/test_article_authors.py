from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils

from packtools.sps.validation.article_authors import ArticleAuthorsValidation

credit_terms_and_urls = [
    {'term': 'Conceptualization',
        'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
    {'term': 'Data curation',
        'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
    {'term': 'Formal analysis',
        'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
    {'term': 'Funding acquisition',
        'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
    {'term': 'Investigation',
        'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
    {'term': 'Methodology', 'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
    {'term': 'Project administration',
        'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
    {'term': 'Resources', 'uri': 'https://credit.niso.org/contributor-roles/resources/'},
    {'term': 'Software', 'uri': 'https://credit.niso.org/contributor-roles/software/'},
    {'term': 'Supervision', 'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
    {'term': 'Validation', 'uri': 'https://credit.niso.org/contributor-roles/validation/'},
    {'term': 'Visualization',
        'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
    {'term': 'Writing – original draft',
        'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
    {'term': 'Writing – review & editing',
        'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
]


class ArticleAuthorsValidationTest(TestCase):

    def test_without_role(self):
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

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_terms_and_urls=credit_terms_and_urls)

        expected_output = [
            {
                'result': 'error',
                'error_type': 'No role found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ does not have a role. Please add a role according to the credit-taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'No role found',
                'message': "The author Vanessa M. Higa does not have a role. Please add a role according to the credit-taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            }
        ]

        self.assertEqual(messages, expected_output)

    def test_role_and_content_type_empty(self):
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

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=data).validate_authors_role(
            credit_terms_and_urls=credit_terms_and_urls)

        expected_output = [
            {
                'result': 'error',
                'error_type': 'Text and content-type not found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role with no text and content-type attributes. Please add valid text and content-type attributes according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'Text and content-type not found',
                'message': "The author Vanessa M. Higa has a role with no text and content-type attributes. Please add valid text and content-type attributes according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
        ]

        self.assertEqual(messages, expected_output)

    def test_role_without_content_type(self):
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

        expected_output = [
            {
                'result': 'error',
                'error_type': 'No content-type found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role Data curation with text but no content-type attribute. Please add a valid URI to the content-type attribute according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'No content-type found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role Concepalization with text but no content-type attribute. Please add a valid URI to the content-type attribute according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'No content-type found',
                'message': "The author Vanessa M. Higa has a role Formal analysis with text but no content-type attribute. Please add a valid URI to the content-type attribute according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(
            xmltree=data).validate_authors_role(credit_terms_and_urls=credit_terms_and_urls)

        self.assertEqual(messages, expected_output)

    def test_role_no_text_with_content_type(self):
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
								<role content-type="content-type="https://credit.niso.org/contributor-roles/data-curation/"></role>
								<role content-type="https://credit.niso.org/contributor-roles/conceptualization/"></role>
								</contrib>
								<contrib contrib-type="author">
								<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
								<name>
									<surname>Higa</surname>
									<given-names>Vanessa M.</given-names>
								</name>
								<xref ref-type="aff" rid="aff1">a</xref>
								<role content-type="https://credit.niso.org/contributor-roles/formal-analysis/"></role>
							</contrib>
						</contrib-group>
					</article-meta>
				</front>
			</article>
			""")

        expected_output = [
            {
                'result': 'error',
                'error_type': 'No text found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role with no text. Please add valid text to the role according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'No text found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role with no text. Please add valid text to the role according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'No text found',
                'message': "The author Vanessa M. Higa has a role with no text. Please add valid text to the role according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
        ]

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
							<role content-type="https://credit.niso.org/contributor-roles/data-curan/">Data curation</role>
							<role content-type="https://credit.niso.org/contributor-roles/conceualizan/">Conceplization</role>
							</contrib>
							<contrib contrib-type="author">
							<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
							<name>
								<surname>Higa</surname>
								<given-names>Vanessa M.</given-names>
							</name>
							<xref ref-type="aff" rid="aff1">a</xref>
							<role content-type="https://credit.niso.org/contributor-roles/foal-analysis/">Formal analysis</role>
						</contrib>
					</contrib-group>
				</article-meta>
			</front>
		</article>
		""")

        expected_output = [
            {
                'result': 'error',
                'error_type': 'Role and content-type not found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role and content-type that are not found in the credit taxonomy. Please check the role and content-type attributes according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'Role and content-type not found',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a role and content-type that are not found in the credit taxonomy. Please check the role and content-type attributes according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
            {
                'result': 'error',
                'error_type': 'Role and content-type not found',
                'message': "The author Vanessa M. Higa has a role and content-type that are not found in the credit taxonomy. Please check the role and content-type attributes according to the credit taxonomy below.",
                'credit_terms_and_urls': [
                    {'term': 'Conceptualization',
                     'uri': 'https://credit.niso.org/contributor-roles/conceptualization/'},
                    {'term': 'Data curation',
                     'uri': 'https://credit.niso.org/contributor-roles/data-curation/'},
                    {'term': 'Formal analysis',
                     'uri': 'https://credit.niso.org/contributor-roles/formal-analysis/'},
                    {'term': 'Funding acquisition',
                     'uri': 'https://credit.niso.org/contributor-roles/funding-acquisition/'},
                    {'term': 'Investigation',
                     'uri': 'https://credit.niso.org/contributor-roles/investigation/'},
                    {'term': 'Methodology',
                     'uri': 'https://credit.niso.org/contributor-roles/methodology/'},
                    {'term': 'Project administration',
                     'uri': 'https://credit.niso.org/contributor-roles/project-administration/'},
                    {'term': 'Resources',
                     'uri': 'https://credit.niso.org/contributor-roles/resources/'},
                    {'term': 'Software',
                     'uri': 'https://credit.niso.org/contributor-roles/software/'},
                    {'term': 'Supervision',
                     'uri': 'https://credit.niso.org/contributor-roles/supervision/'},
                    {'term': 'Validation',
                     'uri': 'https://credit.niso.org/contributor-roles/validation/'},
                    {'term': 'Visualization',
                     'uri': 'https://credit.niso.org/contributor-roles/visualization/'},
                    {'term': 'Writing – original draft',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-original-draft/'},
                    {'term': 'Writing – review & editing',
                     'uri': 'https://credit.niso.org/contributor-roles/writing-review-editing/'}
                ]
            },
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(
            xmltree=data).validate_authors_role(credit_terms_and_urls=credit_terms_and_urls)

        self.assertEqual(messages, expected_output)

    def test_success_role(self):
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
							<role content-type="https://credit.niso.org/contributor-roles/data-curation/">data curation</role>
							<role content-type="https://credit.niso.org/contributor-roles/conceptualization/">Conceptualization</role>
							</contrib>
							<contrib contrib-type="author">
							<contrib-id contrib-id-type="orcid">0000-0001-5518-4853</contrib-id>
							<name>
								<surname>Higa</surname>
								<given-names>Vanessa M.</given-names>
							</name>
							<xref ref-type="aff" rid="aff1">a</xref>
							<role content-type="https://credit.niso.org/contributor-roles/visualization/">Visualization</role>
						</contrib>
					</contrib-group>
				</article-meta>
			</front>
		</article>
		""")

        expected_output = [
            {
                'result': 'success',
                # Testa case-insensitive
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a valid role and content-type attribute for the role data curation."
            },
            {
                'result': 'success',
                'message': "The author FRANCISCO VENEGAS-MARTÍNEZ has a valid role and content-type attribute for the role Conceptualization."
            },
            {
                'result': 'success',
                'message': "The author Vanessa M. Higa has a valid role and content-type attribute for the role Visualization."
            }
        ]

        data = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(
            xmltree=data).validate_authors_role(credit_terms_and_urls=credit_terms_and_urls)

        self.assertEqual(messages, expected_output)


class ArticleAuthorsValidationOrcidTest(TestCase):

    def test_validation_format_orcid(self):
        xml = ("""
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-01-58-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                  <contrib-id contrib-id-type="orcid">00-0001-5518-4853</contrib-id>
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
        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid()

        expected_output = [
            {
                'result': 'error',
                'error_type': 'Format invalid',
                'message': 'The author FRANCISCO VENEGAS-MARTÍNEZ has an orcid in an invalid format. Please ensure that the ORCID is entered correctly, including the proper format (e.g., 0000-0002-1825-0097).',
                'author': {
                    'surname': 'VENEGAS-MARTÍNEZ', 
                    'prefix': 'Prof', 
                    'suffix': 'Nieto', 
                    'given_names': 'FRANCISCO', 
                    'orcid': '0990-01-58-4853'
                },
            },
            {
                'result': 'error',
                'error_type': 'Format invalid',
                'message': 'The author Vanessa M. Higa has an orcid in an invalid format. Please ensure that the ORCID is entered correctly, including the proper format (e.g., 0000-0002-1825-0097).',
                'author': {
                    'surname': 'Higa', 
                    'given_names': 'Vanessa M.', 
                    'orcid': '00-0001-5518-4853'
                }
            }
        ]

        self.assertEqual(messages, expected_output)

    def test_without_orcid(self):
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
                </contrib>
                <contrib contrib-type="author">
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
        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid()

        expected_output = [
            {
                'result': 'error',
                'error_type': 'Orcid not found',
                'message': 'The author FRANCISCO VENEGAS-MARTÍNEZ does not have an orcid. Please add a valid orcid.',
                'author': {
                    'surname': 'VENEGAS-MARTÍNEZ', 
                    'prefix': 'Prof', 
                    'suffix': 'Nieto', 
                    'given_names': 'FRANCISCO', 
                },            
            },
            {
                'result': 'error',
                'error_type': 'Orcid not found',
                'message': 'The author Vanessa M. Higa does not have an orcid. Please add a valid orcid.',
                'author': {
                    'surname': 'Higa', 
                    'given_names': 'Vanessa M.', 
                },               
            }
        ]

        self.assertEqual(messages, expected_output)

    def test_success_orcid(self):
        xml = ("""
        <article>
        <front>
            <article-meta>
              <contrib-group>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0990-0001-0058-4853</contrib-id>
                  <name>
                    <surname>VENEGAS-MARTÍNEZ</surname>
                    <given-names>FRANCISCO</given-names>
                    <prefix>Prof</prefix>
                    <suffix>Nieto</suffix>
                  </name>
                  <xref ref-type="aff" rid="aff1"/>
                </contrib>
                <contrib contrib-type="author">
                    <contrib-id contrib-id-type="orcid">0000-3333-1238-6873</contrib-id>
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

        xmltree = etree.fromstring(xml)
        messages = ArticleAuthorsValidation(xmltree=xmltree).validate_authors_orcid()

        expected_output = [
            {
                'result': 'success',
                'message': 'The author FRANCISCO VENEGAS-MARTÍNEZ has a valid orcid.',
                'author': {
                    'surname': 'VENEGAS-MARTÍNEZ', 
                    'prefix': 'Prof', 
                    'suffix': 'Nieto', 
                    'given_names': 'FRANCISCO', 
                    'orcid': '0990-0001-0058-4853'
                },
            },
            {
                'result': 'success',
                'message': 'The author Vanessa M. Higa has a valid orcid.',
                'author': {
                    'surname': 'Higa', 
                    'given_names': 'Vanessa M.', 
                    'orcid': '0000-3333-1238-6873'
                },            
            }
        ]

        self.assertEqual(messages, expected_output)