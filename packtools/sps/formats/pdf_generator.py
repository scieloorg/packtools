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
        required=False,
        help="Path for writing the PDF file. If omitted, a default name will be used.",
    )
    parser.add_argument(
        "--libreoffice-binary",
        action="store",
        dest="libreoffice_binary",
    )
    arguments = parser.parse_args()

    data = {'base_layout': arguments.layout,}

    xml_tree = xml_utils.get_xml_tree(arguments.path_to_read)
    document = docx.pipeline_docx(xml_tree, data)

    if arguments.path_to_write:
        pdf_path = arguments.path_to_write
    else:
        pdf_path = arguments.path_to_read.replace('.xml', '.pdf')

    dir_name = os.path.dirname(pdf_path)
    base_name = os.path.basename(pdf_path)
    f_name, f_ext = os.path.splitext(base_name)
    docx_path = os.path.join(dir_name, f"{f_name}.docx")

    document.save(docx_path)
    print(f'DOCX generated at {docx_path}')
    
    file_utils.convert_docx_to_pdf(docx_path, arguments.libreoffice_binary)
    print(f'PDF generated at {pdf_path}')

if __name__ == "__main__":
    main()
