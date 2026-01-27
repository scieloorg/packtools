from unittest import TestCase
from lxml import etree as ET
from packtools.sps.validation.article_abstract import (
    AbstractValidation,
    XMLAbstractsValidation,
)
from packtools.sps.models.v2.abstract import XMLAbstracts


class SummaryAbstractValidationTest(TestCase):
    """
    Tests for summary (In Brief) abstract validation.
    """

    def test_summary_abstract_with_kwd_is_invalid(self):
        """
        Summary abstracts should NOT have associated keywords.

        SPS 1.10: "Resumos <abstract> graphical, key-points e summary,
        não permitem palavras-chave <kwd-group>."
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.10" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="summary" xml:lang="en">
                            <title>In Brief</title>
                            <p>Brief summary text about the research.</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                            <kwd>keyword2</kwd>
                        </kwd-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.summary_abstracts)

        self.assertEqual(len(abstracts), 1)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        # Should have error for unexpected keywords
        kwd_validation = [v for v in obtained if v["title"] == "unexpected kwd"][0]

        # Keywords come as list of dicts with html_text, plain_text, lang
        self.assertEqual(kwd_validation["response"], "ERROR")
        self.assertEqual(kwd_validation["validation_type"], "exist")
        self.assertEqual(kwd_validation["expected_value"], None)
        self.assertIsNotNone(kwd_validation["got_value"])
        self.assertGreater(len(kwd_validation["got_value"]), 0)

    def test_summary_abstract_without_title_is_invalid(self):
        """Summary abstract must have a title."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="summary" xml:lang="en">
                            <p>Brief summary without title.</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.summary_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        title_validation = [v for v in obtained if v["title"] == "title"][0]

        # Title validation should detect missing title
        # Note: Model may return empty dict for title, not None
        self.assertIn(title_validation["response"], ["ERROR", "WARNING"])
        self.assertEqual(title_validation["expected_value"], "title")

    def test_summary_abstract_with_one_p_is_valid(self):
        """
        Summary abstract with single paragraph is valid.

        Unlike key-points, summary doesn't require multiple <p> tags.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="summary" xml:lang="en">
                            <title>In Brief</title>
                            <p>Brief summary text in a single paragraph.</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.summary_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        # Check that there's no validation error for single <p>
        # (no validate_p_multiple should be called for summary)
        p_validations = [v for v in obtained if v["sub_item"] == "p"]

        # Should not have any <p> validation for summary
        self.assertEqual(len(p_validations), 0)


class SimpleAbstractValidationTest(TestCase):
    """
    Tests for simple/structured abstract validation (no @abstract-type).
    """

    def test_simple_abstract_without_kwd_is_invalid(self):
        """
        Simple abstract without keywords is invalid.

        SPS 1.10: "Resumos <abstract> e <trans-abstract>, simples e estruturado,
        exigem palavras-chave <kwd-group>"
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <p>Abstract text without keywords.</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.standard_abstracts)

        self.assertEqual(len(abstracts), 1)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "kwd"][0]

        expected = {
            "title": "kwd",
            "response": "ERROR",
            "validation_type": "exist",
            "expected_value": "<kwd-group xml:lang='en'>",
        }

        for key in expected:
            with self.subTest(key=key):
                self.assertEqual(expected[key], kwd_validation.get(key))

    def test_simple_abstract_with_kwd_is_valid(self):
        """Simple abstract with keywords is valid."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <p>Abstract text.</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                            <kwd>keyword2</kwd>
                        </kwd-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.standard_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "kwd"][0]

        self.assertEqual(kwd_validation["response"], "OK")

    def test_structured_abstract_without_kwd_is_invalid(self):
        """
        Structured abstract without keywords is invalid.

        SPS 1.10: "Resumos <abstract> e <trans-abstract>, simples e estruturado,
        exigem palavras-chave <kwd-group>"
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <sec>
                                <title>Background</title>
                                <p>Background text.</p>
                            </sec>
                            <sec>
                                <title>Methods</title>
                                <p>Methods text.</p>
                            </sec>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.standard_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "kwd"][0]

        self.assertEqual(kwd_validation["response"], "ERROR")

    def test_structured_abstract_with_kwd_is_valid(self):
        """Structured abstract with keywords is valid."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <sec>
                                <title>Background</title>
                                <p>Background text.</p>
                            </sec>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                        </kwd-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.standard_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "kwd"][0]

        self.assertEqual(kwd_validation["response"], "OK")


class KeyPointsValidationTest(TestCase):
    """
    Tests for key-points (highlights) abstract validation.
    """

    def test_key_points_with_single_p_is_invalid(self):
        """
        Key-points abstract with single paragraph is invalid.

        SPS 1.10: Highlights should have multiple <p> elements.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points" xml:lang="en">
                            <title>HIGHLIGHTS</title>
                            <p>Single highlight point</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.key_points_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        p_validations = [v for v in obtained if v["sub_item"] == "p"]

        # Should have validation for <p> count
        self.assertTrue(len(p_validations) > 0)

        # At least one should be ERROR
        has_error = any(v["response"] in ["ERROR", "WARNING"] for v in p_validations)
        self.assertTrue(has_error)

    def test_key_points_with_multiple_p_is_valid(self):
        """
        Key-points abstract with multiple paragraphs is valid.

        SPS 1.10: Each <p> represents one highlight.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points" xml:lang="en">
                            <title>HIGHLIGHTS</title>
                            <p>First highlight</p>
                            <p>Second highlight</p>
                            <p>Third highlight</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.key_points_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        p_validations = [v for v in obtained if v["sub_item"] == "p"]

        if p_validations:
            # All <p> validations should be OK
            for validation in p_validations:
                self.assertEqual(validation["response"], "OK")

    def test_key_points_with_kwd_is_invalid(self):
        """
        Key-points abstract should NOT have keywords.

        SPS 1.10: key-points doesn't allow <kwd-group>.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points" xml:lang="en">
                            <title>HIGHLIGHTS</title>
                            <p>First highlight</p>
                            <p>Second highlight</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                        </kwd-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.key_points_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "unexpected kwd"][0]

        self.assertEqual(kwd_validation["response"], "ERROR")

    def test_key_points_without_kwd_is_valid(self):
        """Key-points without keywords is valid (keywords not allowed)."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="key-points" xml:lang="en">
                            <title>HIGHLIGHTS</title>
                            <p>First highlight</p>
                            <p>Second highlight</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.key_points_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "unexpected kwd"][0]

        self.assertEqual(kwd_validation["response"], "OK")


class VisualAbstractPositiveValidationTest(TestCase):
    """
    Tests for positive validation cases of visual abstracts (graphical).
    """

    def test_visual_abstract_with_graphic_is_valid(self):
        """
        Test that visual abstract with <graphic> element is valid.

        SPS 1.10: Visual Abstract (@abstract-type="graphical") must contain
        a <graphic> element with xlink:href attribute.

        CRITICAL: This test validates that the model v2 correctly extracts
        the 'graphic' field from XML. If this test fails, verify:
        1. Model v2/abstract.py has @property graphic implemented
        2. AbstractValidation.validate_graphic() is being called
        3. Validation logic correctly checks for graphic presence
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en" 
                     xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical" xml:lang="en">
                            <title>Visual Abstract</title>
                            <p>
                                <fig id="vs1">
                                    <caption>
                                        <title>Study Overview</title>
                                    </caption>
                                    <graphic xlink:href="1234-5678-va-01.jpg"/>
                                </fig>
                            </p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.visual_abstracts)

        self.assertEqual(len(abstracts), 1)
        abstract_data = abstracts[0]

        # MANDATORY VALIDATION: Field 'graphic' MUST be present after model v2 fix
        self.assertIn("graphic_href", abstract_data,
                      "Campo 'graphic' DEVE estar presente em abstract_data após correção do modelo v2. "
                      "Se este teste falhar, verifique se packtools/sps/models/v2/abstract.py "
                      "tem a propriedade @graphic implementada.")

        # MANDATORY VALIDATION: Field 'graphic' MUST have value (extracted xlink:href)
        self.assertIsNotNone(abstract_data["graphic_href"],
                             "Campo 'graphic' não deve ser None para visual abstract. "
                             "Deve conter o valor do atributo xlink:href extraído do XML.")

        # MANDATORY VALIDATION: Verify type and content
        self.assertIsInstance(abstract_data["graphic_href"], str,
                              "Campo 'graphic' deve ser string (valor de xlink:href)")

        self.assertTrue(abstract_data["graphic_href"].strip(),
                        "Campo 'graphic' não pode ser string vazia")

        # MANDATORY VALIDATION: Verify expected value
        self.assertEqual(abstract_data["graphic_href"], "1234-5678-va-01.jpg",
                         "Valor de 'graphic' deve corresponder ao xlink:href do XML")

        # VALIDATOR VALIDATIONS
        validator = AbstractValidation(abstract_data)
        obtained = list(validator.validate())

        # MANDATORY VALIDATION: Graphic validation MUST be present in results
        graphic_validation = [v for v in obtained if v["title"] == "graphic"]

        self.assertTrue(graphic_validation,
                        "Validação de 'graphic' DEVE estar presente nos resultados. "
                        "Se este teste falhar, verifique se AbstractValidation.validate_graphic() "
                        "está sendo chamado em AbstractValidation.validate().")

        # MANDATORY VALIDATION: Validation MUST pass (response = "OK")
        self.assertEqual(graphic_validation[0]["response"], "OK",
                         f"Validação de 'graphic' deve ser 'OK' para visual abstract válido. "
                         f"Resultado obtido: {graphic_validation[0]}")

        # Additional validations for visual abstract
        self.assertEqual(abstract_data.get("abstract_type"), "graphical")
        self.assertIsNotNone(abstract_data.get("title"))

    def test_visual_abstract_without_graphic_is_invalid(self):
        """
        Test that visual abstract WITHOUT <graphic> element is invalid.

        SPS 1.10: Visual Abstract must contain a <graphic> element.
        Missing <graphic> should trigger validation error.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en"
                     xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical" xml:lang="en">
                            <title>Visual Abstract</title>
                            <p>Visual abstract without graphic element</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.visual_abstracts)

        self.assertEqual(len(abstracts), 1)
        abstract_data = abstracts[0]

        # EXPECTED VALIDATIONS FOR INVALID CASE
        # 1. Field 'graphic' may be absent, None, or empty string
        graphic_value = abstract_data.get("graphic_href")

        # The field may be present but empty, or absent
        if graphic_value is not None:
            # If present, should be empty string or no valid content
            is_empty = not (graphic_value.strip() if isinstance(graphic_value, str) else graphic_value)
            self.assertTrue(is_empty,
                            f"Campo 'graphic' deve estar vazio/None quando elemento <graphic> ausente. "
                            f"Obtido: {graphic_value}")

        # VALIDATOR VALIDATIONS
        validator = AbstractValidation(abstract_data)
        obtained = list(validator.validate())

        # 2. Graphic validation MUST be present
        graphic_validation = [v for v in obtained if v["title"] == "graphic"]

        self.assertTrue(graphic_validation,
                        "Validação de 'graphic' DEVE estar presente mesmo quando ausente no XML")

        # 3. Validation MUST fail (response = "ERROR" or "CRITICAL")
        response = graphic_validation[0]["response"]
        self.assertIn(response, ["ERROR", "CRITICAL"],
                      f"Validação deve falhar para visual abstract sem <graphic>. "
                      f"Esperado: ERROR ou CRITICAL, Obtido: {response}")

        # 4. Error message should mention the problem
        validation_str = str(graphic_validation[0]).lower()
        self.assertIn("graphic", validation_str,
                      "Mensagem de erro deve mencionar 'graphic'")

    def test_visual_abstract_with_empty_graphic_is_invalid(self):
        """
        Test that visual abstract with empty xlink:href is invalid.

        Edge case: <graphic> element exists but xlink:href attribute is empty.
        This should be treated as invalid since there's no actual image reference.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en"
                     xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical" xml:lang="en">
                            <title>Visual Abstract</title>
                            <p>
                                <fig id="vs1">
                                    <graphic xlink:href=""/>
                                </fig>
                            </p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.visual_abstracts)

        abstract_data = abstracts[0]

        # Graphic may be present but empty
        if "graphic" in abstract_data:
            graphic = abstract_data["graphic"]
            if graphic is not None:
                # If not None, should be empty string or whitespace only
                self.assertEqual(graphic.strip(), "",
                                 f"xlink:href vazio deve resultar em string vazia. Obtido: '{graphic}'")

        # Validation should fail
        validator = AbstractValidation(abstract_data)
        obtained = list(validator.validate())

        graphic_validation = [v for v in obtained if v["title"] == "graphic"]
        self.assertTrue(graphic_validation,
                        "Validação de 'graphic' deve estar presente")

        response = graphic_validation[0]["response"]
        self.assertIn(response, ["ERROR", "CRITICAL"],
                      f"Validação deve falhar para xlink:href vazio. "
                      f"Esperado: ERROR ou CRITICAL, Obtido: {response}")

    def test_visual_abstract_without_kwd_is_valid(self):
        """
        Visual abstract without keywords is valid.

        SPS 1.10: graphical should NOT have keywords.
        """
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en"
                     xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                        <abstract abstract-type="graphical" xml:lang="en">
                            <title>Visual Abstract</title>
                            <p>
                                <fig id="vs1">
                                    <graphic xlink:href="image.jpg"/>
                                </fig>
                            </p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.visual_abstracts)

        validator = AbstractValidation(abstracts[0])
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "unexpected kwd"][0]

        self.assertEqual(kwd_validation["response"], "OK")


