# obs.:
#    - nota de tabela não tem o atributo 'fn-type'
#    - o atributo 'id' é obrigatório
#    - pode existir um único 'table' e muitos 'graphic' em 'table-wrap'

import xml.etree.ElementTree as ET


def build_table(data):
    """
    Creates an XML element representing a table or graphic based on the input dictionary.

    Parameters:
    data (dict): Dictionary with keys:
        - "graphic" (str, optional): Path or name of the image file if type is graphic.
        - "table" (str, optional): Content of the table if type is table.
        - "id" (str, optional): Identifier for the element.

    Returns:
    ET.Element: An XML element with the specified attributes and content.

    Raises:
    ValueError: If neither "table" nor "graphic" are provided in the data.

    Example input:
        data = {
            "graphic": "nomedaimagemdatabela.svg",
            "id": "g1"
        }

    Example output:
        <graphic xlink:href="nomedaimagemdatabela.svg" id="g1" />
    """
    for table_type in ("table", "graphic"):
        if table_value := data.get(table_type):
            table_id = data.get("id")
            break
    else:
        raise ValueError("A valid codification type ('table' or 'graphic') is required.")

    # Define attributes based on type and presence of id
    attributes = {"xlink:href": table_value} if table_type == "graphic" else {}
    if table_id:
        attributes["id"] = table_id

    # Create the XML element with attributes
    table_elem = ET.Element(table_type, attrib=attributes)

    # Add text content if it's a table
    if table_type == "table":
        table_elem.text = table_value

    return table_elem


def build_table_wrap(data):
    """
    Creates a table-wrap XML element with optional label, caption, footnotes, and table representations.

    Parameters:
    data (dict): Dictionary with keys:
        - "table-wrap-id" (str): Required identifier for the table-wrap element.
        - "label" (str, optional): Label text for the table-wrap.
        - "caption-title" (str, optional): Title text for the caption.
        - "caption-p" (list of str, optional): Paragraphs for the caption.
        - "fns" (list of dict, optional): Footnotes, each requiring "fn-id" and optionally "fn-label" and "fn-p".
        - "tables" (list of dict): List of table data, with at least one item required.

    Returns:
    ET.Element: An XML element with the constructed structure.

    Raises:
    ValueError: If required keys are missing or data is malformed.

    Example input:
        data = {
            "table-wrap-id": "t01",
            "label": "Table 1",
            "caption-title": "Título da tabela",
            "caption-p": ["Deaths Among Patients..."],
            "fns": [
                {
                    "fn-id": "fn01",
                    "fn-label": "*",
                    "fn-p": "text"
                }
            ],
            "tables": [
                {
                    "graphic": "nomedaimagemdatabela.svg",
                    "id": "g1"
                },
                {
                    "table": "codificação da tabela"
                }
            ]
        }

    Example output:
        <table-wrap id="t01">
            <label>Table 1</label>
            <caption>
                <title>Título da tabela</title>
                <p>Deaths Among Patients...</p>
            </caption>
            <table-wrap-foot>
                <fn id="fn01">
                    <label>*</label>
                    <p>text</p>
                </fn>
            </table-wrap-foot>
            <alternatives>
                <graphic xlink:href="nomedaimagemdatabela.svg" id="g1" />
                <table>codificação da tabela</table>
            </alternatives>
        </table-wrap>
    """
    if not (table_id := data.get("table-wrap-id")):
        raise ValueError("Attrib table-wrap-id is required")

    # build table_wrap
    table_wrap_elem = ET.Element("table-wrap", attrib={"id": table_id})

    # add label
    if label := data.get("label"):
        label_elem = ET.SubElement(table_wrap_elem, "label")
        label_elem.text = label

    # add caption
    caption = data.get("caption-title")
    paragraphs = data.get("caption-p")
    if caption or paragraphs:
        caption_elem = ET.SubElement(table_wrap_elem, "caption")
        if caption:
            title_elem = ET.SubElement(caption_elem, "title")
            title_elem.text = caption

        for paragraph in (paragraphs or []):
            paragraph_elem = ET.SubElement(caption_elem, "p")
            paragraph_elem.text = paragraph

    # add footnotes
    if fns := data.get("fns"):
        table_wrap_foot_elem = ET.SubElement(table_wrap_elem, "table-wrap-foot")
        for fn in fns:
            if not (fn_id := fn.get("fn-id")):
                raise ValueError("fn-id is required")
            fn_elem = ET.SubElement(table_wrap_foot_elem, "fn", attrib={"id": fn_id})

            if label := fn.get("fn-label"):
                label_elem = ET.SubElement(fn_elem, "label")
                label_elem.text = label

            if p := fn.get("fn-p"):
                p_elem = ET.SubElement(fn_elem, "p")
                p_elem.text = p

    if not (tables := data.get("tables", [])):
        raise ValueError("At least one representation of the table is required")

    if len(tables) == 1:
        # add one table
        table_wrap_elem.append(build_table(tables[0]))
    else:
        # add alternatives (many tables)
        alternatives_elem = ET.SubElement(table_wrap_elem, "alternatives")
        for table in tables:
            alternatives_elem.append(build_table(table))

    return table_wrap_elem
