import unittest
from contextvars import Context

from lxml import etree

from packtools.sps import i18n
from packtools.sps.validation.aff import AffiliationValidation
from packtools.sps.validation.ext_link import ExtLinkValidation
from packtools.sps.validation.fig import FigValidation
from packtools.sps.validation.references import ReferenceValidation
from packtools.sps.validation.sec import XMLSecValidation
from packtools.sps.validation.supplementary_material import (
    XmlSupplementaryMaterialValidation,
)


def render_message(result):
    return result["msg_text"].format(**result["msg_params"])


class I18nMessageRenderingTest(unittest.TestCase):
    def test_editorial_translations_from_multilingual_csv(self):
        cases = [
            (
                "Unable to check if issue is registered",
                {},
                "Não é possível verificar se o fascículo está cadastrado",
                "No se puede comprobar si el fascículo está registrado",
            ),
            (
                "The DOI (<article-id pub-id-type=\"doi\">{xml_doi}</article-id>) "
                "is not registered for {expected}. It is registered for {registered}",
                {
                    "xml_doi": "10.1234/example",
                    "expected": "article A",
                    "registered": "article B",
                },
                "O DOI (<article-id pub-id-type=\"doi\">10.1234/example"
                "</article-id>) não está registrado para article A. Ele está "
                "registrado para article B",
                "El DOI (<article-id pub-id-type=\"doi\">10.1234/example"
                "</article-id>) no está registrado para article A. Está "
                "registrado para article B",
            ),
            (
                "Unable to check whether {subject} (<subject-group "
                "subj-group-type=\"heading\"><subject>{subject}</subject>"
                "</subject-group>) is a valid table of contents section "
                "because no sections were provided for the journal {journal}",
                {"subject": "Article", "journal": "Biota Neotropica"},
                "Não foi possível verificar se Article (<subject-group "
                "subj-group-type=\"heading\"><subject>Article</subject>"
                "</subject-group>) é uma seção de sumário válida porque não "
                "foram informadas seções para o periódico Biota Neotropica",
                "No se puede comprobar si Article (<subject-group "
                "subj-group-type=\"heading\"><subject>Article</subject>"
                "</subject-group>) es una sección válida de la tabla de "
                "contenido porque no se informaron secciones para la revista "
                "Biota Neotropica",
            ),
            (
                "{info}: {key} was not marked. Check whether {key} appears "
                "in {original}",
                {
                    "info": "(article - aff2)",
                    "key": "orgdiv1",
                    "original": "Universidade, Brasil.",
                },
                "(article - aff2): orgdiv1 não foi marcado. Verifique se "
                "orgdiv1 aparece em Universidade, Brasil.",
                "(article - aff2): orgdiv1 no fue marcado. Compruebe si "
                "orgdiv1 aparece en Universidade, Brasil.",
            ),
            (
                "Mark the reference year ({year}) with <year>; it must be "
                "earlier than or equal to {end_year}",
                {"year": "2013a", "end_year": "2026"},
                "Marque o ano da referência (2013a) com <year>; ele deve ser "
                "anterior ou igual a 2026",
                "Marque el año de la referencia (2013a) con <year>; debe ser "
                "anterior o igual a 2026",
            ),
            (
                "Got {obtained}, expected one of {expected}",
                {
                    "obtained": "translation",
                    "expected": "['research-article', 'review-article']",
                },
                "Obtido translation, esperado um dos seguintes valores: "
                "['research-article', 'review-article']",
                "Se obtuvo translation, se esperaba uno de los siguientes "
                "valores: ['research-article', 'review-article']",
            ),
            (
                "Missing <alt-text>. Provide a concise textual description "
                "of the visual element content.",
                {},
                "Falta o elemento <alt-text>. Forneça uma descrição textual "
                "concisa do conteúdo do elemento visual.",
                "Falta <alt-text>. Proporcione una descripción textual "
                "concisa del contenido del elemento visual.",
            ),
            (
                'Complete  specific-use="" in {xml} with valid value: '
                "{valid_values}",
                {
                    "xml": "<article>",
                    "valid_values": ["data-available"],
                },
                'Preencha specific-use="" em <article> com um valor válido: '
                "['data-available']",
                'Complete specific-use="" en <article> con un valor válido: '
                "['data-available']",
            ),
        ]

        for template, params, portuguese, spanish in cases:
            for locale, expected in (
                ("pt_BR", portuguese),
                ("es", spanish),
            ):
                with self.subTest(locale=locale, template=template):
                    def translate():
                        i18n.set_locale(locale)
                        return i18n._(template).format(**params)

                    self.assertEqual(expected, Context().run(translate))

    def test_default_reference_advice_is_localized(self):
        reference_data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "source": None,
            "parent": "article",
        }
        params = {
            "publication_type_requires": {"journal": ["source"]},
            "source_error_level": "ERROR",
        }
        expected = {
            "pt_BR": "B1 (journal): Marque reference source com <source>",
            "es": "B1 (journal): Marque reference source con <source>",
        }

        for locale, translated_advice in expected.items():
            with self.subTest(locale=locale):
                def validate():
                    i18n.set_locale(locale)
                    return next(
                        ReferenceValidation(
                            reference_data,
                            params,
                        ).validate_source()
                    )

                result = Context().run(validate)

                self.assertEqual(
                    "B1 (journal) : Mark reference source with <source>",
                    result["advice"],
                )
                self.assertEqual(
                    translated_advice,
                    result["adv_text"].format(**result["adv_params"]),
                )

    def test_missing_data_availability_message_is_localized(self):
        xmltree = etree.fromstring(
            """
            <article article-type="research-article" xml:lang="en">
              <body>
                <sec sec-type="methods">
                  <title>Methods</title>
                  <p>Content.</p>
                </sec>
              </body>
            </article>
            """
        )
        params = {
            "data_availability_required_article_types": [
                "research-article",
            ],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "pt_BR": (
                "A declaração de disponibilidade de dados está ausente; "
                'esperava-se <sec sec-type="data-availability"> em <body> '
                'ou <back>, ou <fn fn-type="data-availability">'
            ),
            "es": (
                "Falta la declaración de disponibilidad de datos; se "
                'esperaba <sec sec-type="data-availability"> en <body> o '
                '<back>, o <fn fn-type="data-availability">'
            ),
        }

        for locale, translated_message in expected.items():
            with self.subTest(locale=locale):
                def validate():
                    i18n.set_locale(locale)
                    return next(
                        XMLSecValidation(
                            xmltree,
                            params,
                        ).validate_data_availability_presence()
                    )

                result = Context().run(validate)

                self.assertEqual("missing", result["got_value"])
                self.assertEqual(
                    "Got missing, expected <sec "
                    'sec-type="data-availability"> in <body> or <back>, '
                    'or <fn fn-type="data-availability">',
                    result["message"],
                )
                self.assertEqual(
                    translated_message,
                    render_message(result),
                )

    def test_fallback_normalizes_nested_display_values_only(self):
        from packtools.sps.validation.utils import build_response

        obtained = {
            "funding-source": [
                "Institute affiliated\\n\\twith the Ministry",
            ],
            "award-id": [],
        }
        result = build_response(
            title="funding",
            parent={"parent": "article"},
            item="funding-group",
            sub_item=None,
            validation_type="exist",
            is_valid=False,
            expected="award-id and funding-source in award-group",
            obtained=obtained,
            advice="Review funding",
            advice_text="Review {funding}",
            advice_params={"funding": obtained},
            data=obtained,
            error_level="ERROR",
        )

        self.assertNotIn("\\n", result["msg_params"]["obtained"])
        self.assertNotIn("\\t", result["msg_params"]["obtained"])
        self.assertEqual(
            "Institute affiliated with the Ministry",
            result["adv_params"]["funding"]["funding-source"][0],
        )
        self.assertEqual(
            "Institute affiliated\\n\\twith the Ministry",
            result["got_value"]["funding-source"][0],
        )

    def test_affiliation_keeps_legacy_values_and_localizes_prose(self):
        raw_orgname = "Universidade Federal Rural da \n\t Amazônia"
        affiliation = {
            "parent": "article",
            "original": raw_orgname,
            "orgname": raw_orgname,
        }
        expected_messages = {
            "pt_BR": (
                "Obtido Universidade Federal Rural da Amazônia, "
                "esperado que orgname esteja marcado"
            ),
            "es": (
                "Se obtuvo Universidade Federal Rural da Amazônia, "
                "se esperaba que orgname estuviera marcado"
            ),
        }

        for locale, expected_message in expected_messages.items():
            with self.subTest(locale=locale):
                def validate():
                    i18n.set_locale(locale)
                    return next(
                        AffiliationValidation(
                            affiliation,
                            {"country_codes_list": ["BR"]},
                        ).validate_aff_components()
                    )

                result = Context().run(validate)

                self.assertEqual("orgname marked", result["expected_value"])
                self.assertEqual(raw_orgname, result["got_value"])
                self.assertEqual(
                    {
                        "obtained": "Universidade Federal Rural da Amazônia",
                        "component": "orgname",
                    },
                    result["msg_params"],
                )
                self.assertEqual(expected_message, render_message(result))

    def test_missing_affiliation_component_does_not_render_none(self):
        affiliation = {
            "parent": "article",
            "original": "Universidade Federal Rural da Amazônia",
            "orgdiv1": None,
        }

        def validate():
            i18n.set_locale("pt_BR")
            return next(
                result
                for result in AffiliationValidation(
                    affiliation,
                    {"country_codes_list": ["BR"]},
                ).validate_aff_components()
                if result["expected_value"] == "orgdiv1 marked"
            )

        result = Context().run(validate)

        self.assertIsNone(result["got_value"])
        self.assertNotIn("None", render_message(result))
        self.assertEqual(
            "Nenhum valor foi encontrado para orgdiv1; "
            "esperado que orgdiv1 esteja marcado",
            render_message(result),
        )

    def test_observed_messages_are_localized_and_keep_technical_tokens(self):
        expectations = {
            "pt_BR": {
                "fig": (
                    "Nenhuma descrição de acessibilidade foi encontrada; "
                    "esperado <alt-text> ou <long-desc>"
                ),
                "url": "O URL ftp://example.org/file deve começar com http:// ou https://",
                "title": (
                    "O atributo @xlink:title é obrigatório quando o texto "
                    "do link é genérico ou um URL"
                ),
                "inline": (
                    "O elemento <inline-supplementary-material> não é permitido"
                ),
            },
            "es": {
                "fig": (
                    "No se encontró ninguna descripción de accesibilidad; "
                    "se esperaba <alt-text> o <long-desc>"
                ),
                "url": (
                    "La URL ftp://example.org/file debe comenzar con "
                    "http:// o https://"
                ),
                "title": (
                    "El atributo @xlink:title es obligatorio cuando el texto "
                    "del enlace es genérico o una URL"
                ),
                "inline": (
                    "El elemento <inline-supplementary-material> no está permitido"
                ),
            },
        }
        ext_link_xml = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
              <body>
                <p>
                  <ext-link ext-link-type="uri"
                            xlink:href="ftp://example.org/file">Leia mais</ext-link>
                </p>
              </body>
            </article>
            """
        )
        inline_xml = etree.fromstring(
            """
            <article>
              <body>
                <inline-supplementary-material>Figure S1</inline-supplementary-material>
              </body>
            </article>
            """
        )

        for locale, expected in expectations.items():
            with self.subTest(locale=locale):
                def validate():
                    i18n.set_locale(locale)
                    ext_link_validator = ExtLinkValidation(ext_link_xml)
                    return {
                        "fig": FigValidation(
                            {
                                "parent": "article",
                                "graphic_alt_text": None,
                                "graphic_long_desc": None,
                            },
                            {"accessibility_error_level": "WARNING"},
                        ).validate_accessibility(),
                        "url": next(
                            ext_link_validator.validate_xlink_href_format()
                        ),
                        "title": next(
                            ext_link_validator.validate_xlink_title_when_generic()
                        ),
                        "inline": XmlSupplementaryMaterialValidation(
                            inline_xml,
                            {"inline_error_level": "CRITICAL"},
                        ).validate_prohibited_inline(),
                    }

                results = Context().run(validate)

                for key, result in results.items():
                    self.assertEqual(expected[key], render_message(result))
                    self.assertNotIn("None", render_message(result))

                self.assertEqual(
                    "<alt-text> or <long-desc>",
                    results["fig"]["expected_value"],
                )
                self.assertEqual(
                    "URL starting with http:// or https://",
                    results["url"]["expected_value"],
                )
                self.assertEqual(
                    "@xlink:title attribute when text is generic or URL",
                    results["title"]["expected_value"],
                )
                self.assertEqual(
                    "No <inline-supplementary-material>",
                    results["inline"]["expected_value"],
                )


if __name__ == "__main__":
    unittest.main()
