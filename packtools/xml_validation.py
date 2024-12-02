import csv
import json
import logging
import sys
import os
import argparse
from importlib.resources import files

from packtools.sps.utils import xml_utils
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.aff import (
    AffiliationsListValidation,
    AffiliationValidation,
)
from packtools.sps.validation.alternatives import (
    AlternativesValidation,
    AlternativeValidation,
)
from packtools.sps.validation.article_abstract import (
    HighlightsValidation,
    VisualAbstractsValidation,
)
from packtools.sps.validation.article_and_subarticles import (
    ArticleAttribsValidation,
    ArticleIdValidation,
    ArticleLangValidation,
    ArticleTypeValidation,
)
from packtools.sps.validation.article_author_notes import AuthorNotesValidation
from packtools.sps.validation.article_citations import (
    ArticleCitationsValidation,
    ArticleCitationValidation,
)
from packtools.sps.validation.article_contribs import (
    ArticleContribsValidation,
    ContribsValidation,
    ContribValidation,
)
from packtools.sps.validation.article_data_availability import (
    DataAvailabilityValidation,
)
from packtools.sps.validation.article_doi import ArticleDoiValidation
from packtools.sps.validation.article_lang import ArticleLangValidation as ArticleLangValidation2
from packtools.sps.validation.article_license import ArticleLicenseValidation
from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation
from packtools.sps.validation.article_xref import ArticleXrefValidation
from packtools.sps.validation.dates import ArticleDatesValidation
from packtools.sps.validation.footnotes import FootnoteValidation
from packtools.sps.validation.front_articlemeta_issue import IssueValidation, Pagination
from packtools.sps.validation.funding_group import FundingGroupValidation
from packtools.sps.validation.journal_meta import (
    AcronymValidation,
    ISSNValidation,
    JournalIdValidation,
    JournalMetaValidation,
    PublisherNameValidation,
    TitleValidation,
)
from packtools.sps.validation.peer_review import (
    AuthorPeerReviewValidation,
    CustomMetaPeerReviewValidation,
    DatePeerReviewValidation,
    PeerReviewsValidation,
    RelatedArticleValidation,
)
from packtools.sps.validation.preprint import PreprintValidation
from packtools.sps.validation.related_articles import RelatedArticlesValidation
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre


def get_xml_tree(xml_file_path):
    with open(xml_file_path, 'r') as file:
        return xml_utils.get_xml_tree(file.read())


def get_data(filename, key, sps_version=None):
    sps_version = sps_version or "default"
    # Reads contents with UTF-8 encoding and returns str.
    content = (
        files(f"packtools.sps.sps_versions")
        .joinpath(f"{sps_version}")
        .joinpath(f"{filename}.json")
        .read_text()
    )
    x = " ".join(content.split())
    fixed = x.replace(", ]", "]").replace(", }", "}")
    data = json.loads(fixed)
    return data[key]


def create_report(report_file_path, xml_path, params, fieldnames=None):
    for xml_with_pre in XMLWithPre.create(path=xml_path):
        rows = validate_xml_content(xml_with_pre.filename, xml_with_pre.xmltree, params)
        save_csv(report_file_path, rows, fieldnames)
        print(f"Created {report_file_path}")


def save_csv(filepath, rows, fieldnames):
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            filtered_row = {key: row.get(key, '') for key in fieldnames}
            writer.writerow(filtered_row)


