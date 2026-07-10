import argparse
import sys

from packtools.sps.formats import pubmed
from packtools.sps.pid_provider import xml_sps_lib


def get_xml_trees_and_errors(path_to_read):
    """
    Reads a single SciELO .xml file or every XML file inside a .zip package
    (xml_sps_lib.get_xml_items handles both transparently) and returns:
      - the list of parsed xmltree objects, ready for build_articles_and_errors
      - the list of per-file errors encountered along the way (dicts with
        "filename"/"error"/"type_error" keys), so a single bad file in a
        package doesn't stop the whole batch.
    """
    xml_trees = []
    errors = []
    for item in xml_sps_lib.get_xml_items(path_to_read, capture_errors=True):
        xml_with_pre = item.get("xml_with_pre")
        if xml_with_pre is None:
            errors.append(item)
            continue
        xml_trees.append(xml_with_pre.xmltree)
    return xml_trees, errors


def build_articles_and_errors(xml_trees):
    """
    Builds one <Article> per xml_tree, skipping (with an error record) any
    article whose SciELO XML is missing data for a PubMed DTD-required
    element (e.g. no usable publication date), since such an article can't
    be represented, but that alone shouldn't fail the rest of the batch.
    """
    articles = []
    errors = []
    for xml_tree in xml_trees:
        try:
            articles.append(pubmed.build_pubmed_article(xml_tree))
        except pubmed.MissingRequiredElementError as exc:
            ids = pubmed.get_elocation(xml_tree)
            identifier = ids.get("doi") or ids.get("v2") or "artigo sem identificador"
            errors.append({"filename": identifier, "error": str(exc)})
    return articles, errors


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert one or more XML files from SciELO format to PubMed format. "
            "Accepts a single .xml file or a .zip package containing multiple "
            "XML files; every article found is written as one <Article> inside "
            "a single <ArticleSet> output document."
        )
    )
    parser.add_argument(
        "-i",
        "--xml_scielo",
        action="store",
        dest="path_to_read",
        required=True,
        help="Path for reading the SciELO XML file or .zip package.",
    )
    parser.add_argument(
        "-o",
        "--xml_pubmed",
        action="store",
        dest="path_to_write",
        required=True,
        help="Path for writing the PubMed XML file.",
    )
    arguments = parser.parse_args()

    xml_trees, errors = get_xml_trees_and_errors(arguments.path_to_read)
    articles, pubdate_errors = build_articles_and_errors(xml_trees)
    errors = errors + pubdate_errors

    for error in errors:
        print(
            "Aviso: falha ao processar {}: {}".format(
                error.get("filename", arguments.path_to_read), error.get("error")
            ),
            file=sys.stderr,
        )

    if not articles:
        print(
            f"Nenhum artigo válido encontrado em: {arguments.path_to_read}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    xml_pubmed_set = pubmed.build_article_set_xml(articles)
    with open(arguments.path_to_write, "w", encoding="utf-8") as file:
        file.write(xml_pubmed_set)

    print(
        "Arquivo criado em: {} ({} artigo(s), {} erro(s))".format(
            arguments.path_to_write, len(articles), len(errors)
        )
    )


if __name__ == "__main__":
    main()