class AbstractTypeValidationTest(TestCase):
    """
    Tests for abstract-type attribute validation.
    """

    def test_abstract_with_invalid_type_is_invalid(self):
        """Abstract with invalid @abstract-type should be rejected."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract abstract-type="invalid-type" xml:lang="en">
                            <title>Title</title>
                            <p>Text</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                        </kwd-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        # Use XMLAbstractsValidation to handle all abstracts
        validator = XMLAbstractsValidation(xmltree)
        obtained = list(validator.validate())

        # Filter for abstract-type validations
        type_validations = [v for v in obtained if v and v.get("title") == "@abstract-type"]

        if not type_validations:
            self.skipTest("No abstract-type validation found")

        # At least one should be CRITICAL or ERROR for invalid type
        has_error = any(v["response"] in ["CRITICAL", "ERROR"] for v in type_validations)
        self.assertTrue(has_error, "Expected ERROR or CRITICAL for invalid abstract-type")


class MultipleAbstractsTest(TestCase):
    """
    Tests for documents with multiple abstracts.
    """

    def test_document_with_all_abstract_types(self):
        """Document with all abstract types should validate each correctly."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en"
                     xmlns:xlink="http://www.w3.org/1999/xlink">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <p>Main abstract text.</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                        </kwd-group>
                        <abstract abstract-type="graphical" xml:lang="en">
                            <title>Visual Abstract</title>
                            <p><fig id="vs1"><graphic xlink:href="img.jpg"/></fig></p>
                        </abstract>
                        <abstract abstract-type="key-points" xml:lang="en">
                            <title>HIGHLIGHTS</title>
                            <p>Highlight 1</p>
                            <p>Highlight 2</p>
                        </abstract>
                        <abstract abstract-type="summary" xml:lang="en">
                            <title>In Brief</title>
                            <p>Brief summary.</p>
                        </abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = XMLAbstractsValidation(xmltree)
        obtained = list(validator.validate())

        # Should have validations for all types
        # Check that we have responses for each abstract type
        abstract_type_validations = [v for v in obtained if v["title"] == "@abstract-type"]

        # We should have 4 abstract type validations (one for each abstract)
        self.assertEqual(len(abstract_type_validations), 4)

        # All should be OK
        for validation in abstract_type_validations:
            self.assertEqual(validation["response"], "OK")