def validate_xml_content(sps_pkg_name, xmltree, params):
    validation_group_and_function_items = (
        ("journal", validate_journal),
        ("article attributes", validate_article_attributes),
        ("article attributes", validate_languages),
        ("article attributes", validate_article_type),
        # ("article-id", validate_article_id_other),
        # ("article-id", validate_doi),
        # ("dates", validate_dates),
        # ("texts and languages", validate_article_languages),
        # ("texts and languages", validate_toc_sections),
        # ("author", validate_contribs),
        # ("author affiliations", validate_affiliations),
        # ("author notes", validate_author_notes),
        # ("open science", validate_data_availability),
        # ("open science", validate_licenses),
        # ("open science", validate_preprint),
        # ("peer review", validate_peer_review),
        # ("funding", validate_funding_group),
        # ("xref", validate_xref),
        # ("references", validate_references),
        # ("footnotes", validate_footnotes),
        # ("table-wrap", validate_table_wrap),
        # ("figures", validate_figures),
        # ("formulas", validate_formulas),
        # ("supplmentary material", validate_supplementary_material),
        # ("related articles", validate_related_articles),
        # ("special abstracts", validate_visual_abstracts),
        # ("special abstracts", validate_highlights),
    )

    sps_version = xmltree.find(".").get("specific-use")

    for validation_group, f in validation_group_and_function_items:
        try:
            items = f(xmltree, sps_version, params)
            for item in items:
                try:
                    item["group"] = validation_group
                    yield item
                except Exception as exc:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    yield dict(
                        exception=exc,
                        exc_traceback=exc_traceback,
                        function=validation_group,
                        sps_pkg_name=sps_pkg_name,
                        item=item,
                    )
        except Exception as exc:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            yield dict(
                exception=exc,
                exc_traceback=exc_traceback,
                function=validation_group,
                sps_pkg_name=sps_pkg_name,
            )


def validate_affiliations(xmltree, sps_version, params):
    validator = AffiliationsListValidation(xmltree)
    data = get_data("country_codes", "country_codes_list")
    yield from validator.validade_affiliations_list(data)


def validate_highlights(xmltree, sps_version, params):
    validator = HighlightsValidation(xmltree)
    yield from validator.highlight_validation()


def validate_visual_abstracts(xmltree, sps_version, params):
    validator = VisualAbstractsValidation(xmltree)
    yield from validator.visual_abstracts_validation()


def validate_languages(xmltree, sps_version, params):
    validator = ArticleLangValidation(xmltree)
    yield from validator.validate_language(get_data("language_codes", "language_codes_list"))


def validate_article_attributes(xmltree, sps_version, params):
    validator = ArticleAttribsValidation(xmltree)

    dtd_version_list = get_data("dtd_version", "dtd_version_list", sps_version)
    specific_use_list = get_data("specific_use", "specific_use_list", sps_version)

    yield from validator.validate_dtd_version(dtd_version_list)
    yield from validator.validate_specific_use(specific_use_list)


def validate_article_id_other(xmltree, sps_version, params):
    validator = ArticleIdValidation(xmltree)
    try:
        return validator.validate_article_id_other()
    except AttributeError:
        return None


def validate_article_type(xmltree, sps_version, params):
    validator = ArticleTypeValidation(xmltree)

    article_type_list = get_data("article_type", "article_type_list", sps_version)

    yield from validator.validate_article_type(article_type_list)

    yield from validator.validate_article_type_vs_subject_similarity()


def validate_author_notes(xmltree, sps_version, params):
    data = {
        "sps_1_9": ["conflict"],
        "sps_1_10": ["coi-statement"]
    }
    validator = AuthorNotesValidation(xmltree, data.get(sps_version))
    yield from validator.validate_author_notes()


def validate_references(xmltree, sps_version, params):
    # FIXME criar json para a versão sps_1_9
    publication_type_list = get_data("publication_types_references", "publication_type_list", "sps_1_10")
    validator = ArticleCitationsValidation(xmltree, data.get(sps_version))
    start_year = None

    xml = ArticleDates(self.xmltree)
    end_year = int(xml.collection_date["year"] or xml.article_date["year"])

    # FIXME remover xmltree do método
    yield from validator.validate_article_citations(
        xmltree, publication_type_list, start_year, end_year)


def validate_contribs(xmltree, sps_version, params):
    data = {
        "credit_taxonomy_terms_and_urls": None,
        "callable_get_data": None,
    }
    validator = ArticleContribsValidation(xmltree)
    # FIXME
    yield validator.validate_contribs_orcid_is_unique(error_level="CRITICAL")
    # for contrib in validator.contribs.contribs:
    #     yield from ContribsValidation(contrib, data, content_types).validate()


