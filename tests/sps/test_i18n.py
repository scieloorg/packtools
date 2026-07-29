import ast
import gettext
import re
import unittest
from contextvars import Context
from pathlib import Path
from unittest.mock import patch

from babel.messages.pofile import read_po
from lxml import etree

from packtools.sps import i18n
from packtools.sps.validation.journal_meta import (
    ISSNFormatValidation,
    JournalMetaPresenceValidation,
)
from packtools.sps.validation.product import ProductValidation
from packtools.sps.validation.utils import build_response, format_response


class PrefixTranslations(gettext.NullTranslations):
    def __init__(self, prefix):
        super().__init__()
        self.prefix = prefix

    def gettext(self, message):
        return f"{self.prefix}:{message}"


class I18nTest(unittest.TestCase):
    def test_catalogs_preserve_xml_tags_and_attribute_names(self):
        token_patterns = {
            "tags": re.compile(r"</?([A-Za-z_][\w:.-]*)"),
            "attributes": re.compile(
                r"(?<![\w:-])([A-Za-z_][\w:.-]*)\s*="
            ),
            "at_attributes": re.compile(
                r"@([A-Za-z_](?:[\w:.-]*[\w:-])?)"
            ),
        }
        mismatches = []

        for locale in ("pt_BR", "es"):
            po_path = (
                i18n.LOCALE_DIR
                / locale
                / "LC_MESSAGES"
                / f"{i18n.DOMAIN}.po"
            )
            with po_path.open(encoding="utf-8") as stream:
                catalog = read_po(stream)

            for message in catalog:
                if (
                    not message.id
                    or not message.string
                    or not isinstance(message.id, str)
                    or not isinstance(message.string, str)
                ):
                    continue

                for token_type, pattern in token_patterns.items():
                    source_tokens = sorted(pattern.findall(message.id))
                    translated_tokens = sorted(
                        pattern.findall(message.string)
                    )
                    if source_tokens != translated_tokens:
                        mismatches.append(
                            (
                                locale,
                                token_type,
                                message.id,
                                source_tokens,
                                translated_tokens,
                            )
                        )

        self.assertEqual([], mismatches)

    def test_validation_result_dicts_include_i18n_contract(self):
        validation_dir = (
            Path(__file__).resolve().parents[2]
            / "packtools"
            / "sps"
            / "validation"
        )
        required_fields = {
            "msg_text",
            "msg_params",
            "adv_text",
            "adv_params",
        }
        incomplete = []

        for path in validation_dir.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Dict):
                    continue

                keys = {
                    key.value
                    for key in node.keys
                    if isinstance(key, ast.Constant)
                    and isinstance(key.value, str)
                }
                if "message" not in keys:
                    continue

                missing = required_fields - keys
                if missing:
                    incomplete.append(
                        f"{path.name}:{node.lineno}: "
                        f"{', '.join(sorted(missing))}"
                    )

        self.assertEqual([], incomplete)

    def test_uses_null_translation_before_locale_is_set(self):
        translated = Context().run(
            i18n._,
            "Got {obtained}, expected {expected}",
        )

        self.assertEqual("Got {obtained}, expected {expected}", translated)

    def test_set_locale_loads_expected_domain_and_directory(self):
        translation = PrefixTranslations("pt_BR")

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ) as load_translation:
            context = Context()
            context.run(i18n.set_locale, "pt_BR")

            self.assertEqual(
                "pt_BR:Message",
                context.run(i18n._, "Message"),
            )

        load_translation.assert_called_once_with(
            i18n.DOMAIN,
            localedir=str(i18n.LOCALE_DIR),
            languages=["pt_BR"],
            fallback=True,
        )

    def test_set_locale_defaults_to_english_with_catalog_fallback(self):
        context = Context()

        context.run(i18n.set_locale)

        self.assertEqual("Message", context.run(i18n._, "Message"))

    def test_locales_are_isolated_between_contexts(self):
        translations = {
            "pt_BR": PrefixTranslations("pt_BR"),
            "es": PrefixTranslations("es"),
        }

        def load_translation(domain, localedir, languages, fallback):
            return translations[languages[0]]

        with patch(
            "packtools.sps.i18n.gettext.translation",
            side_effect=load_translation,
        ):
            portuguese_context = Context()
            spanish_context = Context()
            portuguese_context.run(i18n.set_locale, "pt_BR")
            spanish_context.run(i18n.set_locale, "es")

            self.assertEqual(
                "pt_BR:Message",
                portuguese_context.run(i18n._, "Message"),
            )
            self.assertEqual(
                "es:Message",
                spanish_context.run(i18n._, "Message"),
            )

    def test_build_response_uses_active_translation(self):
        translation = PrefixTranslations("pt_BR")
        context = Context()

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ):
            def validate():
                i18n.set_locale("pt_BR")
                return build_response(
                    title="article title",
                    parent={
                        "parent": "article",
                        "parent_id": None,
                        "parent_article_type": "research-article",
                        "parent_lang": "pt",
                    },
                    item="article-title",
                    sub_item=None,
                    validation_type="value",
                    is_valid=False,
                    expected="present",
                    obtained="missing",
                    advice="Mark article title for pt language",
                    data=None,
                    error_level="ERROR",
                    advice_text=i18n._(
                        "Mark {element} for {language} language"
                    ),
                    advice_params={
                        "element": "article title",
                        "language": "pt",
                    },
                )

            result = context.run(validate)

        self.assertEqual(
            "Got missing, expected present",
            result["message"],
        )
        self.assertEqual(
            "pt_BR:Got {obtained}, expected {expected}",
            result["msg_text"],
        )
        self.assertEqual(
            "Mark article title for pt language",
            result["advice"],
        )
        self.assertEqual(
            "pt_BR:Mark {element} for {language} language",
            result["adv_text"],
        )

    def test_value_in_list_uses_localized_fallback_without_legacy_prefix(self):
        translation = PrefixTranslations("pt_BR")

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ):
            def validate():
                i18n.set_locale("pt_BR")
                return build_response(
                    title="article type",
                    parent={"parent": "article"},
                    item="article",
                    sub_item="@article-type",
                    validation_type="value in list",
                    is_valid=False,
                    expected=["research-article", "review-article"],
                    obtained="translation",
                    advice="Use a valid article type",
                    data=None,
                    error_level="CRITICAL",
                )

            result = Context().run(validate)

        self.assertEqual(
            "one of ['research-article', 'review-article']",
            result["expected_value"],
        )
        self.assertEqual(
            "Got translation, expected one of "
            "['research-article', 'review-article']",
            result["message"],
        )
        self.assertEqual(
            "pt_BR:Got {obtained}, expected one of {expected}",
            result["msg_text"],
        )
        self.assertEqual(
            {
                "obtained": "translation",
                "expected": "['research-article', 'review-article']",
            },
            result["msg_params"],
        )

    def test_format_response_uses_explicit_advice_template(self):
        translation = PrefixTranslations("es")
        context = Context()

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ):
            def validate():
                i18n.set_locale("es")
                return format_response(
                    title="journal meta presence",
                    parent="article",
                    parent_id=None,
                    parent_article_type="research-article",
                    parent_lang="pt",
                    item="journal-meta",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected="present",
                    obtained=None,
                    advice="Add <journal-meta> inside <front>",
                    data=None,
                    error_level="ERROR",
                    advice_text=i18n._(
                        "Add <{element}> inside <{parent}>"
                    ),
                    advice_params={
                        "element": "journal-meta",
                        "parent": "front",
                    },
                )

            result = context.run(validate)

        self.assertEqual(
            "Add <journal-meta> inside <front>",
            result["advice"],
        )
        self.assertEqual(
            "es:Add <{element}> inside <{parent}>",
            result["adv_text"],
        )
        self.assertEqual(
            {
                "element": "journal-meta",
                "parent": "front",
            },
            result["adv_params"],
        )

    def test_explicit_message_template_is_not_translated_twice(self):
        translation = PrefixTranslations("pt_BR")

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ):
            def validate():
                i18n.set_locale("pt_BR")
                translated = i18n._(
                    "The required <date date-type=\"{date_type}\"> is missing"
                )
                return build_response(
                    title="history date",
                    parent={"parent": "article"},
                    item="date",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected='<date date-type="accepted"> present',
                    obtained="missing",
                    advice="Add the date",
                    data=None,
                    error_level="ERROR",
                    message_text=translated,
                    message_params={"date_type": "accepted"},
                )

            result = Context().run(validate)

        self.assertEqual(
            'pt_BR:The required <date date-type="{date_type}"> is missing',
            result["msg_text"],
        )
        self.assertEqual({"date_type": "accepted"}, result["msg_params"])
        self.assertNotIn("pt_BR:pt_BR:", result["msg_text"])
        self.assertEqual(
            'Got missing, expected <date date-type="accepted"> present',
            result["message"],
        )

    def test_empty_message_template_uses_central_fallback(self):
        translation = PrefixTranslations("es")

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ):
            def validate():
                i18n.set_locale("es")
                return format_response(
                    title="title",
                    parent="article",
                    parent_id=None,
                    parent_article_type=None,
                    parent_lang=None,
                    item="item",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected="present",
                    obtained="missing",
                    advice=None,
                    data=None,
                    error_level="ERROR",
                    message_text="",
                    message_params={"unused": "value"},
                )

            result = Context().run(validate)

        self.assertEqual(
            "es:Got {obtained}, expected {expected}",
            result["msg_text"],
        )
        self.assertEqual(
            {"obtained": "missing", "expected": "present"},
            result["msg_params"],
        )

    def test_explicit_message_without_params_uses_empty_params(self):
        result = build_response(
            title="title",
            parent={"parent": "article"},
            item="item",
            sub_item=None,
            validation_type="exist",
            is_valid=False,
            expected="present",
            obtained="missing",
            advice=None,
            data=None,
            error_level="ERROR",
            message_text="Required element is missing",
        )

        self.assertEqual("Required element is missing", result["msg_text"])
        self.assertEqual({}, result["msg_params"])

    def test_invalid_response_with_advice_uses_it_as_adv_text_fallback(self):
        result = format_response(
            title="article title",
            parent="article",
            parent_id=None,
            parent_article_type="research-article",
            parent_lang="pt",
            item="article-title",
            sub_item=None,
            validation_type="exist",
            is_valid=False,
            expected="present",
            obtained=None,
            advice=None,
            data=None,
            error_level="ERROR",
            element_name="article-title",
        )

        self.assertEqual(
            "Mark article title with <article-title>",
            result["advice"],
        )
        self.assertEqual(result["advice"], result["adv_text"])
        self.assertEqual({}, result["adv_params"])

    def test_invalid_build_response_with_advice_uses_fallback(self):
        translation = PrefixTranslations("pt_BR")

        with patch(
            "packtools.sps.i18n.gettext.translation",
            return_value=translation,
        ):
            def validate():
                i18n.set_locale("pt_BR")
                return build_response(
                    title="history date",
                    parent={
                        "parent": "article",
                        "parent_id": None,
                        "parent_article_type": "research-article",
                        "parent_lang": "pt",
                    },
                    item="date",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected="present",
                    obtained=None,
                    advice="Add <date> to <history>",
                    data=None,
                    error_level="ERROR",
                )

            result = Context().run(validate)

        self.assertEqual("Add <date> to <history>", result["advice"])
        self.assertEqual(
            "pt_BR:Add <date> to <history>",
            result["adv_text"],
        )
        self.assertEqual({}, result["adv_params"])

    def test_portuguese_catalog_translates_validator_templates(self):
        xmltree = etree.fromstring("<article><front/></article>")

        def validate():
            i18n.set_locale("pt_BR")

            return next(
                JournalMetaPresenceValidation(
                    xmltree
                ).validate_journal_meta_presence()
            )

        result = Context().run(validate)

        self.assertEqual(
            "Obtido {obtained}, esperado {expected}",
            result["msg_text"],
        )
        self.assertEqual(
            "Adicione o elemento <journal-meta> dentro de <front>",
            result["adv_text"],
        )

    def test_spanish_catalog_translates_parameterized_validator_template(self):
        xmltree = etree.fromstring(
            """
            <article>
                <front>
                    <journal-meta>
                        <issn pub-type="epub">invalid</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )

        def validate():
            i18n.set_locale("es")

            return next(
                ISSNFormatValidation(xmltree).validate_issn_format()
            )

        result = Context().run(validate)

        self.assertEqual(
            "Se obtuvo {obtained}, se esperaba {expected}",
            result["msg_text"],
        )
        self.assertEqual(
            "Corrija el formato del ISSN al patrón XXXX-XXXX. Valor actual: {issn_value}",
            result["adv_text"],
        )
        self.assertEqual(
            {"issn_value": "invalid"},
            result["adv_params"],
        )
        self.assertEqual(
            "Correct ISSN format to XXXX-XXXX pattern. Current value: invalid",
            result["advice"],
        )

    def test_product_and_parameterized_advice_contract_in_supported_locales(self):
        product_data = {
            "product_type": None,
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "book-review",
            "parent_lang": "en",
        }
        issn_xml = etree.fromstring(
            """
            <article>
                <front>
                    <journal-meta>
                        <issn pub-type="epub">invalid</issn>
                    </journal-meta>
                </front>
            </article>
            """
        )
        expectations = {
            "pt_BR": {
                "product": 'Adicione o atributo @product-type="book" a <product>.',
                "issn": (
                    "Corrija o formato do ISSN para o padrão XXXX-XXXX."
                    " Valor atual: {issn_value}"
                ),
            },
            "es": {
                "product": 'Agregue el atributo @product-type="book" a <product>.',
                "issn": (
                    "Corrija el formato del ISSN al patrón XXXX-XXXX."
                    " Valor actual: {issn_value}"
                ),
            },
        }

        for locale, translated in expectations.items():
            with self.subTest(locale=locale):
                def validate():
                    i18n.set_locale(locale)
                    product = ProductValidation(
                        product_data,
                        {"product_type_presence_error_level": "CRITICAL"},
                    ).validate_product_type_presence()
                    issn = next(
                        ISSNFormatValidation(issn_xml).validate_issn_format()
                    )
                    return product, issn

                product, issn = Context().run(validate)

                self.assertEqual(
                    'Add @product-type="book" attribute to <product>.',
                    product["advice"],
                )
                self.assertEqual(translated["product"], product["adv_text"])
                self.assertEqual({}, product["adv_params"])
                self.assertEqual(
                    "Correct ISSN format to XXXX-XXXX pattern."
                    " Current value: invalid",
                    issn["advice"],
                )
                self.assertEqual(translated["issn"], issn["adv_text"])
                self.assertEqual(
                    {"issn_value": "invalid"},
                    issn["adv_params"],
                )

    def test_message_params_preserve_controlled_values_in_all_locales(self):
        for locale in ("pt_BR", "es"):
            with self.subTest(locale=locale):
                def validate():
                    i18n.set_locale(locale)
                    return build_response(
                        title="CRediT taxonomy term",
                        parent={"parent": "article"},
                        item="role",
                        sub_item=None,
                        validation_type="exist",
                        is_valid=False,
                        expected="contributor role",
                        obtained="study design",
                        advice="Check the contributor role",
                        data=None,
                        error_level="CRITICAL",
                    )

                result = Context().run(validate)
                rendered = result["msg_text"].format(
                    **result["msg_params"]
                )

                self.assertEqual(
                    {
                        "obtained": "study design",
                        "expected": "contributor role",
                    },
                    result["msg_params"],
                )
                self.assertIn("study design", rendered)
                self.assertIn("contributor role", rendered)


if __name__ == "__main__":
    unittest.main()
