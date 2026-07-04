import argparse
import sys

from packtools.sps.formats import pubmed
from packtools.sps.pid_provider import xml_sps_lib


def get_xml_trees_and_errors(path_to_read):
    """
    Reads a single SciELO .xml file or every XML file inside a .zip package
    (xml_sps_lib.get_xml_items handles both transparently) and returns:
      - the list of parsed xmltree objects, ready for pubmed.pipeline_pubmed_set
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

    for error in errors:
        print(
            "Aviso: falha ao processar {}: {}".format(
                error.get("filename", arguments.path_to_read), error.get("error")
            ),
            file=sys.stderr,
        )

    if not xml_trees:
        print(
            f"Nenhum XML válido encontrado em: {arguments.path_to_read}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    xml_pubmed_set = pubmed.pipeline_pubmed_set(xml_trees)
    with open(arguments.path_to_write, "w", encoding="utf-8") as file:
        file.write(xml_pubmed_set)

    print(
        "Arquivo criado em: {} ({} artigo(s), {} erro(s))".format(
            arguments.path_to_write, len(xml_trees), len(errors)
        )
    )


if __name__ == "__main__":
    main()