def validate_data_availability(xmltree, sps_version, params):
    validator = DataAvailabilityValidation(xmltree)
    try:
        specific_use_list = get_data("data_availability_specific_use", "specific_use", sps_version)
    except Exception as e:
        specific_use_list = None

    if specific_use_list:
        yield validator.validate_data_availability(
            specific_use_list,
            error_level="ERROR",
        )


def validate_doi(xmltree, sps_version, params):
    # FIXME falta de padrão
    validator = ArticleDoiValidation(xmltree)

    if params.get("doi_required"):
        error = "CRITICAL"
    else:
        error_level = "ERROR"
    yield validator.validate_main_article_doi_exists(error_level=error_level)
    yield from validator.validate_translations_doi_exists(error_level=error_level)
    yield validator.validate_all_dois_are_unique(error_level="ERROR")

    callable_get_data = params.get("get_doi_data")
    if callable_get_data:
        # TODO
        yield validator.validate_doi_registered(callable_get_data)


def validate_article_languages(xmltree, sps_version, params):
    # FIXME falta de padrão
    validator = ArticleLangValidation2(xmltree)
    yield from validator.validate_article_lang()


def validate_licenses(xmltree, sps_version, params):
    validator = ArticleLicenseValidation(xmltree)
    # yield from validator.validate_license(license_expected_value)
    # falta de json em sps_1_9
    yield from validator.validate_license_code(
        get_data("license_data", "expected_data", sps_version))


def validate_toc_sections(xmltree, sps_version, params):
    validator = ArticleTocSectionsValidation(xmltree)
    yield from validator.validate_article_toc_sections(params.get("expected_toc_sections"))
    yield from validator.validade_article_title_is_different_from_section_titles()


def validate_xref(xmltree, sps_version, params):
    validator = ArticleXrefValidation(xmltree)
    yield from validator.validate_id()
    yield from validator.validate_rid()


def validate_dates(xmltree, sps_version, params):
    validator = ArticleDatesValidation(xmltree)
    order = get_data(
        "history_dates_order_of_events", "order", sps_version,
    )
    required_events = get_data(
        "history_dates_required_events", "required_events", sps_version,
    )
    yield from validator.validate_history_dates(order, required_events)
    yield from validator.validate_number_of_digits_in_article_date()

    # FIXME
    yield validator.validate_article_date(future_date=None)
    yield validator.validate_collection_date(future_date=None)


def validate_figures(xmltree, sps_version, params):
    # FIXME faltam validações de label, caption, graphic ou alternatives
    validator = FigValidation(xmltree)
    yield from validator.validate_fig_existence()


def validate_footnotes(xmltree, sps_version, params):
    # FIXME não existe somente um tipo de footnotes, faltam validações, error_level
    validator = FootnoteValidation(xmltree)
    yield from validator.fn_validation()


def validate_formulas(xmltree, sps_version, params):
    # FIXME faltam validações de label, caption, graphic ou alternatives
    validator = FormulaValidation(xmltree)
    yield from validator.validate_formula_existence()


def validate_funding_group(xmltree, sps_version, params):
    # FIXME ? _callable_extern_validate_default
    # faltam validações
    validator = FundingGroupValidation(xmltree)
    yield from validator.funding_sources_exist_validation()
    # ??? yield from validator.award_id_format_validation(_callable_extern_validate_default)


def validate_journal(xmltree, sps_version, params):

    validator = AcronymValidation(xmltree)
    yield from validator.acronym_validation(params["journal_acron"])

    validator = PublisherNameValidation(xmltree)
    yield from validator.validate_publisher_names(params["publisher_name_list"])

    try:
        if params["nlm_ta"]:
            validator = JournalIdValidation(xmltree)
            yield from validator.nlm_ta_id_validation(params["nlm_ta"])
    except KeyError:
        pass


def validate_peer_review(xmltree, sps_version, params):
    # FIXME temos todos os json?

    validator = PeerReviewsValidation(
        xml_tree,
        contrib_type_list=get_data("specific_use_for_peer_review", "contrib_type_list", sps_version),
        specific_use_list=get_data("specific_use_for_peer_review", "specif_use_list", sps_version),
        date_type_list=get_data("specific_use_for_peer_review", "date_type_list", sps_version),
        meta_value_list=get_data("meta_value", "meta_value_list", sps_version),
        related_article_type_list=get_data("related_article_type", "related_article_type_list", sps_version),
        link_type_list=get_data("related_article__ext_link_type", "related_article__ext_link_type_list", sps_version),
    )
    yield from validator.validate()


