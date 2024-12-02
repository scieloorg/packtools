from lxml import etree as ET


def build_funding_group(data):
    """
    Builds an XML element representing a funding group.

    Args:
        data (dict): A dictionary containing funding information with the following structure:
            - "award-group" (list): A list of dictionaries, each representing an award group with:
                - "funding-source" (list): A list of funding sources (strings) (required).
                - "award-id" (list): A list of award IDs (strings) (required).

    Returns:
        xml.etree.ElementTree.Element: An XML element representing the funding group.

    Raises:
        ValueError: If any award group does not include at least one funding source and one award ID.

    Example input:
        data = {
            "award-group": [
                {
                    "funding-source": ["CNPq"],
                    "award-id": ["00001", "00002"]
                },
                {
                    "funding-source": ["CNPq", "FAPESP"],
                    "award-id": ["#09/06953-4"]
                }
            ]
        }

    Example output:
        <funding-group>
            <award-group>
                <funding-source>CNPq</funding-source>
                <award-id>00001</award-id>
                <award-id>00002</award-id>
            </award-group>
            <award-group>
                <funding-source>CNPq</funding-source>
                <funding-source>FAPESP</funding-source>
                <award-id>#09/06953-4</award-id>
            </award-group>
        </funding-group>
    """

    if award_groups := data.get("award-group"):
        funding_group_elem = ET.Element("funding-group")

        for award_group in award_groups:
            if not (funding_sources := award_group.get("funding-source")) or not (award_ids := award_group.get("award-id")):
                raise ValueError("At least one funding-source and one award-id are required")

            award_group_elem = ET.SubElement(funding_group_elem, "award-group")
            for funding_source in funding_sources:
                ET.SubElement(award_group_elem, "funding-source").text = funding_source
            for award_id in award_ids:
                ET.SubElement(award_group_elem, "award-id").text = award_id

        return funding_group_elem