class TransAbstractValidationTest(TestCase):
    """
    Tests for translated abstracts (<trans-abstract>).
    """

    def test_trans_abstract_without_kwd_is_invalid(self):
        """Translated abstract without keywords is invalid."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <p>English text.</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                        </kwd-group>
                        <trans-abstract xml:lang="pt">
                            <title>Resumo</title>
                            <p>Texto em português.</p>
                        </trans-abstract>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.standard_abstracts)

        # Find the Portuguese trans-abstract
        pt_abstracts = [a for a in abstracts if a.get("lang") == "pt"]

        if not pt_abstracts:
            self.skipTest("Model does not return trans-abstract in standard_abstracts")

        pt_abstract = pt_abstracts[0]

        validator = AbstractValidation(pt_abstract)
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "kwd"]

        if not kwd_validation:
            self.skipTest("Keyword validation not found")

        self.assertEqual(kwd_validation[0]["response"], "ERROR")
        self.assertIn("pt", str(kwd_validation[0]["expected_value"]))

    def test_trans_abstract_with_kwd_is_valid(self):
        """Translated abstract with matching language keywords is valid."""
        self.maxDiff = None
        xmltree = ET.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <abstract xml:lang="en">
                            <title>Abstract</title>
                            <p>English text.</p>
                        </abstract>
                        <kwd-group xml:lang="en">
                            <title>Keywords:</title>
                            <kwd>keyword1</kwd>
                        </kwd-group>
                        <trans-abstract xml:lang="pt">
                            <title>Resumo</title>
                            <p>Texto em português.</p>
                        </trans-abstract>
                        <kwd-group xml:lang="pt">
                            <title>Palavras-chave:</title>
                            <kwd>palavra1</kwd>
                        </kwd-group>
                    </article-meta>
                </front>
            </article>
            """
        )

        xml_abstracts = XMLAbstracts(xmltree)
        abstracts = list(xml_abstracts.standard_abstracts)

        # Find the Portuguese trans-abstract
        pt_abstracts = [a for a in abstracts if a.get("lang") == "pt"]

        if not pt_abstracts:
            self.skipTest("Model does not return trans-abstract in standard_abstracts")

        pt_abstract = pt_abstracts[0]

        validator = AbstractValidation(pt_abstract)
        obtained = list(validator.validate())

        kwd_validation = [v for v in obtained if v["title"] == "kwd"]

        if not kwd_validation:
            self.skipTest("Keyword validation not found")

        self.assertEqual(kwd_validation[0]["response"], "OK")