def validate_preprint(xmltree, sps_version, params):
    # FIXME fora de padrão
    validator = PreprintValidation(xmltree)
    yield from validator.preprint_validation()


def validate_related_articles(xmltree, sps_version, params):
    validator = RelatedArticlesValidation(xmltree)
    correspondence_list = get_data(
        "related_article", "correspondence_list", sps_version,
    )
    yield from validator.related_articles_matches_article_type_validation(correspondence_list)
    yield from validator.related_articles_doi()


def validate_supplementary_material(xmltree, sps_version, params):
    # FIXME validações incompletas
    validator = SupplementaryMaterialValidation(xmltree)
    yield from validator.validate_supplementary_material_existence()


def validate_table_wrap(xmltree, sps_version, params):
    # FIXME validações incompletas
    validator = TableWrapValidation(xmltree)
    yield from validator.validate_tablewrap_existence()


def process_folder(input_folder, output_folder, params, selected_fields):
    # Verifica se a pasta de saída existe, e caso não exista, cria a pasta
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Percorre todos os arquivos na pasta de entrada
    for filename in os.listdir(input_folder):
        # Verifica se o arquivo termina com a extensão '.xml'
        if filename.endswith('.xml'):
            # Constrói o caminho completo do arquivo XML
            file_path = os.path.join(input_folder, filename)
            # Constrói o caminho completo do arquivo de saída CSV, usando o mesmo nome do arquivo XML, mas com extensão '.csv'
            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.csv")
            # Chama a função create_report para criar o relatório CSV com base no arquivo XML, passando os parâmetros e os campos selecionados
            create_report(output_file, file_path, params, selected_fields)



if __name__ == "__main__":
    # Inicializa o analisador de argumentos para a linha de comando
    parser = argparse.ArgumentParser(description="Validate XML files and save the results to CSV.")

    # Adiciona argumento obrigatório para a pasta de entrada contendo os arquivos XML a serem validados
    parser.add_argument('-i', dest='input_folder', required=True, help='Folder path containing XML files to validate')

    # Adiciona argumento obrigatório para a pasta de saída onde os arquivos CSV com os resultados das validações serão salvos
    parser.add_argument('-o', dest='output_folder', required=True,
                        help='Folder path to save the validation result CSV files')

    # Adiciona argumento opcional para listar os campos a serem incluídos no CSV
    parser.add_argument('--fields', required=False, nargs='+', help='List of fields to include in the CSV')

    # Adiciona argumento opcional para especificar um dicionário com parâmetros a serem considerados nas validações
    parser.add_argument('--params', required=False, nargs='+',
                        help='Dictionary with parameters to be considered in the validations')

    # Analisa os argumentos fornecidos na linha de comando
    args = parser.parse_args()

    # Comenta a linha que pega os parâmetros dos argumentos
    # params = args.params

    # Define um dicionário de parâmetros apenas para teste
    params = {
        "journal_acron": "aaa",
        "publisher_name_list": ["aaa", "bbb"],
        "nlm_ta": "ccc"
    }

    # Verifica se os campos foram fornecidos nos argumentos
    if args.fields:
        # Se fornecido, usa os campos especificados pelo usuário
        selected_fields = args.fields
    else:
        # Caso contrário, usa um conjunto padrão de campos
        selected_fields = [
            "title", "parent", "parent_id", "parent_article_type", "parent_lang",
            "item", "sub_item", "validation_type", "response", "expected_value",
            "got_value", "message", "advice", "data",
            "group", "exception", "exc_traceback", "function", "sps_pkg_name"
        ]

    # Chama a função process_folder com as pastas de entrada e saída, os parâmetros e os campos selecionados
    process_folder(args.input_folder, args.output_folder, params, selected_fields)

