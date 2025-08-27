import argparse
import os

from packtools.sps.formats.pdf.pipeline import docx  
from packtools.sps.formats.pdf.utils import file_utils
from packtools.sps.utils import xml_utils


def main():
    parser = argparse.ArgumentParser(
        description="Convert XML file from SciELO format to PDF format."
    )
    parser.add_argument(
        "-i",
        "--xml_scielo",
        action="store",
        dest="path_to_read",
        required=True,
        help="Path for reading the SciELO XML file.",
    )
    parser.add_argument(
        "-l",
        "--layout",
        action="store",
        help="Path for reading the DOCX layout file.",
    )
    parser.add_argument(
        "-o",
        "--pdf",
        action="store",
        dest="path_to_write",
        required=True,
        help="Path for writing the PDF file.",
    )
    arguments = parser.parse_args()

    data = {
        'base_layout': arguments.layout,
    }

    xml_tree = xml_utils.get_xml_tree(arguments.path_to_read)
    document = docx.pipeline_docx(xml_tree, data)

    path_intermediate_docx = arguments.path_to_write.replace(".pdf", ".docx")
    document.save(path_intermediate_docx)
    print(f"Documento intermediário salvo em {path_intermediate_docx}")

    file_utils.convert_docx_to_pdf(path_intermediate_docx, arguments.path_to_write)


if __name__ == "__main__":
    main()
